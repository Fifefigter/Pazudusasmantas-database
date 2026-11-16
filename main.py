
import tkinter as tk
from tkinter import ttk, messagebox
import funkcijas


# Galvenā loga izveide
root = tk.Tk()
root.title("Pazudušās mantas")
root.geometry("950x650")
root.configure(bg="#1E1E2E")


# Krāsas
FONS = "#1E1E2E"
POGAS = "#45475A"
AKTIVS = "#7C3AED"
TEKSTS = "#FFFFFF"
IEVADE = "#313244"


# Virsraksts
virsraksts = tk.Label(
    root,
    text="Pazudušo mantu sistēma",
    font=("Arial", 22, "bold"),
    bg=FONS,
    fg=TEKSTS
)
virsraksts.pack(pady=20)


# Izvēlnes rāmis
izvelne = tk.Frame(root, bg=FONS)
izvelne.pack(pady=10)


# Satura rāmis
saturs = tk.Frame(
    root,
    bg="#28283A",
    bd=0
)
saturs.pack(fill="both", expand=True, padx=25, pady=15)


# Funkcija satura notīrīšanai
def notirit_saturu():
    for elements in saturs.winfo_children():
        elements.destroy()


# Tabulas izveide
def izveidot_tabulu(kolonnas, dati):

    tabulas_ramis = tk.Frame(saturs, bg="#28283A")
    tabulas_ramis.pack(fill="both", expand=True, padx=10, pady=10)

    stils = ttk.Style()
    stils.theme_use("clam")

    stils.configure(
        "Treeview",
        background="#313244",
        foreground="white",
        fieldbackground="#313244",
        rowheight=30
    )

    stils.configure(
        "Treeview.Heading",
        background="#45475A",
        foreground="white",
        font=("Arial", 10, "bold")
    )

    stils.map(
        "Treeview",
        background=[("selected", "#7C3AED")]
    )

    tabula = ttk.Treeview(
        tabulas_ramis,
        columns=kolonnas,
        show="headings"
    )

    for kolonna in kolonnas:
        tabula.heading(kolonna, text=kolonna)
        tabula.column(kolonna, width=130)

    for rinda in dati:
        tabula.insert("", "end", values=rinda)

    tabula.pack(fill="both", expand=True)


# Poga
def izveidot_pogu(teksts, komanda):
    return tk.Button(
        izvelne,
        text=teksts,
        command=komanda,
        bg=POGAS,
        fg=TEKSTS,
        activebackground=AKTIVS,
        activeforeground=TEKSTS,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=8
    )


# Visas mantas
def redzet_mantas():

    notirit_saturu()

    tk.Label(
        saturs,
        text="Visas mantas",
        font=("Arial", 18, "bold"),
        bg="#28283A",
        fg=TEKSTS
    ).pack(pady=15)

    try:
        mantas = funkcijas.apskatit_mantas()

        dati = [
            (
                m[0],
                m[1],
                m[2],
                m[4],
                m[5],
                m[6]
            )
            for m in mantas
        ]

        izveidot_tabulu(
            ("ID", "Nosaukums", "Apraksts",
             "Vieta", "Datums", "Statuss"),
            dati
        )

    except Exception as e:
        messagebox.showerror("Kļūda", str(e))


# Pievienot mantu
def pievienot_mantu():

    logs = tk.Toplevel(root)
    logs.title("Pievienot mantu")
    logs.geometry("400x430")
    logs.configure(bg=FONS)

    tk.Label(
        logs,
        text="Pievienot jaunu mantu",
        font=("Arial", 17, "bold"),
        bg=FONS,
        fg=TEKSTS
    ).pack(pady=15)

    ievades = {}

    lauki = [
        "Nosaukums",
        "Apraksts",
        "Kategorijas ID",
        "Vieta",
        "Pievienotāja ID"
    ]

    for lauks in lauki:

        tk.Label(
            logs,
            text=lauks,
            bg=FONS,
            fg=TEKSTS,
            font=("Arial", 10)
        ).pack(pady=3)

        entry = tk.Entry(
            logs,
            bg=IEVADE,
            fg=TEKSTS,
            insertbackground=TEKSTS,
            relief="flat",
            font=("Arial", 11)
        )
        entry.pack(padx=30, fill="x", ipady=5)

        ievades[lauks] = entry

    def saglabat():

        try:
            funkcijas.pievienot_mantu(
                ievades["Nosaukums"].get(),
                ievades["Apraksts"].get(),
                int(ievades["Kategorijas ID"].get()),
                ievades["Vieta"].get(),
                __import__("datetime").date.today().isoformat(),
                "Pieejama",
                int(ievades["Pievienotāja ID"].get()),
                None
            )

            messagebox.showinfo(
                "Gatavs",
                "Manta veiksmīgi pievienota!"
            )

            logs.destroy()
            redzet_mantas()

        except Exception as e:
            messagebox.showerror("Kļūda", str(e))

    tk.Button(
        logs,
        text="Saglabāt",
        command=saglabat,
        bg=AKTIVS,
        fg=TEKSTS,
        relief="flat",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=8
    ).pack(pady=20)


# Lietotāji
def redzet_lietotajus():

    notirit_saturu()

    tk.Label(
        saturs,
        text="Lietotāji",
        font=("Arial", 18, "bold"),
        bg="#28283A",
        fg=TEKSTS
    ).pack(pady=15)

    try:
        lietotaji = funkcijas.apskatit_lietotajus()

        dati = [
            (l[0], l[1], l[2], l[3], l[4], l[5])
            for l in lietotaji
        ]

        izveidot_tabulu(
            ("ID", "Vārds", "Uzvārds",
             "E-pasts", "Klase", "Loma"),
            dati
        )

    except Exception as e:
        messagebox.showerror("Kļūda", str(e))


# Pieteikumi
def redzet_pieteikumus():

    notirit_saturu()

    tk.Label(
        saturs,
        text="Pieteikumi",
        font=("Arial", 18, "bold"),
        bg="#28283A",
        fg=TEKSTS
    ).pack(pady=15)

    try:
        pieteikumi = funkcijas.apskatit_pieteikumus()

        dati = [
            (p[0], p[1], p[2], p[4], p[5])
            for p in pieteikumi
        ]

        izveidot_tabulu(
            ("ID", "Manta", "Lietotājs",
             "Datums", "Apstiprināts"),
            dati
        )

    except Exception as e:
        messagebox.showerror("Kļūda", str(e))


# Galvenā lapa
def sakums():

    notirit_saturu()

    tk.Label(
        saturs,
        text="Laipni lūdzam!",
        font=("Arial", 22, "bold"),
        bg="#28283A",
        fg=TEKSTS
    ).pack(pady=40)

    tk.Label(
        saturs,
        text="Šeit vari apskatīt un pārvaldīt pazudušās un atrastās mantas.",
        font=("Arial", 12),
        bg="#28283A",
        fg="#CBA6F7"
    ).pack(pady=10)

    try:
        mantas = funkcijas.apskatit_mantas()
        skaits = len(mantas)

        tk.Label(
            saturs,
            text=f"Kopā reģistrētas mantas: {skaits}",
            font=("Arial", 14, "bold"),
            bg="#28283A",
            fg=TEKSTS
        ).pack(pady=20)

    except Exception as e:
        messagebox.showerror("Kļūda", str(e))


# Izvēlnes pogas
izveidot_pogu("Sākums", sakums).pack(side="left", padx=5)
izveidot_pogu("Visas mantas", redzet_mantas).pack(side="left", padx=5)
izveidot_pogu("Pievienot mantu", pievienot_mantu).pack(side="left", padx=5)
izveidot_pogu("Lietotāji", redzet_lietotajus).pack(side="left", padx=5)
izveidot_pogu("Pieteikumi", redzet_pieteikumus).pack(side="left", padx=5)


# Atvērt sākuma lapu
sakums()


# Programmas palaišana
root.mainloop()
