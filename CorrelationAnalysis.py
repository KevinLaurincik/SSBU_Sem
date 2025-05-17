import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency


def analyze_diagnosis_relation(df):
    # Prepare liver disease column
    df["pecenove_ochorenie"] = df["diagnoza_MKCH10"].str.upper().isin(["K76.0", "K75.9"])

    # Check if we have both cases and controls
    if df["pecenove_ochorenie"].nunique() < 2:
        plt.figure(figsize=(8, 4))
        plt.text(0.5, 0.5, "Nedostatok dát\n(chýbajú pacienti s alebo bez pečeňového ochorenia)",
                 ha='center', va='center', fontsize=12)
        plt.axis('off')
        plt.tight_layout()
        return [plt.gcf()]

    results = []

    for gene in ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]:
        # Prepare mutation status (True = has mutation)
        df["mutacia"] = df[gene].str.lower().isin(["heterozygot", "mutant"])

        # Create contingency table
        contingency = pd.crosstab(df["mutacia"], df["pecenove_ochorenie"])

        # Add column names if missing (can happen with all True/False)
        if contingency.shape[1] < 2:
            for val in [False, True]:
                if val not in contingency.columns:
                    contingency[val] = 0
            contingency = contingency[[False, True]]  # Ensure correct order

        # Calculate percentages for visualization
        total_counts = contingency.sum(axis=1)
        percent_with_disease = (contingency[True] / total_counts * 100).round(1)

        # Prepare data for plotting
        plot_data = pd.DataFrame({
            'Mutácia': ['Bez mutácie', 'S mutáciou'],
            'Percento s ochorením': percent_with_disease.values,
            'Celkový počet': total_counts.values
        })

        # Create visualization
        plt.figure(figsize=(8, 5))

        # Bar plot
        bars = plt.bar(plot_data['Mutácia'], plot_data['Percento s ochorením'],
                       color=['#4c72b0', '#c44e52'])

        # Add percentages on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height}%',
                     ha='center', va='bottom')

        # Add sample sizes below x-axis
        for i, count in enumerate(plot_data['Celkový počet']):
            plt.text(i, -5, f'n={count}', ha='center', va='top')

        plt.title(f"Výskyt pečeňových ochorení podľa prítomnosti {gene} mutácie")
        plt.ylabel("Percento pacientov s ochorením pečene (%)")
        plt.ylim(0, min(100, max(plot_data['Percento s ochorením']) * 1.3))

        # Statistical test info
        if contingency.shape == (2, 2):
            chi2, p, dof, expected = chi2_contingency(contingency)
            test_result = f"Chi² = {chi2:.2f}, p = {p:.4f}"
            if p < 0.05:
                test_result += " (významná súvislosť)"
            else:
                test_result += " (žiadna významná súvislosť)"
        else:
            test_result = "⚠️ Nedostatok dát pre štatistický test"

        plt.text(0.5, 0.95, test_result,
                 transform=plt.gca().transAxes,
                 ha='center', va='top',
                 bbox=dict(facecolor='white', alpha=0.8))

        plt.tight_layout()
        results.append(plt.gcf())

    return results