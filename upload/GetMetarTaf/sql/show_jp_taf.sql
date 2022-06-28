.headers on
.mode csv

SELECT * FROM taf WHERE station_id LIKE 'RJ%' OR station_id LIKE 'RO%' ORDER BY station_id ASC;
