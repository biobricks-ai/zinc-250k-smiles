import os
import requests
from pathlib import Path

url = "https://raw.githubusercontent.com/aspuru-guzik-group/chemical_vae/master/models/zinc_properties/250k_rndm_zinc_drugs_clean_3.csv"
download_dir = Path("download")
download_dir.mkdir(exist_ok=True)
output_path = download_dir / "250k_rndm_zinc_drugs_clean_3.csv"

print(f"Downloading from {url}...")
try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f"Download complete: {output_path}")
except Exception as e:
    print(f"Failed to download: {e}")
    exit(1)
