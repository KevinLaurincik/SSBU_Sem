import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

def analyze_diagnosis_relation(df):
    # Prepare liver disease column
    df["PO"] = df["diagnoza_MKCH10"].str.upper().isin(["K76.0", "K75.9"])

    # Check if we have both cases and controls
    if df["PO"].nunique() < 2:
        plt.figure(figsize=(8, 4))
        plt.text(0.5, 0.5, "Nedostatok dát\n(chýbajú pacienti s alebo bez pečeňového ochorenia)",
                 ha='center', va='center', fontsize=12)
        plt.axis('off')
        plt.tight_layout()
        return [plt.gcf()]

    # Convert categorical variables to numerical codes for correlation analysis
    df_encoded = df[["HFE_C282Y", "HFE_H63D", "HFE_S65C", "PO"]].apply(lambda x: x.astype('category').cat.codes)

    # Compute correlation matrix
    corr_matrix = df_encoded.corr()

    # Create correlation matrix plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Korelačná matica mutácií a pečeňového ochorenia")
    plt.tight_layout()

    return [plt.gcf()]