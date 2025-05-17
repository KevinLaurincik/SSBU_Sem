from scipy.stats import chi2_contingency
import pandas as pd
import matplotlib.pyplot as plt

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

        # --- Graf ---
        # Pre lepšie čítanie vytvoríme % pacientov s ochorením a bez ochorenia pre obidve skupiny (mutácia áno/nie)
        counts = contingency.values
        # Kontingenčná tabuľka má riadky: mutácia = False/True, stĺpce: ochorenie = False/True
        groups = ["Bez mutácie", "S mutáciou"]
        labels = ["Bez pečeňového ochorenia", "S pečeňovým ochorením"]

        # Percentá v rámci každej skupiny (riadku)
        percents = counts / counts.sum(axis=1, keepdims=True) * 100

        plt.figure(figsize=(6,4))
        bar1 = plt.bar(groups, percents[:, 0], label=labels[0], color="#4c72b0")
        bar2 = plt.bar(groups, percents[:, 1], bottom=percents[:, 0], label=labels[1], color="#c44e52")

        plt.ylabel("Percento (%)")
        plt.title(f"Vzťah medzi {gene} mutáciou a pečeňovým ochorením")
        plt.ylim(0, 100)
        plt.legend()

        # Pridanie hodnôt nad stĺpcami
        for i in range(len(groups)):
            plt.text(i, percents[i,0]/2, f"{percents[i,0]:.1f}%", ha='center', va='center', color='white', fontsize=10)
            plt.text(i, percents[i,0] + percents[i,1]/2, f"{percents[i,1]:.1f}%", ha='center', va='center', color='white', fontsize=10)

        plt.tight_layout()
        plt.show()
