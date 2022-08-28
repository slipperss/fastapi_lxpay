-- upgrade --
CREATE TABLE IF NOT EXISTS "chat" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "date_created" TIMESTAMPTZ NOT NULL
);;
CREATE TABLE "chat_user" ("user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,"chat_id" UUID NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "chat_user";
DROP TABLE IF EXISTS "chat";
