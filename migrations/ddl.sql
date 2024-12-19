CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "role_id" integer,
  "username" varchar,
  "email" varchar,
  "password" varchar,
  "created_at" timestamp
);
COMMENT ON TABLE "users" IS 'Таблица пользователей. Хранит информацию о всех зарегистрированных пользователях.';
COMMENT ON COLUMN "users"."id" IS 'Идентификатор пользователя';
COMMENT ON COLUMN "users"."role_id" IS 'Роль пользователя (ссылается на таблицу roles)';
COMMENT ON COLUMN "users"."username" IS 'Имя пользователя';
COMMENT ON COLUMN "users"."email" IS 'Электронная почта пользователя';
COMMENT ON COLUMN "users"."password" IS 'Зашифрованный пароль пользователя';
COMMENT ON COLUMN "users"."created_at" IS 'Дата и время регистрации пользователя';

CREATE TABLE "roles" (
  "id" integer PRIMARY KEY,
  "name" varchar
);
COMMENT ON TABLE "roles" IS 'Таблица ролей.';
COMMENT ON COLUMN "roles"."id" IS 'Идентификатор роли';
COMMENT ON COLUMN "roles"."name" IS 'Название роли';

CREATE TABLE "trains" (
  "id" serial PRIMARY KEY,
  "type" varchar,
  "start_time" timestamp
);
COMMENT ON TABLE "trains" IS 'Таблица поездов. Хранит информацию о поездах.';
COMMENT ON COLUMN "trains"."id" IS 'Идентификатор поезда';
COMMENT ON COLUMN "trains"."type" IS 'Тип поезда';
COMMENT ON COLUMN "trains"."start_time" IS 'Дата и время отправления';

CREATE TABLE "tickets" (
  "id" serial PRIMARY KEY,
  "following_user_id" integer,
  "followed_train_id" integer,
  "followed_seat_id" integer,
  "created_at" timestamp
);
COMMENT ON TABLE "tickets" IS 'Таблица билетов.';
COMMENT ON COLUMN "tickets"."id" IS 'Идентификатор билета';
COMMENT ON COLUMN "tickets"."following_user_id" IS 'Идентификатор пользователя, который купил билет';
COMMENT ON COLUMN "tickets"."followed_train_id" IS 'Идентификатор поезда, на который купили билет';
COMMENT ON COLUMN "tickets"."followed_seat_id" IS 'Идентификатор места, на который купили билет';
COMMENT ON COLUMN "tickets"."created_at" IS 'Дата и время покупки';

CREATE TABLE "routes" (
  "id" serial PRIMARY KEY,
  "train_id" integer,
  "start_station" integer,
  "finish_station" integer
);
COMMENT ON TABLE "routes" IS 'Таблица маршрутов.';
COMMENT ON COLUMN "routes"."id" IS 'Идентификатор маршрута';
COMMENT ON COLUMN "routes"."train_id" IS 'Идентификатор задачи, к которой оставлен комментарий (ссылается на таблицу trains)';
COMMENT ON COLUMN "routes"."start_station" IS 'начальная станция';
COMMENT ON COLUMN "routes"."finish_station" IS 'Конечная станция';

CREATE TABLE "available_seats" (
  "id" serial PRIMARY KEY,
  "train_id" integer,
  "seat_number" integer,
  "status" varchar
);
COMMENT ON TABLE "available_seats" IS 'Таблица тегов. Хранит список всех возможных тегов для задач.';
COMMENT ON COLUMN "available_seats"."id" IS 'Идентификатор места';
COMMENT ON COLUMN "available_seats"."train_id" IS 'Идентификатор поезда';
COMMENT ON COLUMN "available_seats"."seat_number" IS 'Номер места';
COMMENT ON COLUMN "available_seats"."status" IS 'Статус';

CREATE TABLE "station" (
  "id" serial PRIMARY KEY,
  "name" varchar
);
COMMENT ON TABLE "station" IS 'Таблица станция.';
COMMENT ON COLUMN "station"."id" IS 'Идентификатор станции';
COMMENT ON COLUMN "station"."name" IS 'Имя станции';

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id");

ALTER TABLE "tickets" ADD FOREIGN KEY ("following_user_id") REFERENCES "users" ("id");

ALTER TABLE "tickets" ADD FOREIGN KEY ("followed_train_id") REFERENCES "trains" ("id");

ALTER TABLE "tickets" ADD FOREIGN KEY ("followed_seat_id") REFERENCES "available_seats" ("id");

ALTER TABLE "routes" ADD FOREIGN KEY ("train_id") REFERENCES "trains" ("id");

ALTER TABLE "routes" ADD FOREIGN KEY ("start_station") REFERENCES "station" ("id");

ALTER TABLE "routes" ADD FOREIGN KEY ("finish_station") REFERENCES "station" ("id");

ALTER TABLE "available_seats" ADD FOREIGN KEY ("train_id") REFERENCES "trains" ("id");