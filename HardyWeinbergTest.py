from scipy.stats import chisquare


def hardy_weinberg_test(df, column):
    # Prevod všetkých na malé písmená pre istotu
    genotypes = df[column].str.lower()

    # Spočítanie výskytov
    count_nn = (genotypes == "normal").sum()
    count_nm = (genotypes == "heterozygot").sum()
    count_mm = (genotypes == "mutant").sum()  # ak vôbec existuje

    n = count_nn + count_nm + count_mm
    if n == 0:
        print(f"Žiadne záznamy pre {column}")
        return

    # Vypočítaj frekvencie alelov
    p = (2 * count_nn + count_nm) / (2 * n)
    q = 1 - p

    # Očakávané počty podľa HWE
    expected_nn = p ** 2 * n
    expected_nm = 2 * p * q * n
    expected_mm = q ** 2 * n

    # Chi-kvadrát test
    observed = [count_nn, count_nm, count_mm]
    expected = [expected_nn, expected_nm, expected_mm]

    chi2, pval = chisquare(f_obs=observed, f_exp=expected)

    print(f"\n🧬 Hardy-Weinberg test pre {column}:")
    print(f"Pozorované:  normal={count_nn}, heterozygot={count_nm}, homozygot={count_mm}")
    print(f"Očakávané:  normal={expected_nn:.2f}, heterozygot={expected_nm:.2f}, homozygot={expected_mm:.2f}")
    print(f"Chi² = {chi2:.4f}, p-hodnota = {pval:.4f}")

    if pval < 0.05:
        print("❌ Genotypy NIE sú v Hardy-Weinbergovej rovnováhe (p < 0.05)")
    else:
        print("✅ Genotypy sú v Hardy-Weinbergovej rovnováhe (p ≥ 0.05)")

