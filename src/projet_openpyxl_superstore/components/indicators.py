from openpyxl.styles import Font, Alignment


def apply_numerical_kpi(ws_visualisations, cell, colonne, cell_format):
    c = ws_visualisations[cell]
    # Modifié pour pointer vers VISUALISATIONS!B5 et B11
    c.value = f"=SUMIFS(DATA!{colonne}:{colonne}, DATA!M:M, VISUALISATIONS!B5, DATA!K:K, VISUALISATIONS!B11)"
    c.number_format = cell_format
    c.font = Font(name="Calibri", size=16, bold=True, color="1F497D")
    c.alignment = Alignment(horizontal="left", vertical="center")

    col_letter = c.column_letter
    current_width = ws_visualisations.column_dimensions[col_letter].width or 10
    needed_width = max(len(cell_format) + 5, 18)
    ws_visualisations.column_dimensions[col_letter].width = max(current_width, needed_width)
    ws_visualisations.row_dimensions[c.row].height = 30


def calculate_delivery_times(ws_data, dataset_length):
    for row_cell in range(2, dataset_length + 2):
        cell_application = f"V{row_cell}"
        date_debut = f"C{row_cell}"
        date_fin = f"D{row_cell}"
        ws_data[cell_application] = f'=IF(OR({date_debut} = "", {date_fin} = ""), "", DATEDIF({date_debut}, {date_fin}, "D"))'


def build_indicators(ws_data, ws_visualisations, dataset_length):
    apply_numerical_kpi(ws_visualisations, "C4", "R", "#,##0.0 $")
    apply_numerical_kpi(ws_visualisations, "E4", "U", "#,##0.0 $")
    apply_numerical_kpi(ws_visualisations, "G4", "S", "#,##0")

    calculate_delivery_times(ws_data, dataset_length)
    
    ws_visualisations["J4"] = "=ROUND(AVERAGEIFS(DATA!V:V, DATA!M:M, VISUALISATIONS!B5, DATA!K:K, VISUALISATIONS!B11),1)"
    c = ws_visualisations["J4"]
    c.font = Font(name="Calibri", size=16, bold=True, color="1F497D")
    c.alignment = Alignment(horizontal="left", vertical="center")
    
    ws_visualisations.row_dimensions[4].height = 30
    ws_visualisations.column_dimensions["J"].width = max(ws_visualisations.column_dimensions["J"].width or 10, 18)