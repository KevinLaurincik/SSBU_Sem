from shiny import ui

app_ui = ui.page_fluid(
    ui.navset_bar(
        ui.nav_panel("Načítanie súboru",
                     ui.input_file("file1", "Vyber Excel súbor", accept=[".xls", ".xlsx"], multiple=False),
                     ui.input_checkbox("show_data", "Zobraziť dáta", value=False),
                     ui.output_table("summary")),
        ui.nav_panel("Hardy-Weinbergov test",
                     ui.input_select("test", "Mutácia:", ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]),
                     ui.output_text_verbatim("HDT")),
        ui.nav_panel("Genotypové zastúpenie",
                     ui.input_select("selected_gene", "Vyber gén:", ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]),
                     ui.output_plot("genotype_barplot")),
        ui.nav_panel("Závislosť mutácií a diagnóz",
                     ui.output_plot("diagnosis_relation_plot"),  # Changed to plot output
                     ui.output_text_verbatim("diagnosis_relation_text")),  # Added text output
        ui.nav_panel("Genotypové grafy",
                     ui.input_select("gene_plot", "Vyber gén", ["HFE_C282Y", "HFE_H63D", "HFE_S65C"]),
                     ui.input_select("plot_type", "Typ grafu", ["Boxplot (vek)", "Rozdelenie podľa pohlavia"]),
                     ui.output_plot("genotype_plot")),
        ui.nav_panel("Vývoj diagnóz podľa rokov",
                     ui.output_plot("vCase")),
        ui.nav_panel("Zaradenie pacientov",
                     ui.output_text_verbatim("Kategorizacia")),
        title="SSBU semestrálna práca"
    )
)