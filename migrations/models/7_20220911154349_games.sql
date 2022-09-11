-- upgrade --
CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "game" IS 'Модель игр ';
-- downgrade --
DROP TABLE IF EXISTS "game";
