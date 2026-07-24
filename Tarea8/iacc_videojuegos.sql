-- ============================================================
--  PROGRAMACION AVANZADA - SEMANA 8
--  Script SQL: Crear Base de Datos, Tabla e Insertar Registros
--  Autor: Claudio Baeza Henríquez  - 2026
-- ============================================================

-- PASO 1: Crear la base de datos
CREATE DATABASE IF NOT EXISTS iacc_videojuegos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- PASO 2: Usar la base de datos creada
USE iacc_videojuegos;

-- PASO 3: Eliminar la tabla si ya existe (para empezar limpio)
DROP TABLE IF EXISTS Videojuegos;

-- PASO 4: Crear la tabla Videojuegos
CREATE TABLE Videojuegos (
    ID             INT          PRIMARY KEY,
    Titulo         VARCHAR(100) NOT NULL,
    Genero         VARCHAR(50)  NOT NULL,
    Clasificacion  VARCHAR(30)  NOT NULL,
    Plataforma     VARCHAR(50)  NOT NULL
);

-- PASO 5: Insertar los registros de ejemplo
INSERT INTO Videojuegos (ID, Titulo, Genero, Clasificacion, Plataforma) VALUES
    (1, 'The Legend of Zelda: Breath of the Wild', 'Aventura',  'E10+ (Mayores de 10)', 'Nintendo Switch'),
    (2, 'FIFA 22',                                 'Deportes',  'E (Todos)',             'Multiplataforma'),
    (3, 'Cyberpunk 2077',                          'RPG',       'M (Adultos)',           'PC'),
    (4, 'God of War',                              'Accion',    'M (Adultos)',           'PlayStation 4'),
    (5, 'Minecraft',                               'Simulacion','E10+ (Mayores de 10)', 'Multiplataforma'),
    (6, 'Call of Duty: Warzone',                   'Accion',    'M (Adultos)',           'Multiplataforma'),
    (7, 'Among Us',                                'Estrategia','E10+ (Mayores de 10)', 'Multiplataforma'),
    (8, 'Forza Horizon 5',                         'Carreras',  'E (Todos)',             'Xbox Series X');

-- PASO 6: Verificar que los datos se insertaron correctamente
SELECT * FROM Videojuegos;
