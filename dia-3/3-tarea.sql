-- Crear una base de datos de una empresa que gestiona plataforma de aprendizaje en linea
-- Tablas
-- categoria (id AI PK, nombre unico no nulo y TEXT)
-- cursos (id AI PK, nombre TEXT no puede ser nulo, categoria_id INT)
-- estudiantes (id AI PK, nombre TEXT no nulo, correo unico texto no nulo)
-- inscripciones (id AI PK, curso_id INT NO nulo, estudiante_id int no nulo, fecha_inscripcion timestamp)
-- evaluaciones (id AI PK, una relacion con la tabla de inscripciones en la cual una inscripcion tiene varias evaluaciones y una evaluacion pertenece a una inscripcion, nota float, fecha_evaluacion timestamp)
CREATE DATABASE cursos_en_linea;

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    categoria_id TEXT,
    CONSTRAINT fk_categorias FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE inscripciones (
    id INT PRIMARY KEY,
    curso_id INT NOT NULL,
    estudiante_id INT NOT NULL,
    fecha_inscripcion TIMESTAMP,
    CONSTRAINT fk_curso FOREIGN KEY (curso_id) REFERENCES cursos(id),
    CONSTRAINT fk_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
);

CREATE TABLE evaluaciones (
    id INT PRIMARY KEY,
    inscripcion_id INT,
    nota FLOAT,
    fecha_evaluacion DATE,
    CONSTRAINT fk_inscripcion FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id)
);

-- Devolver todos los estudiantes y los cursos que estan inscritos
SELECT 
    E.nombre, 
    C.nombre 
FROM 
    estudiantes E
INNER JOIN 
    inscripciones I ON E.id = I.estudiante_id
INNER JOIN 
    cursos C ON I.curso_id = C.id;

-- mostrar todos los cursos y los estudiantes que estan inscritos en ellos (tener en cuenta que puede haber cursos sin estudiantes)
SELECT 
    C.nombre, 
    E.nombre 
FROM 
    cursos C
LEFT JOIN 
    inscripciones I ON C.id = I.curso_id
LEFT JOIN 
    estudiantes E ON I.estudiante_id = E.id;

-- Obtener el promedio de notas por curso
SELECT 
    C.nombre, 
    AVG(EV.Nota) AS promedio_nota 
FROM 
    cursos C
INNER JOIN 
    inscripciones I ON C.id = I.curso_id
INNER JOIN 
    evaluaciones EV ON I.id = EV.inscripcion_id
GROUP BY 
    C.nombre
HAVING 
    COUNT(EV.id) > 0;


-- Listar los estudiantes con su nombre y su promedio de notas (GROUP BY)
SELECT 
    E.nombre, 
    AVG(EV.nota) AS PromedioNota 
FROM 
    estudiantes E
INNER JOIN 
    inscripciones I ON E.id = I.estudiante_id
INNER JOIN 
    evaluaciones EV ON I.id = EV.inscripcion_id
GROUP BY 
    E.nombre
HAVING 
    COUNT(EV.id) > 0;

