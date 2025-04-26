def analyze_genotypes(df):
    result_parts = []
    result_parts.append("\n--- Genotypové zastúpenie ---\n")

    for gene in ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]:
        genotypes = df[gene].str.lower()
        total = genotypes.count()
        counts = genotypes.value_counts()
        result_parts.append(f"\n🧬 {gene}:\n")
        for gtype, count in counts.items():
            percent = 100 * count / total
            result_parts.append(f"  {gtype}: {count} ({percent:.2f}%)\n")

    # --- Prenášači a predisponovaní ---
    result_parts.append("\n--- Prenášači a predisponovaní pacienti ---\n")

    prenasaci = df[
        (df["HFE_C282Y"].str.lower() == "heterozygot") |
        (df["HFE_H63D"].str.lower() == "heterozygot") |
        (df["HFE_S65C"].str.lower() == "heterozygot")
    ]

    predisponovani = df[
        (df["HFE_C282Y"].str.lower() == "mutant") |
        ((df["HFE_C282Y"].str.lower() == "heterozygot") & (df["HFE_H63D"].str.lower() == "heterozygot")) |
        ((df["HFE_C282Y"].str.lower() == "heterozygot") & (df["HFE_S65C"].str.lower() == "heterozygot"))
    ]

    result_parts.append(f"\n👥 Počet prenášačov: {len(prenasaci)}\n")
    result_parts.append(f"👥 Počet predisponovaných pacientov na HH: {len(predisponovani)}\n")

    return "".join(result_parts)
