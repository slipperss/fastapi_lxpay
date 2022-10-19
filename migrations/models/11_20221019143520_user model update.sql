-- upgrade --
ALTER TABLE "user" ADD "is_online" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "is_online";
