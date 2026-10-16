import sqlite3

DB = "mantas.db"


def savienot():
    return sqlite3.connect(DB)


def apskatit_mantas():
    with savienot() as conn:
        return conn.execute("SELECT * FROM mantas").fetchall()


def apskatit_lietotajus():
    with savienot() as conn:
        return conn.execute("SELECT * FROM lietotaji").fetchall()


def apskatit_pieteikumus():
    with savienot() as conn:
        return conn.execute(
            "SELECT pieteikumi.id, mantas.nosaukums, lietotaji.vards || ' ' || lietotaji.uzvards, "
            "pieteikumi.pieradijums, pieteikumi.datums, pieteikumi.apstiprinats "
            "FROM pieteikumi "
            "JOIN mantas ON pieteikumi.manta_id = mantas.id "
            "JOIN lietotaji ON pieteikumi.lietotajs_id = lietotaji.id"
        ).fetchall()


def izveidot_pieteikumu(manta_id, lietotajs_id, pieradijums, datums):
    with savienot() as conn:
        conn.execute(
            "INSERT INTO pieteikumi (manta_id, lietotajs_id, pieradijums, datums, apstiprinats) VALUES (?, ?, ?, ?, ?)",
            (manta_id, lietotajs_id, pieradijums, datums, False),
        )


def pievienot_lietotaju(vards, uzvards, epasts, klase, loma):
    with savienot() as conn:
        conn.execute(
            "INSERT INTO lietotaji (vards, uzvards, epasts, klase, loma) VALUES (?, ?, ?, ?, ?)",
            (vards, uzvards, epasts, klase, loma),
        )


def pievienot_kategoriju(nosaukums):
    with savienot() as conn:
        conn.execute("INSERT INTO kategorijas (nosaukums) VALUES (?)", (nosaukums,))


def pievienot_mantu(nosaukums, apraksts, kategorija_id, vieta, datums, statuss, pievienoja_id, foto):
    with savienot() as conn:
        conn.execute(
            "INSERT INTO mantas (nosaukums, apraksts, kategorija_id, vieta, datums, statuss, pievienoja_id, foto) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (nosaukums, apraksts, kategorija_id, vieta, datums, statuss, pievienoja_id, foto),
        )
