-- Para la tabla clientes vea el archivo 1_repaso_sql.sql

-- id autoincrementable primary key
-- numero_cuenta text not null unico,
-- tipo_moneda SOLES | DOLARES | EUROS no nulo
-- fecha_creacion timestamp valor actual del servidor no nulo
-- mantenimiento float puede ser nulo

CREATE TYPE enum_tipo_moneda AS ENUM ('SOLES', 'DOLARES', 'EUROS');

CREATE TABLE cuentas (
    id SERIAL PRIMARY KEY NOT NULL,
    numero_cuenta TEXT NOT NULL UNIQUE,
    tipo_moneda enum_tipo_moneda NOT NULL,
    fecha_creacion TIMESTAMP default NOW(),
    mantenimiento FLOAT NULL,
    cliente_id INT NOT NULL,
    -- CREO LA RELACION ENTRE CUENTAS Y CLIENTES
    CONSTRAINT fk_clientes FOREIGN KEY(cliente_id) REFERENCES clientes(id)
);


INSERT INTO cuentas (numero_cuenta, tipo_moneda, fecha_creacion, mantenimiento, cliente_id) VALUES
('0f302b7e-41b6-45e9-950c-d2640f3ddcdf', 'SOLES', '2023-10-08T10:05', '1.5', '1'),
('7160f103-dc2a-4e67-9123-3d795bf4938b', 'SOLES', '2024-02-01T14:23', '1', '2'),
('b2eeb8ab-f06b-49df-8dac-332b2b48d7ff', 'DOLARES', '2020-12-08T16:17', '0', '1'),
('82c51e22-f4a6-4430-b401-05e458979c1b', 'SOLES', '2022-05-14T09:45', '1', '3'),
('57c54a3c-0a92-45b7-b888-0cbf827c93f8', 'SOLES', '2024-03-14T11:28', '1.2', '4'),
('c62ed24c-430b-462f-bdb3-ba79199bcffc', 'EUROS', '2023-10-04T12:27', '0.5', '3'),
('2343b92e-152a-4316-a4af-7406f8e551b8', 'SOLES', '2023-11-09T11:11', '0', '2');


-- Cuantas cuentas hay en soles, dolares y euros
SELECT COUNT(*), tipo_moneda 
FROM cuentas 
GROUP BY tipo_moneda;

-- Mostrar los numeros de cuenta y su tipo de moneda ordenados por la fecha de creacion del mas nuevo al mas viejo
SELECT numero_cuenta, tipo_moneda, fecha_creacion 
FROM cuentas 
ORDER BY fecha_creacion DESC;

-- Cual es la cuenta con mayor mantenimiento 
SELECT mantenimiento, numero_cuenta 
FROM cuentas 
ORDER BY mantenimiento DESC 
LIMIT 1;

-- Que cliente tiene mas cuentas
-- Como hay un triple empate entre los clientes con mas cuentas no es correspondiente colocar el limit
SELECT count(*), cliente_id 
FROM cuentas 
GROUP BY cliente_id 
ORDER BY 1 DESC;

-- Ingresar un nuevo cliente 
INSERT INTO clientes (nombre, correo, status, activo) VALUES
('Eduardo de Rivero Manrique', 'ederivero@gmail.com', 'TIPO_B', true);