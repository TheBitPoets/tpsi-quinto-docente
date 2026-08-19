CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    author TEXT NOT NULL CHECK (length(trim(author)) > 0),
    text TEXT NOT NULL CHECK (length(trim(text)) BETWEEN 1 AND 280),
    likes INTEGER NOT NULL DEFAULT 0 CHECK (likes >= 0),
    liked INTEGER NOT NULL DEFAULT 0 CHECK (liked IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE INDEX idx_posts_liked_created
ON posts(liked, created_at DESC);

INSERT INTO posts(id, author, text, likes, liked)
VALUES
('p1', 'Docente', 'Primo post persistente', 2, 1),
('p2', 'Studente', 'Secondo post persistente', 0, 0);
