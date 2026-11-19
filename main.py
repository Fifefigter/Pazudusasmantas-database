import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import funkcijas


# Dizaina krāsas (saglabāts sākotnējais dizains)
FONS = "#E5E7EB"
PANELIS = "#F8FAFC"
POGU_KRASA = "#64748B"
POGU_AKTIVA = "#475569"
TEKSTS = "#1F2937"
BALTS = "#FFFFFF"

lietotajs = None


def loga_dizains(logs):
    logs.configure(bg=FONS)


def pogas_dizains(poga):
    poga.configure(bg=POGU_KRASA, fg=BALTS, activebackground=POGU_AKTIVA,
                   activeforeground=BALTS, font=("Arial", 10), relief="flat",
                   bd=0, cursor="hand2", padx=10, pady=7)


def ir_admin():
    return lietotajs and (lietotajs[5] or "").lower() == "admin"


def tabulas_logs(nosaukums, kolonnas, rindas):
    logs = tk.Toplevel(root)
    logs.title(nosaukums)
    logs.geometry("700x400")
    loga_dizains(logs)
    stils = ttk.Style()
    stils.theme_use("clam")
    stils.configure("Treeview", background=BALTS, foreground=TEKSTS,
                    rowheight=30, fieldbackground=BALTS, font=("Arial", 10))
    stils.configure("Treeview.Heading", background=POGU_KRASA,
                    foreground=BALTS, font=("Arial", 10, "bold"), relief="flat")
    tabula = ttk.Treeview(logs, columns=kolonnas, show="headings")
    for kolonna in kolonnas:
        tabula.heading(kolonna, text=kolonna)
        tabula.column(kolonna, width=700 // len(kolonnas), anchor="center")
    tabula.pack(fill="both", expand=True, padx=15, pady=15)
    for rinda in rindas:
        tabula.insert("", "end", values=rinda)
    return logs, tabula


def formas_logs(nosaukums, lauki, saglabat):
    logs = tk.Toplevel(root)
    logs.title(nosaukums)
    logs.geometry("400x350")
    loga_dizains(logs)
    ievades = []
    tk.Label(logs, text=nosaukums, bg=FONS, fg=TEKSTS,
             font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
    for i, lauks in enumerate(lauki):
        tk.Label(logs, text=lauks, bg=FONS, fg=TEKSTS,
                 font=("Arial", 10)).grid(row=i+1, column=0, padx=10, pady=8, sticky="w")
        ievade = tk.Entry(logs, width=30, font=("Arial", 10), bg=BALTS,
                          fg=TEKSTS, relief="solid", bd=1)
        ievade.grid(row=i+1, column=1, padx=10, pady=8)
        ievades.append(ievade)

    def nospiests():
        try:
            saglabat(*[e.get().strip() or None for e in ievades])
        except Exception as e:
            messagebox.showerror("Kļūda", str(e), parent=logs)
            return
        messagebox.showinfo("Gatavs", "Saglabāts", parent=logs)
        logs.destroy()
    poga = tk.Button(logs, text="Saglabāt", command=nospiests)
    pogas_dizains(poga)
    poga.grid(row=len(lauki)+1, column=0, columnspan=2, pady=20)


def redzet_mantas():
    logs, tabula = tabulas_logs("Mantas",
        ("ID", "Manta", "Kategorija", "Atrašanās vieta", "Pievienota", "Statuss"), [])
    augsa = tk.Frame(logs, bg=FONS)
    augsa.pack(fill="x", padx=15)
    tk.Label(augsa, text="Meklēt:", bg=FONS, fg=TEKSTS).pack(side="left")
    meklesana = tk.Entry(augsa, width=25)
    meklesana.pack(side="left", padx=6)
    kategorijas = funkcijas.apskatit_kategorijas()
    izveles = ["Visas kategorijas"] + [k[1] for k in kategorijas]
    filtrs = ttk.Combobox(augsa, values=izveles, state="readonly", width=20)
    filtrs.set("Visas kategorijas")
    filtrs.pack(side="left", padx=6)

    visas = funkcijas.apskatit_mantas()
    redzamie = {}

    def atjaunot(*_):
        tabula.delete(*tabula.get_children())
        redzamie.clear()
        teksts = meklesana.get().lower()
        kategorija = filtrs.get()
        for m in visas:
            if not ir_admin() and (m[6] or "Pieejama") != "Pieejama":
                continue
            if teksts not in m[1].lower():
                continue
            if kategorija != "Visas kategorijas" and m[9] != kategorija:
                continue
            dati = (m[0], m[1], m[9], m[4] or "-", m[5], m[6] or "Pieejama")
            redzamie[str(m[0])] = m
            tabula.insert("", "end", iid=str(m[0]), values=dati)
        if not tabula.get_children():
            tabula.insert("", "end", values=("", "Mantas nav atrastas", "", "", "", ""))

    meklesana.bind("<KeyRelease>", atjaunot)
    filtrs.bind("<<ComboboxSelected>>", atjaunot)
    atjaunot()

    apaks = tk.Frame(logs, bg=FONS)
    apaks.pack(pady=5)
    def izveleta_manta():
        izvele = tabula.selection()
        if not izvele or izvele[0] not in redzamie:
            messagebox.showerror("Kļūda", "Vispirms izvēlies mantu.", parent=logs)
            return None
        return redzamie[izvele[0]]

    def detalas():
        m = izveleta_manta()
        if not m: return
        info = (f"Nosaukums: {m[1]}\\nApraksts: {m[2] or '-'}\\nKategorija: {m[9]}\\n"
                f"Atrašanās vieta: {m[4] or '-'}\\nDatums: {m[5]}\\n"
                f"Statuss: {m[6] or 'Pieejama'}\\nPievienoja: {m[10]}")
        detalas_logs = tk.Toplevel(logs)
        detalas_logs.title("Mantas informācija")
        detalas_logs.geometry("500x400")
        loga_dizains(detalas_logs)
        tk.Label(detalas_logs, text=info, bg=FONS, fg=TEKSTS,
                 font=("Arial", 10), justify="left", anchor="w").pack(fill="x", padx=15, pady=15)
        if m[8]:
            try:
                try:
                    from PIL import Image, ImageTk
                    attels = Image.open(m[8])
                    attels.thumbnail((250, 200))
                    foto = ImageTk.PhotoImage(attels)
                except ImportError:
                    foto = tk.PhotoImage(file=m[8])
                attela_uzl = tk.Label(detalas_logs, image=foto, bg=FONS)
                attela_uzl.image = foto
                attela_uzl.pack(pady=5)
            except Exception:
                tk.Label(detalas_logs, text="Attēlu nevar atvērt vai fails nav pieejams.",
                         bg=FONS, fg=TEKSTS).pack(pady=5)
        else:
            tk.Label(detalas_logs, text="Attēls nav pievienots",
                     bg=FONS, fg=TEKSTS).pack(pady=5)

    def rediget():
        m = izveleta_manta()
        if not m: return
        kategorijas = funkcijas.apskatit_kategorijas()
        forma = tk.Toplevel(logs)
        forma.title("Rediģēt mantu")
        forma.geometry("400x390")
        loga_dizains(forma)
        lauki = [("Nosaukums", m[1]), ("Apraksts", m[2] or ""), ("Atrašanās vieta", m[4] or "")]
        iev = []
        for i, (nos, vert) in enumerate(lauki):
            tk.Label(forma, text=nos, bg=FONS, fg=TEKSTS).grid(row=i, column=0, padx=10, pady=8)
            e=tk.Entry(forma, width=28); e.insert(0, vert); e.grid(row=i,column=1); iev.append(e)
        tk.Label(forma,text="Kategorija",bg=FONS,fg=TEKSTS).grid(row=3,column=0,padx=10,pady=8)
        kat=ttk.Combobox(forma,values=[f"{k[0]}: {k[1]}" for k in kategorijas],state="readonly",width=25)
        for k in kategorijas:
            if k[0] == m[3]: kat.set(f"{k[0]}: {k[1]}")
        kat.grid(row=3,column=1)
        foto=[m[8]]
        def izveleties_foto():
            fails=filedialog.askopenfilename(filetypes=[("Attēli","*.jpg *.jpeg *.png")])
            if fails: foto[0]=fails; foto_label.config(text=fails.split("/")[-1])
        foto_label=tk.Label(forma,text=m[8] or "Attēls nav pievienots",bg=FONS,fg=TEKSTS)
        tk.Button(forma,text="Izvēlēties attēlu",command=izveleties_foto).grid(row=4,column=0,pady=8)
        foto_label.grid(row=4,column=1)
        def saglabat():
            try:
                kat_id=kat.get().split(":")[0] if kat.get() else None
                funkcijas.rediget_mantu(m[0],iev[0].get(),iev[1].get(),kat_id,iev[2].get(),foto[0])
                messagebox.showinfo("Gatavs","Izmaiņas saglabātas.",parent=forma)
                forma.destroy(); logs.destroy(); redzet_mantas()
            except Exception as e: messagebox.showerror("Kļūda",str(e),parent=forma)
        p=tk.Button(forma,text="Saglabāt",command=saglabat); pogas_dizains(p); p.grid(row=5,column=0,columnspan=2,pady=15)

    def dzest():
        m=izveleta_manta()
        if not m:return
        if messagebox.askyesno("Apstiprināt","Vai tiešām dzēst šo mantu un tās pieteikumus?",parent=logs):
            funkcijas.dzest_mantu(m[0]); logs.destroy(); redzet_mantas()

    for teksts, komanda in [("Apskatīt",detalas)]:
        p=tk.Button(apaks,text=teksts,command=komanda); pogas_dizains(p); p.pack(side="left",padx=4)
    if ir_admin():
        for teksts, komanda in [("Rediģēt mantu",rediget),("Dzēst mantu",dzest)]:
            p=tk.Button(apaks,text=teksts,command=komanda); pogas_dizains(p); p.pack(side="left",padx=4)


def redzet_pieteikumus():
    rindas=funkcijas.apskatit_pieteikumus(lietotajs[0],ir_admin())
    logs,tabula=tabulas_logs("Pieteikumi",("ID","Manta","Lietotājs","Datums","Statuss"),[])
    for p in rindas:
        tabula.insert("","end",iid=str(p[0]),values=(p[0],p[1] or "Dzēsta manta",p[2] or "Nezināms",p[4],p[5]))
    if ir_admin():
        apaks=tk.Frame(logs,bg=FONS); apaks.pack(pady=5)
        def darbiba(statuss):
            iz=tabula.selection()
            if not iz:
                messagebox.showerror("Kļūda","Izvēlies pieteikumu.",parent=logs); return
            try:
                funkcijas.mainit_pieteikuma_statusu(iz[0],statuss)
                logs.destroy(); redzet_pieteikumus()
            except Exception as e: messagebox.showerror("Kļūda",str(e),parent=logs)
        for txt,st in [("Apstiprināt","Apstiprināts"),("Noraidīt","Noraidīts")]:
            p=tk.Button(apaks,text=txt,command=lambda s=st:darbiba(s)); pogas_dizains(p); p.pack(side="left",padx=4)
        def dzest():
            iz=tabula.selection()
            if iz and messagebox.askyesno("Apstiprināt","Dzēst izvēlēto pieteikumu?",parent=logs):
                funkcijas.dzest_pieteikumu(iz[0]); logs.destroy(); redzet_pieteikumus()
        p=tk.Button(apaks,text="Dzēst pieteikumu",command=dzest); pogas_dizains(p); p.pack(side="left",padx=4)


def izveidot_pieteikumu():
    formas_logs("Izveidot pieteikumu",["Mantas ID","Pierādījums / papildu informācija"],
        lambda manta_id,pieradijums: funkcijas.izveidot_pieteikumu(
            manta_id,lietotajs[0],pieradijums,date.today().isoformat()))


def pievienot_lietotaju():
    formas_logs("Pievienot lietotāju",["Vārds","Uzvārds","E-pasts","Klase","Loma (admin/lietotajs)"],
                funkcijas.pievienot_lietotaju)


def pievienot_kategoriju():
    formas_logs("Pievienot kategoriju",["Nosaukums"],funkcijas.pievienot_kategoriju)


def pievienot_mantu():
    kategorijas=funkcijas.apskatit_kategorijas()
    if not kategorijas:
        messagebox.showerror("Kļūda","Vispirms pievieno vismaz vienu kategoriju.")
        return
    logs=tk.Toplevel(root); logs.title("Pievienot mantu"); logs.geometry("400x390"); loga_dizains(logs)
    ievades={}
    for i,nos in enumerate(["Nosaukums","Apraksts","Atrašanās vieta"]):
        tk.Label(logs,text=nos,bg=FONS,fg=TEKSTS).grid(row=i,column=0,padx=10,pady=8,sticky="w")
        e=tk.Entry(logs,width=30); e.grid(row=i,column=1,padx=8); ievades[nos]=e
    tk.Label(logs,text="Kategorija",bg=FONS,fg=TEKSTS).grid(row=3,column=0,padx=10,pady=8)
    kat=ttk.Combobox(logs,values=[f"{k[0]}: {k[1]}" for k in kategorijas],state="readonly",width=27)
    kat.grid(row=3,column=1)
    foto=[None]
    def izveleties():
        f=filedialog.askopenfilename(filetypes=[("Attēli","*.jpg *.jpeg *.png")])
        if f: foto[0]=f; foto_label.config(text=f.split("/")[-1])
    p=tk.Button(logs,text="Izvēlēties attēlu",command=izveleties); pogas_dizains(p); p.grid(row=4,column=0,pady=8)
    foto_label=tk.Label(logs,text="Attēls nav pievienots",bg=FONS,fg=TEKSTS); foto_label.grid(row=4,column=1)
    def saglabat():
        try:
            if not kat.get(): raise ValueError("Izvēlies kategoriju.")
            funkcijas.pievienot_mantu(ievades["Nosaukums"].get(),ievades["Apraksts"].get(),
                kat.get().split(":")[0],ievades["Atrašanās vieta"].get(),date.today().isoformat(),
                "Pieejama",lietotajs[0],foto[0])
            messagebox.showinfo("Gatavs","Manta pievienota.",parent=logs); logs.destroy()
        except Exception as e: messagebox.showerror("Kļūda",str(e),parent=logs)
    p=tk.Button(logs,text="Saglabāt",command=saglabat); pogas_dizains(p); p.grid(row=5,column=0,columnspan=2,pady=15)


def izveleties_lietotaju():
    logs=tk.Toplevel(root); logs.title("Izvēlēties lietotāju"); logs.geometry("300x300"); loga_dizains(logs)
    logs.protocol("WM_DELETE_WINDOW",root.destroy)
    lietotaji=funkcijas.apskatit_lietotajus()
    tk.Label(logs,text="Izvēlies lietotāju",bg=FONS,fg=TEKSTS,font=("Arial",14,"bold")).pack(pady=12)
    saraksts=tk.Listbox(logs,bg=BALTS,fg=TEKSTS,font=("Arial",10),selectbackground="#CBD5E1",selectforeground=TEKSTS,relief="solid",bd=1)
    for l in lietotaji: saraksts.insert("end",f"{l[1]} {l[2]} (ID: {l[0]})")
    saraksts.pack(fill="both",expand=True,padx=15,pady=10)
    def izvelets():
        global lietotajs
        iz=saraksts.curselection()
        if not iz:
            messagebox.showerror("Kļūda","Izvēlies lietotāju",parent=logs); return
        lietotajs=lietotaji[iz[0]]
        lietotaja_info.config(text=f"{lietotajs[1]} {lietotajs[2]} | ID: {lietotajs[0]} | Klase: {lietotajs[4] or '-'}")
        logs.destroy(); root.deiconify()
        if not ir_admin():
            for poga in admin_pogas: poga.pack_forget()
    p=tk.Button(logs,text="Izvēlēties",command=izvelets); pogas_dizains(p); p.pack(pady=10)


root=tk.Tk()
root.title("Pazudušās mantas")
root.geometry("400x450")
root.configure(bg=FONS)
root.withdraw()

try:
    funkcijas.sagatavot_datubazi()
except Exception as e:
    messagebox.showerror("Datubāzes kļūda",str(e))
    root.destroy()
    raise

virsraksts=tk.Label(root,text="Pazudušās mantas",bg=FONS,fg=TEKSTS,font=("Arial",19,"bold"))
virsraksts.pack(pady=20)

pogas=[
    ("Redzēt mantas",redzet_mantas,False),
    ("Redzēt pieteikumus",redzet_pieteikumus,False),
    ("Izveidot pieteikumu",izveidot_pieteikumu,False),
    ("Pievienot lietotāju",pievienot_lietotaju,True),
    ("Pievienot kategoriju",pievienot_kategoriju,True),
    ("Pievienot mantu",pievienot_mantu,True),
]
admin_pogas=[]
for teksts,komanda,admin_only in pogas:
    p=tk.Button(root,text=teksts,command=komanda,width=25)
    pogas_dizains(p); p.pack(pady=6)
    if admin_only: admin_pogas.append(p)

lietotaja_info=tk.Label(root,bg="#D1D5DB",fg=TEKSTS,font=("Arial",9),padx=5,pady=10)
lietotaja_info.pack(side="bottom",fill="x",pady=10)
izveleties_lietotaju()
root.mainloop()
