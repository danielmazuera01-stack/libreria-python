--  0. BORRAR TODO (reinicio limpio)
DROP TABLE IF EXISTS libros CASCADE;
DROP TABLE IF EXISTS autores CASCADE;
DROP TABLE IF EXISTS generos CASCADE;

--  1. CREAR TABLA INICIAL
CREATE TABLE libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    genero VARCHAR(100),
    anio INT
);

--  2. INSERTAR DATOS DE PRUEBA
INSERT INTO libros (titulo, autor, genero, anio) VALUES
('Cien años de soledad', 'Gabriel Garcia Marquez', 'Realismo magico', 1967),
('El principito', 'Antoine de Saint-Exupery', 'Ficcion', 1943),
('1984', 'George Orwell', 'Distopia', 1949),
('Rebelion en la granja', 'George Orwell', 'Satira', 1945),
('Don Quijote', 'Miguel de Cervantes', 'Novela', 1605);

--  3. CREAR TABLAS NORMALIZADAS
CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE generos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

--  4. INSERTAR AUTORES SIN REPETIR
INSERT INTO autores (nombre)
SELECT DISTINCT autor FROM libros;

--  5. INSERTAR GENEROS SIN REPETIR
INSERT INTO generos (nombre)
SELECT DISTINCT genero FROM libros;

--  6. AGREGAR COLUMNAS DE RELACIÓN
ALTER TABLE libros ADD COLUMN autor_id INT;
ALTER TABLE libros ADD COLUMN genero_id INT;

--  7. RELACIONAR AUTORES
UPDATE libros
SET autor_id = autores.id
FROM autores
WHERE libros.autor = autores.nombre;

--  8. RELACIONAR GENEROS
UPDATE libros
SET genero_id = generos.id
FROM generos
WHERE libros.genero = generos.nombre;

--  9. CREAR CLAVES FORÁNEAS
ALTER TABLE libros
ADD CONSTRAINT fk_autor FOREIGN KEY (autor_id) REFERENCES autores(id);

ALTER TABLE libros
ADD CONSTRAINT fk_genero FOREIGN KEY (genero_id) REFERENCES generos(id);

--  10. BORRAR COLUMNAS ANTIGUAS 
ALTER TABLE libros DROP COLUMN autor;
ALTER TABLE libros DROP COLUMN genero;

-- 11. CONSULTA FINAL 
SELECT l.id, l.titulo, l.anio, a.nombre AS autor, g.nombre AS genero
FROM libros l
JOIN autores a ON l.autor_id = a.id
JOIN generos g ON l.genero_id = g.id;
SELECT * FROM autores;
SELECT * FROM generos;
SELECT l.titulo, a.nombre AS autor, g.nombre AS genero
FROM libros l
JOIN autores a ON l.autor_id = a.id
JOIN generos g ON l.genero_id = g.id;