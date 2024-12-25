import os
import csv
import re

def extract_number_from_filename(filename):
    """Ekstrak angka dari nama file untuk pengurutan."""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

def process_file(filepath):
    """Proses file untuk mengambil data sesuai format kolom."""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Ekstrak data menggunakan regex
    data = {}
    keys = {
        "Nomor": r"Nomor\s*:\s*(.+)",
        "Attack_Category": r"Attack Category\s*:\s*(.+)",
        "Attack_Sub_Category": r"Attack Sub Category\s*:\s*(.+)",
        "Protocol": r"Protocol\s*:\s*(.+)",
        "Source_IP": r"Source IP\s*:\s*(.+)",
        "Source_Port": r"Source Port\s*:\s*(.+)",
        "Destination_IP": r"Destination IP\s*:\s*(.+)",
        "Destination_Port": r"Destination Port\s*:\s*(.+)",
        "Attack_Name": r"Attack Name\s*:\s*(.+)",
        "Attack_Reference": r"Attack Reference\s*:\s*(.+)",
    }

    for key, pattern in keys.items():
        match = re.search(pattern, content)
        data[key] = match.group(1).strip() if match else ""

    return data

# Folder input dan output
input_folder = "scraping_khadafi"
output_file = "scraped_data.csv"

# Dapatkan daftar file dan urutkan berdasarkan nomor dalam nama file
files = os.listdir(input_folder)
files_with_numbers = [(file, extract_number_from_filename(file)) for file in files if file.endswith(".txt")]
files_sorted = [file[0] for file in sorted(files_with_numbers, key=lambda x: x[1])]

# Proses semua file dan simpan hasilnya ke dalam CSV
data = []

for file in files_sorted:
    filepath = os.path.join(input_folder, file)
    row_data = process_file(filepath)
    if row_data:
        data.append(row_data)

# Tulis ke dalam file CSV
columns = [
    "Nomor", "Attack_Category", "Attack_Sub_Category", "Protocol",
    "Source_IP", "Source_Port", "Destination_IP", "Destination_Port",
    "Attack_Name", "Attack_Reference"
]

with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data)

print(f"Proses selesai! Data telah disimpan ke file: {output_file}")
