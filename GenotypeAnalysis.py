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

    # --- Prenášači a predisponovaní ---
    print("\n--- Prenášači a predisponovaní pacienti ---")

    prenasaci = df[
        (df["HFE_C282Y"].str.lower() == "heterozygot") |
        (df["HFE_H63D"].str.lower() == "heterozygot") |
        (df["HFE_S65C"].str.lower() == "heterozygot")
    ]

    predisponovani = df[
        (df["HFE_C282Y"].str.lower() == "homozygot") |
        ((df["HFE_C282Y"].str.lower() == "heterozygot") & (df["HFE_H63D"].str.lower() == "heterozygot")) |
        ((df["HFE_C282Y"].str.lower() == "heterozygot") & (df["HFE_S65C"].str.lower() == "heterozygot"))
    ]

    print(f"\n👥 Počet prenášačov: {len(prenasaci)}")
    print(f"👥 Počet predisponovaných pacientov na HH: {len(predisponovani)}")
