from shiny import ui

app_ui = ui.page_fluid(
    ui.navset_bar(ui.nav_panel("file load",
                               ui.input_file("file1", "Choose Excel File", accept=[".xls", ".xlsx"], multiple=False),
                               ui.input_checkbox("show_data", "Show Data", value=False),
                               ui.output_table("summary")),
                  ui.nav_panel("Hardy-Weinberg test",
                               ui.input_select("test", "mutácia: ", ["HFE_C282Y", "HFE_H63D", "HFE_S65C"], selected=["HFE_C282Y"]),
                               ui.output_text_verbatim("HDT")),
                  ui.nav_panel("Genotypove zastupenie",
                               ui.output_text_verbatim("Genotype")),
                  ui.nav_panel("závislosť medzi mutáciami a diagnózami",
                               ui.output_text_verbatim("Zavislost")),
                  ui.nav_panel("grafy"),
                  ui.nav_panel("vývoj v čase",
                                ui.output_plot("vCase")),
                  title="SSBU semestrálka"),
)