-- upgrade --
CREATE UNIQUE INDEX "uid_game_name_a89c92" ON "game" ("name");
-- downgrade --
DROP INDEX "idx_game_name_a89c92";
