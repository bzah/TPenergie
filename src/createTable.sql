DROP TABLE measure;
DROP TABLE measure_without_zero;
DROP TABLE measure_with_filter;
DROP TABLE appliance;
DROP TABLE household;


CREATE TABLE household (
  id INTEGER PRIMARY KEY
);

CREATE TABLE appliance (
  id        SERIAL PRIMARY KEY,
  name      VARCHAR(50),
  project   VARCHAR(50),
  household INTEGER,
  file      VARCHAR(50),
  FOREIGN KEY (household) REFERENCES household (id)
);


CREATE TABLE measure (
  id        SERIAL PRIMARY KEY,
  appliance INTEGER,
  date      TIMESTAMP,
  state     INTEGER,
  energy    INTEGER,
  FOREIGN KEY (appliance) REFERENCES appliance (id)
);

CREATE TABLE measure_without_zero (
  id        SERIAL PRIMARY KEY,
  appliance INTEGER,
  date      TIMESTAMP,
  state     INTEGER,
  energy    INTEGER,
  FOREIGN KEY (appliance) REFERENCES appliance (id)
);

CREATE TABLE measure_with_filter (
  id        SERIAL PRIMARY KEY,
  appliance INTEGER,
  date      TIMESTAMP,
  state     INTEGER,
  energy    INTEGER,
  recurrence INTEGER,
  FOREIGN KEY (appliance) REFERENCES appliance (id)
);
