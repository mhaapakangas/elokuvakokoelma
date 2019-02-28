## Käyttäjätarinat

- Järjestelmän ylläpitäjänä haluan lisätä tietokantaan elokuvia.
```SQL
INSERT INTO movie (date_created, date_modified, name, year, genre_id, runtime)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Ghostbusters', 1984, 3, 105);
```

- Järjestelmän ylläpitäjänä haluan muokata tietokantaan tallennettujen elokuvien tietoja.
```SQL
UPDATE movie SET date_modified=CURRENT_TIMESTAMP, runtime=107 WHERE movie.id = 3;
```

- Järjestelmän ylläpitäjänä haluan poistaa tietokannasta elokuvia.
```SQL
DELETE FROM movie WHERE movie.id = 1;
```

- Järjestelmän ylläpitäjänä haluan lisätä tietokantaan näyttelijöitä.
```SQL
INSERT INTO actor (date_created, date_modified, name)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Bill Murray');
```

- Järjestelmän ylläpitäjänä haluan muokata tietokantaan tallennettujen näyttelijöiden tietoja.
```SQL
UPDATE actor SET date_modified=CURRENT_TIMESTAMP, name='Scarlett Johansson' WHERE actor.id = 2;
```

- Järjestelmän ylläpitäjänä haluan poistaa tietokannasta näyttelijöitä.
```SQL
DELETE FROM actor WHERE actor.id = 1;
```

- Järjestelmän ylläpitäjänä haluan lisätä elokuvan näyttelijäkaartiin näyttelijöitä.
```SQL
INSERT INTO movie_cast (actor_id, movie_id) VALUES (4, 3);
```

- Järjestelmän ylläpitäjänä haluan poistaa elokuvan näyttelijäkaartista näyttelijöitä.
```SQL
DELETE FROM movie_cast WHERE movie_cast.actor_id = 2 AND movie_cast.movie_id = 3;
```

- Järjestelmän ylläpitäjänä haluan kirjautua sisään järjestelmään.

- Käyttäjänä haluan rekisteröityä järjestelmään.
```SQL
INSERT INTO account (date_created, date_modified, name, username, password)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'example', 'user', 'password');
```

- Käyttäjänä haluan kirjautua sisään järjestelmään.
```SQL
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified,
account.name AS account_name, account.username AS account_username, account.password AS account_password 
FROM account WHERE account.username = 'user' AND account.password = 'password'
 LIMIT 1 OFFSET 0;
```

- Käyttäjänä haluan nähdä listauksen tietokannan elokuvista
```SQL
SELECT movie.id AS movie_id, movie.date_created AS movie_date_created, movie.date_modified AS movie_date_modified,
movie.name AS movie_name, movie.year AS movie_year, movie.genre_id AS movie_genre_id, movie.runtime AS movie_runtime 
FROM movie ORDER BY movie.name
 LIMIT 10 OFFSET 0;
``` 

- Käyttäjänä haluan nähdä listauksen parhaiten arvostelluista elokuvista
```SQL
SELECT movie.id, movie.name, movie.year, ROUND(AVG(rating.rating), 1) as average
FROM movie
JOIN rating ON rating.movie_id = movie.id WHERE rating.rating IS NOT NULL
GROUP BY movie.id ORDER BY average
DESC LIMIT 10;
``` 

- Käyttäjänä haluan hakea elokuvia eri kriteerien perusteella, jotta löydän helposti haluamani elokuvan.
```SQL
Hae elokuvia nimen perusteella:
SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie
WHERE movie.name LIKE '%matrix%'
ORDER BY movie.name;

Hae elokuvia näyttelijän perusteella:
SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie
JOIN movie_cast ON movie_id=movie.id JOIN actor ON actor_id=actor.id
WHERE actor.name LIKE '%bill%'
ORDER BY movie.name;

Hae elokuvia genren perusteella:
SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie
WHERE movie.genre_id = 3
ORDER BY movie.name;

Hae elokuvia vuoden perusteella:
SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie
WHERE movie.year BETWEEN 1990 AND 2010
ORDER BY movie.name;

Hae elokuvia arvostelujen perusteella:
SELECT m.id, m.name, m.year, m.genre_id, m.runtime, ROUND(m.average, 1) as average
FROM (SELECT movie.id, movie.name, movie.year, movie.genre, movie.runtime, AVG(rating.rating) as average
    FROM movie
    JOIN rating ON rating.movie_id = movie.id WHERE rating.rating IS NOT NULL
    GROUP BY movie.id)
as m WHERE m.average BETWEEN 8 AND 10
ORDER BY m.name;
```

- Käyttäjänä haluan antaa arvosanan katsomalleni elokuvalle.
```SQL
INSERT INTO rating (date_created, date_modified, movie_id, user_id, want_to_watch, rating)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 3, 2, 0, 9);
```
- Käyttäjänä haluan tallentaa toivelistalle elokuvan jonka haluaisin nähdä, jotta löydän sen helposti myöhemmin.
```SQL
INSERT INTO rating (date_created, date_modified, movie_id, user_id, want_to_watch, rating)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2, 2, 1, None);
```

- Käyttäjänä haluan nähdä listauksen antamistani arvosanoista.
- Käyttäjänä haluan nähdä listauksen toivelistani elokuvista.
```SQL
SELECT rating.id AS rating_id, rating.date_created AS rating_date_created, rating.date_modified AS rating_date_modified, rating.movie_id AS rating_movie_id, rating.user_id AS rating_user_id, rating.want_to_watch AS rating_want_to_watch, rating.rating AS rating_rating 
FROM rating 
WHERE rating.user_id = 2;
```

- Käyttäjänä haluan muokata elokuvalle antamaani arvosanaa.
```SQL
UPDATE rating SET date_modified=CURRENT_TIMESTAMP, rating=10 WHERE rating.id = 3;
```

- Käyttäjänä haluan poistaa elokuvalle antamani arvosanan.
```SQL
UPDATE rating SET date_modified=CURRENT_TIMESTAMP, rating=None WHERE rating.id = 3;
```

- Käyttäjänä haluan poistaa elokuvan toivelistalta.
```SQL
UPDATE rating SET date_modified=CURRENT_TIMESTAMP, want_to_watch=0 WHERE rating.id = 2;
```
