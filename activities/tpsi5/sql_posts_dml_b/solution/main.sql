CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    author TEXT NOT NULL,
    text TEXT NOT NULL CHECK (length(trim(text)) BETWEEN 1 AND 280),
    likes INTEGER NOT NULL DEFAULT 0 CHECK (likes >= 0),
    liked INTEGER NOT NULL DEFAULT 0 CHECK (liked IN (0, 1))
) STRICT;

INSERT INTO posts(id, author, text, likes, liked)
VALUES
('p1', 'Docente', 'Primo post persistente', 2, 1),
('p2', 'Studente', 'Secondo post persistente', 0, 0),
('draft-remove', 'Studente', 'Bozza da eliminare', 0, 0);

INSERT INTO posts(id, author, text, likes, liked)
VALUES('p3', 'Studente', 'Terzo post persistente', 0, 0);

UPDATE posts
SET liked = 1,
    likes = 1
WHERE id = 'p2';

DELETE FROM posts
WHERE id = 'draft-remove';

CREATE VIEW liked_posts AS
SELECT id, author, text, likes, liked
FROM posts
WHERE liked = 1
ORDER BY id;
