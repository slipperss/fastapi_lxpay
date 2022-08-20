-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(200) NOT NULL UNIQUE,
    "password" VARCHAR(100) NOT NULL,
    "email_verified" BOOL NOT NULL  DEFAULT False,
    "join_date" TIMESTAMPTZ NOT NULL,
    "last_activity" TIMESTAMPTZ NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True
);
CREATE INDEX IF NOT EXISTS "idx_user_usernam_9987ab" ON "user" ("username");
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
CREATE TABLE IF NOT EXISTS "verification" (
    "link" UUID NOT NULL  PRIMARY KEY,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "verification" IS 'Модель для подтверждения регистрации пользователя';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
