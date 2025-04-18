import matplotlib.pyplot as plt
import seaborn as sns

def plot_genotype_distributions(df):
    print("\n--- Vizuálna analýza genotypov ---")

    sns.set(style="whitegrid")

    # 1. Rozdelenie genotypov pre každú mutáciu
    genes = ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]
    for gene in genes:
        plt.figure(figsize=(6, 4))
        sns.countplot(data=df, x=gene, order=["normal", "heterozygot", "mutant"])
        plt.title(f"Rozdelenie genotypov pre {gene}")
        plt.ylabel("Počet pacientov")
        plt.xlabel("Genotyp")
        plt.tight_layout()
        plt.show()

    # 2. Vek vs. genotyp (napr. pre C282Y)
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x="HFE_C282Y", y="vek", order=["normal", "heterozygot", "mutant"])
    plt.title("Vek podľa genotypu HFE_C282Y")
    plt.xlabel("Genotyp")
    plt.ylabel("Vek")
    plt.tight_layout()
    plt.show()

    # 3. Pohlavie vs. genotyp (napr. pre H63D)
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="HFE_H63D", hue="pohlavie", order=["normal", "heterozygot", "mutant"])
    plt.title("Pohlavie podľa genotypu HFE_H63D")
    plt.xlabel("Genotyp")
    plt.ylabel("Počet")
    plt.legend(title="Pohlavie")
    plt.tight_layout()
    plt.show()

    # 4. Diagnóza vs. genotyp (napr. len pacienti s pečeňovým ochorením)
    df["pecen"] = df["diagnoza_MKCH10"].str.upper().isin(["K75.9", "K76.0"])
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df[df["pecen"] == True], x="HFE_C282Y", order=["normal", "heterozygot", "mutant"])
    plt.title("Genotyp C282Y u pacientov s pečeňovým ochorením")
    plt.xlabel("Genotyp")
    plt.ylabel("Počet pacientov")
    plt.tight_layout()
    plt.show()
