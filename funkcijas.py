import sqlite3
from pathlib import Path
from datetime import date

DB = Path(__file__).with_name("mantas.db")


def savienot():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def sagatavot_datubazi():
    """Pievieno trūkstošos laukus vecākai datubāzei, nedzēšot esošos datus."""
    with savienot() as conn:
        kolonnas = [r[1] for r in conn.execute("PRAGMA table_info(pieteikumi)")]
        if "statuss" not in kolonnas:
            conn.execute("ALTER TABLE pieteikumi ADD COLUMN statuss TEXT")
            conn.execute("""
                UPDATE pieteikumi
                SET statuss = CASE WHEN apstiprinats = 1
                    THEN 'Apstiprināts' ELSE 'Gaida' END
            """)
        conn.execute("UPDATE mantas SET statuss = 'Pieejama' WHERE statuss IS NULL OR statuss = ''")


def apskatit_mantas():
    with savienot() as conn:
        return conn.execute("""
            SELECT m.id, m.nosaukums, m.apraksts, m.kategorija_id,
                   m.vieta, m.datums, m.statuss, m.pievienoja_id, m.foto,
                   COALESCE(k.nosaukums, 'Nav kategorijas'),
                   COALESCE(l.vards || ' ' || l.uzvards, 'Nav norādīts')
            FROM mantas m
            LEFT JOIN kategorijas k ON k.id = m.kategorija_id
            LEFT JOIN lietotaji l ON l.id = m.pievienoja_id
            ORDER BY m.id DESC
        """).fetchall()


def apskatit_lietotajus():
    with savienot() as conn:
        return conn.execute("SELECT * FROM lietotaji ORDER BY vards, uzvards").fetchall()


def apskatit_kategorijas():
    with savienot() as conn:
        return conn.execute("SELECT id, nosaukums FROM kategorijas ORDER BY nosaukums").fetchall()


def apskatit_pieteikumus(lietotajs_id=None, ir_admin=False):
    with savienot() as conn:
        sql = """
            SELECT p.id, m.nosaukums,
                   l.vards || ' ' || l.uzvards, p.pieradijums,
                   p.datums, COALESCE(p.statuss, 'Gaida'), p.manta_id,
                   p.lietotajs_id
            FROM pieteikumi p
            LEFT JOIN mantas m ON m.id = p.manta_id
            LEFT JOIN lietotaji l ON l.id = p.lietotajs_id
        """
        if not ir_admin:
            sql += " WHERE p.lietotajs_id = ?"
            return conn.execute(sql + " ORDER BY p.id DESC", (lietotajs_id,)).fetchall()
        return conn.execute(sql + " ORDER BY p.id DESC").fetchall()


def pievienot_lietotaju(vards, uzvards, epasts, klase, loma):
    vards, uzvards = (vards or "").strip(), (uzvards or "").strip()
    if not vards or not uzvards:
        raise ValueError("Vārds un uzvārds ir obligāti.")
    epasts = (epasts or "").strip() or None
    if epasts and ("@" not in epasts or "." not in epasts.split("@")[-1]):
        raise ValueError("Ievadi derīgu e-pasta adresi.")
    loma = (loma or "lietotajs").strip().lower()
    if loma not in ("admin", "lietotajs"):
        raise ValueError("Lomai jābūt 'admin' vai 'lietotajs'.")
    with savienot() as conn:
        conn.execute(
            "INSERT INTO lietotaji (vards, uzvards, epasts, klase, loma) VALUES (?, ?, ?, ?, ?)",
            (vards, uzvards, epasts, (klase or "").strip() or None, loma)
        )


def pievienot_kategoriju(nosaukums):
    nosaukums = (nosaukums or "").strip()
    if not nosaukums:
        raise ValueError("Kategorijas nosaukums nedrīkst būt tukšs.")
    with savienot() as conn:
        eksiste = conn.execute("SELECT 1 FROM kategorijas WHERE lower(nosaukums)=lower(?)", (nosaukums,)).fetchone()
        if eksiste:
            raise ValueError("Šāda kategorija jau eksistē.")
        conn.execute("INSERT INTO kategorijas (nosaukums) VALUES (?)", (nosaukums,))


def pievienot_mantu(nosaukums, apraksts, kategorija_id, vieta, datums, statuss, pievienoja_id, foto):
    nosaukums = (nosaukums or "").strip()
    if not nosaukums:
        raise ValueError("Mantas nosaukums ir obligāts.")
    kategorija_id = int(kategorija_id) if kategorija_id not in (None, "") else None
    if kategorija_id is not None:
        with savienot() as conn:
            if not conn.execute("SELECT 1 FROM kategorijas WHERE id=?", (kategorija_id,)).fetchone():
                raise ValueError("Izvēlētā kategorija neeksistē.")
            conn.execute("""
                INSERT INTO mantas (nosaukums, apraksts, kategorija_id, vieta, datums, statuss, pievienoja_id, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nosaukums, apraksts, kategorija_id, vieta, datums or date.today().isoformat(),
                  statuss or "Pieejama", pievienoja_id, foto))
    else:
        with savienot() as conn:
            conn.execute("""
                INSERT INTO mantas (nosaukums, apraksts, kategorija_id, vieta, datums, statuss, pievienoja_id, foto)
                VALUES (?, ?, NULL, ?, ?, ?, ?, ?)
            """, (nosaukums, apraksts, vieta, datums or date.today().isoformat(),
                  statuss or "Pieejama", pievienoja_id, foto))


def rediget_mantu(manta_id, nosaukums, apraksts, kategorija_id, vieta, foto):
    if not (nosaukums or "").strip():
        raise ValueError("Mantas nosaukums ir obligāts.")
    kat_id = int(kategorija_id) if kategorija_id else None
    with savienot() as conn:
        conn.execute("""
            UPDATE mantas SET nosaukums=?, apraksts=?, kategorija_id=?, vieta=?, foto=?
            WHERE id=?
        """, (nosaukums.strip(), apraksts, kat_id, vieta, foto, int(manta_id)))


def dzest_mantu(manta_id):
    with savienot() as conn:
        conn.execute("DELETE FROM pieteikumi WHERE manta_id=?", (int(manta_id),))
        conn.execute("DELETE FROM mantas WHERE id=?", (int(manta_id),))


def izveidot_pieteikumu(manta_id, lietotajs_id, pieradijums=None, datums=None):
    try:
        manta_id, lietotajs_id = int(manta_id), int(lietotajs_id)
    except (TypeError, ValueError):
        raise ValueError("Mantas ID nav derīgs.")
    with savienot() as conn:
        manta = conn.execute("SELECT statuss FROM mantas WHERE id=?", (manta_id,)).fetchone()
        if not manta:
            raise ValueError("Manta ar šādu ID nav atrasta.")
        if manta[0] == "Atdota":
            raise ValueError("Šī manta jau ir atdota.")
        if not conn.execute("SELECT 1 FROM lietotaji WHERE id=?", (lietotajs_id,)).fetchone():
            raise ValueError("Lietotājs nav atrasts.")
        aktivs = conn.execute("""
            SELECT 1 FROM pieteikumi
            WHERE manta_id=? AND lietotajs_id=? AND COALESCE(statuss, 'Gaida') IN ('Gaida', 'Apstiprināts')
        """, (manta_id, lietotajs_id)).fetchone()
        if aktivs:
            raise ValueError("Tev jau ir aktīvs pieteikums uz šo mantu.")
        conn.execute("""
            INSERT INTO pieteikumi (manta_id, lietotajs_id, pieradijums, datums, apstiprinats, statuss)
            VALUES (?, ?, ?, ?, 0, 'Gaida')
        """, (manta_id, lietotajs_id, pieradijums, datums or date.today().isoformat()))


def mainit_pieteikuma_statusu(pieteikuma_id, statuss):
    if statuss not in ("Apstiprināts", "Noraidīts"):
        raise ValueError("Nederīgs pieteikuma statuss.")
    with savienot() as conn:
        p = conn.execute("SELECT manta_id, statuss FROM pieteikumi WHERE id=?", (int(pieteikuma_id),)).fetchone()
        if not p:
            raise ValueError("Pieteikums nav atrasts.")
        manta_id = p[0]
        if statuss == "Apstiprināts":
            manta = conn.execute("SELECT statuss FROM mantas WHERE id=?", (manta_id,)).fetchone()
            if not manta or manta[0] == "Atdota":
                raise ValueError("Šī manta vairs nav pieejama.")
            cits = conn.execute("""
                SELECT 1 FROM pieteikumi
                WHERE manta_id=? AND statuss='Apstiprināts' AND id<>?
            """, (manta_id, int(pieteikuma_id))).fetchone()
            if cits:
                raise ValueError("Šai mantai jau ir apstiprināts cits pieteikums.")
            conn.execute("UPDATE pieteikumi SET statuss='Noraidīts', apstiprinats=0 WHERE manta_id=? AND id<>? AND statuss='Gaida'",
                         (manta_id, int(pieteikuma_id)))
            conn.execute("UPDATE mantas SET statuss='Atdota' WHERE id=?", (manta_id,))
        conn.execute("UPDATE pieteikumi SET statuss=?, apstiprinats=? WHERE id=?",
                     (statuss, 1 if statuss == "Apstiprināts" else 0, int(pieteikuma_id)))


def dzest_pieteikumu(pieteikuma_id):
    with savienot() as conn:
        conn.execute("DELETE FROM pieteikumi WHERE id=?", (int(pieteikuma_id),))
