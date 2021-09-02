CREATE TABLE iF NOT EXISTS restaurants (
	id TEXT PRIMARY KEY,
	rating INTEGER,
	name TEXT,
	site TEXT,
	email TEXT,
	phone TEXT,
	street TEXT,
	city TEXT,
	state TEXT,
	lat DECIMAL,
	lng DECIMAL
	
	CHECK (rating BETWEEN 0 AND 4)
);

CREATE EXTENSION IF NOT EXISTS postgis SCHEMA public;

ALTER TABLE restaurants
ADD COLUMN IF NOT EXISTS geom geometry(Point, 4326)