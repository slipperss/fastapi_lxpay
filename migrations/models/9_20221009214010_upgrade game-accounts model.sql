-- upgrade --
ALTER TABLE "game_account" ADD "price" DOUBLE PRECISION NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "game_account" DROP COLUMN "price";
