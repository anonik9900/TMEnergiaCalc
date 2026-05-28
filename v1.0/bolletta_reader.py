import pdfplumber
import re


def pulisci_numero(valore):

    valore = valore.replace(".", "")
    valore = valore.replace(",", ".")

    return valore


def leggi_bolletta(percorso_pdf):

    testo_completo = ""

    with pdfplumber.open(percorso_pdf) as pdf:

        for pagina in pdf.pages:

            testo = pagina.extract_text()

            if testo:
                testo_completo += testo + "\n"

    print("\n========== TESTO PDF ==========\n")
    print(testo_completo)
    print("\n===============================\n")

    risultati = {
        "kwh": "",
        "smc": "",
        "prezzo_smc": "",
        "cliente": "",
        "prezzo_kwh": "",
        "kwh_annuo": "",
    }

    # =========================
    # NOME CLIENTE
    # =========================

    match_cliente = re.search(
        r"Ciao\s+([A-Z\s]+),",
        testo_completo
    )

    if match_cliente:
        risultati["cliente"] = match_cliente.group(1).strip()




    # =========================
    # CONSUMO MEDIO MENSILE
    # =========================

    match_media = re.search(
        r"Consumo medio mensile.*?(\d+)\s*kWh",
        testo_completo,
        re.IGNORECASE | re.DOTALL
    )
    
    if match_media:

        consumo_medio = int(match_media.group(1))

        consumo_annuo = consumo_medio * 12

        risultati["kwh_annuo"] = str(consumo_annuo)


    # =========================
    # CONSUMO LUCE
    # =========================

    match_kwh = re.search(
        r"Consumo del periodo\s+(\d+)\s+kWh",
        testo_completo,
        re.IGNORECASE
    )

    if match_kwh:

        risultati["kwh"] = match_kwh.group(1)


    # =========================
    # PREZZO MEDIO €/KWH
    # =========================

    match_prezzo_kwh = re.search(
        r"Quota consumi\s+\d+\s*kWh\s+([0-9]+,[0-9]+)\s*€/kWh",
        testo_completo,
        re.IGNORECASE
    )

    if match_prezzo_kwh:

        risultati["prezzo_kwh"] = str(
            round(
                float(
                    match_prezzo_kwh.group(1).replace(",", ".")
                ),
                3
            )
        )

    # =========================
    # CONSUMO ANNUO SMC
    # =========================

    pattern_annuo_smc = [
        r"In un anno hai consumato\s+(\d+[.,]?\d*)\s*Smc",
        r"Consumo annuo\s+(\d+[.,]?\d*)\s*Smc",
    ]

    for pattern in pattern_annuo_smc:

        match = re.search(pattern, testo_completo, re.IGNORECASE)

        if match:

            risultati["smc"] = pulisci_numero(
                match.group(1)
            )

            break

    # =========================
    # FALLBACK SMC
    # =========================

    if risultati["smc"] == "":

        match_smc = re.search(
            r"(\d+[.,]?\d*)\s*Smc",
            testo_completo,
            re.IGNORECASE
        )

        if match_smc:

            risultati["smc"] = pulisci_numero(
                match_smc.group(1)
            )

    # =========================
    # PREZZO MEDIO €/SMC
    # =========================


    

    match_prezzo = re.search(
        r"QUOTA PER CONSUMI\s+\d+\s+Smc\s+([0-9]+,[0-9]+)",
        testo_completo,
        re.IGNORECASE | re.DOTALL
    )

    if match_prezzo:

        risultati["prezzo_smc"] = str(
            round(float(match_prezzo.group(1).replace(",", ".")), 3)
        )

    

    

    print("\n========== RISULTATI ==========")
    print(risultati)
    print("================================\n")

    return risultati