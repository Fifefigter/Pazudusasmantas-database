
# Pazudušās mantas

## 1. Aplikācijas mērķis

„Pazudušās mantas” ir aplikācija, kas paredzēta skolas vai organizācijas pazudušo un atrasto mantu uzskaitei.

Aplikācijas galvenais mērķis ir ļaut lietotājiem apskatīt atrastās mantas, atrast sev piederošas mantas un pieteikties to saņemšanai.

Visa informācija tiek glabāta vienā kopīgā SQLite datubāzē `mantas.db`.

## 2. Lietotāji un piekļuves tiesības

Aplikācijā ir divu veidu lietotāji:

### Administrators

Administrators var:
- Apskatīt visas mantas.
- Pievienot jaunas mantas.
- Rediģēt mantu informāciju.
- Dzēst mantas.
- Apskatīt visus pieteikumus.
- Apstiprināt vai noraidīt pieteikumus.
- Dzēst pieteikumus.
- Pievienot lietotājus.
- Pievienot kategorijas.

### Parastais lietotājs

Parastais lietotājs var:
- Apskatīt visas pieejamās mantas.
- Meklēt mantas pēc nosaukuma.
- Filtrēt mantas pēc kategorijām.
- Apskatīt mantu aprakstus un fotogrāfijas.
- Izveidot pieteikumu uz mantu.
- Apskatīt savus pieteikumus un to statusus.

Parastais lietotājs nedrīkst mainīt citu lietotāju datus, rediģēt mantas vai mainīt pieteikumu statusus.

## 3. Lietotāja izvēle

Atverot programmu, parādās logs „Izvēlēties lietotāju”.

Tajā tiek parādīti visi datubāzē reģistrētie lietotāji.

Katram lietotājam tiek parādīts:
- Vārds.
- Uzvārds.
- ID.

Lietotājs izvēlas savu profilu un nospiež „Izvēlēties”.

Pēc izvēles programma:
1. Nolasa lietotāja ID.
2. Iegūst lietotāja vārdu, uzvārdu un klasi.
3. Nosaka lietotāja lomu.
4. Atver galveno logu.
5. Saglabā informāciju par pašreizējo lietotāju programmas darbības laikā.

Galvenā loga apakšā vienmēr ir redzams izvēlētā lietotāja vārds, ID un klase.

## 4. Galvenais logs

Galvenajā logā ir šādas funkcijas:

1. Redzēt mantas.
2. Redzēt pieteikumus.
3. Izveidot pieteikumu.
4. Pievienot lietotāju.
5. Pievienot kategoriju.
6. Pievienot mantu.

Administratoram ir pieejamas visas funkcijas.

Parastajam lietotājam pieejamas tikai tās funkcijas, kuras atļautas viņa lomai.

## 5. Mantu datubāzes darbība

Visas atrastās mantas tiek glabātas tabulā `mantas`.

Katram mantas ierakstam ir:
- `id` – unikāls mantas ID.
- `nosaukums` – mantas nosaukums.
- `apraksts` – mantas apraksts.
- `kategorija_id` – kategorijas ID.
- `vieta` – atrašanas vieta.
- `datums` – pievienošanas datums.
- `statuss` – mantas pašreizējais statuss.
- `pievienoja_id` – lietotāja ID, kurš pievienoja mantu.
- `foto` – fotogrāfijas atrašanās vieta.

Mantas ID tiek izveidots automātiski.

### 5.1. Mantas pievienošana

Administrators nospiež „Pievienot mantu”.

Atveras forma ar laukiem:
- Nosaukums.
- Apraksts.
- Kategorija.
- Atrašanās vieta.
- Fotogrāfija.

Nospiežot „Saglabāt”:
1. Tiek pārbaudīts nosaukums.
2. Tiek pārbaudīta izvēlētā kategorija.
3. Tiek iegūts pašreizējā lietotāja ID.
4. Tiek pievienots šodienas datums.
5. Mantas sākotnējais statuss tiek iestatīts uz „Pieejama”.
6. Ieraksts tiek saglabāts tabulā `mantas`.
7. Manta parādās kopējā mantu sarakstā.

### 5.2. Mantu apskate

Nospiežot „Redzēt mantas”, tiek parādītas visas datubāzē esošās mantas.

Tabulā redzams:
- ID.
- Nosaukums.
- Kategorija.
- Atrašanās vieta.
- Pievienošanas datums.
- Statuss.

Izvēloties konkrētu mantu, atveras detalizētas informācijas logs.

Tajā redzams:
- Mantas nosaukums.
- Apraksts.
- Kategorija.
- Atrašanās vieta.
- Pievienošanas datums.
- Statuss.
- Fotogrāfija.
- Lietotājs, kurš pievienojis mantu.

Ja fotogrāfijas nav, tiek parādīts teksts „Attēls nav pievienots”.

## 6. Mantu meklēšana 

Mantu saraksta augšdaļā atrodas meklēšanas lauks.

Lietotājs var ievadīt pilnu mantas nosaukumu vai tikai tā daļu.

Piemēram:
- „Telefons” parāda mantas, kuru nosaukumā ir šis vārds.
- „Atslē” parāda mantas, kuru nosaukumā ir šī teksta daļa.

Meklēšana darbojas neatkarīgi no lielajiem un mazajiem burtiem.

Rezultāti atjaunojas automātiski, kamēr lietotājs raksta.

Ja nekas nav atrasts, tiek parādīts „Mantas nav atrastas”.

Izdzēšot meklēšanas tekstu, atkal parādās visas mantas.

Meklēšana darbojas kopā ar kategoriju filtrēšanu.

## 7. Kategoriju filtrēšana 

Kategorijas tiek glabātas tabulā `kategorijas`.

Katrai kategorijai ir:
- `id` – unikāls kategorijas ID.
- `nosaukums` – kategorijas nosaukums.

Mantu sarakstā atrodas kategoriju izvēles lauks.

Izvēloties kategoriju, tiek parādītas tikai tās mantas, kuru `kategorija_id` sakrīt ar izvēlēto kategoriju.

Pieejama arī izvēle „Visas kategorijas”.

Izvēloties to, tiek parādītas visas mantas.

Kategoriju filtrēšana un meklēšana darbojas vienlaikus.

Piemēram, izvēloties kategoriju „Elektronika” un ierakstot meklēšanas laukā „telefons”, tiek parādīti tikai elektronikas kategorijas telefoni.

## 8. Mantu fotogrāfijas 

Katrai mantai iespējams pievienot fotogrāfiju.

Fotogrāfijas atrašanās vieta tiek saglabāta tabulas `mantas` laukā `foto`.

Atbalstītie formāti:
- JPG.
- JPEG.
- PNG.

Pievienojot fotogrāfiju:
1. Lietotājs nospiež „Izvēlēties attēlu”.
2. Atveras failu izvēles logs.
3. Lietotājs izvēlas attēlu.
4. Attēla atrašanās vieta tiek saglabāta datubāzē.

Apskatot mantu, tās fotogrāfija tiek parādīta blakus informācijai.

Fotogrāfiju var nomainīt vai noņemt.

Ja attēla fails vairs nav pieejams, programma turpina darboties un parāda paziņojumu.

## 9. Mantu rediģēšana 

Administratoram ir iespēja rediģēt esošās mantas.

Izvēloties mantu un nospiežot „Rediģēt mantu”, atveras forma ar jau aizpildītiem laukiem.

Var mainīt:
- Nosaukumu.
- Aprakstu.
- Kategoriju.
- Atrašanās vietu.
- Fotogrāfiju.

Nospiežot „Saglabāt”:
1. Programma pārbauda ievadīto informāciju.
2. Atrod mantu pēc tās ID.
3. Atjauno mainītos laukus datubāzē.
4. Saglabā izmaiņas.
5. Atjauno mantu sarakstu.

Mantas ID un sākotnējais pievienošanas datums netiek mainīti.

Nospiežot „Atcelt”, izmaiņas netiek saglabātas.

## 10. Mantu dzēšana

Administratoram ir iespēja dzēst mantas.

Izvēloties mantu un nospiežot „Dzēst mantu”, parādās apstiprinājuma logs.

Ja administrators apstiprina dzēšanu:
1. Programma atrod mantu pēc ID.
2. Pārbauda, vai tai ir saistīti pieteikumi.
3. Pārbauda datubāzes savstarpējās saites.
4. Droši apstrādā saistītos pieteikumus.
5. Dzēš mantas ierakstu.
6. Atjauno mantu sarakstu.

Ja administrators izvēlas „Nē”, nekas netiek dzēsts.

Nedrīkst pieļaut situāciju, kurā datubāzē paliek pieteikumi, kas norāda uz neeksistējošu mantu.

## 11. Pieteikumu datubāzes darbība

Visi pieteikumi tiek glabāti tabulā `pieteikumi`.

Katram pieteikumam ir:
- `id` – unikāls pieteikuma ID.
- `manta_id` – mantas ID, uz kuru lietotājs piesakās.
- `lietotajs_id` – lietotāja ID, kurš izveidojis pieteikumu.
- `pieradijums` – papildu pierādījums vai informācija.
- `datums` – pieteikuma izveidošanas datums.
- `apstiprinats` – apstiprinājuma lauks.
- `statuss` – pieteikuma statuss.

Katrs pieteikums ir saistīts ar vienu lietotāju un vienu mantu.

Izmantojot šīs saites, programma var parādīt mantas nosaukumu un lietotāja vārdu, nevis tikai ID numurus.

## 12. Pieteikuma izveidošana

Lietotājs nospiež „Izveidot pieteikumu”.

Atveras forma, kurā jānorāda mantas ID.

Pašreizējā lietotāja ID programma iegūst automātiski.

Pirms saglabāšanas tiek pārbaudīts:
- Vai manta eksistē.
- Vai lietotājs eksistē.
- Vai manta ir pieejama.
- Vai lietotājam jau nav aktīva pieteikuma uz šo mantu.

Ja pārbaudes ir veiksmīgas:
1. Tiek izveidots jauns pieteikuma ID.
2. Tiek saglabāts mantas ID.
3. Tiek saglabāts lietotāja ID.
4. Tiek ievietots pašreizējais datums.
5. Statuss tiek iestatīts uz „Gaida”.
6. Pieteikums tiek saglabāts datubāzē.

Pēc veiksmīgas saglabāšanas lietotājs saņem paziņojumu.

## 13. Pieteikumu apskate

Nospiežot „Redzēt pieteikumus”, atveras pieteikumu saraksts.

Administratoram redzami visi pieteikumi.

Parastajam lietotājam redzami tikai viņa paša pieteikumi.

Tabulā redzams:
- Pieteikuma ID.
- Mantas nosaukums.
- Lietotāja vārds un uzvārds.
- Pieteikuma datums.
- Pieteikuma statuss.

Šī informācija tiek iegūta, savienojot tabulas `pieteikumi`, `mantas` un `lietotaji`.

## 14. Pieteikumu statusi

Katram pieteikumam ir viens no trim statusiem:

| Statuss | Nozīme |
|---|---|
| Gaida | Pieteikums vēl nav izskatīts |
| Apstiprināts | Administrators ir apstiprinājis pieteikumu |
| Noraidīts | Administrators ir noraidījis pieteikumu |

Jauns pieteikums automātiski saņem statusu „Gaida”.

Administrators var izvēlēties pieteikumu un nospiest:
- „Apstiprināt”.
- „Noraidīt”.

Pēc izvēles programma atrod pieteikumu pēc ID un maina tā statusu datubāzē.

### Pieteikuma apstiprināšana

Apstiprinot pieteikumu:
1. Programma pārbauda, vai manta joprojām ir pieejama.
2. Pārbauda, vai tai nav cita apstiprināta pieteikuma.
3. Maina pieteikuma statusu uz „Apstiprināts”.
4. Maina mantas statusu uz „Atdota”.
5. Saglabā abas izmaiņas datubāzē vienas transakcijas ietvaros.

Ja kāda darbība neizdodas, abas izmaiņas tiek atceltas.

Vienai mantai var būt tikai viens apstiprināts pieteikums.

Pārējie pieteikumi uz šo mantu vairs nevar tikt apstiprināti.

### Pieteikuma noraidīšana

Noraidot pieteikumu:
1. Programma atrod konkrēto pieteikumu.
2. Maina tā statusu uz „Noraidīts”.
3. Saglabā izmaiņas datubāzē.
4. Atjauno pieteikumu sarakstu.

Ja manta vēl nav atdota un tai nav cita apstiprināta pieteikuma, tā paliek pieejama.

## 15. Pieteikumu dzēšana

Administratoram ir iespēja dzēst pieteikumus.

Izvēloties pieteikumu un nospiežot „Dzēst pieteikumu”, parādās apstiprinājuma logs.

Pēc apstiprināšanas:
1. Programma atrod pieteikumu pēc ID.
2. Pārbauda tā statusu.
3. Dzēš pieteikuma ierakstu.
4. Pārbauda saistītās mantas statusu.
5. Atjauno pieteikumu sarakstu.

Lietotāja un mantas ieraksti netiek dzēsti kopā ar pieteikumu.

Ja tiek dzēsts apstiprināts pieteikums, manta automātiski nekļūst pieejama, jo tas nenozīmē, ka manta ir fiziski atgriezta.

## 16. Lietotāju pārvaldība

Lietotāji tiek glabāti tabulā `lietotaji`.

Tabulas lauki:
- `id` – lietotāja ID.
- `vards` – vārds.
- `uzvards` – uzvārds.
- `epasts` – e-pasts.
- `klase` – klase.
- `loma` – lietotāja loma.

### Lietotāja pievienošana

Administrators nospiež „Pievienot lietotāju”.

Atveras forma ar laukiem:
- Vārds.
- Uzvārds.
- E-pasts.
- Klase.
- Loma.

Pēc saglabāšanas programma:
1. Pārbauda, vai obligātie lauki ir aizpildīti.
2. Pārbauda e-pasta formātu.
3. Pārbauda izvēlēto lomu.
4. Izveido jaunu lietotāja ID.
5. Saglabā lietotāju tabulā `lietotaji`.

Jaunais lietotājs parādās lietotāju izvēles logā.

## 17. Kategoriju pārvaldība

Kategorijas tiek glabātas tabulā `kategorijas`.

Katram ierakstam ir:
- `id` – kategorijas ID.
- `nosaukums` – kategorijas nosaukums.

Administrators nospiež „Pievienot kategoriju”.

Atveras logs ar lauku „Nosaukums”.

Pēc saglabāšanas:
1. Tiek pārbaudīts, vai nosaukums nav tukšs.
2. Tiek pārbaudīts, vai tāda kategorija jau neeksistē.
3. Tiek izveidots jauns kategorijas ieraksts.
4. Kategorija tiek saglabāta datubāzē.

Jaunā kategorija uzreiz ir pieejama mantu pievienošanas un rediģēšanas formās.

## 18. Datubāzes struktūra

Datubāzes nosaukums ir `mantas.db`.

### Tabula `kategorijas`

| Lauks | Nozīme |
|---|---|
| id | Kategorijas ID |
| nosaukums | Kategorijas nosaukums |

### Tabula `lietotaji`

| Lauks | Nozīme |
|---|---|
| id | Lietotāja ID |
| vards | Vārds |
| uzvards | Uzvārds |
| epasts | E-pasts |
| klase | Klase |
| loma | Loma |

### Tabula `mantas`

| Lauks | Nozīme |
|---|---|
| id | Mantas ID |
| nosaukums | Mantas nosaukums |
| apraksts | Apraksts |
| kategorija_id | Kategorijas ID |
| vieta | Atrašanās vieta |
| datums | Pievienošanas datums |
| statuss | Mantas statuss |
| pievienoja_id | Pievienotāja ID |
| foto | Fotogrāfijas ceļš |

### Tabula `pazaudetas`

| Lauks | Nozīme |
|---|---|
| id | Ieraksta ID |
| lietotajs_id | Lietotāja ID |
| kategorija_id | Kategorijas ID |
| vieta | Pazaudēšanas vieta |
| apraksts | Apraksts |
| datums | Datums |

### Tabula `pieteikumi`

| Lauks | Nozīme |
|---|---|
| id | Pieteikuma ID |
| manta_id | Mantas ID |
| lietotajs_id | Lietotāja ID |
| pieradijums | Pierādījums |
| datums | Pieteikuma datums |
| apstiprinats | Apstiprinājuma lauks |
| statuss | Pieteikuma statuss |

### Tabulu savstarpējās attiecības

- Vienai kategorijai var būt vairākas mantas.
- Vienam lietotājam var būt pievienotas vairākas mantas.
- Vienam lietotājam var būt vairāki pieteikumi.
- Vienai mantai var būt vairāki pieteikumi.
- Katrs pieteikums pieder vienam lietotājam un vienai mantai.
- Katra manta pieder vienai kategorijai.

Datubāzes saites nodrošina, ka pieteikumi, lietotāji, mantas un kategorijas ir savstarpēji saistīti.

## 19. Datubāzes drošība un datu saglabāšana

Visas izmaiņas tiek saglabātas datubāzē.

Programmai jānodrošina:
- Neeksistējošu lietotāju un mantu ID izmantošanas novēršana.
- Nederīgu kategoriju izmantošanas novēršana.
- Tukšu obligāto lauku novēršana.
- Vienas mantas vairākkārtējas nodošanas novēršana.
- Nederīgu pieteikumu novēršana.
- Saistīto ierakstu droša dzēšana.

Ja viena darbība maina vairākus savstarpēji saistītus ierakstus, piemēram, apstiprinot pieteikumu un mainot mantas statusu, abas izmaiņas jāsaglabā vienas datubāzes transakcijas ietvaros.

Ja darbība neizdodas, izmaiņas tiek atceltas.

Aizverot un atkārtoti atverot programmu, iepriekš saglabātā informācija paliek datubāzē.

## 20. Gala rezultāta prognoze

Pēc visu aprakstīto funkciju ieviešanas aplikācija būs pilnvērtīga pazudušo un atrasto mantu uzskaites sistēma.

Parastais lietotājs varēs:
- Apskatīt atrastās mantas.
- Ātri atrast sev nepieciešamo mantu.
- Apskatīt mantu fotogrāfijas.
- Izveidot pieteikumu.
- Sekot līdzi pieteikuma statusam.

Administrators varēs:
- Pārvaldīt visas mantas.
- Pievienot un rediģēt informāciju.
- Pārvaldīt lietotājus un kategorijas.
- Izskatīt pieteikumus.
- Kontrolēt mantu pieejamību.

**Prognozētais gala rezultāts:** vienkārša, pārskatāma un praktiski izmantojama aplikācija, kas ļaus vienuviet reģistrēt atrastās mantas, palīdzēs to īpašniekiem tās atgūt un nodrošinās administratoram pilnīgu pārskatu par mantām un to pieteikumiem.

Sistēmas galvenais ieguvums būs centralizēta datu glabāšana un skaidra mantu aprites kontrole — no mantas pievienošanas līdz tās nodošanai īpašniekam.
