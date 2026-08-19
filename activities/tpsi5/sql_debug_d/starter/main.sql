CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    author TEXT NOT NULL,
    text TEXT NOT NULL CHECK (length(trim(text)) BETWEEN 1 AND 280),
    likes INTEGER NOT NULL DEFAULT 0 CHECK (likes >= 0),
    liked INTEGER NOT NULL DEFAULT 0 CHECK (liked IN (0, 1))
) STRICT;

INSERT INTO posts(id, author, text, likes, liked)
VALUES
('p1', 'Docente', 'Primo', 2, 1),
('p2', 'Studente', 'Secondo', 0, 0),
('p3', 'Studente', 'Terzo', 0, 0);

-- BROKEN 1: il seed temporaneo viola l'invariante liked 0/1.
INSERT INTO posts(id, author, text, likes, liked)
VALUES('remove-me', 'Debug', 'Temporaneo', 0, 2);

-- BROKEN 2: doveva mettere like soltanto a p2.
UPDATE posts
SET liked = 1,
    likes = likes + 1;

-- BROKEN 3: doveva eliminare soltanto remove-me.
DELETE FROM posts
WHERE id <> 'p1';
