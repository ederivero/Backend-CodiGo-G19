-- Crear base de datos llamada finanzas
CREATE DATABASE finanzas;

-- Crear una tabla en la cual registremos la informacion de los clientes de la siguiente manera
-- id autoincrementable primary key
-- nombre texto no puede ser nulo
-- correo unico(no se repite) no puede ser nulo
-- status texto no puede ser nulo
-- activo booleano por defecto sea verdadero
-- fecha_creacion timestamp 

-- Cuando queremos indicar un numero limitado de opciones para guardar entonces debemos usar un ENUMerable (ENUM)
CREATE TYPE enum_status AS ENUM ('TIPO_A', 'TIPO_B', 'TIPO_C');

CREATE TABLE clientes (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    status enum_status NOT NULL DEFAULT 'TIPO_A',
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT NOW() -- Asi se captura la hora actual del servidor al momento de hacer un insert
);


-- Insertar los siguientes registros
INSERT INTO clientes (nombre, correo, status, activo) VALUES
('Rodrigo Juarez Quispe', 'rjuarez@gmail.com', 'TIPO_A', true),
('Mariana Sanchez Gil', 'msanchez@hotmail.com', 'TIPO_B', true),
('Juliana Taco Martinez', 'jtaco@gmail.com', 'TIPO_A', true),
('Gabriel Gonza Perez', 'ggonza@yahoo.es', 'TIPO_C', false);

-- FUNCIONES DE AGREGACION
-- promedio > avg(COLUMNA_NUMERICA)
-- minimo > min(COLUMNA_NUMERICA)
-- maximo > max(COLUMNA_NUMERICA)
-- contar > count(COLUMNA O REGISTRO CUALQUIERA)

-- Si usamos a parte de la funcion de agregacion otra columna, entonces nos vemos en la obligacion de utilizar el GROUP BY (agrupamiento)

SELECT COUNT(id), correo FROM clientes GROUP BY correo;


-- Cuantos usuarios estan activos o no
SELECT COUNT(*), activo FROM clientes GROUP BY activo;



-- Cuantos clientes son del TIPO_A o TIPO_B
-- 3 TIPO_A
-- 2 TIPO_B

SELECT COUNT(*), status 
FROM clientes 
-- WHERE status = 'TIPO_A' OR status = 'TIPO_B' 
WHERE status IN ('TIPO_A','TIPO_B') 
GROUP BY status
ORDER BY count(*) ASC;
-- En el order by se puede poner el nombre de la columna O el numero de la columna, es decir, si queremos la primera columna sera el 1
ORDER BY 1 ASC;





