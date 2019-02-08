## Käyttäjätarinat

- Järjestelmän ylläpitäjänä haluan lisätä tietokantaan elokuvia.
```SQL
INSERT INTO movie (date_created, date_modified, name, year, genre, runtime) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Ghostbusters', 1984, 'Action', 105)
```

- Järjestelmän ylläpitäjänä haluan muokata tietokantaan tallennettujen elokuvien tietoja.
```SQL
UPDATE movie SET date_modified=CURRENT_TIMESTAMP, runtime=107 WHERE movie.id = 3
```

- Järjestelmän ylläpitäjänä haluan poistaa tietokannasta elokuvia.
```SQL
DELETE FROM movie WHERE movie.id = 1
```

- Järjestelmän ylläpitäjänä haluan lisätä tietokantaan näyttelijöitä.
```SQL
INSERT INTO actor (date_created, date_modified, name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Bill Murray')
```

- Järjestelmän ylläpitäjänä haluan muokata tietokantaan tallennettujen näyttelijöiden tietoja.
```SQL
UPDATE actor SET date_modified=CURRENT_TIMESTAMP, name='Scarlett Johansson' WHERE actor.id = 2
```

- Järjestelmän ylläpitäjänä haluan poistaa tietokannasta näyttelijöitä.
```SQL
DELETE FROM actor WHERE actor.id = 1
```

- Järjestelmän ylläpitäjänä haluan lisätä elokuvan näyttelijäkaartiin näyttelijöitä.
```SQL
INSERT INTO movie_cast (actor_id, movie_id) VALUES (4, 3)
```

- Järjestelmän ylläpitäjänä haluan poistaa elokuvan näyttelijäkaartista näyttelijöitä.
```SQL
DELETE FROM movie_cast WHERE movie_cast.actor_id = 2 AND movie_cast.movie_id = 3
```

- Järjestelmän ylläpitäjänä haluan kirjautua sisään järjestelmään.

- Käyttäjänä haluan rekisteröityä järjestelmään.
```SQL
INSERT INTO account (date_created, date_modified, name, username, password) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'example', 'user', 'password')
```

- Käyttäjänä haluan kirjautua sisään järjestelmään.
```SQL
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.name AS account_name, account.username AS account_username, account.password AS account_password 
FROM account 
WHERE account.username = 'user' AND account.password = 'password'
 LIMIT 1 OFFSET 0
```

- Käyttäjänä haluan nähdä listauksen tietokannan elokuvista
```SQL
SELECT movie.id AS movie_id, movie.date_created AS movie_date_created, movie.date_modified AS movie_date_modified, movie.name AS movie_name, movie.year AS movie_year, movie.genre AS movie_genre, movie.runtime AS movie_runtime 
FROM movie
``` 

- Käyttäjänä haluan hakea elokuvia eri kriteerien perusteella, jotta löydän helposti haluamani elokuvan.
```SQL
Hae elokuvia näyttelijän perusteella:
SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre, movie.runtime FROM movie JOIN movie_cast ON movie_id=movie.id JOIN actor ON actor_id=actor.id WHERE actor.name LIKE '%bill%'
```

- Käyttäjänä haluan antaa arvosanan katsomalleni elokuvalle.
```SQL
INSERT INTO rating (date_created, date_modified, movie_id, user_id, want_to_watch, rating) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 3, 2, 0, 1)
```

- Käyttäjänä haluan nähdä listauksen antamistani arvosanoista.

- Käyttäjänä haluan muokata elokuvalle antamaani arvosanaa.
```SQL
UPDATE rating SET date_modified=CURRENT_TIMESTAMP, rating=10 WHERE rating.id = 3
```

- Käyttäjänä haluan poistaa elokuvalle antamani arvosanan.
```SQL
UPDATE rating SET date_modified=CURRENT_TIMESTAMP, rating=None WHERE rating.id = 3
```

- Käyttäjänä haluan tallentaa toivelistalle elokuvan jonka haluaisin nähdä, jotta löydän sen helposti myöhemmin.
```SQL
INSERT INTO rating (date_created, date_modified, movie_id, user_id, want_to_watch, rating) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2, 2, 1, None)
```

- Käyttäjänä haluan nähdä listauksen toivelistani elokuvista.

- Käyttäjänä haluan poistaa elokuvan toivelistalta.
```SQL
UPDATE rating SET date_modified=CURRENT_TIMESTAMP, want_to_watch=0 WHERE rating.id = 2
```