DROP TABLE IF EXISTS sensor;
DROP TABLE IF EXISTS environment;
DROP TABLE IF EXISTS identity;


CREATE TABLE sensor (
  sensor_id TEXT PRIMARY KEY,
  ip TEXT NOT NULL,
  gps TEXT NOT NULL,
  energy INT NOT NULL,
  data_types TEXT ,
  neighborhood_nodes TEXT ,
  status INT
);

CREATE TABLE environment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_id TEXT NOT NULL,
  temperature INT ,
  humidity INT ,
  combustibleGas INT ,
  smoke INT ,
  year INT NOT NULL,
  month INT NOT NULL,
  date INT NOT NULL,
  hour INT NOT NULL                  
);

CREATE TABLE identity(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account TEXT NOT NULL,
  password TEXT NOT NULL
);
