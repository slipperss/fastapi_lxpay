-- upgrade --
ALTER TABLE "user" ALTER COLUMN "password" SET DEFAULT '';
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "password" DROP DEFAULT;
