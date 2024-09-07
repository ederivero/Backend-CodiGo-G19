/*
  Warnings:

  - You are about to drop the column `imagen` on the `equipos` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "equipos" DROP COLUMN "imagen";

-- CreateTable
CREATE TABLE "imagenes" (
    "id" UUID NOT NULL,
    "key" TEXT NOT NULL,
    "path" TEXT,
    "content_type" TEXT NOT NULL,
    "extension" TEXT NOT NULL,
    "equipo_id" UUID,
    "jugador_id" UUID,

    CONSTRAINT "imagenes_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "imagenes_key_key" ON "imagenes"("key");

-- AddForeignKey
ALTER TABLE "imagenes" ADD CONSTRAINT "imagenes_equipo_id_fkey" FOREIGN KEY ("equipo_id") REFERENCES "equipos"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "imagenes" ADD CONSTRAINT "imagenes_jugador_id_fkey" FOREIGN KEY ("jugador_id") REFERENCES "jugadores"("id") ON DELETE SET NULL ON UPDATE CASCADE;
