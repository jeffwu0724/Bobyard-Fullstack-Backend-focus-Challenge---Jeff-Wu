from typing import Optional
from fastapi import FastAPI
from modify_comments import add_admin_comment, delete_all_comments, delete_comment_by_id, edit_comment_text, fetch_all_comments
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app's origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class CommmentRequest(BaseModel):
    keyword: str
    story: str
    picture_url: str
    id: str
    author: str
    text: str
    date: str
    likes: int
    image: str

@app.post("/add_comment")
async def add_comment_api(text: str, image: Optional[str] = ""):
    response = await add_admin_comment(text, image)
    return response
    


@app.get("/edit_text_of_comment")
async def edit_text_of_comment_api(id:str, new_text:str):
    response = await edit_comment_text(id, new_text)
   
    return response


@app.get("/fetch_all_comments")
async def fetch_all_comments_api():
    response = await fetch_all_comments()
    return response

@app.get("/delete_comment_by_id")
async def delete_comment_by_id_api(id: str):
    response = await delete_comment_by_id(id)
   
    return response


@app.get("/delete_all_comments")
async def delete_all_comments_api():
    response = await delete_all_comments()
   
    return response


@app.get("/")
async def root():
    return {"message": "FastAPI ↔ DynamoDB Direct Access Example"}