-- Activity A - completa lo schema senza cambiare i due seed finali.

CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    author TEXT NOT NULL,
    text TEXT NOT NULL,
    likes INTEGER NOT NULL DEFAULT 0,
    liked INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- TODO: rendi la tabella STRICT e aggiungi i CHECK richiesti.
-- TODO: crea idx_posts_liked_created su liked, created_at DESC.

INSERT INTO posts(id, author, text, likes, liked)
VALUES
('p1', 'Docente', 'Primo post persistente', 2, 1),
('p2', 'Studente', 'Secondo post persistente', 0, 0);
