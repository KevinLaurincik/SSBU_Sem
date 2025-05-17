import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shiny import App, Inputs, Outputs, Session, reactive, render
from shiny.types import FileInfo

from app_ui import app_ui
from CorrelationAnalysis import analyze_diagnosis_relation
from DiagnosisAnalysis import categorize_diagnosis
from GenotypeAnalysis import analyze_genotypes
from HardyWeinbergTest import hardy_weinberg_test


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def parsed_file():
        file: list[FileInfo] | None = input.file1()
        if not file:
            return pd.DataFrame()
        return pd.read_excel(
            file[0]["datapath"],
            engine="xlrd",
            usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            dtype={0: str, 2: str, 3: str, 4: str, 5: str}
        )

    @reactive.calc
    def clean_data():
        df = parsed_file()
        if df.empty:
            return df

        df.columns = [
            "id", "validovany_datum", "validovany_cas",
            "prijem_datum", "prijem_cas", "pohlavie", "vek",
            "diagnoza_MKCH10", "HFE_H63D", "HFE_S65C", "HFE_C282Y"
        ]

        df["validovany_vysledok"] = pd.to_datetime(
            df["validovany_datum"] + " " + df["validovany_cas"],
            format="%d.%m.%Y %H:%M", errors="coerce"
        )
        df["prijem_vzorky"] = pd.to_datetime(
            df["prijem_datum"] + " " + df["prijem_cas"],
            format="%d.%m.%Y %H:%M", errors="coerce"
        )

        df.drop(columns=["validovany_datum", "validovany_cas", "prijem_datum", "prijem_cas"], inplace=True)
        df["vek"] = df["vek"].astype(str).str.replace(",", ".").astype(float)
        df.dropna(inplace=True)

        # Aktualizácia zastaraných kódov
        df["diagnoza_MKCH10"] = df["diagnoza_MKCH10"].replace({
            "K76.0": "E66.9", "K75.9": "K75.8"
        })

        return df

    @render.text
    def HDT():
        df = clean_data()
        if df.empty:
            return "Žiadne dáta k dispozícii"
        return hardy_weinberg_test(df, input.test())

    @render.text
    def Genotype():
        df = clean_data()
        if df.empty:
            return "Žiadne dáta"
        return analyze_genotypes(df)

    @render.text
    def Zavislost():
        df = clean_data()
        if df.empty:
            return "Žiadne dáta"
        return analyze_diagnosis_relation(df)

    @render.plot
    def vCase():
        df = clean_data()
        if df.empty:
            return None
        df["rok_vysetrenia"] = df["validovany_vysledok"].dt.year
        df["diagnoza_skupina"] = df["diagnoza_MKCH10"].apply(categorize_diagnosis)
        diagnosis_time = df.groupby(["rok_vysetrenia", "diagnoza_skupina"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 6))
        diagnosis_time.plot(kind="line", marker='o', ax=ax)
        ax.set_title("Vývoj typov diagnóz podľa rokov")
        ax.set_xlabel("Rok")
        ax.set_ylabel("Počet prípadov")
        ax.legend(title="Skupina diagnóz")
        plt.tight_layout()
        return fig

    @render.text
    def Kategorizacia():
        df = clean_data()
        if df.empty:
            return "Žiadne dáta"

        def classify_patient(row):
            c282y = row["HFE_C282Y"].lower()
            h63d = row["HFE_H63D"].lower()
            s65c = row["HFE_S65C"].lower()
            if c282y == "mutant" or \
               (c282y == "heterozygot" and h63d == "heterozygot") or \
               (c282y == "heterozygot" and s65c == "heterozygot") or \
               (h63d == "heterozygot" and s65c == "heterozygot"):
                return "predispozícia"
            elif c282y == "heterozygot" or h63d == "heterozygot" or s65c == "heterozygot":
                return "prenášač"
            elif c282y == "normal" and h63d == "normal" and s65c == "normal":
                return "zdravý"
            else:
                return "nezaradený"

        df["stav"] = df.apply(classify_patient, axis=1)
        counts = df["stav"].value_counts()
        total = len(df)
        return "\n".join([f"{cat.capitalize()}: {cnt} ({100*cnt/total:.2f}%)" for cat, cnt in counts.items()])

    @render.plot
    def genotype_plot():
        df = clean_data()
        if df.empty:
            return None
        gene = input.gene_plot()
        plot_type = input.plot_type()

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.set(style="whitegrid")

        if plot_type == "Boxplot (vek)":
            sns.boxplot(data=df, x=gene, y="vek", order=["normal", "heterozygot", "mutant"], ax=ax)
            ax.set_title(f"Vek podľa genotypu {gene}")
        elif plot_type == "Rozdelenie podľa pohlavia":
            sns.countplot(data=df, x=gene, hue="pohlavie", order=["normal", "heterozygot", "mutant"], ax=ax)
            ax.set_title(f"Pohlavie podľa genotypu {gene}")
            ax.legend(title="Pohlavie")

        plt.tight_layout()
        return fig

    @render.table
    def summary():
        df = clean_data()
        return df if input.show_data() else pd.DataFrame()


app = App(app_ui, server)
