from scipy.stats import chi2_contingency
import pandas as pd

def analyze_diagnosis_relation(df):
    print("\n--- Súvislosť HFE mutácií s chorobami pečene (K76.0, K75.9) ---")

    # Vytvor nový stĺpec: má ochorenie pečene (True/False)
    df["pecenove_ochorenie"] = df["diagnoza_MKCH10"].str.upper().isin(["K76.0", "K75.9"])

    for gene in ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]:
        print(f"\n🧬 Vzťah medzi {gene} a pečeňovými diagnózami:")

        # Vytvoríme binárne skupiny: má mutáciu alebo nie
        df["mutacia"] = df[gene].str.lower().isin(["heterozygot", "mutant"])

        # Kontingenčná tabuľka
        contingency = pd.crosstab(df["mutacia"], df["pecenove_ochorenie"])

        print("\nKontingenčná tabuľka:")
        print(contingency)

        # Chi-squared test
        chi2, p, dof, expected = chi2_contingency(contingency)

        print(f"\nChi² = {chi2:.4f}, p-hodnota = {p:.4f}")
        if p < 0.05:
            print("❗️Existuje štatisticky významná súvislosť (p < 0.05)")
        else:
            print("✅ Žiadna významná súvislosť (p ≥ 0.05)")
