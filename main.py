
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import funkcijas


# Dizaina krāsas
FONS = "#E5E7EB"
PANELIS = "#F8FAFC"
POGU_KRASA = "#64748B"
POGU_AKTIVA = "#475569"
TEKSTS = "#1F2937"
BALTS = "#FFFFFF"


def loga_dizains(logs):
    logs.configure(bg=FONS)


def pogas_dizains(poga):
    poga.configure(
        bg=POGU_KRASA,
        fg=BALTS,
        activebackground=POGU_AKTIVA,
        activeforeground=BALTS,
        font=("Arial", 10),
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=10,
        pady=7
    )


def tabulas_logs(nosaukums, kolonnas, rindas):
    logs = tk.Toplevel(root)
    logs.title(nosaukums)
    logs.geometry("700x400")
    loga_dizains(logs)

    stils = ttk.Style()
    stils.theme_use("clam")

    stils.configure(
        "Treeview",
        background=BALTS,
        foreground=TEKSTS,
        rowheight=30,
        fieldbackground=BALTS,
        font=("Arial", 10)
    )

    stils.configure(
        "Treeview.Heading",
        background=POGU_KRASA,
        foreground=BALTS,
        font=("Arial", 10, "bold"),
        relief="flat"
    )

    stils.map(
        "Treeview",
        background=[("selected", "#CBD5E1")],
        foreground=[("selected", TEKSTS)]
    )

    tabula = ttk.Treeview(
        logs,
        columns=kolonnas,
        show="headings"
    )

    for kolonna in kolonnas:
        tabula.heading(kolonna, text=kolonna)
        tabula.column(
            kolonna,
            width=700 // len(kolonnas),
            anchor="center"
        )

    tabula.pack(fill="both", expand=True, padx=15, pady=15)

    for rinda in rindas:
        tabula.insert("", "end", values=rinda)


def formas_logs(nosaukums, lauki, saglabat):
    logs = tk.Toplevel(root)
    logs.title(nosaukums)
    logs.geometry("400x350")
    loga_dizains(logs)

    ievades = []

    virsraksts = tk.Label(
        logs,
        text=nosaukums,
        bg=FONS,
        fg=TEKSTS,
        font=("Arial", 15, "bold")
    )
    virsraksts.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=15
    )

    for i, lauks in enumerate(lauki):
        tk.Label(
            logs,
            text=lauks,
            bg=FONS,
            fg=TEKSTS,
            font=("Arial", 10)
        ).grid(
            row=i + 1,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        ievade = tk.Entry(
            logs,
            width=30,
            font=("Arial", 10),
            bg=BALTS,
            fg=TEKSTS,
            relief="solid",
            bd=1
        )

        ievade.grid(
            row=i + 1,
            column=1,
            padx=10,
            pady=8
        )

        ievades.append(ievade)

    def nospiests():
        vertibas = [ievade.get() or None for ievade in ievades]

        try:
            saglabat(*vertibas)
        except Exception as e:
            messagebox.showerror("Kļūda", str(e), parent=logs)
            return

        messagebox.showinfo("Gatavs", "Saglabāts", parent=logs)
        logs.destroy()

    poga = tk.Button(
        logs,
        text="Saglabāt",
        command=nospiests
    )
    pogas_dizains(poga)
    poga.grid(
        row=len(lauki) + 1,
        column=0,
        columnspan=2,
        pady=20
    )


def redzet_mantas():
    rindas = [
        (m[0], m[1], m[5])
        for m in funkcijas.apskatit_mantas()
    ]

    tabulas_logs(
        "Mantas",
        ("ID", "Manta", "Pievienota"),
        rindas
    )


def redzet_pieteikumus():
    rindas = [
        (p[1], p[2], p[4], "Jā" if p[5] else "Nē")
        for p in funkcijas.apskatit_pieteikumus()
    ]

    tabulas_logs(
        "Pieteikumi",
        ("Manta", "Lietotājs", "Datums", "Apstiprināts"),
        rindas
    )


def izveidot_pieteikumu():
    formas_logs(
        "Izveidot pieteikumu",
        ["Mantas ID", "Lietotāja ID"],
        lambda manta_id, lietotajs_id:
            funkcijas.izveidot_pieteikumu(
                manta_id,
                lietotajs_id,
                None,
                date.today().isoformat()
            )
    )


def pievienot_lietotaju():
    formas_logs(
        "Pievienot lietotāju",
        ["Vārds", "Uzvārds", "E-pasts", "Klase", "Loma"],
        funkcijas.pievienot_lietotaju
    )


def pievienot_kategoriju():
    formas_logs(
        "Pievienot kategoriju",
        ["Nosaukums"],
        funkcijas.pievienot_kategoriju
    )


def pievienot_mantu():
    formas_logs(
        "Pievienot mantu",
        ["Nosaukums", "Apraksts", "Kategorijas ID"],
        lambda nosaukums, apraksts, kategorija_id:
            funkcijas.pievienot_mantu(
                nosaukums,
                apraksts,
                kategorija_id,
                None,
                date.today().isoformat(),
                None,
                None,
                None
            )
    )


def izveleties_lietotaju():
    logs = tk.Toplevel(root)
    logs.title("Izvēlēties lietotāju")
    logs.geometry("300x300")
    loga_dizains(logs)

    logs.protocol("WM_DELETE_WINDOW", root.destroy)

    lietotaji = funkcijas.apskatit_lietotajus()

    virsraksts = tk.Label(
        logs,
        text="Izvēlies lietotāju",
        bg=FONS,
        fg=TEKSTS,
        font=("Arial", 14, "bold")
    )
    virsraksts.pack(pady=12)

    saraksts = tk.Listbox(
        logs,
        bg=BALTS,
        fg=TEKSTS,
        font=("Arial", 10),
        selectbackground="#CBD5E1",
        selectforeground=TEKSTS,
        relief="solid",
        bd=1
    )

    for l in lietotaji:
        saraksts.insert("end", f"{l[1]} {l[2]}".strip())

    saraksts.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    def izvelets():
        global lietotajs

        izvele = saraksts.curselection()

        if not izvele:
            messagebox.showerror(
                "Kļūda",
                "Izvēlies lietotāju",
                parent=logs
            )
            return

        lietotajs = lietotaji[izvele[0]]

        lietotaja_info.config(
            text=f"{lietotajs[1]} {lietotajs[2]} | ID: {lietotajs[0]} | Klase: {lietotajs[4] or '-'}"
        )

        logs.destroy()
        root.deiconify()

    poga = tk.Button(
        logs,
        text="Izvēlēties",
        command=izvelets
    )
    pogas_dizains(poga)
    poga.pack(pady=10)


lietotajs = None

root = tk.Tk()
root.title("Pazudušās mantas")
root.geometry("400x450")
root.configure(bg=FONS)

root.withdraw()

# Galvenais virsraksts
virsraksts = tk.Label(
    root,
    text="Pazudušās mantas",
    bg=FONS,
    fg=TEKSTS,
    font=("Arial", 19, "bold")
)
virsraksts.pack(pady=20)

# Galvenās pogas
pogas = [
    ("Redzēt mantas", redzet_mantas),
    ("Redzēt pieteikumus", redzet_pieteikumus),
    ("Izveidot pieteikumu", izveidot_pieteikumu),
    ("Pievienot lietotāju", pievienot_lietotaju),
    ("Pievienot kategoriju", pievienot_kategoriju),
    ("Pievienot mantu", pievienot_mantu),
]

for teksts, komanda in pogas:
    poga = tk.Button(
        root,
        text=teksts,
        command=komanda,
        width=25
    )

    pogas_dizains(poga)
    poga.pack(pady=6)

# Lietotāja informācija apakšā
lietotaja_info = tk.Label(
    root,
    bg="#D1D5DB",
    fg=TEKSTS,
    font=("Arial", 9),
    padx=5,
    pady=10
)

lietotaja_info.pack(
    side="bottom",
    fill="x",
    pady=10
)

izveleties_lietotaju()

root.mainloop()
