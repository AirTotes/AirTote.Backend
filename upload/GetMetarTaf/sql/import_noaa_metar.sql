DROP TABLE IF EXISTS metar_noaa_tmp;
CREATE TABLE metar_noaa_tmp(
  station_id TEXT,
  raw_text TEXT,
  observation_time TEXT
);

.mode csv
.import metars.cache.csv metar_noaa_tmp

CREATE TABLE IF NOT EXISTS metar(
  station_id TEXT PRIMARY KEY,
  raw_text TEXT,
  observation_time TEXT
);

INSERT OR REPLACE INTO metar (station_id, raw_text, observation_time)
  SELECT metar_noaa_tmp.station_id, metar_noaa_tmp.raw_text, metar_noaa_tmp.observation_time FROM metar_noaa_tmp
    LEFT OUTER JOIN metar ON metar_noaa_tmp.station_id = metar.station_id
      WHERE metar_noaa_tmp.observation_time > metar.observation_time OR metar.observation_time IS NULL;

DROP TABLE metar_noaa_tmp;
