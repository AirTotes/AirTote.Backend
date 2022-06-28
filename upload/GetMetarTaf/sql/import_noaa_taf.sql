DROP TABLE IF EXISTS taf_noaa_tmp;
CREATE TABLE taf_noaa_tmp(
  station_id TEXT,
  raw_text TEXT,
  issue_time TEXT
);

.mode csv
.import tafs.cache.csv taf_noaa_tmp

CREATE TABLE IF NOT EXISTS taf(
  station_id TEXT PRIMARY KEY,
  raw_text TEXT,
  issue_time TEXT
);

INSERT OR REPLACE INTO taf (station_id, raw_text, issue_time)
  SELECT taf_noaa_tmp.station_id, taf_noaa_tmp.raw_text, taf_noaa_tmp.issue_time FROM taf_noaa_tmp
    LEFT OUTER JOIN taf ON taf_noaa_tmp.station_id = taf.station_id
      WHERE taf_noaa_tmp.issue_time > taf.issue_time OR taf.issue_time IS NULL;

DROP TABLE taf_noaa_tmp;
