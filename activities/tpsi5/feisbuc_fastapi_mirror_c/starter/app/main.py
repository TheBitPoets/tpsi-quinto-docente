from fastapi import FastAPI

from .store import MemoryPostStore

app = FastAPI(title="Feisbuc FastAPI mirror", version="0.1.0")
post_store = MemoryPostStore()

# TODO: GET /api/posts
# TODO: POST /api/posts con 201 + Location
# TODO: PATCH /api/posts/{post_id}
# TODO: response_model e 404
