CREATE TABLE restaurants (
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
)