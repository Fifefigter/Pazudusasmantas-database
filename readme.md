
# Pazudušās mantas

Programma pazudušo un atrasto mantu uzskaitei. Dati glabājas SQLite datubāzē `mantas.db`, logs veidots ar Tkinter.

## Palaišana

```bash
python main.py
```

Nepieciešams Python 3 (Tkinter un sqlite3 ir iekļauti standarta bibliotēkā).

## Lietotāji

Palaižot programmu, vispirms atveras logs **Izvēlēties lietotāju**. Pēc izvēles atveras galvenais logs, kura apakšā vienmēr redzams izvēlētā lietotāja vārds, ID un klase.

Datubāzē jau ir divi lietotāji:

| ID | Vārds | Loma |
|---|---|---|
| 1 | Admin | admin |
| 2 | test | – |

## Iespējas

- **Redzēt mantas** – visu mantu saraksts ar ID un pievienošanas datumu
- **Redzēt pieteikumus** – visi pieteikumi (manta, lietotājs, datums, apstiprināts)
- **Izveidot pieteikumu** – pieteikties uz mantu (mantas ID, lietotāja ID)
- **Pievienot lietotāju** – vārds, uzvārds, e-pasts, klase, loma
- **Pievienot kategoriju** – nosaukums
- **Pievienot mantu** – nosaukums, apraksts, kategorijas ID

Mantai un pieteikumam datums tiek ielikts automātiski (šodiena).

## Plānotie uzlabojumi

### 41. Mantu meklēšana

Mantu sarakstā būs pieejams meklēšanas lauks.

- Meklēšana notiks pēc mantas nosaukuma.
- Būs iespējams meklēt arī pēc daļēja nosaukuma.
- Meklēšana nebūs atkarīga no lielajiem un mazajiem burtiem.
- Rezultāti automātiski atjaunosies pēc meklēšanas.
- Ja manta netiks atrasta, tiks parādīts paziņojums „Mantas nav atrastas”.
- Izdzēšot meklēšanas tekstu, atkal būs redzams pilns mantu saraksts.

### 42. Kategoriju filtrēšana

Mantu sarakstā būs iespējams atlasīt mantas pēc to kategorijas.

- Virs mantu saraksta būs kategoriju izvēles lauks.
- Kategorijas tiks ielādētas no datubāzes tabulas `kategorijas`.
- Izvēloties kategoriju, tiks parādītas tikai tai piederošās mantas.
- Būs pieejama izvēle „Visas kategorijas”.
- Ja izvēlētajā kategorijā nebūs mantu, tiks parādīts atbilstošs paziņojums.
- Kategoriju filtrēšanu varēs izmantot kopā ar mantu meklēšanu.

### 43. Mantu attēli

Pievienojot jaunu mantu, būs iespējams pievienot arī tās fotogrāfiju.

- Mantas pievienošanas logā būs poga „Izvēlēties attēlu”.
- Nospiežot pogu, atvērsies datora failu izvēles logs.
- Būs iespējams izvēlēties attēlu no datora.
- Izvēlētā attēla atrašanās vieta tiks saglabāta datubāzes laukā `foto`.
- Apskatot mantas informāciju, būs redzama tās fotogrāfija.
- Būs iespējams arī nomainīt vai noņemt pievienoto attēlu.
- Ja attēls nav pievienots, programma parādīs tekstu „Attēls nav pievienots”.
- Programma pārbaudīs, vai izvēlētais attēls eksistē.

### 45. Pieteikumu statuss

Katram pieteikumam būs atsevišķs statuss, kas parādīs, kādā stadijā atrodas pieteikums.

Būs pieejami trīs statusi:

- **Gaida** – pieteikums ir izveidots un vēl nav izskatīts.
- **Apstiprināts** – administrators ir apstiprinājis pieteikumu.
- **Noraidīts** – administrators ir noraidījis pieteikumu.

Darbības princips:

- Izveidojot jaunu pieteikumu, tā statuss automātiski būs „Gaida”.
- Administrators varēs apskatīt visus pieteikumus.
- Administrators varēs mainīt pieteikuma statusu uz „Apstiprināts” vai „Noraidīts”.
- Statuss tiks saglabāts SQLite datubāzē.
- Pieteikumu sarakstā būs redzams mantas nosaukums, lietotāja vārds, datums un statuss.

### 46. Dzēšanas funkcija

Aplikācijā būs iespējams dzēst nevajadzīgas mantas un pieteikumus.

Darbības princips:

- Mantu sarakstā būs poga „Dzēst mantu”.
- Pieteikumu sarakstā būs poga „Dzēst pieteikumu”.
- Pirms dzēšanas programma parādīs apstiprinājuma logu.
- Ja lietotājs izvēlēsies „Nē”, nekas netiks dzēsts.
- Ja lietotājs izvēlēsies „Jā”, izvēlētais ieraksts tiks dzēsts no datubāzes.
- Pēc dzēšanas saraksts automātiski atjaunosies.
- Dzēšanas funkcija būs pieejama tikai administratoram.
- Programma pārbaudīs, vai mantai nav saistītu pieteikumu, lai novērstu datubāzes kļūdas.

### 47. Rediģēšana

Aplikācijā būs iespējams rediģēt jau pievienotu mantu informāciju.

Darbības princips:

- Mantu sarakstā būs poga „Rediģēt mantu”.
- Vispirms lietotājam būs jāizvēlas manta, kuru vēlas rediģēt.
- Atvērsies jauns logs ar pašreizējo mantas informāciju.
- Būs iespējams mainīt mantas nosaukumu, aprakstu, kategoriju, atrašanās vietu un attēlu.
- Nospiežot pogu „Saglabāt”, izmaiņas tiks saglabātas SQLite datubāzē.
- Nospiežot „Atcelt”, izmaiņas netiks saglabātas.
- Pēc saglabāšanas mantu saraksts automātiski atjaunosies.
- Rediģēšanas funkcija būs pieejama tikai administratoram.

## Faili

- `main.py` – galvenais logs un formas
- `funkcijas.py` – funkcijas darbam ar datubāzi
- `mantas.db` – datubāze

## Datubāze

| Tabula | Lauki |
|---|---|
| `kategorijas` | id, nosaukums |
| `lietotaji` | id, vards, uzvards, epasts, klase, loma |
| `mantas` | id, nosaukums, apraksts, kategorija_id → kategorijas, vieta, datums, statuss, pievienoja_id → lietotaji, foto |
| `pazaudetas` | id, lietotajs_id → lietotaji, kategorija_id → kategorijas, vieta, apraksts, datums |
| `pieteikumi` | id, manta_id → mantas, lietotajs_id → lietotaji, pieradijums, datums, apstiprinats |

**Piezīme:** Lai ieviestu jaunos pieteikumu statusus, datubāzes tabula `pieteikumi` būs jāpapildina ar atsevišķu statusa lauku. Pārējās jaunās funkcijas izmantos esošās datubāzes tabulas un laukus, vajadzības gadījumā tos papildinot.
