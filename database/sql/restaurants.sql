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
	lat DOUBLE PRECISION,
	lng DOUBLE PRECISION
	
	CHECK (rating BETWEEN 0 AND 4)
);

/*Adding postgis extesion*/
CREATE EXTENSION IF NOT EXISTS postgis SCHEMA public;

/*Creating Geometry Column Point Type*/
ALTER TABLE restaurants
ADD COLUMN IF NOT EXISTS geom geometry(Point, 4326)