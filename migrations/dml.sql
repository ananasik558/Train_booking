TRUNCATE TABLE "trains" CASCADE;
TRUNCATE TABLE "station" CASCADE;
TRUNCATE TABLE "available_seats" CASCADE;
TRUNCATE TABLE "routes" CASCADE;
TRUNCATE TABLE "tickets" CASCADE;
TRUNCATE TABLE "users" CASCADE;
TRUNCATE TABLE "roles" CASCADE;

INSERT INTO "roles" ("id", "name")
VALUES
  (1, 'admin'),
  (2, 'user');

INSERT INTO "users" ("id", "role_id", "username", "email", "password", "created_at")
VALUES
  (1, 1, 'superadmin', 'superadmin@example.com', '$2b$12$Zgx4fNIZ3T0IxXVA6VYn8enmFOIF14oO9xJobVqD.feyCdQ3GtJO.', '2024-12-03 10:00:00'),
  (2, 1, 'denis', 'admin.mark@example.com', '$2b$12$LA./XFS0ssQeJuU4w/yDeeVjIx6RvxlnQ4oq8UEoqQqSNSrR9.3Sm', '2024-12-03 10:05:00'),
  (3, 2, 'tigran', 'john.doe@example.com', '$2b$12$BXpQq2BRaT1q7Er0EaJnheH6pFt6/FgTOHcoRSccfNtS/AG6tIZga', '2024-12-03 10:10:00'),
  (4, 2, 'user_4', 'user.smith@example.com', '$2b$12$VL5v4VJiBIF55rzoNP10leBDofMZ5agiefbiXRWXLpFi9CU1RRj.u', '2024-12-03 10:20:00'),
  (5, 1, 'user_5', 'guest.user@example.com', '$2b$12$mwBqTTmV9hpzE6.89flrueq9T9tFcUcYKWs4VeB8I36Kzgkyo5UaC', '2024-12-03 10:25:00'),
  (6, 2, 'user_6', 'nikita.ponomarev@example.com', '$2b$12$zjFIefMmPhgI/dqIA/JOZes6zRTnxBoKYwlvF8vR/4Wwwhm6CRD1i', '2024-12-03 10:30:00');

INSERT INTO "station" ("id", "name")
VALUES
  (1, 'Moskow'),
  (2, 'Kamishin'),
  (3, 'Perm'),
  (4, 'Volgograd'),
  (5, 'Piter'),
  (6, 'MAI');

INSERT INTO "trains" ("id", "type", "start_time")
VALUES
  (1, 'Passanger', '2024-12-27 14:30:00'),
  (2, 'Passanger', '2025-01-11 14:30:00'),
  (3, 'Passanger', '2024-12-12 14:30:00'),
  (4, 'Passanger', '2024-12-13 14:30:00'),
  (5, 'Passanger', '2024-12-14 14:30:00'),
  (6, 'Passanger', '2024-12-15 14:30:00');

INSERT INTO "routes" ("id", "train_id", "start_station", "finish_station")
VALUES
  (1, 2, 1, 2),
  (2, 3, 2, 1),
  (3, 4, 3, 6),
  (4, 5, 4, 1),
  (5, 1, 5, 1),
  (6, 6, 6, 2);

INSERT INTO "available_seats" ("id", "train_id", "seat_number", "status")
VALUES
  (1, 1, 1, 'occupied'),
  (2, 1, 2, 'occupied'),
  (3, 2, 1, 'available'),
  (4, 2, 2, 'occupied'),
  (5, 3, 1, 'occupied'),
  (6, 3, 2, 'available'),
  (7, 4, 1, 'occupied'),
  (8, 4, 2, 'available'),
  (9, 5, 1, 'occupied');

INSERT INTO "tickets" ("id", "following_user_id", "followed_train_id", "followed_seat_id", "created_at")
VALUES
  (1, 2, 5, 1, '2024-12-03 10:30:00'),
  (2, 3, 1, 5, '2024-12-03 10:35:00'),
  (3, 4, 4, 7, '2024-12-03 10:40:00'),
  (4, 1, 3, 2, '2024-12-03 10:45:00'),
  (5, 5, 6, 9, '2024-12-03 10:50:00'),
  (6, 6, 2, 4, '2024-12-03 10:55:00');

