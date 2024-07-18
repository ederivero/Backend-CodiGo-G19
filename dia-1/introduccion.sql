-- Esta es la forma de escribir comentarios en la bd
-- DDL (Data definition language) Crear una nueva base de datos en el servidor
CREATE DATABASE pruebas;

-- Se recomienda que el nombre sea pluralizado porque se guadaran varios registros de esa tabla
CREATE TABLE alumnos(
    -- nombre_de_la_columna tipo_de_dato
    -- constraint columns: PRIMARY KEY | NOT NULL | NULL | UNIQUE | FOREIGN KEY | DEFAULT ... | REFERENCES
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NULL, -- SU VALOR POR DEFECTO DE UNA COLUMNA ES NULL
    correo TEXT NOT NULL UNIQUE, -- El correo va a ser unico y no repetible
    matriculado BOOLEAN DEFAULT true, -- Indicamos un valor por defecto en el caso no se ingrese
    fecha_nacimiento DATE NULL -- En la ultima columna no se coloca la coma ya que no hay otra columna
);

DROP TABLE alumnos; -- Eliminamos de manera definitiva la tabla de la base de datos


-- DML(Data Manipulation Language) Todo lo relacionado a como se puede manejar los datos en la base de datos

INSERT INTO alumnos(id, nombre, apellidos, correo, matriculado, fecha_nacimiento) VALUES
                    (DEFAULT, 'Eduardo', 'de Rivero', 'ederiveroman@gmail.com', true, '1992-08-1');
