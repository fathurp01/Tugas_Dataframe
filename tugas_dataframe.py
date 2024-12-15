import pandas as pd

# import dataset dan menghapus data null
df_csv = pd.read_csv(
    "disperkim-od_16985_jumlah_produksi_sampah_berdasarkan_kabupatenkota_v3_data.csv"
)
proc_df = df_csv.dropna()


# No.1 - Data Produksi Sampah Provinsi Jawa Barat
print("\nNo.1\n")
print("Data Produksi Sampah Provinsi Jawa Barat")
filter_data = proc_df.loc[
    df_csv["nama_provinsi"] == "JAWA BARAT",
    ["nama_kabupaten_kota", "jumlah_produksi_sampah", "tahun"],
]

df_no1 = filter_data


# No.2 - Menampilkan total produksi sampah pada tahun tertentu
print("\nNo.2\n")
print("Masukkan tahun untuk menampilkan total produksi sampah pada tahun tersebut")
tahun_in = int(input("Anda akan menapilkan data tahun: "))
print(f"Anda memilih tahun {tahun_in}\n")

total_prod = 0
for index, row in filter_data.iterrows():
    if row["tahun"] == tahun_in:
        total_prod += row["jumlah_produksi_sampah"]

print(
    f"Total produksi sampah di seluruh Kabupaten/Kota di Jawa Barat untuk tahun {tahun_in} adalah {total_prod:.2f} ton."
)

df_no2 = pd.DataFrame(
    {"Tahun": [tahun_in], "Total Produksi Sampah (ton)": [total_prod]}
)


# No.3 - Jumlah Data Pertahun
print("\nNo.3\n")
print("Jumlah Data Pertahun:")
jum_pertahun = {}

for index, row in proc_df.iterrows():
    if row["tahun"] in jum_pertahun:
        jum_pertahun[row["tahun"]] += 1
    else:
        jum_pertahun[row["tahun"]] = 1

for tahun, jumlah in jum_pertahun.items():
    print(f"Tahun {tahun} memiliki data sebesar {jumlah} data.")

data_pertahun = [
    {"Tahun": tahun, "Jumlah Data": jumlah} for tahun, jumlah in jum_pertahun.items()
]
df_no3 = pd.DataFrame(data_pertahun)


# No.4 - Jumlah Data Perkabupaten/Kota
print("\nNo.4\n")
print("Jumlah Data Perkabupaten/Kota:")
jum_perkab = {}

for index, row in proc_df.iterrows():
    if row["nama_kabupaten_kota"] not in jum_perkab:
        jum_perkab[row["nama_kabupaten_kota"]] = {}
    if row["tahun"] in jum_perkab[row["nama_kabupaten_kota"]]:
        jum_perkab[row["nama_kabupaten_kota"]][row["tahun"]] += 1
    else:
        jum_perkab[row["nama_kabupaten_kota"]][row["tahun"]] = 1

for daerah, data in jum_perkab.items():
    print(f"Kabupaten {daerah}:")
    for tahun, jumlah in data.items():
        print(f" - Tahun {tahun}: {jumlah} data")

data_perkab = [
    {"Kabupaten/Kota": daerah, "Tahun": tahun, "Jumlah Data": jumlah}
    for daerah, data in jum_perkab.items()
    for tahun, jumlah in data.items()
]
df_no4 = pd.DataFrame(data_perkab)

# export dataframe ke excel
with pd.ExcelWriter("hasil/hasil_produksi_sampah.xlsx") as writer:
    df_no1.to_excel(writer, sheet_name="No1_Produksi_Sampah_Jawa_Barat", index=False)
    df_no2.to_excel(
        writer,
        sheet_name=f"No2_Total_Produksi_Sampah_Jawa_Barat_Tahun_{tahun_in}",
        index=False,
    )
    df_no3.to_excel(writer, sheet_name="No3_Jumlah_Data_Pertahun", index=False)
    df_no4.to_excel(writer, sheet_name="No4_Jumlah_Data_Perkabupaten", index=False)

# export dataframe ke csv
df_no1.to_csv("hasil/No1_produksi_sampah_jawa_barat.csv", index=False)
df_no2.to_csv(
    f"hasil/No2_total_produksi_sampah_jawa_barat_tahun_{tahun_in}.csv", index=False
)
df_no3.to_csv("hasil/No3_jumlah_data_pertahun.csv", index=False)
df_no4.to_csv("hasil/No4_jumlah_data_perkabupaten.csv", index=False)
