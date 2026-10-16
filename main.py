import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

import funkcijas


def tabulas_logs(nosaukums, kolonnas, rindas):
    logs = tk.Toplevel(root)
    logs.title(nosaukums)
    logs.geometry("700x400")

    tabula = ttk.Treeview(logs, columns=kolonnas, show="headings")
    for kolonna in kolonnas:
        tabula.heading(kolonna, text=kolonna)
        tabula.column(kolonna, width=700 // len(kolonnas))
    tabula.pack(fill="both", expand=True)

    for rinda in rindas:
        tabula.insert("", "end", values=rinda)


def formas_logs(nosaukums, lauki, saglabat):
    logs = tk.Toplevel(root)
    logs.title(nosaukums)
    logs.geometry("400x350")

    ievades = []
    for i, lauks in enumerate(lauki):
        tk.Label(logs, text=lauks).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        ievade = tk.Entry(logs, width=30)
        ievade.grid(row=i, column=1, padx=10, pady=5)
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

    tk.Button(logs, text="Saglabāt", command=nospiests).grid(row=len(lauki), column=0, columnspan=2, pady=15)


def redzet_mantas():
    rindas = [(m[0], m[1], m[5]) for m in funkcijas.apskatit_mantas()]
    tabulas_logs("Mantas", ("ID", "Manta", "Pievienota"), rindas)


def redzet_pieteikumus():
    rindas = [(p[1], p[2], p[4], "Jā" if p[5] else "Nē") for p in funkcijas.apskatit_pieteikumus()]
    tabulas_logs("Pieteikumi", ("Manta", "Lietotājs", "Datums", "Apstiprināts"), rindas)


def izveidot_pieteikumu():
    formas_logs(
        "Izveidot pieteikumu",
        ["Mantas ID", "Lietotāja ID"],
        lambda manta_id, lietotajs_id: funkcijas.izveidot_pieteikumu(
            manta_id, lietotajs_id, None, date.today().isoformat()
        ),
    )


def pievienot_lietotaju():
    formas_logs(
        "Pievienot lietotāju",
        ["Vārds", "Uzvārds", "E-pasts", "Klase", "Loma"],
        funkcijas.pievienot_lietotaju,
    )


def pievienot_kategoriju():
    formas_logs("Pievienot kategoriju", ["Nosaukums"], funkcijas.pievienot_kategoriju)


def pievienot_mantu():
    formas_logs(
        "Pievienot mantu",
        ["Nosaukums", "Apraksts", "Kategorijas ID"],
        lambda nosaukums, apraksts, kategorija_id: funkcijas.pievienot_mantu(
            nosaukums, apraksts, kategorija_id, None, date.today().isoformat(), None, None, None
        ),
    )


def izveleties_lietotaju():
    logs = tk.Toplevel(root)
    logs.title("Izvēlēties lietotāju")
    logs.geometry("300x300")
    logs.protocol("WM_DELETE_WINDOW", root.destroy)

    lietotaji = funkcijas.apskatit_lietotajus()
    saraksts = tk.Listbox(logs)
    for l in lietotaji:
        saraksts.insert("end", f"{l[1]} {l[2]}".strip())
    saraksts.pack(fill="both", expand=True, padx=10, pady=10)

    def izvelets():
        global lietotajs
        izvele = saraksts.curselection()
        if not izvele:
            messagebox.showerror("Kļūda", "Izvēlies lietotāju", parent=logs)
            return
        lietotajs = lietotaji[izvele[0]]
        lietotaja_info.config(text=f"{lietotajs[1]} {lietotajs[2]} | ID: {lietotajs[0]} | Klase: {lietotajs[4] or '-'}")
        logs.destroy()
        root.deiconify()

    tk.Button(logs, text="Izvēlēties", command=izvelets).pack(pady=10)


lietotajs = None

root = tk.Tk()
root.title("Pazudušās mantas")
root.geometry("400x400")
root.withdraw()

pogas = [
    ("Redzēt mantas", redzet_mantas),
    ("Redzēt pieteikumus", redzet_pieteikumus),
    ("Izveidot pieteikumu", izveidot_pieteikumu),
    ("Pievienot lietotāju", pievienot_lietotaju),
    ("Pievienot kategoriju", pievienot_kategoriju),
    ("Pievienot mantu", pievienot_mantu),
]
for teksts, komanda in pogas:
    tk.Button(root, text=teksts, command=komanda, width=25).pack(pady=8)

lietotaja_info = tk.Label(root)
lietotaja_info.pack(side="bottom", pady=10)

izveleties_lietotaju()
root.mainloop()
