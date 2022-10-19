-- upgrade --
ALTER TABLE "message" ADD "is_read" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "message" DROP COLUMN "is_read";
