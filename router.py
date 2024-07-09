from typing import Optional, Union

from fastapi import APIRouter, UploadFile
from starlette import status
from starlette.responses import JSONResponse
from models import MemStorage
from schemas import MemAdd
from storage import storage

router = APIRouter(tags=["router"], prefix="/memes")


# all memes list
@router.get("/")
async def get_memes():
    mem_id = await storage.list_objects()
    return mem_id, JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "success"})


# getting exact picture by id
@router.get("/{id}")
async def get_mem_by_id(id: int) -> JSONResponse:
    mem = await MemStorage.get_mem(id)
    if mem is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'message': f"{id} not found"})
    else:
        link = storage.download_file(filename=mem)
        return link


# adding picture
@router.post("/")
async def add_mem(file: UploadFile) -> JSONResponse:
    check = await MemStorage.check_mem(file.filename)
    if check is True:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={'message': f"File {file.filename} "
                                                f"already exists"})
    else:
        id = await MemStorage.add_mem(data=MemAdd(name=file.filename))
        await storage.upload_file(file.filename, file.file, file.size)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": f"Succesfully uploaded "
                                                f"{file.filename}, "
                                                f"file id: {id}"})


# renewing existed pic
@router.put("/{id}")
async def renew_exist_mem(file: UploadFile, id: int):
    await storage.upload_file(file.filename, file.file, file.size)
    name = await MemStorage.update_mem(id, name=file.filename)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": f"Succesfully replaced "
                                            f"{file.filename}, "
                                            f"file id: {name}"})


# delete picture
@router.delete("/{id}")
async def delete_mem(id: int):
    mem = await MemStorage.get_mem(id)
    if mem is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'message': f"{mem} not found"})
    else:
        await MemStorage.delete_mem(id)
        storage.delete_file(filename=mem)
