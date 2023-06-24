import mysql.connector as mysql
import random
import numpy as np
import pandas as pd
from datetime import date, datetime

def hapus_nilai_budaya(nama_pemilih, conn):
    # Hapus data penilai terlibih dahulu
    mycursor = conn.cursor(dictionary= True)
    sql_delete = f' DELETE FROM data_budaya WHERE nama = "{nama_pemilih}" '

    mycursor.execute(sql_delete)
    conn.commit()

def hapus_nominasi(nama_pemilih, conn):
    # Hapus data penilai terlibih dahulu
    mycursor = conn.cursor(dictionary= True)
    sql_delete = f' DELETE FROM data_penilaian WHERE nama = "{nama_pemilih}" '

    mycursor.execute(sql_delete)
    conn.commit()

def insert_nominasi(nama_pemilih, list_nominasi, conn):
    mycursor = conn.cursor(dictionary= True)

    # Tambah kolom bulan
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    bulan_penilaian =str(currentMonth) + '-' + str(currentYear)

    # Masukin ke DB
    for nominasi in list_nominasi:
        sql = "INSERT data_penilaian VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        baris = (
            nama_pemilih,
            '-',
            '-',
            nominasi,
            '-',
            bulan_penilaian,
            None,
            None,
            None,
            None,
            None,
            None,
        )

        mycursor.execute(sql, baris)
        conn.commit()

def insert_nominasi_all(data_all, nama_pemilih, conn):
    mycursor = conn.cursor(dictionary= True)

    # Tambah kolom bulan
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    bulan_penilaian =str(currentMonth) + '-' + str(currentYear)

    for data in data_all:
        # Masukin ke DB
        sql = "INSERT data_penilaian VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        baris = (
            nama_pemilih,
            '-',
            '-',
            data[0],
            '-',
            bulan_penilaian,
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            None,
        )

        mycursor.execute(sql, baris)
        conn.commit()

def insert_nilai_budaya(data_budaya, conn):
    mycursor = conn.cursor(dictionary= True)

    # Tambah kolom bulan
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    bulan_penilaian =str(currentMonth) + '-' + str(currentYear)

    # Masukin ke DB
    sql = "INSERT data_budaya VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    baris = (
        data_budaya[0],
        bulan_penilaian,
        data_budaya[1],
        data_budaya[2],
        data_budaya[3],
        data_budaya[4],
        data_budaya[5],
        data_budaya[6],
        data_budaya[7],
        data_budaya[8],
        data_budaya[9],
        data_budaya[10]
    )

    mycursor.execute(sql, baris)
    conn.commit()

def insert_nilai(p1, p2, p3, p4, p5, pilihNama, selected, conn):
    mycursor = conn.cursor(dictionary= True)

    sql = "UPDATE `data_penilaian` SET `p1`=%s, `p2`=%s, `p3`=%s, `p4`=%s, `p5`=%s WHERE `nama` = %s AND `nama_ternilai` = %s"
    baris = (p1, p2, p3, p4, p5, pilihNama, selected)

    mycursor.execute(sql, baris)
    conn.commit()

def resampling(conn):
    df_daftar_nama = pd.read_excel('Data/Nama untuk sistem (1).xlsx')

    # Clean nama
    def clean_teks(teks):
        teks = ' '.join(teks.split())
        return teks

    df_daftar_nama['Nama'] = df_daftar_nama['Nama'].apply(clean_teks)
    df_daftar_nama['Tim'] = df_daftar_nama['Tim'].apply(clean_teks)
    df_daftar_nama['Jabatan'] = df_daftar_nama['Jabatan'].apply(clean_teks)

    # Daftar Tim dan daftar tim
    daftar_tim = df_daftar_nama['Tim'].drop_duplicates().to_list()
    daftar_nama = df_daftar_nama['Nama'].drop_duplicates().to_list()

    # UNTUK SEMUA TIM
    list_data = []
    for tim in daftar_tim:
        print(f'Pengerjaan {tim}')
        df_tim = df_daftar_nama[df_daftar_nama['Tim'] == tim].reset_index(drop=True)

        for index, row in df_tim.iterrows():
            nama = row['Nama']
            tim = row['Tim']
            jabatan = row['Jabatan']

            ## Jika ANGGOTA TIM
            if jabatan == 'Anggota Tim':
                # List rekan kerja
                list_rekan_kerja = df_tim[(df_tim['Nama'] != nama) & (df_tim['Jabatan'] == 'Anggota Tim')]['Nama'].to_list()
                # List atasan
                list_atasan = df_tim[df_tim['Jabatan'] == 'Ketua Tim']['Nama'].to_list()

                # Memilih 4 sampel random dari list rekan kerja dan 1 sampel rando dari list atasan
                try:
                    sampel_rekan_kerja = random.sample(list_rekan_kerja, 4)
                    sampel_atasan = random.sample(list_atasan, 1)
                except:
                    sampel_rekan_kerja = random.sample(list_rekan_kerja, len(list_rekan_kerja))
                    sampel_atasan = random.sample(list_atasan, len(list_atasan))

                # Menggabungkan kedua sampel
                sampel_terpilih = sampel_atasan + sampel_rekan_kerja

            elif jabatan == 'Ketua Tim':
                # List bawahan
                list_bawahan = df_tim[(df_tim['Nama'] != nama) & (df_tim['Jabatan'] == 'Anggota Tim')]['Nama'].to_list()

                # Memilih 5 sampel random dari list bawahan
                try:
                    sampel_bawahan = random.sample(list_bawahan, 5)
                except:
                    sampel_bawahan = random.sample(list_bawahan, len(list_bawahan))

                # Menggabungkan kedua sampel
                sampel_terpilih = sampel_bawahan

            for sampel in sampel_terpilih:
                baris = [nama, tim, jabatan, sampel]

                list_data.append(baris)

    # Buat DF
    df_jadi = pd.DataFrame(data=list_data, columns=['nama', 'tim', 'jabatan', 'nama_ternilai'])
    df_jadi = df_jadi.merge(df_daftar_nama, how='left', left_on=['nama_ternilai', 'tim'], right_on=['Nama', 'Tim'])
    df_jadi = df_jadi.drop(columns=['Nama','Tim'])
    df_jadi = df_jadi.rename(columns={'Jabatan': 'jabatan_ternilai'})

    # Cleaning kalau lebih dari 5 kemudian diambil semua ketua tim, sisanya random
    df_clean = pd.DataFrame()
    for nama in daftar_nama:
        df_per_nama = df_jadi[df_jadi['nama'] == nama].reset_index(drop=True)
        df_per_nama = df_per_nama.drop_duplicates(subset = ['nama_ternilai']).reset_index(drop=True)

        # DF yang dinilai adalah ketua tim
        df_per_nama_ketua = df_per_nama[df_per_nama['jabatan_ternilai'] == 'Ketua Tim'].drop_duplicates(subset = ['nama_ternilai']).reset_index(drop=True)
        jumlah_ternilai_ketua = len(df_per_nama_ketua)

        # DF yang dinilai adalah rekan kerja atau bawahan
        df_per_nama_rekan = df_per_nama[df_per_nama['jabatan_ternilai'] != 'Ketua Tim'].drop_duplicates(subset = ['nama_ternilai']).reset_index(drop=True)
        jumlah_ternilai = len(df_per_nama_rekan)

        if jumlah_ternilai_ketua + jumlah_ternilai > 5:
            drop_indices = np.random.choice(df_per_nama_rekan.index, jumlah_ternilai_ketua + jumlah_ternilai - 5, replace=False)
            df_per_nama_rekan = df_per_nama_rekan.drop(drop_indices).reset_index(drop=True)
            # print(f'{nama} - {jumlah_ternilai_ketua} ketua - {jumlah_ternilai} rekan kerja - kurangi {pengurang}')

        df_gabungan = pd.concat([df_per_nama_ketua, df_per_nama_rekan], ignore_index=True).reset_index(drop=True)

        df_clean = pd.concat([df_clean, df_gabungan], ignore_index=True).reset_index(drop=True)

    # Tambah kolom bulan
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    df_clean['bulan_penilaian'] = str(currentMonth) + '-' + str(currentYear)

    # Tambah kolom nilai
    df_clean[['p1', 'p2', 'p3', 'p4', 'p5', 'p6']] = None

    ## UPDATE DATABASE
    bulan_penilaian = str(currentMonth) + '-' + str(currentYear)

    # Hapus data terlebih dahulu
    mycursor = conn.cursor(dictionary= True)
    sql_delete = ' DELETE FROM data_penilaian '

    mycursor.execute(sql_delete)
    conn.commit()

    for index, row in df_clean.iterrows():
        # Masukin ke DB
        sql = "INSERT data_penilaian VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        baris = (
            row['nama'],
            row['tim'],
            row['jabatan'],
            row['nama_ternilai'],
            row['jabatan_ternilai'],
            row['bulan_penilaian'],
            row['p1'],
            row['p2'],
            row['p3'],
            row['p4'],
            row['p5'],
            row['p6'],
        )

        mycursor.execute(sql, baris)
        conn.commit()
