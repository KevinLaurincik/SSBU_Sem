from scipy.stats import chi2_contingency
import pandas as pd

def analyze_diagnosis_relation(df):
    result_parts = []
    result_parts.append("\n--- Súvislosť HFE mutácií s chorobami pečene (K76.0, K75.9) ---\n")

    # Vytvor nový stĺpec: má ochorenie pečene (True/False)
    df["pecenove_ochorenie"] = df["diagnoza_MKCH10"].str.upper().isin(["K76.0", "K75.9"])

    for gene in ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]:
        result_parts.append(f"\n🧬 Vzťah medzi {gene} a pečeňovými diagnózami:\n")

        # Vytvoríme binárne skupiny: má mutáciu alebo nie
        df["mutacia"] = df[gene].str.lower().isin(["heterozygot", "mutant"])

        # Kontingenčná tabuľka
        contingency = pd.crosstab(df["mutacia"], df["pecenove_ochorenie"])

        result_parts.append("\nKontingenčná tabuľka:\n")
        result_parts.append(str(contingency) + "\n")

        # Chi-squared test
        chi2, p, dof, expected = chi2_contingency(contingency)

        result_parts.append(f"\nChi² = {chi2:.4f}, p-hodnota = {p:.4f}\n")
        if p < 0.05:
            result_parts.append("❗️Existuje štatisticky významná súvislosť (p < 0.05)\n")
        else:
            result_parts.append("✅ Žiadna významná súvislosť (p ≥ 0.05)\n")

    return "".join(result_parts)
