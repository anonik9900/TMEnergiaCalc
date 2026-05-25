import tkinter as tk
from tkinter import messagebox
from pdf_generator import genera_pdf

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
    try:
        global ultimo_nome
        global ultimo_totale_attuale
        global ultimo_totale_tim
        global ultimo_risparmio
        # DATI CLIENTE
        nome = entry_nome.get()

        prezzo_luce_cliente = float(entry_luce_prezzo.get())
        consumo_luce = float(entry_luce_consumo.get())

        prezzo_gas_cliente = float(entry_gas_prezzo.get())
        consumo_gas = float(entry_gas_consumo.get())

        # SPESA ATTUALE
        spesa_luce_attuale = prezzo_luce_cliente * consumo_luce
        spesa_gas_attuale = prezzo_gas_cliente * consumo_gas

        totale_attuale = spesa_luce_attuale + spesa_gas_attuale

        # SPESA TIM
        spesa_luce_tim = TIM_LUCE * consumo_luce
        spesa_gas_tim = TIM_GAS * consumo_gas

        totale_tim = spesa_luce_tim + spesa_gas_tim

        # RISPARMIO
        risparmio = totale_attuale - totale_tim

        ultimo_nome = nome
        ultimo_totale_attuale = totale_attuale
        ultimo_totale_tim = totale_tim
        ultimo_risparmio = risparmio

        risultato.set(
            f"Cliente: {nome}\n\n"
            f"Spesa attuale: € {totale_attuale:.2f}\n"
            f"Spesa TIM Energia: € {totale_tim:.2f}\n\n"
            f"Risparmio annuo: € {risparmio:.2f}"
        )

    except ValueError:
        messagebox.showerror("Errore", "Inserisci valori validi")


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
        ultimo_risparmio
    )

    messagebox.showinfo(
        "PDF Creato",
        f"PDF salvato come:\n{nome_file}"
    )

# =========================
# FINESTRA
# =========================

root = tk.Tk()
root.title("TIM Energia Calculator")
root.geometry("650x750")
root.configure(bg="#f4f6f9")

# =========================
# TITOLO
# =========================

titolo = tk.Label(
    root,
    text="TIM Energia - Analisi Risparmio",
    font=("Arial", 24, "bold"),
    bg="#f4f6f9",
    fg="#008f39"
)

titolo.pack(pady=20)

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