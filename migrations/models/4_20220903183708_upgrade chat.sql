-- upgrade --
ALTER TABLE "chat" RENAME COLUMN "date_created" TO "created_date";
-- downgrade --
ALTER TABLE "chat" RENAME COLUMN "created_date" TO "date_created";
