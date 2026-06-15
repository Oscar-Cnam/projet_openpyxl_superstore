from pathlib import Path
from src.projet_openpyxl_superstore.data.data import import_and_clean_data, initialize_workbook, upload_to_minio
from src.projet_openpyxl_superstore.components.styles import apply_all_styles
from src.projet_openpyxl_superstore.components.tables import build_all_tables
from src.projet_openpyxl_superstore.components.indicators import build_indicators
from src.projet_openpyxl_superstore.components.charts import build_all_charts
from src.projet_openpyxl_superstore.components.filter import build_all_filters

# *** Identifiants du bucket Onyxia d'export ***
# A modifier en fonction de l'utilisateur
bucket_name = "oscar04"
minio_path = "Superstore/reporting.xlsx"


def main():
    output_path = Path("output/reporting.xlsx")

    dataset = import_and_clean_data()
    print("Importation et nettoyage des données ✅")

    wb, ws_data, ws_visualisations = initialize_workbook(dataset, output_path)
    print("Initialisation du fichier Excel ✅")

    apply_all_styles(ws_visualisations)
    print("Application du design ✅")

    build_all_filters(ws_visualisations, dataset)
    print("Paramétrage des filtres ✅")

    build_all_tables(ws_data, ws_visualisations, dataset)
    print("Création des tables de calcul ✅")

    build_indicators(ws_data, ws_visualisations, len(dataset))
    print("Calcul des indicateurs ✅")

    build_all_charts(ws_data, ws_visualisations)
    print("Génération des graphiques ✅")

    wb.save(output_path)
    print("Sauvegarde finale ✅")
    print(f"Terminé ! Fichier disponible à l'emplacement : {output_path}")

    upload_to_minio(output_path, bucket_name, minio_path)
    print("Export sur MinIO ✅")


if __name__ == "__main__":
    main()
