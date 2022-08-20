-- upgrade --
ALTER TABLE "user" ADD "avatar" VARCHAR(250) NOT NULL  DEFAULT '';
ALTER TABLE "user" ADD "is_superuser" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "avatar";
ALTER TABLE "user" DROP COLUMN "is_superuser";
