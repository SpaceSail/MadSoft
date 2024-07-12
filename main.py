from database import create_tables, drop_tables
from contextlib import asynccontextmanager
from fastapi import FastAPI
from router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print('Clearing db')
    await create_tables()
    print('Creating db')
    yield
    print('Shutting down')


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)



