from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from web.container import get_container
from web.handlers import zones, places
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

container = get_container()
app.include_router(zones.router)
app.include_router(places.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
