from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import re

def genera_pdf(
    nome_cliente,
    totale_attuale,
    totale_tim,
    risparmio,
    dettagli
):

    
    #PULIZIA NOME FILE
    nome_cliente_pulito = re.sub(
        r'[^A-Za-z0-9À-ÿ ]',
        '',
        nome_cliente
    )
    nome_cliente_pulito = nome_cliente_pulito.strip()

    nome_file = f"Preventivo_{nome_cliente_pulito}.pdf"

    c = canvas.Canvas(nome_file, pagesize=A4)

    width, height = A4

    # =========================
    # TITOLO
    # =========================

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 50, "TIM Energia")

    c.setFont("Helvetica", 16)
    c.drawString(50, height - 90, "Analisi Risparmio Cliente")

    # =========================
    # DATA
    # =========================

    data = datetime.now().strftime("%d/%m/%Y")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 120, f"Data: {data}")

    # =========================
    # CLIENTE
    # =========================

    c.drawString(50, height - 150, f"Cliente: {nome_cliente}")

    # =========================
    # TABELLA
    # =========================

    data_table = [
        ["Voce", "Costo"],
        ["Spesa Attuale", f"€ {totale_attuale:.2f}"],
        ["TIM Energia", f"€ {totale_tim:.2f}"],
        ["Risparmio Annuo", f"€ {risparmio:.2f}"],
    ]

    table = Table(data_table, colWidths=[250, 150])

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ])

    table.setStyle(style)

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 320)

    # =========================
    # RISPARMIO EVIDENZIATO
    # =========================

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.green)

    c.drawString(
        50,
        height - 380,
        f"Risparmio stimato: € {risparmio:.2f} / anno"
    )



    c.setFont("Helvetica", 11)

    altezza_dettagli = height - 450

    for dettaglio in dettagli:

        for linea in dettaglio.split("\n"):

            c.drawString(50, altezza_dettagli, linea)
            altezza_dettagli -= 18

        altezza_dettagli -= 10


    # =========================
    # FOOTER
    # =========================

    c.setFillColor(colors.black)

    c.setFont("Helvetica", 10)

    c.drawString(
        50,
        50,
        "Preventivo generato automaticamente con TIM Energia Calculator"
    )

    c.save()

    return nome_file