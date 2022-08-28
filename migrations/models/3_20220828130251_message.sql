-- upgrade --
CREATE TABLE IF NOT EXISTS "message" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "msg" VARCHAR(10000) NOT NULL,
    "created_date" TIMESTAMPTZ NOT NULL,
    "chat_id" UUID NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "message";
