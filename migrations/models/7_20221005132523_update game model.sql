-- upgrade --
ALTER TABLE "game" ADD "image" VARCHAR(255) NOT NULL  DEFAULT 'https://res.cloudinary.com/dgcdfglif/image/upload/v1664625373/profile_avatar/fmwbdgbpdrbbskv2pifq.jpg';
-- downgrade --
ALTER TABLE "game" DROP COLUMN "image";
