import tkinter as tk
from tkinter import messagebox
from pdf_generator import genera_pdf
from tkinter import filedialog
from bolletta_reader import leggi_bolletta

# =========================
# TARIFFE TIM ENERGIA
# =========================

TIM_LUCE = 0.18
TIM_GAS = 0.65
ultimo_nome = ""
ultimo_totale_attuale = 0
ultimo_totale_tim = 0
ultimo_risparmio = 0


# =========================
# FUNZIONE CALCOLO
# =========================

def calcola_risparmio():

    global ultimo_nome
    global ultimo_totale_attuale
    global ultimo_totale_tim
    global ultimo_risparmio
    global ultimo_dettagli

    try:

        nome = entry_nome.get()

        totale_attuale = 0
        totale_tim = 0

        dettagli = []

        # =========================
        # LUCE
        # =========================

        if calcola_luce.get():

            prezzo_luce_cliente = float(entry_luce_prezzo.get())
            consumo_luce = float(entry_luce_consumo.get())

            spesa_luce_attuale = prezzo_luce_cliente * consumo_luce
            spesa_luce_tim = TIM_LUCE * consumo_luce

            totale_attuale += spesa_luce_attuale
            totale_tim += spesa_luce_tim

            dettagli.append(
                f"LUCE\n"
                f"Attuale: € {spesa_luce_attuale:.2f}\n"
                f"TIM Energia: € {spesa_luce_tim:.2f}\n"
            )

        # =========================
        # GAS
        # =========================

        if calcola_gas.get():

            prezzo_gas_cliente = float(entry_gas_prezzo.get())
            consumo_gas = float(entry_gas_consumo.get())

            spesa_gas_attuale = prezzo_gas_cliente * consumo_gas
            spesa_gas_tim = TIM_GAS * consumo_gas

            totale_attuale += spesa_gas_attuale
            totale_tim += spesa_gas_tim

            dettagli.append(
                f"GAS\n"
                f"Attuale: € {spesa_gas_attuale:.2f}\n"
                f"TIM Energia: € {spesa_gas_tim:.2f}\n"
            )

        # =========================
        # CONTROLLO
        # =========================

        if not calcola_luce.get() and not calcola_gas.get():
            messagebox.showwarning(
                "Attenzione",
                "Seleziona almeno Luce o Gas"
            )
            return

        risparmio = totale_attuale - totale_tim

        ultimo_nome = nome
        ultimo_totale_attuale = totale_attuale
        ultimo_totale_tim = totale_tim
        ultimo_risparmio = risparmio
        ultimo_dettagli = dettagli

        risultato.set(
            f"Cliente: {nome}\n\n"
            + "\n".join(dettagli)
            + f"\n"
            f"Spesa Attuale Totale: € {totale_attuale:.2f}\n"
            f"Spesa TIM Energia: € {totale_tim:.2f}\n\n"
            f"RISPARMIO ANNUO: € {risparmio:.2f}"
        )

    except ValueError:
        messagebox.showerror(
            "Errore",
            "Inserisci valori numerici validi"
        )


def crea_pdf():

    if ultimo_nome == "":
        messagebox.showwarning(
            "Attenzione",
            "Calcola prima il preventivo"
        )
        return

    nome_file = genera_pdf(
        ultimo_nome,
        ultimo_totale_attuale,
        ultimo_totale_tim,
        ultimo_risparmio,
        ultimo_dettagli
    )

    messagebox.showinfo(
        "PDF Creato",
        f"PDF salvato come:\n{nome_file}"
    )




def importa_bolletta():

    percorso_file = filedialog.askopenfilename(
        title="Seleziona Bolletta PDF",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not percorso_file:
        return

    try:

        dati = leggi_bolletta(percorso_file)

        # =========================
        # COMPILA CAMPI
        # =========================

        if dati["cliente"] != "":

            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, dati["cliente"])

        if dati["prezzo_smc"] != "":

            entry_gas_prezzo.delete(0, tk.END)
            entry_gas_prezzo.insert(0, dati["prezzo_smc"])

        if dati["prezzo_kwh"] != "":

            entry_luce_prezzo.delete(0, tk.END)
            entry_luce_prezzo.insert(0, dati["prezzo_kwh"])

        if dati["kwh_annuo"] != "":

            entry_luce_consumo.delete(0, tk.END)
            entry_luce_consumo.insert(0, dati["kwh_annuo"])

        if dati["smc"] != "":

            entry_gas_consumo.delete(0, tk.END)
            entry_gas_consumo.insert(0, dati["smc"])

        messagebox.showinfo(
            "Importazione completata",
            "Dati bolletta caricati correttamente"
        )

    except Exception as errore:

        messagebox.showerror(
            "Errore",
            f"Errore lettura PDF:\\n{errore}"
        )


# =========================
# FINESTRA
# =========================

root = tk.Tk()
root.title("TIM Energia Calculator")
root.geometry("650x750")
root.configure(bg="#f4f6f9")



# =========================
# MODALITÀ CALCOLO
# =========================

calcola_luce = tk.BooleanVar(value=True)
calcola_gas = tk.BooleanVar(value=True)


# =========================
# TITOLO
# =========================

btn_importa = tk.Button(
    root,
    text="IMPORTA BOLLETTA PDF",
    font=("Arial", 12, "bold"),
    bg="#ff9800",
    fg="white",
    padx=20,
    pady=10,
    bd=0,
    command=importa_bolletta
)

btn_importa.pack(pady=10)


titolo = tk.Label(
    root,
    text="TIM Energia - Analisi Risparmio",
    font=("Arial", 24, "bold"),
    bg="#f4f6f9",
    fg="#008f39"
)

titolo.pack(pady=20)



frame_servizi = tk.Frame(root, bg="#f4f6f9")
frame_servizi.pack(pady=10)

check_luce = tk.Checkbutton(
    frame_servizi,
    text="Luce",
    variable=calcola_luce,
    bg="#f4f6f9",
    font=("Arial", 11, "bold")
)

check_luce.pack(side="left", padx=10)

check_gas = tk.Checkbutton(
    frame_servizi,
    text="Gas",
    variable=calcola_gas,
    bg="#f4f6f9",
    font=("Arial", 11, "bold")
)

check_gas.pack(side="left", padx=10)

# =========================
# NOME CLIENTE
# =========================

tk.Label(
    root,
      text="Nome Cliente",
      bg="#f4f6f9",
      font=("Arial", 11, "bold")
    
    ).pack()

entry_nome = tk.Entry(root, width=40)
entry_nome.pack(pady=5)

# =========================
# LUCE
# =========================

tk.Label(
    root,
      text="--- LUCE ---",
      bg="#f4f6f9",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

tk.Label(
    root,
      text="Prezzo attuale €/kWh",
      bg="#f4f6f9",
      font=("Arial", 11)
    ).pack()

entry_luce_prezzo = tk.Entry(root)
entry_luce_prezzo.pack()

tk.Label(
    root,
      text="Consumo annuo kWh",
      bg="#f4f6f9",
      font=("Arial", 11)
    ).pack()

entry_luce_consumo = tk.Entry(root)
entry_luce_consumo.pack()

# =========================
# GAS
# =========================

tk.Label(
    root,
      text="--- GAS ---",
      bg="#f4f6f9",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

tk.Label(
    root,
      text="Prezzo attuale €/Smc",
      bg="#f4f6f9",
      font=("Arial", 11)
    ).pack()

entry_gas_prezzo = tk.Entry(root)
entry_gas_prezzo.pack()

tk.Label(
    root,
      text="Consumo annuo Smc",
      bg="#f4f6f9",
      font=("Arial", 11)
    ).pack()

entry_gas_consumo = tk.Entry(root)
entry_gas_consumo.pack()

# =========================
# BOTTONE
# =========================

btn_calcola = tk.Button(
    root,
    text="CALCOLA RISPARMIO",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=calcola_risparmio
)

btn_calcola.pack(pady=20)

btn_pdf = tk.Button(
    root,
    text="GENERA PDF",
    font=("Arial", 12, "bold"),
    bg="blue",
    fg="white",
    command=crea_pdf
)

btn_pdf.pack(pady=10)

# =========================
# RISULTATO
# =========================

risultato = tk.StringVar()

label_risultato = tk.Label(
    root,
    textvariable=risultato,
    font=("Arial", 12),
    justify="left"
)

label_risultato.pack(pady=20)

# =========================
# AVVIO
# =========================

root.mainloop()