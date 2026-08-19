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

-- TODO 1: inserisci p3 / Studente / Terzo post persistente / likes 0 / liked 0.

-- TODO 2: modifica SOLTANTO p2 portando liked a 1 e likes a 1.

-- TODO 3: elimina SOLTANTO draft-remove.

-- TODO 4: crea la view liked_posts con id, author, text, likes, liked,
--          filtrata liked = 1 e ordinata per id.
