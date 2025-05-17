import matplotlib.pyplot as plt

def analyze_genotypes(df):
    print("\n--- Genotypové zastúpenie ---")

    for gene in ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]:
        genotypes = df[gene].str.lower()
        total = genotypes.count()
        counts = genotypes.value_counts()
        print(f"\n🧬 {gene}:")
        for gtype, count in counts.items():
            percent = 100 * count / total
            print(f"  {gtype}: {count} ({percent:.2f}%)")

        # Graf percentuálneho zastúpenia genotypov pre daný gén
        labels = counts.index.tolist()
        sizes = [100 * c / total for c in counts.values]

        plt.figure(figsize=(6,4))
        bars = plt.bar(labels, sizes, color=['#4c72b0', '#55a868', '#c44e52'][:len(labels)])
        plt.title(f"Percentuálne zastúpenie genotypov - {gene}")
        plt.ylabel("Percento (%)")
        plt.ylim(0, 100)

        # Popisky hodnôt nad stĺpcami
        for bar, size in zip(bars, sizes):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{size:.2f}%', ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

    # --- Zaradenie pacientov ---
    print("\n--- Kategorizácia pacientov ---")

    def classify_patient(row):
        c282y = row["HFE_C282Y"].lower()
        h63d = row["HFE_H63D"].lower()
        s65c = row["HFE_S65C"].lower()

        # Predispozícia – homozygot mutant alebo zložený heterozygot
        if c282y == "mutant" or \
           (c282y == "heterozygot" and h63d == "heterozygot") or \
           (c282y == "heterozygot" and s65c == "heterozygot") or \
           (h63d == "heterozygot" and s65c == "heterozygot"):
            return "predispozícia"

        # Prenášač – aspoň jeden heterozygot (ale nie kombinácia viacerých)
        elif (c282y == "heterozygot" or h63d == "heterozygot" or s65c == "heterozygot"):
            return "prenášač"

        # Zdravý – všetko normal
        elif c282y == "normal" and h63d == "normal" and s65c == "normal":
            return "zdravý"

        # Všetko ostatné (neočakávané kombinácie)
        else:
            return "nezaradený"

    df["stav"] = df.apply(classify_patient, axis=1)

    counts = df["stav"].value_counts()
    total = len(df)

    print("\n👤 Počet pacientov podľa kategórie:")
    for stav in ["zdravý", "prenášač", "predispozícia"]:
        count = counts.get(stav, 0)
        percent = 100 * count / total if total > 0 else 0
        print(f"  {stav.capitalize()}: {count} pacientov ({percent:.2f}%)")

    # Graf rozdelenia pacientov podľa kategórie
    categories = ["zdravý", "prenášač", "predispozícia"]
    cat_counts = [counts.get(cat, 0) for cat in categories]
    cat_percents = [100 * c / total if total > 0 else 0 for c in cat_counts]

    plt.figure(figsize=(6,4))
    bars = plt.bar(categories, cat_percents, color=['#8dd3c7', '#ffffb3', '#fb8072'])
    plt.title("Percentuálne zastúpenie pacientov podľa genetickej kategórie")
    plt.ylabel("Percento (%)")
    plt.ylim(0, 100)

    for bar, percent in zip(bars, cat_percents):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{percent:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
