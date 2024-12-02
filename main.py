from fastapi import FastAPI
from routers import zones, places
import uvicorn

app = FastAPI(title="Parking Management API")

app.include_router(zones.router)
app.include_router(places.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
