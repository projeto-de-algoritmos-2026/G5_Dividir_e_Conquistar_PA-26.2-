-- Dados fixos das categorias e itens + pessoas fictícias de demonstração.
-- INSERT OR IGNORE: pode rodar mais de uma vez sem duplicar.

INSERT OR IGNORE INTO categoria (id, nome, eixo_x, eixo_y) VALUES
    (1, 'Jogos',          'Casual → Competitivo', 'História → Gameplay'),
    (2, 'Músicas',        'Calma → Agitada',      'Alegre → Melancólica'),
    (3, 'Séries/Animes',  'Leve → Pesada',        'Ação → Drama');

INSERT OR IGNORE INTO item (id, categoria_id, nome) VALUES
    (1,  1, 'Minecraft'),
    (2,  1, 'Counter-Strike 2'),
    (3,  1, 'Stardew Valley'),
    (4,  1, 'Elden Ring'),
    (5,  1, 'League of Legends'),
    (6,  1, 'Hollow Knight'),
    (7,  1, 'GTA V'),
    (8,  1, 'The Legend of Zelda: Breath of the Wild'),
    (9,  2, 'Bohemian Rhapsody - Queen'),
    (10, 2, 'Evidências - Chitãozinho & Xororó'),
    (11, 2, 'Blinding Lights - The Weeknd'),
    (12, 2, 'Construção - Chico Buarque'),
    (13, 2, 'Enter Sandman - Metallica'),
    (14, 2, 'Anunciação - Alceu Valença'),
    (15, 2, 'Billie Jean - Michael Jackson'),
    (16, 2, 'Shape of You - Ed Sheeran'),
    (17, 3, 'Breaking Bad'),
    (18, 3, 'Naruto'),
    (19, 3, 'Attack on Titan'),
    (20, 3, 'Stranger Things'),
    (21, 3, 'One Piece'),
    (22, 3, 'The Office'),
    (23, 3, 'Death Note'),
    (24, 3, 'Game of Thrones');

INSERT OR IGNORE INTO pessoa (id, nome) VALUES
    (1, 'Ana'),
    (2, 'Bruno'),
    (3, 'Carla'),
    (4, 'Diego'),
    (5, 'Elisa'),
    (6, 'Felipe');

INSERT OR IGNORE INTO nota (pessoa_id, categoria_id, x, y) VALUES
    (1, 1, 2, 3), (2, 1, 8, 8), (3, 1, 5, 2), (4, 1, 7, 7), (5, 1, 3, 9), (6, 1, 9, 4),
    (1, 2, 9, 2), (2, 2, 3, 7), (3, 2, 8, 3), (4, 2, 1, 1), (5, 2, 5, 9), (6, 2, 4, 5),
    (1, 3, 6, 4), (2, 3, 2, 2), (3, 3, 9, 9), (4, 3, 6, 6), (5, 3, 1, 8), (6, 3, 4, 3);
