from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance with the new title
app = FastAPI(title="KCW CRM")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this later for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0"}

# Example endpoint for Excel ping (you can adjust as needed)
@app.get("/excel/ping")
async def excel_ping():
    return {"message": "Excel ping successful!"}

# Add any other routes or logic you need below

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
