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

-- GET DB disk usage (from : https://wiki.postgresql.org/wiki/Disk_Usage)

SELECT *, pg_size_pretty(total_bytes) AS total
    , pg_size_pretty(index_bytes) AS INDEX
    , pg_size_pretty(toast_bytes) AS toast
    , pg_size_pretty(table_bytes) AS TABLE
  FROM (
  SELECT *, total_bytes-index_bytes-COALESCE(toast_bytes,0) AS table_bytes FROM (
      SELECT c.oid,nspname AS table_schema, relname AS TABLE_NAME
              , c.reltuples AS row_estimate
              , pg_total_relation_size(c.oid) AS total_bytes
              , pg_indexes_size(c.oid) AS index_bytes
              , pg_total_relation_size(reltoastrelid) AS toast_bytes
          FROM pg_class c
          LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
          WHERE relkind = 'r'
  ) a
) a;