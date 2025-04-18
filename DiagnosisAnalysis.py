import pandas as pd
import matplotlib.pyplot as plt

def categorize_diagnosis(code):
    if pd.isna(code):
        return "Neznáme"
    code = code.upper()
    if code.startswith("K7"):
        return "Pečeňové ochorenia"
    elif code.startswith("E"):
        return "Metabolické poruchy"
    elif code.startswith("I"):
        return "Kardiovaskulárne"
    elif code.startswith("C"):
        return "Onkologické"
    elif code.startswith("J"):
        return "Dýchacie ochorenia"
    else:
        return "Iné"

def analyzuj_diagnozy_a_vyvoj_v_case(df):
    # Získame rok z dátumu vyšetrenia
    df["rok_vysetrenia"] = pd.to_datetime(df["validovany_vysledok"]).dt.year

    # Zoskupíme diagnózy do kategórií
    df["diagnoza_skupina"] = df["diagnoza_MKCH10"].apply(categorize_diagnosis)

    # Diagnózy podľa rokov a skupín
    diagnosis_time = df.groupby(["rok_vysetrenia", "diagnoza_skupina"]).size().unstack(fill_value=0)

    print("\n📊 Diagnózy podľa rokov:")
    print(diagnosis_time)

    # Graf vývoja v čase
    diagnosis_time.plot(kind="line", figsize=(10, 6), marker='o')
    plt.title("Vývoj typov diagnóz podľa rokov")
    plt.xlabel("Rok")
    plt.ylabel("Počet prípadov")
    plt.legend(title="Skupina diagnóz")
    plt.tight_layout()
    plt.show()

    # Voliteľne: výpis unikátnych diagnóz pre kontrolu
    print("\n📋 Unikátne diagnózy v dataset:")
    print(sorted(df["diagnoza_MKCH10"].dropna().unique()))
