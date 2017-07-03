
-- REQUETE 1 --
EXPLAIN ANALYZE
Select energy from measure inner join appliance on measure.appliance = appliance.id where appliance.id = 5 and measure.date = '1998-01-22 14:00:00.000000';

EXPLAIN ANALYZE
Select energy
from measure_without_zero
inner join appliance
on measure_without_zero.appliance = appliance.id
where appliance.id = 21 and measure_without_zero.date <= '1998-01-22 14:00:00.000000'
order by measure_without_zero.date DESC LIMIT 1;

EXPLAIN ANALYZE
Select energy
from measure_with_filter
inner join appliance
on measure_with_filter.appliance = appliance.id
where appliance.id = 21 and measure_with_filter.date <= '1998-01-22 14:00:00.000000'
order by measure_with_filter.date DESC LIMIT 1;

-- REQUETE 2 --
EXPLAIN ANALYZE
SELECT sum(m.energy) as total_conso
FROM Measure m
Inner join Appliance a on a.id = m.appliance
Inner join Household h on h.id = a.household
Where h.id = 2000900
AND m.date >= ((
  select max(m.date)
  from  Measure m
  Inner join Appliance a on a.id = m.appliance
  Inner join Household h on h.id = a.household
  Where h.id= 2000900
) - interval '1hours' );


-- REQUETE 3 --
EXPLAIN ANALYSE
  SELECT a.name, sum(m.energy) as conso
  FROM Measure m
  Inner join Appliance a on a.id = m.appliance
  Where m.date >= (
    (
        select max(m2.date)
        from  Measure m2
        Inner join Appliance a2 on a2.id = m2.appliance
        Where m2.id = m.id
    ) - interval '1months' )
  Group by a.name
ORDER BY conso DESC LIMIT 1;

EXPLAIN ANALYSE
  SELECT a.name, sum(m.energy*m.recurrence) as conso
  FROM measure_with_filter m
  Inner join Appliance a on a.id = m.appliance
  Where m.date >= (
    (
        select max(m2.date)
        from  measure_with_filter m2
        Inner join Appliance a2 on a2.id = m2.appliance
        Where m2.id = m.id
    ) - interval '1months' )
  Group by a.name
ORDER BY conso DESC;

-- REQUETE 4 --
Select m.date as current_date, (mt.date) as prec_date, m.energy, mt.energy as prec_energie
FROM measure m, measure mt
where mt.date = m.date - INTERVAL '7 DAY'
and m.energy > mt.energy

-- INDEXES --
CREATE INDEX date_indx ON measure (date);
CREATE INDEX date_indxNZ ON measure_without_zero (date);
CREATE INDEX date_indxF ON measure_with_filter (date);

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

