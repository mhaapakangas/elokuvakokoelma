## Käyttöohjeet

### Ylläpitäjän ohjeet

Ylläpitäjän tili luodaan automaattisesti, kun sovellus käynnistetään. Sen käyttäjätunnus on admin ja oletussalasana on password. Salasanan voi vaihtaa kirjautumalla tietokantaan seuraavalla komennolla:

```SQL
UPDATE account SET password='newpassword' WHERE name='admin';
```

Ylläpitäjä voi lisätä elokuvia ja näyttelijöitä tietokantaan. Elokuvien listauksessa voi muokata kunkin elokuvan tietoja, muuttaa elokuvan näyttelijöitä tai poistaa elokuvia tietokannasta. Näyttelijöiden listauksesta voi muokata näyttelijöiden tietoja tai poistaa näyttelijöitä tietokannasta.

### Käyttäjän ohjeet

Kirjautumatta sisään käyttäjä voi hakea tietokannasta elokuvia elokuvan nimen, näyttelijöiden, vuoden tai käyttäjien antaman arvosanan perusteella. Lisäksi käyttäjä voi tarkastella listaa parhaiten arvostelluista elokuvista tai minkä tahansa elokuvan omaa sivua. Se sisältää perustiedot elokuvasta sekä sen saamien arvosanojen jakauman.

Käyttäjä voi myös rekisteröityä sovellukseen. Sisäänkirjautuneena käyttäjä voi lisätä elokuvan toivelistalleen tai antaa sille arvosanan elokuvan omalta sivulta. Samalta sivulta voi myös poistaa elokuvan toivelistalta ja poistaa tai muokata annettua arvosanaa. Käyttäjä näkee omasta kokoelmasta omat arvostelunsa ja toivelistansa sisällön. 
