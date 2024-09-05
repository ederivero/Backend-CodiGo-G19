-- CreateEnum
CREATE TYPE "USUARIO_ROL" AS ENUM ('ADMINISTRADOR', 'CLIENTE');

-- CreateEnum
CREATE TYPE "PARTIDO_ESTADO" AS ENUM ('POR_EMPEZAR', 'EMPEZADO', 'FINALIZADO', 'SUSPENDIDO');

-- CreateTable
CREATE TABLE "fechas" (
    "id" UUID NOT NULL,
    "nombre" TEXT NOT NULL,

    CONSTRAINT "fechas_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "usuarios" (
    "id" UUID NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "rol" "USUARIO_ROL" NOT NULL DEFAULT 'CLIENTE',

    CONSTRAINT "usuarios_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "equipos" (
    "id" UUID NOT NULL,
    "nombre" TEXT NOT NULL,
    "imagen" TEXT,

    CONSTRAINT "equipos_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "jugadores" (
    "id" UUID NOT NULL,
    "nombre" TEXT NOT NULL,
    "posicion" TEXT,
    "fecha_nacimiento" DATE NOT NULL,
    "equipo_id" UUID NOT NULL,

    CONSTRAINT "jugadores_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Partido" (
    "id" UUID NOT NULL,
    "fecha_id" UUID NOT NULL,
    "equipo_local_id" UUID NOT NULL,
    "equipo_visitante_id" UUID NOT NULL,
    "fecha_partido" DATE NOT NULL,
    "hora" TIME NOT NULL,
    "zona_horaria" TEXT NOT NULL,
    "lugar" TEXT NOT NULL,
    "estado" "PARTIDO_ESTADO" NOT NULL DEFAULT 'POR_EMPEZAR',
    "marcador_local" INTEGER NOT NULL,
    "marcador_visitante" INTEGER NOT NULL,

    CONSTRAINT "Partido_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "fechas_nombre_key" ON "fechas"("nombre");

-- CreateIndex
CREATE UNIQUE INDEX "usuarios_email_key" ON "usuarios"("email");

-- CreateIndex
CREATE UNIQUE INDEX "equipos_nombre_key" ON "equipos"("nombre");

-- AddForeignKey
ALTER TABLE "jugadores" ADD CONSTRAINT "jugadores_equipo_id_fkey" FOREIGN KEY ("equipo_id") REFERENCES "equipos"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Partido" ADD CONSTRAINT "Partido_fecha_id_fkey" FOREIGN KEY ("fecha_id") REFERENCES "fechas"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Partido" ADD CONSTRAINT "Partido_equipo_local_id_fkey" FOREIGN KEY ("equipo_local_id") REFERENCES "equipos"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Partido" ADD CONSTRAINT "Partido_equipo_visitante_id_fkey" FOREIGN KEY ("equipo_visitante_id") REFERENCES "equipos"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
