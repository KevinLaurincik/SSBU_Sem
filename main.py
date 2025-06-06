import pandas as pd

from CorrelationAnalysis import analyze_diagnosis_relation
from HardyWeinbergTest import hardy_weinberg_test



def main():
    # 1. Načítanie súboru, vynechanie druhého stĺpca (index 1)
    df = pd.read_excel(
        "SSBU25_dataset.xls",
        engine="xlrd",
        usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        dtype={
            0: str,
            2: str,
            3: str,
            4: str,
            5: str
        }
    )

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.expand_frame_repr', False)

    # 2. Nastavenie názvov stĺpcov podľa obrázka
    df.columns = [
        "id",
        "validovany_datum", "validovany_cas",
        "prijem_datum", "prijem_cas",
        "pohlavie",
        "vek",
        "diagnoza_MKCH10",
        "HFE_H63D",
        "HFE_S65C",
        "HFE_C282Y"
    ]

    # 3. Spojenie dátumu a času do jedného stĺpca a konverzia na datetime
    df["validovany_vysledok"] = pd.to_datetime(
        df["validovany_datum"].astype(str) + " " + df["validovany_cas"].astype(str),
        format="%d.%m.%Y %H:%M",
        errors="coerce"
    )

    df["prijem_vzorky"] = pd.to_datetime(
        df["prijem_datum"].astype(str) + " " + df["prijem_cas"].astype(str),
        format="%d.%m.%Y %H:%M",
        errors="coerce"
    )

    # 4. Vymazanie pôvodných stĺpcov (už ich nepotrebujeme)
    df.drop(columns=["validovany_datum", "validovany_cas", "prijem_datum", "prijem_cas"], inplace=True)

    # 5. Úprava veku (zmena čiarky na bodku a konverzia na float)
    df["vek"] = df["vek"].astype(str).str.replace(",", ".").astype(float)

    # 6. Očistenie dát – ak je niečo NaN v hociktorom stĺpci, celý riadok sa vyhodí
    df.dropna(inplace=True)

    # 7. Spustenie všetkých analýz
    hardy_weinberg_test(df, "HFE_C282Y")
    hardy_weinberg_test(df, "HFE_H63D")
    hardy_weinberg_test(df, "HFE_S65C")

    ##analyze_genotypes(df)
    analyze_diagnosis_relation(df)
    ##plot_genotype_distributions(df)
    ##analyzuj_diagnozy_a_vyvoj_v_case(df)


if __name__ == "__main__":
    main()
