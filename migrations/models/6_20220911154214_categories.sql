-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
COMMENT ON TABLE "category" IS 'Модель категорий игр ';
-- downgrade --
DROP TABLE IF EXISTS "category";
