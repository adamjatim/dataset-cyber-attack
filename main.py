import requests
from bs4 import BeautifulSoup  # type: ignore
import os
from tqdm import tqdm  # type: ignore
import time  # Untuk menambahkan delay
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL dasar untuk scraping
base_url = "https://rock.hangtuah.ac.id/analis/nusw/nuswnb15gtview/"

output_folder = "scraping_khadafi"
os.makedirs(output_folder, exist_ok=True)

# Fungsi untuk scraping satu halaman
def scrape_page(page_number, max_retries=5, retry_delay=5):
    url = f"{base_url}{page_number}?showdetail="
    attempt = 0

    while attempt < max_retries:
        try:
            response = requests.get(url, verify=False)  # Menonaktifkan verifikasi SSL sementara
            response.raise_for_status()  # Raise error jika HTTP error terjadi
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Ambil bagian tabel dengan class table-striped
            table = soup.find("table", class_="table table-striped table-sm ew-view-table")
            if table:
                # Ambil nilai dari setiap baris berdasarkan id
                def get_row_value(row_id):
                    row = table.find("tr", id=row_id)
                    if row:
                        value_cell = row.find("td", {"data-name": row_id.split("_", 1)[1]})
                        if value_cell:
                            return value_cell.get_text(strip=True)
                    return None
                
                # Ambil data
                nomor = get_row_value("r_nomor")
                atkCategory = get_row_value("r_Attack_category")
                atkSubCategory = get_row_value("r_Attack_subcategory")
                protocol = get_row_value("r_Protocol")
                sourceIP = get_row_value("r_Source_IP")
                sourcePort = get_row_value("r_Source_Port")
                destinationIP = get_row_value("r_Destination_IP")
                destinationPort = get_row_value("r_Destination_Port")
                atkName = get_row_value("r_Attack_Name")
                atkReference = get_row_value("r_Attack_Reference")
                
                # Simpan hasil scraping ke file
                with open(os.path.join(output_folder, f"page_{page_number}.txt"), "w", encoding="utf-8") as file:
                    file.write(f"Nomor :                \n{nomor or 'Nomor tidak ditemukan'}\n\n")
                    file.write(f"Attack Category:       \n{atkCategory or 'Attack Category Tidak ditemukan'}\n\n")
                    file.write(f"Attack Sub Category:   \n{atkSubCategory or 'Attack Sub Category Tidak ditemukan'}\n\n")
                    file.write(f"Protocol :             \n{protocol or 'Protocol tidak ditemukan'}\n\n")
                    file.write(f"Source IP :            \n{sourceIP or 'Source IP tidak ditemukan'}\n\n")
                    file.write(f"Source Port :          \n{sourcePort or 'Source Port tidak ditemukan'}\n\n")
                    file.write(f"Destination IP :       \n{destinationIP or 'Destination IP tidak ditemukan'}\n\n")
                    file.write(f"Destination Port :     \n{destinationPort or 'Destination Port tidak ditemukan'}\n\n")
                    file.write(f"Attack Name :          \n{atkName or 'Attack Name Tidak ditemukan'}\n\n")
                    file.write(f"Attack Reference :     \n{atkReference or 'Attack Reference tidak ditemukan'}\n\n")
                return  # Keluar jika berhasil
            else:
                print(f"Konten tidak ditemukan di halaman {page_number}")
                return

        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Error pada halaman {page_number}, percobaan {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)  # Tunggu sebelum mencoba lagi
            else:
                print(f"Gagal mendapatkan halaman {page_number} setelah {max_retries} percobaan.")

# Looping melalui semua halaman
total_pages = 174347
delay_seconds = 1  # Tambahkan delay 1 detik antara permintaan

for page in tqdm(range(1, total_pages + 1), desc="Scraping Pages"):
    scrape_page(page)
    time.sleep(delay_seconds)  # Tambahkan delay di sini
