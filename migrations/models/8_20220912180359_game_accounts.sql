-- upgrade --
CREATE TABLE IF NOT EXISTS "game_account" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "created_date" TIMESTAMPTZ NOT NULL,
    "is_published" BOOL NOT NULL  DEFAULT True,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE,
    "seller_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_game_accoun_title_a1461b" ON "game_account" ("title");
COMMENT ON TABLE "game_account" IS 'Модель аккаунта на продажу ';
-- downgrade --
DROP TABLE IF EXISTS "game_account";
