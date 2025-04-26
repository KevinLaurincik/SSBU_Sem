import pandas as pd
import matplotlib.pyplot as plt
import app_ui as shiny_app

from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shiny.types import FileInfo

from CorrelationAnalysis import analyze_diagnosis_relation
from DiagnosisAnalysis import categorize_diagnosis
from GenotypeAnalysis import analyze_genotypes
from HardyWeinbergTest import hardy_weinberg_test

def server(input: Inputs, output: Outputs, session: Session):
    DataFrame = pd.DataFrame()

    @reactive.calc
    def parsed_file():
        file: list[FileInfo] | None = input.file1()
        if file is None:
            return pd.DataFrame()
        return pd.read_excel(
            file[0]["datapath"],
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

    @reactive.calc
    def clean_data():
        df = parsed_file()

        if df.empty:
            return pd.DataFrame()

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

        df.drop(columns=["validovany_datum", "validovany_cas", "prijem_datum", "prijem_cas"], inplace=True)
        df["vek"] = df["vek"].astype(str).str.replace(",", ".").astype(float)
        df.dropna(inplace=True)

        print(DataFrame)
        return df

    @render.text
    @reactive.calc
    def HDT():
        df = clean_data()
        #print(str(input.test()))
        if df.empty:
            return "žiadne data k dispozicii"

        result = hardy_weinberg_test(df, str(input.test()))
        #print(result)
        return result

    @render.text
    @reactive.calc
    def Genotype():
        df = clean_data()

        if df.empty:
            return "žiadne data k dispozicii"

        result = analyze_genotypes(df)
        return result

    @render.text
    @reactive.calc
    def Zavislost():
        df = clean_data()

        if df.empty:
            return "žiadne data k dispozicii"


        return analyze_diagnosis_relation(df)

    @render.plot
    def vCase():
        df = clean_data()

        if df.empty:
            return None

        # Získame rok z dátumu vyšetrenia
        df["rok_vysetrenia"] = pd.to_datetime(df["validovany_vysledok"]).dt.year

        # Zoskupíme diagnózy do kategórií
        df["diagnoza_skupina"] = df["diagnoza_MKCH10"].apply(categorize_diagnosis)

        # Diagnózy podľa rokov a skupín
        diagnosis_time = df.groupby(["rok_vysetrenia", "diagnoza_skupina"]).size().unstack(fill_value=0)

        # Vytvorenie grafu priamo
        fig, ax = plt.subplots(figsize=(10, 6))
        diagnosis_time.plot(kind="line", marker='o', ax=ax)
        ax.set_title("Vývoj typov diagnóz podľa rokov")
        ax.set_xlabel("Rok")
        ax.set_ylabel("Počet prípadov")
        ax.legend(title="Skupina diagnóz")
        plt.tight_layout()

        return fig

        # # Voliteľne: výpis unikátnych diagnóz pre kontrolu
        # print("\n📋 Unikátne diagnózy v dataset:")
        # print(sorted(df["diagnoza_MKCH10"].dropna().unique()))
        #
        # np.random.seed(19680801)
        # x_rand = 100 + 15 * np.random.randn(437)
        # fig, ax = plt.subplots()
        # ax.hist(x_rand, 50, density=True)
        # return fig

    @render.table
    def summary():
        df = clean_data()

        if df.empty:
            return pd.DataFrame()

        if input.show_data():
            return df
        else:
            return pd.DataFrame()

app = App(shiny_app.app_ui, server)