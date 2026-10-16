# Pazudušās mantas

Programma pazudušo un atrasto mantu uzskaitei. Dati glabājas SQLite datubāzē `mantas.db`, logs veidots ar Tkinter.

## Palaišana

```
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
