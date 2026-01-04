from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "org",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "platform_account",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.Text(), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column("merchant_id", sa.Text()),
        sa.Column("access_token", sa.Text()),
        sa.Column("refresh_token", sa.Text()),
        sa.Column("token_expires_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("settings", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("org_id", "platform", "merchant_id", name="uq_platform_account"),
    )

    op.create_table(
        "customer",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("crn", sa.Text(), nullable=False),
        sa.Column("full_name", sa.Text()),
        sa.Column("primary_email", sa.Text()),
        sa.Column("primary_phone", sa.Text()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("org_id", "crn", name="uq_customer_org_crn"),
    )

    op.create_table(
        "customer_identity",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("customer_id", sa.BigInteger(), sa.ForeignKey("customer.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.Text()),
        sa.Column("platform_customer_id", sa.Text()),
        sa.Column("email", sa.Text()),
        sa.Column("phone", sa.Text()),
        sa.Column("raw", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("org_id", "platform", "platform_customer_id", name="uq_identity_platform_customer"),
    )

    op.create_table(
        "product",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sku", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("org_id", "sku", name="uq_product_org_sku"),
    )

    op.create_table(
        "inventory",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.BigInteger(), sa.ForeignKey("product.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_stock", sa.Integer(), server_default="0", nullable=False),
        sa.Column("reserved_stock", sa.Integer(), server_default="0", nullable=False),
        sa.Column("available_stock", sa.Integer(), server_default="0", nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("org_id", "product_id", name="uq_inventory_org_product"),
    )

    op.create_table(
        "inventory_file_source",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_type", sa.Text(), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column("config", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("poll_minutes", sa.Integer()),
        sa.Column("last_poll_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "excel_inventory_file",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_id", sa.BigInteger(), sa.ForeignKey("inventory_file_source.id", ondelete="SET NULL")),
        sa.Column("filename", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("remote_file_id", sa.Text()),
        sa.Column("remote_modified_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("status", sa.Text(), server_default="UPLOADED", nullable=False),
        sa.Column("error", sa.Text()),
        sa.Column("uploaded_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("processed_at", sa.TIMESTAMP(timezone=True)),
    )

    op.create_table(
        "excel_inventory_row",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("excel_file_id", sa.BigInteger(), sa.ForeignKey("excel_inventory_file.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sku", sa.Text(), nullable=False),
        sa.Column("product_name", sa.Text()),
        sa.Column("total_stock", sa.BigInteger()),
        sa.Column("raw", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
    )

    op.create_table(
        "order",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.Text(), nullable=False),
        sa.Column("platform_account_id", sa.BigInteger(), sa.ForeignKey("platform_account.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform_order_id", sa.Text(), nullable=False),
        sa.Column("customer_id", sa.BigInteger(), sa.ForeignKey("customer.id", ondelete="SET NULL")),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("currency", sa.Text(), server_default="PHP", nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), server_default="0", nullable=False),
        sa.Column("order_created_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("imported_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.UniqueConstraint("org_id", "platform_account_id", "platform_order_id", name="uq_order_platform_id"),
    )

    op.create_table(
        "order_item",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("order_id", sa.BigInteger(), sa.ForeignKey("order.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.BigInteger(), sa.ForeignKey("product.id", ondelete="SET NULL")),
        sa.Column("platform_sku", sa.Text()),
        sa.Column("name", sa.Text()),
        sa.Column("quantity", sa.BigInteger(), nullable=False),
        sa.Column("raw", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
    )

    op.create_table(
        "order_item_reservation",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order_id", sa.BigInteger(), sa.ForeignKey("order.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order_item_id", sa.BigInteger(), sa.ForeignKey("order_item.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.BigInteger(), sa.ForeignKey("product.id", ondelete="CASCADE"), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("reserved_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("released_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("reserve_event", sa.Text()),
        sa.Column("release_event", sa.Text()),
        sa.UniqueConstraint("org_id", "order_item_id", name="uq_reservation_org_order_item"),
    )

    op.create_table(
        "sync_run",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("org_id", sa.BigInteger(), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.Text()),
        sa.Column("platform_account_id", sa.BigInteger(), sa.ForeignKey("platform_account.id", ondelete="SET NULL")),
        sa.Column("job_type", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), server_default="QUEUED", nullable=False),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("finished_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("error", sa.Text()),
        sa.Column("stats", sa.JSON(), server_default=sa.text("'{}'::json"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

def downgrade():
    op.drop_table("sync_run")
    op.drop_table("order_item_reservation")
    op.drop_table("order_item")
    op.drop_table("order")
    op.drop_table("excel_inventory_row")
    op.drop_table("excel_inventory_file")
    op.drop_table("inventory_file_source")
    op.drop_table("inventory")
    op.drop_table("product")
    op.drop_table("customer_identity")
    op.drop_table("customer")
    op.drop_table("platform_account")
    op.drop_table("org")
