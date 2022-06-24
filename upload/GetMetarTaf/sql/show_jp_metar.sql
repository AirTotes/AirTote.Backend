.headers on
.mode csv

SELECT * FROM metar WHERE station_id LIKE 'RJ%' OR station_id LIKE 'RO%';
