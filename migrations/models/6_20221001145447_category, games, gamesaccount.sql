-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
COMMENT ON TABLE "category" IS 'Модель категорий игр ';;
CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "game" IS 'Модель игр ';;
CREATE TABLE IF NOT EXISTS "game_account" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "created_date" TIMESTAMPTZ NOT NULL,
    "is_published" BOOL NOT NULL  DEFAULT True,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE RESTRICT,
    "seller_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS "idx_game_accoun_title_a1461b" ON "game_account" ("title");
COMMENT ON TABLE "game_account" IS 'Модель аккаунта на продажу ';-- downgrade --
DROP TABLE IF EXISTS "category";
DROP TABLE IF EXISTS "game";
DROP TABLE IF EXISTS "game_account";
