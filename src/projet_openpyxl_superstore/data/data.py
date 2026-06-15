import pandas as pd
import openpyxl
from pathlib import Path
import os
import boto3


def import_and_clean_data(url="https://minio.lab.sspcloud.fr/oscar04/Superstore/Superstore.csv"):
    """Importe et formate les données Superstore."""
    dataset = pd.read_csv(url, encoding="windows-1252")
    
    # Retypage
    dataset["Row ID"] = dataset["Row ID"].astype(str)
    dataset["Postal Code"] = dataset["Postal Code"].astype(str)
    
    # Transformation en format date
    dataset["Order Date"] = pd.to_datetime(dataset["Order Date"], format='%d/%m/%Y', errors='coerce')
    dataset["Ship Date"] = pd.to_datetime(dataset["Ship Date"], format='%d/%m/%Y', errors='coerce')
    
    return dataset


def initialize_workbook(dataset, output_path):
    """Génère le fichier Excel brut et prépare les feuilles."""
    chemin_dossier = Path(output_path).parent
    chemin_dossier.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        dataset.to_excel(writer, sheet_name="DATA", index=False)
        
    wb = openpyxl.load_workbook(output_path)
    ws_visualisations = wb.create_sheet(title="VISUALISATIONS")
    
    # Masquer le quadrillage
    ws_visualisations.sheet_view.showGridLines = False
    
    ws_data = wb["DATA"]
    return wb, ws_data, ws_visualisations


def upload_to_minio(chemin_local, bucket_name="oscar04", minio_path="Superstore/reporting.xlsx"):
    """Exporte le fichier généré vers MinIO"""
    s3_endpoint = os.environ.get("AWS_S3_ENDPOINT")
    
    if not s3_endpoint:
        print("AWS_S3_ENDPOINT non défini, skip de l'upload MinIO.")
        return
        
    s3 = boto3.client("s3", endpoint_url=f"https://{s3_endpoint}")
    s3.upload_file(str(chemin_local), bucket_name, minio_path)
    print(f"Fichier exporté sur MinIO dans le bucket {bucket_name}/{minio_path}")
