# import os
from pathlib import Path

# La modification se trouve ici : on importe depuis le dossier data, fichier data
from data.data import import_and_clean_data, initialize_workbook, upload_to_minio

from components.styles import apply_all_styles
from components.tables import build_all_tables
from components.indicators import build_indicators
from components.charts import build_all_charts
from components.filter import build_all_filters


def main():
    output_path = Path("../output/reporting.xlsx")

    print("🔄 Importation et nettoyage des données...")
    dataset = import_and_clean_data()

    print("🔄 Initialisation du fichier Excel...")
    wb, ws_data, ws_visualisations = initialize_workbook(dataset, output_path)

    print("🎨 Application du design...")
    apply_all_styles(ws_visualisations)

    print("⚙️ Paramétrage des filtres...")
    build_all_filters(ws_visualisations, dataset)

    print("🧮 Création des tables de calcul (avec arrayformulas)...")
    build_all_tables(ws_data, ws_visualisations, dataset)

    print("📊 Calcul des indicateurs et KPIs...")
    build_indicators(ws_data, ws_visualisations, len(dataset))

    print("📈 Génération des graphiques...")
    build_all_charts(ws_data, ws_visualisations)

    print("💾 Sauvegarde finale...")
    wb.save(output_path)
    print(f"✅ Terminé ! Fichier disponible à l'emplacement : {output_path}")

    print("☁️ Export sur MinIO...")
    upload_to_minio(output_path)


if __name__ == "__main__":
    main()
