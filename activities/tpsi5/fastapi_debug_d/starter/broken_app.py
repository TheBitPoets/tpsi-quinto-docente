from fastapi import FastAPI

app = FastAPI()

posts = {
    "p1": {
        "id": "p1",
        "text": "seed",
        "authorId": "server-user",
        "author": "Server User",
        "liked": False,
        "likes": 0,
        "internalSecret": "NON PUBBLICARE",
    }
}


@app.post("/api/posts")
def create_post(payload: dict):
    post = {
        "id": "p2",
        "text": payload["text"],
        "authorId": payload["authorId"],
        "author": "Client Chosen",
        "liked": False,
        "likes": 0,
        "internalSecret": "leak",
    }
    posts[post["id"]] = post
    return post


@app.get("/api/posts/{post_id}")
def get_post(post_id: str):
    return posts[post_id]
