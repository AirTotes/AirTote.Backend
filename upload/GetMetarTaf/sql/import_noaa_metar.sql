DROP TABLE IF EXISTS metar_noaa_tmp;
CREATE TABLE metar_noaa_tmp(
  raw_text TEXT,
  station_id TEXT,
  observation_time TEXT,
  latitude REAL,
  longitude REAL,
  temp_c INTEGER,
  dewpoint_c INTEGER,
  wind_dir_degrees INTEGER,
  wind_speed_kt INTEGER,
  wind_gust_kt INTEGER,
  visibility_statute_mi REAL,
  altim_in_hg REAL,
  sea_level_pressure_mb REAL,
  corrected TEXT,
  "auto" TEXT,
  auto_station TEXT,
  maintenance_indicator_on TEXT,
  no_signal TEXT,
  lightning_sensor_off TEXT,
  freezing_rain_sensor_off TEXT,
  present_weather_sensor_off TEXT,
  wx_string TEXT,

  sky_cover_1 TEXT,
  cloud_base_ft_agl_1 INTEGER,
  sky_cover_2 TEXT,
  cloud_base_ft_agl_2 INTEGER,
  sky_cover_3 TEXT,
  cloud_base_ft_agl_3 INTEGER,
  sky_cover_4 TEXT,
  cloud_base_ft_agl_4 INTEGER,

  flight_category TEXT,
  three_hr_pressure_tendency_mb REAL,
  maxT_c REAL,
  minT_c REAL,
  maxT24hr_c REAL,
  minT24hr_c REAL,
  precip_in REAL,
  pcp3hr_in REAL,
  pcp6hr_in REAL,
  pcp24hr_in REAL,
  snow_in TEXT,
  vert_vis_ft INTEGER,
  metar_type TEXT,
  elevation_m TEXT
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
