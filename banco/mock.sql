-- Perfis fictícios para a demonstração do app (vídeo de apresentação).
-- Completa a seed: 4 pessoas novas com notas, e listas de interesses de todas
-- as 10 pessoas nas 3 categorias, coerentes com as notas de cada uma.
-- Carregado por banco/conexao.py só uma vez, num banco ainda sem listas.

INSERT OR IGNORE INTO pessoa (id, nome) VALUES
    (7, 'Gabriel'),
    (8, 'Helena'),
    (9, 'Igor'),
    (10, 'Júlia');

INSERT OR IGNORE INTO nota (pessoa_id, categoria_id, x, y) VALUES
    (7, 1, 8, 6),
    (7, 2, 7, 4),
    (7, 3, 7, 5),
    (8, 1, 2, 8),
    (8, 2, 2, 6),
    (8, 3, 3, 7),
    (9, 1, 6, 3),
    (9, 2, 6, 8),
    (9, 3, 5, 3),
    (10, 1, 9, 5),
    (10, 2, 4, 2),
    (10, 3, 8, 8);

-- Interesses: posição 1 = favorito.
INSERT OR IGNORE INTO ranking (pessoa_id, item_id, posicao) VALUES
    -- Ana, Jogos
    (1, 8, 1),  -- The Legend of Zelda: Breath of the Wild
    (1, 6, 2),  -- Hollow Knight
    (1, 3, 3),  -- Stardew Valley
    (1, 20, 4),  -- The Last of Us
    (1, 22, 5),  -- The Witcher 3: Wild Hunt
    (1, 1, 6),  -- Minecraft
    -- Ana, Bandas
    (1, 58, 1),  -- Slayer
    (1, 60, 2),  -- Death
    (1, 95, 3),  -- Sepultura
    (1, 61, 4),  -- Cannibal Corpse
    (1, 97, 5),  -- Krisiun
    (1, 51, 6),  -- Black Sabbath
    (1, 63, 7),  -- Mayhem
    -- Ana, Séries/Animes
    (1, 128, 1),  -- Attack on Titan
    (1, 134, 2),  -- Jujutsu Kaisen
    (1, 133, 3),  -- Demon Slayer: Kimetsu no Yaiba
    (1, 108, 4),  -- The Boys
    (1, 135, 5),  -- Chainsaw Man
    (1, 102, 6),  -- Stranger Things
    -- Bruno, Jogos
    (2, 2, 1),  -- Counter-Strike 2
    (2, 9, 2),  -- VALORANT
    (2, 5, 3),  -- League of Legends
    (2, 17, 4),  -- Dota 2
    (2, 12, 5),  -- Tom Clancy's Rainbow Six Siege
    (2, 13, 6),  -- Overwatch
    -- Bruno, Bandas
    (2, 73, 1),  -- Linkin Park
    (2, 77, 2),  -- Bring Me the Horizon
    (2, 55, 3),  -- Avenged Sevenfold
    (2, 80, 4),  -- Evanescence
    (2, 92, 5),  -- Foo Fighters
    (2, 93, 6),  -- Red Hot Chili Peppers
    -- Bruno, Séries/Animes
    (2, 126, 1),  -- One Piece
    (2, 125, 2),  -- Naruto
    (2, 129, 3),  -- Dragon Ball Z
    (2, 136, 4),  -- SPY x FAMILY
    (2, 142, 5),  -- One Punch Man
    (2, 117, 6),  -- Brooklyn Nine-Nine
    -- Carla, Jogos
    (3, 20, 1),  -- The Last of Us
    (3, 18, 2),  -- Red Dead Redemption 2
    (3, 19, 3),  -- God of War
    (3, 26, 4),  -- Final Fantasy VII
    (3, 24, 5),  -- Baldur's Gate 3
    (3, 6, 6),  -- Hollow Knight
    -- Carla, Bandas
    (3, 58, 1),  -- Slayer
    (3, 60, 2),  -- Death
    (3, 95, 3),  -- Sepultura
    (3, 97, 4),  -- Krisiun
    (3, 61, 5),  -- Cannibal Corpse
    (3, 56, 6),  -- Metallica
    (3, 57, 7),  -- Megadeth
    -- Carla, Séries/Animes
    (3, 101, 1),  -- Breaking Bad
    (3, 121, 2),  -- Chernobyl
    (3, 113, 3),  -- Dark
    (3, 127, 4),  -- Death Note
    (3, 119, 5),  -- Black Mirror
    (3, 145, 6),  -- Neon Genesis Evangelion
    (3, 109, 7),  -- Euphoria
    -- Diego, Jogos
    (4, 9, 1),  -- VALORANT
    (4, 2, 2),  -- Counter-Strike 2
    (4, 13, 3),  -- Overwatch
    (4, 14, 4),  -- Fortnite
    (4, 5, 5),  -- League of Legends
    (4, 16, 6),  -- PUBG: Battlegrounds
    -- Diego, Bandas
    (4, 85, 1),  -- Queen
    (4, 86, 2),  -- Pink Floyd
    (4, 84, 3),  -- Led Zeppelin
    (4, 99, 4),  -- Legião Urbana
    (4, 89, 5),  -- Deep Purple
    (4, 90, 6),  -- Scorpions
    -- Diego, Séries/Animes
    (4, 104, 1),  -- Game of Thrones
    (4, 114, 2),  -- Peaky Blinders
    (4, 128, 3),  -- Attack on Titan
    (4, 115, 4),  -- Narcos
    (4, 105, 5),  -- La Casa de Papel
    (4, 127, 6),  -- Death Note
    -- Elisa, Jogos
    (5, 35, 1),  -- Mario Kart 8 Deluxe
    (5, 48, 2),  -- Among Us
    (5, 1, 3),  -- Minecraft
    (5, 3, 4),  -- Stardew Valley
    (5, 47, 5),  -- It Takes Two
    (5, 38, 6),  -- Super Smash Bros. Ultimate
    -- Elisa, Bandas
    (5, 74, 1),  -- Slipknot
    (5, 75, 2),  -- System of a Down
    (5, 71, 3),  -- Gojira
    (5, 83, 4),  -- Rammstein
    (5, 70, 5),  -- Tool
    (5, 76, 6),  -- Korn
    -- Elisa, Séries/Animes
    (5, 116, 1),  -- Friends
    (5, 103, 2),  -- The Office
    (5, 118, 3),  -- The Big Bang Theory
    (5, 146, 4),  -- Haikyu!!
    (5, 137, 5),  -- Frieren e a Jornada para o Além
    (5, 107, 6),  -- Wandinha
    -- Felipe, Jogos
    (6, 33, 1),  -- EA Sports FC 27
    (6, 34, 2),  -- Rocket League
    (6, 10, 3),  -- Call of Duty: Modern Warfare
    (6, 7, 4),  -- Grand Theft Auto V
    (6, 11, 5),  -- Battlefield 6
    (6, 14, 6),  -- Fortnite
    -- Felipe, Bandas
    (6, 52, 1),  -- Iron Maiden
    (6, 66, 2),  -- Helloween
    (6, 67, 3),  -- Blind Guardian
    (6, 96, 4),  -- Angra
    (6, 68, 5),  -- Sabaton
    (6, 79, 6),  -- Nightwish
    (6, 69, 7),  -- Dream Theater
    -- Felipe, Séries/Animes
    (6, 124, 1),  -- Arcane
    (6, 138, 2),  -- Solo Leveling
    (6, 140, 3),  -- Hunter x Hunter
    (6, 139, 4),  -- Fullmetal Alchemist: Brotherhood
    (6, 148, 5),  -- Cowboy Bebop
    (6, 130, 6),  -- Os Cavaleiros do Zodíaco
    -- Gabriel, Jogos
    (7, 4, 1),  -- Elden Ring
    (7, 28, 2),  -- Dark Souls
    (7, 6, 3),  -- Hollow Knight
    (7, 30, 4),  -- Cuphead
    (7, 29, 5),  -- Hades
    (7, 19, 6),  -- God of War
    -- Gabriel, Bandas
    (7, 71, 1),  -- Gojira
    (7, 65, 2),  -- Behemoth
    (7, 62, 3),  -- Arch Enemy
    (7, 81, 4),  -- Amon Amarth
    (7, 95, 5),  -- Sepultura
    (7, 61, 6),  -- Cannibal Corpse
    (7, 56, 7),  -- Metallica
    -- Gabriel, Séries/Animes
    (7, 128, 1),  -- Attack on Titan
    (7, 135, 2),  -- Chainsaw Man
    (7, 147, 3),  -- Tokyo Ghoul
    (7, 134, 4),  -- Jujutsu Kaisen
    (7, 108, 5),  -- The Boys
    (7, 113, 6),  -- Dark
    -- Helena, Jogos
    (8, 35, 1),  -- Mario Kart 8 Deluxe
    (8, 48, 2),  -- Among Us
    (8, 1, 3),  -- Minecraft
    (8, 3, 4),  -- Stardew Valley
    (8, 47, 5),  -- It Takes Two
    (8, 44, 6),  -- The Sims 4
    -- Helena, Bandas
    (8, 80, 1),  -- Evanescence
    (8, 79, 2),  -- Nightwish
    (8, 85, 3),  -- Queen
    (8, 73, 4),  -- Linkin Park
    (8, 99, 5),  -- Legião Urbana
    (8, 100, 6),  -- Titãs
    -- Helena, Séries/Animes
    (8, 116, 1),  -- Friends
    (8, 107, 2),  -- Wandinha
    (8, 136, 3),  -- SPY x FAMILY
    (8, 137, 4),  -- Frieren e a Jornada para o Além
    (8, 146, 5),  -- Haikyu!!
    (8, 102, 6),  -- Stranger Things
    (8, 103, 7),  -- The Office
    -- Igor, Jogos
    (9, 18, 1),  -- Red Dead Redemption 2
    (9, 22, 2),  -- The Witcher 3: Wild Hunt
    (9, 23, 3),  -- Cyberpunk 2077
    (9, 21, 4),  -- The Elder Scrolls V: Skyrim
    (9, 24, 5),  -- Baldur's Gate 3
    (9, 7, 6),  -- Grand Theft Auto V
    -- Igor, Bandas
    (9, 70, 1),  -- Tool
    (9, 69, 2),  -- Dream Theater
    (9, 71, 3),  -- Gojira
    (9, 83, 4),  -- Rammstein
    (9, 75, 5),  -- System of a Down
    (9, 86, 6),  -- Pink Floyd
    -- Igor, Séries/Animes
    (9, 101, 1),  -- Breaking Bad
    (9, 114, 2),  -- Peaky Blinders
    (9, 115, 3),  -- Narcos
    (9, 120, 4),  -- Mr. Robot
    (9, 123, 5),  -- Rick and Morty
    (9, 124, 6),  -- Arcane
    -- Júlia, Jogos
    (10, 33, 1),  -- EA Sports FC 27
    (10, 34, 2),  -- Rocket League
    (10, 14, 3),  -- Fortnite
    (10, 15, 4),  -- Free Fire
    (10, 43, 5),  -- Clash Royale
    (10, 32, 6),  -- Roblox
    -- Júlia, Bandas
    (10, 88, 1),  -- Guns N' Roses
    (10, 87, 2),  -- AC/DC
    (10, 91, 3),  -- Nirvana
    (10, 94, 4),  -- Ramones
    (10, 93, 5),  -- Red Hot Chili Peppers
    (10, 98, 6),  -- Ratos de Porão
    (10, 92, 7),  -- Foo Fighters
    -- Júlia, Séries/Animes
    (10, 106, 1),  -- Round 6
    (10, 105, 2),  -- La Casa de Papel
    (10, 110, 3),  -- Sintonia
    (10, 111, 4),  -- DNA do Crime
    (10, 112, 5),  -- Cidade Invisível
    (10, 109, 6),  -- Euphoria
    (10, 119, 7);  -- Black Mirror
