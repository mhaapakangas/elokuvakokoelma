##Asennusohje

###Tarvittavat työkalut
Asenna git, python3 ja Heroku CLI. Tarvitset lisäksi Herokun käyttäjätunnuksen.

###Paikallinen kehitysympäristö
1. Lataa projektin tiedostot koneellesi ja siirry projektikansioon.
    ```
    git clone https://github.com/mhaapakangas/elokuvakokoelma.git
    cd elokuvakokoelma
    ```
2. Luo ja aktivoi Python-virtuaaliympäristö.
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Asenna projektin riippuvuudet.
    ```
    pip install -r requirements.txt
    ```
4. Käynnistä sovellus. Sovellukseen pääsee selaimella osoitteessa http://127.0.0.1:5000/.
    ```
    python3 run.py
    ```

###Tuotantoympäristö
1. Lataa projektin tiedostot koneellesi ja siirry projektikansioon..
    ```
    git clone https://github.com/mhaapakangas/elokuvakokoelma.git
    cd elokuvakokoelma
    ```
2.  Luo sovellukselle paikka Herokussa valitsemallasi nimellä.
    ```
    heroku create my-app-name
    ```
3.  Luo HEROKU-ympäristömuuttuja, jonka perusteella sovellus käyttää Herokussa oikeaa konfiguraatiota.
    ```
    heroku config:set HEROKU=1
    ```
4.  Ota käyttöön PostgreSQL-tietokanta.
    ```
    heroku addons:add heroku-postgresql:hobby-dev
    ```       
5.  Lähetä sovellus Herokuun. Sovellus löytyy osoitteesta https://my-app-name.herokuapp.com/
    ```
    git remote add heroku https://git.heroku.com/my-app-name.git
    git push heroku master
    ```