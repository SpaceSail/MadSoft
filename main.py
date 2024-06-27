from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "some_mem"}


@app.get("/memes/{id}")
async def get_mem_by_id(id: int):
    return {id}


@app.post("/memes")
async def add_mem(name: str):
    return {"message": f"Hello {name}"}


@app.put("/memes/{id}")
async def renew_exist_mem(name: str):
    return {"message": f"Hello {name}"}


@app.delete("/memes/{id}")
async def delete_mem(id: int):
    return {"message": f"Hello {id}"}
