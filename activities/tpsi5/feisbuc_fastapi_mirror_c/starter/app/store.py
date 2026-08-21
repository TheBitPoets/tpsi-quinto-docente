class MemoryPostStore:
    def __init__(self):
        self._posts = []

    def list(self):
        return list(self._posts)

    # TODO: create(text), set_liked(post_id, liked), find(post_id)
