PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categoria (
    id      INTEGER PRIMARY KEY,
    nome    TEXT NOT NULL UNIQUE,
    eixo_x  TEXT NOT NULL,   -- nota 0 = lado esquerdo, 10 = lado direito
    eixo_y  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item (
    id            INTEGER PRIMARY KEY,
    categoria_id  INTEGER NOT NULL REFERENCES categoria(id),
    nome          TEXT NOT NULL,
    UNIQUE (categoria_id, nome)
);

CREATE TABLE IF NOT EXISTS pessoa (
    id    INTEGER PRIMARY KEY,
    nome  TEXT NOT NULL UNIQUE
);

-- Aba Compatibilidade: posição que a pessoa deu a cada item (1 = favorito)
CREATE TABLE IF NOT EXISTS ranking (
    pessoa_id  INTEGER NOT NULL REFERENCES pessoa(id),
    item_id    INTEGER NOT NULL REFERENCES item(id),
    posicao    INTEGER NOT NULL CHECK (posicao >= 1),
    PRIMARY KEY (pessoa_id, item_id)
);

-- Aba Dupla mais parecida: ponto (x, y) da pessoa em cada categoria
CREATE TABLE IF NOT EXISTS nota (
    pessoa_id     INTEGER NOT NULL REFERENCES pessoa(id),
    categoria_id  INTEGER NOT NULL REFERENCES categoria(id),
    x             REAL NOT NULL CHECK (x BETWEEN 0 AND 10),
    y             REAL NOT NULL CHECK (y BETWEEN 0 AND 10),
    PRIMARY KEY (pessoa_id, categoria_id)
);
