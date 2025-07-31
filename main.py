from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = FastAPI()


class ObjectModel(BaseModel):
    author: str
    title: str
    content: str

objects_list: List[ObjectModel] = []

def serialized_objects_list():
    objects_converted = []
    for theobject in objects_list:
        objects_converted.append(theobject.model_dump())
    return objects_converted

@app.get("/ping")
def pingpong():
    return "pong"

@app.get("/home")
def welcome():
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

@app.post("/posts")
def new_objects(object_payload: List[ObjectModel]):
    objects_list.extend(object_payload)
    return JSONResponse({"objects": serialized_objects_list()}, status_code=201)

@app.get("/posts")
def list_objects():
    return {"posts": serialized_objects_list()}

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
