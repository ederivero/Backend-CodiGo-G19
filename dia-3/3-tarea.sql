-- Crear una base de datos de una empresa que gestiona plataforma de aprendizaje en linea
-- Tablas
-- categoria (id AI PK, nombre unico no nulo y TEXT)
-- cursos (id AI PK, nombre TEXT no puede ser nulo, categoria_id INT)
-- estudiantes (id AI PK, nombre TEXT no nulo, correo unico texto no nulo)
-- inscripciones (id AI PK, curso_id INT NO nulo, estudiante_id int no nulo, fecha_inscripcion timestamp)
-- evaluaciones (id AI PK, una relacion con la tabla de inscripciones en la cual una inscripcion tiene varias evaluaciones y una evaluacion pertenece a una inscripcion, nota float, fecha_evaluacion timestamp)

-- Devolver todos los estudiantes y los cursos que estan inscritos

-- mostrar todos los cursos y los estudiantes que estan inscritos en ellos (tener en cuenta que puede haber cursos sin estudiantes)

-- Obtener el promedio de notas por curso

-- Listar los estudiantes con su nombre y su promedio de notas (GROUP BY)

