from uuid import uuid4


class MemoryPostStore:
    def __init__(self):
        self._posts = [
            {
                "id": "seed-1",
                "text": "Post iniziale del mirror",
                "authorId": "mirror-user",
                "author": "Mirror Student",
                "liked": False,
                "likes": 0,
            }
        ]

    def list(self):
        return [dict(post) for post in self._posts]

    def find(self, post_id):
        return next((dict(post) for post in self._posts if post["id"] == post_id), None)

    def create(self, text):
        post = {
            "id": str(uuid4()),
            "text": text,
            "authorId": "mirror-user",
            "author": "Mirror Student",
            "liked": False,
            "likes": 0,
        }
        self._posts.insert(0, post)
        return dict(post)

    def set_liked(self, post_id, liked):
        for post in self._posts:
            if post["id"] != post_id:
                continue
            if post["liked"] != liked:
                post["likes"] += 1 if liked else -1
                post["liked"] = liked
            return dict(post)
        return None
