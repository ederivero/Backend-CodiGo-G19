-- INNER JOIN devuelve los registros que tengan en comun la tabla izquierda con la tabla derecha
SELECT * FROM clientes INNER JOIN cuentas 
ON -- INDICAR QUE COLUMNAS VAMOS A UTILIZAR PARA HACER LA REFERENCIA
clientes.id = cuentas.cliente_id; 

-- El LEFT JOIN devuelve toda la informacion (registros) de la tabla de la izquierda y opcionalmente si tiene registros en la tabla de la derecha
SELECT * FROM clientes LEFT JOIN cuentas
ON
clientes.id = cuentas.cliente_id;


-- Devolver la informacion ( nombre, correo, status, numero_cuenta, tipo_moneda)
SELECT nombre, correo, status, numero_cuenta, tipo_moneda FROM clientes INNER JOIN cuentas 
ON clientes.id = cuentas.cliente_id; 

-- Devolver la informacion de los usuarios que tengan cuenta que no sea en soles (nombre, correo)
SELECT nombre, correo 
FROM clientes INNER JOIN cuentas ON clientes.id = cuentas.cliente_id
WHERE tipo_moneda != 'SOLES'; 

-- Devolver el usuario que tenga mantenimiento mas alto y que tipo de moneda es su cuenta
SELECT nombre, mantenimiento, tipo_moneda
FROM clientes INNER JOIN cuentas ON clientes.id = cuentas.cliente_id
ORDER BY mantenimiento DESC
LIMIT 1; 


-- Crear tabla
-- id ai primary key no nulo
-- cuenta_origen RELACION con la tabla cuentas puede ser null
-- cuenta_destino RELACION con la tabla cuentas no puede ser null
-- monto float no puede ser null
-- fecha_operacion timestamp la hora del servidor x defecto

CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY NOT NULL,
    cuenta_origen INT,
    cuenta_destino INT NOT NULL,
    monto FLOAT NOT NULL,
    fecha_operacion TIMESTAMP DEFAULT NOW(),
    -- RELACIONES
    CONSTRAINT fk_cuenta_origen FOREIGN KEY(cuenta_origen) REFERENCES cuentas(id),
    CONSTRAINT fk_cuenta_destino FOREIGN KEY(cuenta_destino) REFERENCES cuentas(id)
);

-- Si tenemos cuenta de origen y cuenta destino entonces es una transferencia
-- Si tenemos solo cuenta de destino > deposito
-- Si tenemos solo cuenta de origen > retiro

-- Asi se puede editar la configuracion de una tabla sin la necesidad de eliminarla y volver a crear ya que se perderia la informacion dentro de ella
ALTER TABLE movimientos ALTER COLUMN cuenta_destino DROP NOT NULL;

-- Cambia el nombre de la columna
ALTER TABLE movimientos RENAME COLUMN fecha_operacion TO fecha_transaccion;