CREATE TABLE appliance (
  id        SERIAL PRIMARY KEY,
  name      VARCHAR(50),
  project   VARCHAR(50),
  household VARCHAR(50),
  file      VARCHAR(50)
);


CREATE TABLE measure (
  id        SERIAL PRIMARY KEY,
  appliance INTEGER,
  date      TIMESTAMP,
  state     INTEGER,
  energy    INTEGER,
  FOREIGN KEY (appliance) REFERENCES appliance (id)

);