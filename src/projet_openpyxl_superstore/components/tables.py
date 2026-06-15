from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.styles import Alignment


def create_sub_categories_table(ws_data, len_sous_cat):
    formula = "=_xlfn.UNIQUE(DATA!P:P)"
    ws_data['Z2'] = ArrayFormula(f"Z2:Z{len_sous_cat+1}", formula)

    # Références modifiées : $B$5 et $B$11
    for num_cell in range(3, len_sous_cat+2):
        cell = "AA" + str(num_cell)
        ws_data[cell] = f"=SUMIFS(DATA!U:U,DATA!P:P,DATA!Z{num_cell},DATA!M:M,VISUALISATIONS!$B$5, DATA!K:K, VISUALISATIONS!$B$11)"

    formula_sort = "=_xlfn.SORT(DATA!Z3:AA19,2,-1)"
    ws_data['AC3'] = ArrayFormula("AC3:AD19", formula_sort)


def create_categories_table(ws_data, len_cat):
    formula = "=_xlfn.UNIQUE(DATA!O:O)"
    ws_data['Z25'] = ArrayFormula(f"Z25:Z{len_cat+24}", formula)

    for row_cell in range(26, 29):
        ws_data[f"AA{row_cell}"] = f"=SUMIFS(DATA!R:R, DATA!O:O, DATA!Z{row_cell}, DATA!M:M, VISUALISATIONS!$B$5, DATA!K:K, VISUALISATIONS!$B$11)"

    ws_data["AA29"] = "=SUM(AA26:AA28)"
    for row_cell in range(26, 29):
        ws_data[f"AB{row_cell}"] = f"=AA{row_cell} / AA29"
        ws_data[f"AB{row_cell}"].number_format = '0.00%'


def create_abc_method_table(ws_data, len_products):
    formula = "=_xlfn.UNIQUE(DATA!Q:Q)"
    ws_data['Z33'] = ArrayFormula(f"Z33:Z{len_products+1}", formula)

    for num_cell in range(34, len_products+36):
        ws_data[f"Y{num_cell}"] = f"=SUMIFS(DATA!R:R,DATA!Q:Q,DATA!Z{num_cell},DATA!M:M,VISUALISATIONS!$B$5, DATA!K:K, VISUALISATIONS!$B$11)"

    ws_data["Y33"] = f"=SUM(DATA!Y34:Y{len_products+1})"

    for num_cell in range(34, len_products+36):
        ws_data[f"X{num_cell}"] = f"=Y{num_cell}/$Y$33"

    formula_sort = f"=_xlfn.SORT(DATA!X34:Z{len_products+36},1,-1)"
    ws_data[f"Y{len_products+40}"] = ArrayFormula(f"Y{len_products+40}:AA{len_products*2+37}", formula_sort)

    start_cell = len_products + 40
    end_cell = len_products * 2 + 40

    ws_data[f"X{start_cell}"] = f"=Y{start_cell}"
    ws_data[f"W{start_cell}"] = f'=IF(X{start_cell} <= 0.8, "A", IF(X{start_cell} <= 0.95, "B", "C"))'

    for num_cell in range(start_cell + 1, end_cell + 1):
        ws_data[f"X{num_cell}"] = f"=Y{num_cell} + X{num_cell-1}"
        ws_data[f"W{num_cell}"] = f'=IF(X{num_cell} <= 0.8, "A", IF(X{num_cell} <= 0.95, "B", "C"))'

    return start_cell, end_cell


def render_abc_filters(ws_visualisations, start_cell, end_cell, len_products):
    row_fin = 7 + len_products 

    formula_a = f'=_xlfn.FILTER(DATA!AA{start_cell}:AA{end_cell}, DATA!W{start_cell}:W{end_cell}="A", "Aucun")'
    formula_b = f'=_xlfn.FILTER(DATA!AA{start_cell}:AA{end_cell}, DATA!W{start_cell}:W{end_cell}="B", "Aucun")'
    formula_c = f'=_xlfn.FILTER(DATA!AA{start_cell}:AA{end_cell}, DATA!W{start_cell}:W{end_cell}="C", "Aucun")'

    # Affichage sur les colonnes K, N et P
    ws_visualisations["K7"] = ArrayFormula(f"K7:K{row_fin}", formula_a)
    ws_visualisations["N7"] = ArrayFormula(f"N7:N{row_fin}", formula_b)
    ws_visualisations["P7"] = ArrayFormula(f"P7:P{row_fin}", formula_c)

    alignement_propre = Alignment(wrap_text=True, vertical='top')
    for col_lettre in ['K', 'N', 'P']:
        ws_visualisations.column_dimensions[col_lettre].width = 45
        for row in range(7, row_fin + 1):
            ws_visualisations[f"{col_lettre}{row}"].alignment = alignement_propre


def build_all_tables(ws_data, ws_visualisations, dataset):
    len_sous_cat = len(dataset["Sub-Category"].unique()) + 1
    len_cat = len(dataset["Category"].unique()) + 1
    len_products = len(dataset["Product Name"].unique()) + 1

    create_sub_categories_table(ws_data, len_sous_cat)
    create_categories_table(ws_data, len_cat)
    start_cell, end_cell = create_abc_method_table(ws_data, len_products)
    render_abc_filters(ws_visualisations, start_cell, end_cell, len_products)