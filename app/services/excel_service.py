from __future__ import annotations

import hashlib
import io
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.excel import ExcelInventoryFile, ExcelInventoryRow
from app.models.product import Product
from app.models.inventory import Inventory

REQUIRED = ["SKU", "Product Name", "Total Stock"]

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def parse_excel_to_rows(file_bytes: bytes) -> list[dict]:
    df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}. Expected: {REQUIRED}")

    df = df[REQUIRED].copy()
    df["SKU"] = df["SKU"].astype(str).str.strip()
    df["Product Name"] = df["Product Name"].astype(str).fillna("").str.strip()
    df["Total Stock"] = pd.to_numeric(df["Total Stock"], errors="coerce").fillna(0).astype(int)
    df = df[df["SKU"] != ""]

    rows: list[dict] = []
    for r in df.to_dict(orient="records"):
        rows.append({
            "sku": r["SKU"],
            "product_name": r["Product Name"] or r["SKU"],
            "total_stock": max(0, int(r["Total Stock"])),
            "raw": r,
        })
    return rows

def create_excel_file_record(db: Session, *, org_id: int, filename: str, file_bytes: bytes) -> ExcelInventoryFile:
    h = sha256_bytes(file_bytes)
    excel_file = ExcelInventoryFile(org_id=org_id, filename=filename, content_hash=h, status="UPLOADED")
    db.add(excel_file)
    db.flush()
    return excel_file

def import_excel_file(db: Session, *, org_id: int, excel_file_id: int, file_bytes: bytes) -> dict:
    excel_file = db.get(ExcelInventoryFile, excel_file_id)
    if not excel_file or excel_file.org_id != org_id:
        raise ValueError("Excel file not found")

    rows = parse_excel_to_rows(file_bytes)

    # Save rows for audit
    db.query(ExcelInventoryRow).filter(ExcelInventoryRow.excel_file_id == excel_file_id).delete()
    for r in rows:
        db.add(ExcelInventoryRow(
            excel_file_id=excel_file_id,
            sku=r["sku"],
            product_name=r["product_name"],
            total_stock=r["total_stock"],
            raw=r["raw"],
        ))

    updated_inv = 0
    created_products = 0

    for r in rows:
        sku = r["sku"]
        name = r["product_name"]
        total = r["total_stock"]

        product = db.scalar(select(Product).where(Product.org_id == org_id, Product.sku == sku))
        if not product:
            product = Product(org_id=org_id, sku=sku, name=name)
            db.add(product)
            db.flush()
            created_products += 1
        else:
            if name and product.name != name:
                product.name = name

        inv = db.scalar(select(Inventory).where(Inventory.org_id == org_id, Inventory.product_id == product.id))
        if not inv:
            inv = Inventory(org_id=org_id, product_id=product.id, total_stock=0, reserved_stock=0, available_stock=0)
            db.add(inv)
            db.flush()

        inv.total_stock = total
        inv.available_stock = max(0, inv.total_stock - inv.reserved_stock)
        updated_inv += 1

    excel_file.status = "PROCESSED"
    excel_file.error = None

    return {"rows": len(rows), "products_created": created_products, "inventory_updated": updated_inv}
