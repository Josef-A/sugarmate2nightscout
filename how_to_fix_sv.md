# Trolig lösning på problemet med data från Dexcom share

## Vad är problemet
Det verkar som om Dexcom share någonstans i sina system inte klarar av att användarnamnet består av annat än vanliga bokstäver.

Genom att byta användarnamn har det här löst sig för alla som försökt än så länge.
Om det inte fungerar för dig meddela det på https://github.com/nightscout/cgm-remote-monitor/issues/5608 eller om du kan kommentera det här inlägget.

## Byta användarnamn
Tyvärr så går det inte att byta användarnamn på ett Dexcom konto. Man måste skapa ett helt nytt konto.

### Skapa nytt konto
Gå till https://www.dexcom.com och leta rätt på skapa konto.
Följ instruktionerna för att göra ett nytt konto. Det går bara att associera en epostadress med ett Dexcomkonto. 
Se till att använda en annan epost till det nya kontot. Alternativet är att radera det gamla kontot. Men gör **inte** det. Det kan vara bra att kunna gå tillbaka och hämta historiska data.
Se till att det nya användarnamnet bara innehåller bokstäver. Bäst är nog att hålla sig till a-z. Vi vet att tecknet . skapar problem. Men vi vet inte vilka andra tecken som det är problem med. 

### Installera om Dexcom sändarapp
Det här är hur det fungerar under Android. Jag antar att det är likartat med IPhone.
När man installerar Dexcom G6 appen så knyts den till ett Dexcomkonto. Det finns tyvärr inga möjligheter att byta konto. Det man får göra är helt enkelt att avinstallera appen och installera den igen.
I princip så blir det samma förfarande som om man byter telefon. Se tex [Infucare om att byta telefon](https://www.infucare.com/sites/infucare/files/2019/09/04/dexcom_g6_snabbguide_byta_mobil_alvik.pdf)
Fast nu ska du förstås logga in med det nya kontot.
* Skriv upp aktuell Sändarid. Finns att se om man tittar i inställningar i G6-appen.
* Avinstallera G6-appen 
* Installera G6-appen igen
* Logga in med nya kontot
* Följ instruktionerna i appen. 
* Välj ingen sensorkod. Sensorkoden ligger redan på din gamla sändare.
* Skriv in sändarens ID och vänta på parkoppling
* Svara ja på frågan om "har du satt in sensor"

Sedan får man på nytt bjuda in alla följare som man vill ha.


### Nightscout
* Logga in på Heroku https://www.heroku.com/
* Leta rätt på projektet med din Nightscout
* Klicka på _Settings_
* Klicka på <Reveal Config Vars>
* Ändra _BRIDGE_USER_NAME_ och _BRIDGE_PASSWORD_ så att det stämmer med det nya kontot
* Se till att _bridge_ är med i _ENABLE_

När man ändrar dessa variabler så startar Heroku om Nightscout. Så nu borde allt fungera 

### Diasend
Du måste byta så att Diasend hämtar data från det nya kontot.
Diasend får data från Dexcom med ganska stor fördröjning. För att tappa så lite data som möjligt är det bäst att vänta tills all data från det gamla kontot kommit till Diasend. Det kan ta flera dygn.
Sedan är det bara att 
* Logga in på Diasend https://diasend.com/
* Gå till "Connect apps"
* Tryck _Disconnect_ under Dexcom G5/G6
* Tryck sedan på _Connect_
* Logga in med ditt nya Dexcomkonto

## Fungerar det?
Du får väldigt gärna meddela hur det gick. Antingen direkt i det här inlägget eller på https://github.com/nightscout/cgm-remote-monitor/issues/5608
Speciellt viktigt att du hör av dig om det inte fungerar.
