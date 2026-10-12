CREATE TABLE IF NOT EXISTS temperature_readings (
    id BIGSERIAL PRIMARY KEY,
    reading_id VARCHAR(100) NOT NULL,
    room_id VARCHAR(100) NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    temperature INTEGER NOT NULL,
    location VARCHAR(10) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_temperature_readings_business_key
ON temperature_readings (
    reading_id,
    room_id,
    reading_timestamp,
    temperature,
    location
);
