from openpyxl.worksheet.datavalidation import DataValidation


def create_filter(ws_visualisations, dataset, column_ref, title, cell_ref_title, cell_ref_filter):
    """ Construction d'une méthode de filtre dynamique """
    # Récupérer les valeurs uniques d'une colonne
    distinct_value_list = ",".join(dataset[column_ref].dropna().astype(str).unique())
    
    ws_visualisations[cell_ref_title] = title
    ws_visualisations[cell_ref_filter] = dataset[column_ref].iloc[0]

    # Création du filtre
    dv = DataValidation(type="list", formula1=f'"{distinct_value_list}"', allow_blank=True)

    ws_visualisations.add_data_validation(dv)
    dv.add(ws_visualisations[cell_ref_filter])


def build_all_filters(ws_visualisations, dataset):
    """ Crée les 2 filtres fonctionnels : Region et State """
    create_filter(ws_visualisations, dataset, "Region", "Choisir une région :", "A5", "B5")
    create_filter(ws_visualisations, dataset, "State", "Choisir un État :", "A11", "B11")
