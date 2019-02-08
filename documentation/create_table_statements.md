```SQL
CREATE TABLE movie (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	year INTEGER NOT NULL,
	genre VARCHAR(144) NOT NULL,
	runtime INTEGER NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE actor (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE account (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	username VARCHAR(144) NOT NULL,
	password VARCHAR(144) NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE movie_cast (
	actor_id INTEGER NOT NULL,
	movie_id INTEGER NOT NULL,
	PRIMARY KEY (actor_id, movie_id),
	FOREIGN KEY(actor_id) REFERENCES actor (id),
	FOREIGN KEY(movie_id) REFERENCES movie (id)
)

CREATE TABLE rating (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	movie_id INTEGER,
	user_id INTEGER,
	want_to_watch BOOLEAN,
	rating INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(movie_id) REFERENCES movie (id),
	FOREIGN KEY(user_id) REFERENCES account (id),
	CHECK (want_to_watch IN (0, 1))
)
```