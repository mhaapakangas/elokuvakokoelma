## Käyttöohjeet

### Ylläpitäjän ohjeet

Ylläpitäjän tili luodaan automaattisesti, kun sovellus käynnistetään. Sen käyttäjätunnus on admin ja oletussalasana on password. Salasanan voi vaihtaa kirjautumalla tietokantaan seuraavalla komennolla:

```SQL
UPDATE account SET password='newpassword' WHERE name='admin';
```

Ylläpitäjä voi lisätä elokuvia tietokantaan yläpalkin 'Add a movie' -linkistä. Elokuvien listauksessa sovelluksen kotisivulla voi muokata kunkin elokuvan tietoja, muokata elokuvissa esiintyviä näyttelijöitä 'Update cast'-linkistä tai poistaa elokuvia tietokannasta. 

Tietokannassa olevat elokuvien genret näkee palkin 'Genres'-linkistä, ja samalta sivulta voi lisätä uusia genrejä tai muokata vanhojen nimiä.

Listauksen tietokannan näyttelijöistä näkee 'Actors'-linkin takana olevalta sivulta, jolta voi myös lisätä näyttelijöitä tietokantaan.  Näyttelijöiden listauksesta voi lisäksi muokata näyttelijöiden tietoja tai poistaa näyttelijöitä tietokannasta.

### Käyttäjän ohjeet

Kirjautumatta sisään käyttäjä voi hakea etusivulla elokuvia elokuvan nimen, näyttelijöiden, genren, vuoden tai käyttäjien antaman arvosanan perusteella. Hakukategoria valitaan alasvetovalikosta. Elokuvia voi etsiä haluamallaan hakusanalla tai ehdolla 'Filter'-napista. Hakuehtojen poistaminen ja -kategorian vaihtaminen onnistuu 'Reset filter'-napista.

Kirjautumaton käyttäjä voi tarkastella listaa parhaiten arvostelluista elokuvista yläpalkin 'Top rated movies'-linkistä. Minkä tahansa elokuvan nimen linkistä pääsee elokuvan omalle sivulle. Se sisältää perustiedot elokuvasta sekä sen käyttäjiltä saamien arvosanojen jakauman.

Käyttäjä voi myös rekisteröityä sovellukseen. Sisäänkirjautuneena käyttäjä voi lisätä elokuvan toivelistalleen tai antaa sille arvosanan elokuvan omalta sivulta. Samalta sivulta voi myös poistaa elokuvan toivelistalta ja poistaa tai muokata annettua arvosanaa. Yläpalkin 'My collection'-linkistä käyttäjä näkee elokuvilla antamansa arvostelut sekä toivelistansa sisällön. 
