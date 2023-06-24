import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import mysql.connector as mysql
import all_func_2
import yaml
from Apps import penilaian
from statistics import mean
from deta import Deta  # Import Deta
import io
from datetime import date, datetime

# Fullscreen
im = Image.open("image/page_icon.png")
st.set_page_config(
        page_title="DAPS INSPIRING FELLOW",
        page_icon=im,
        layout="wide",
    )

# Remove Whitespace
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

# Connect to Deta Base with your Data Key
deta = Deta(st.secrets["data_key"])

# Configuration login/logout function
drive_user = deta.Drive("dapscan")
file_user = drive_user.get('config.yaml')
file_user_string = file_user.read().decode("utf-8")
config = yaml.safe_load(file_user_string)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Login Page
judul = st.markdown("<h1 style='text-align: center; color: #6eb52f;'>INSPIRING FELLOW - DAPS</h1>", unsafe_allow_html=True)
subjudul = st.markdown("<h2 style='text-align: center; color: white;'>Sistem Pemilihan Inspiring Fellow DAPS</h2>", unsafe_allow_html=True)
    
col1, col2, col3 = st.columns(3)
with col2:
    # Login form
    name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    judul.empty()
    subjudul.empty()

    # Coba SIDEBAR DINAMIS
    df_list_nama = pd.read_csv('data/list_username.csv', sep = ';')
    pilihNama = st.session_state["name"]

    if pilihNama == "admin":
        # Sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title = 'IF-DAPS',
                menu_icon = 'ui-radios',
                options = ['Penilaian IF', 'Perubahan Budaya Kerja', 'Atur Profil'],
                icons = ['house-door', 'person-workspace', 'gear']
            )

        # Halaman Beranda
        if selected == 'Penilaian IF':
            st.title('Hasil Penilaian IF')

            st.write(f'Hallo *{st.session_state["name"]}*, berikut hasil penilaian Inspiring Fellow DAPS.')
            
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            # DATA UNDUH
            # READ DATA PENILAIAN
            db = deta.Base("data_penilaian")
            df_unduh = db.fetch().items
            df_unduh = pd.json_normalize(df_unduh)
            df_unduh = df_unduh[['nama', 'nama_ternilai', 'p1', 'p2', 'p3', 'p4', 'p5']]
            csv = convert_df(df_unduh)
            st.download_button(
                label="Unduh Hasil Penilaian Mentah(CSV)",
                data=csv,
                file_name='Hasil Penilaian IF Mentah.csv',
                mime='text/csv',
            )

            # READ DATA HASIL PENILAIAN
            list_nama_penilai = df_unduh['nama'].drop_duplicates().sort_values().to_list()
            df_unduh[['p1', 'p2', 'p3', 'p4', 'p5']] = df_unduh[['p1', 'p2', 'p3', 'p4', 'p5']].astype(int)
            df_unduh['nilai_akhir'] = (df_unduh['p1'] + df_unduh['p2']  + df_unduh['p3'] + df_unduh['p4'] + df_unduh['p5']) / 5
            df_unduh = df_unduh[['nama_ternilai','nilai_akhir']]
            df_unduh = df_unduh.groupby(['nama_ternilai'], as_index=False).agg(jumlah_penilai = ('nilai_akhir','count')).reset_index(drop=True)
            df_unduh = df_unduh.sort_values(by=['jumlah_penilai','nama_ternilai'], ascending = [False, True]).reset_index(drop=True)
            df_unduh = df_unduh.rename(columns={'nama_ternilai': 'Nama', 'jumlah_penilai': 'Jumlah Penilai'})

            # List yang sudah menilai
            with st.expander("Lihat daftar nama yang sudah menilai"):
                st.write(list_nama_penilai)

            st.table(df_unduh)

            # DATA UNDUH
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')
            csv_hasil = convert_df(df_unduh)
            st.download_button(
                label="Unduh Hasil Penilaian Akhir (CSV)",
                data=csv_hasil,
                file_name='Hasil Penilaian Akhir.csv',
                mime='text/csv',
            )


        if selected == 'Perubahan Budaya Kerja':
            st.title(selected)

            # READ DATA HASIL PENILAIAN BUDAYA
            db_budaya = deta.Base("data_budaya")
            df_budaya = db_budaya.fetch().items
            df_budaya = pd.json_normalize(df_budaya)
            df_budaya = df_budaya[['nama', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']]
            list_nama_penilai = df_budaya['nama'].drop_duplicates().sort_values().to_list()
            df_budaya = df_budaya[['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']]

            # DATA UNDUH
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')
            csv_hasil = convert_df(df_budaya)
            st.download_button(
                label="Unduh Hasil Penilaian Perubahan Budaya Kerja (CSV)",
                data=csv_hasil,
                file_name='Hasil Penilaian Perubahan Budaya Kerja.csv',
                mime='text/csv',
            )

            # List yang sudah menilai
            with st.expander("Lihat daftar nama yang sudah menilai"):
                st.write(list_nama_penilai)

            st.table(df_budaya)

        if selected == 'Atur Profil':
            st.title(selected)
            # Tombol Logout
            authenticator.logout('Logout', 'main')
            
            # Fungsi ADMIN
            colpro1, colpro2 = st.columns(2)
            with colpro1:
                # Ganti Password
                with st.expander("Ganti Password"):
                    # st.write('Mohon maaf fitur ini sedang tidak dapat digunakan.')
                    if authentication_status:
                        try:
                            if authenticator.reset_password(username, 'Ganti Password'):
                                st.success('Password berhasil diganti')
                                # Save data user to db
                                str_config = str(config)
                                drive_user.put('config.yaml', io.StringIO(str_config))
                        except Exception as e:
                            st.error(e)
            
            with colpro2:
                # Tambah User baru
                with st.expander("Tambah User Baru"):
                    # st.write('Mohon maaf fitur ini sedang tidak dapat digunakan.')
                    if authentication_status:
                        try:
                            if authenticator.register_user('Register user', preauthorization=False):
                                st.success('User registered successfully')
                                # Save data user to db
                                str_config = str(config)
                                drive_user.put('config.yaml', io.StringIO(str_config))
                        except Exception as e:
                            st.error(e)

    else:
        
        # READ DATA PENILAIAN
        db = deta.Base("data_penilaian")
        # df_penilaian = db.fetch({"nama": pilihNama}).items
        df_penilaian = db.fetch().items
        df_penilaian = pd.json_normalize(df_penilaian)
        df_penilaian = df_penilaian[df_penilaian['nama'] == pilihNama].reset_index(drop=True)
        st.session_state["df_penilaian"] = df_penilaian

        # LIST NAMA YANG DINILAI
        list_nama_ternilai = df_penilaian['nama_ternilai'].to_list()

        # Sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title = 'IF-DAPS',
                menu_icon = 'ui-radios',
                options = ['Penilaian IF', 'Perubahan Budaya Kerja', 'Penilaian Anda', 'Atur Profil'],
                icons = ['house-door', 'person-workspace', 'map', 'gear']
            )

        # Halaman Beranda
        if selected == 'Penilaian IF':
            st.title('INSPIRING FELLOW - DAPS')

            if len(list_nama_ternilai) == 0:
                st.write(f'''
                    Hallo *{st.session_state["name"]}*,

                    Silakan nominasikan 3 (tiga) nama pegawai DAPS yang layak menjadi Inspiring Fellow Triwulan I 2023, sesuai kriteria di bawah ini.
                    Harap memberikan nilai antara 1 sampai 10 untuk setiap kriteria. Semakin tinggi nilai, maka pegawai semakin mendekati kriteria yang diharapkan.
                    1.	**Responsif**: Pegawai memahami kebutuhan tim kerja, mengerti apa yang haru dilakukan, cekatan dan solutif.
                    2.	**Kualitas**: Pegawai mengutamakan output yang berkualitas bukan “yang penting ada” atau “yang penting selesai”.
                    3.	**Integritas**: Pegawai memiliki sifat yang jujur, bertanggung jawab, dan disiplin dalam bekerja.
                    4.	**Dapat diandalkan**: Pegawai dapat diandalkan untuk menyelesaikan tugas dengan caranya sendiri secara tepat waktu. 
                    5.	**Transparan**: Pegawai tidak segan mengkomunikasikan apa yang sedang dikerjakan dan masalah yang dihadapi secara terbuka.
                    
                    🚫 **Note: pegawai diizinkan mengajukan diri sendiri** 🚫

                    ''')
                
                # DF LIST NAMA
                list_nama = pd.read_excel('Data/list_username.xlsx', engine="openpyxl")
                list_nama_non_eligible = ['Dr. Muchammad Romzi', 'Yuniarti S.Si', 'Dewi Krismawati SST, M.T.I', 'Yohanes Eki Apriliawan SST', 'Nurarifin SST, M.Ec.Dev, M.Ec.', 'Ema Tusianti SST, SAB, M.T., M.Sc']
                list_nama = list_nama[~list_nama['name'].isin(list_nama_non_eligible)]
                list_nama = list_nama['name'].drop_duplicates().to_list()
                list_nama = ['- Belum dipilih -'] + list_nama
                # st.write(st.session_state["name"])
                # st.write(list_nama)
                # list_nama.remove(st.session_state["name"])

                st.write('---')

                st.subheader('👑 NOMINASI PERTAMA')
                
                nama_1 = st.selectbox(
                    'Silakan pilih nama pegawai pertama',
                    list_nama)

                if nama_1 != '- Belum dipilih -':
                    try:
                        # p1
                        p1_1 = st.radio(f'Responsif – {nama_1} memahami kebutuhan tim kerja, mengerti apa yang haru dilakukan, cekatan dan solutif.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p2
                        p2_1 = st.radio(f'Kualitas – {nama_1} mengutamakan output yang berkualitas bukan “yang penting ada” atau “yang penting selesai”.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p3
                        p3_1 = st.radio(f'Integritas – {nama_1} memiliki sifat yang jujur, bertanggung jawab, dan disiplin dalam bekerja.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p4
                        p4_1 = st.radio(f'Dapat diandalkan – {nama_1} dapat diandalkan untuk menyelesaikan tugas dengan caranya sendiri secara tepat waktu.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p5
                        p5_1 = st.radio(f'Transparan – {nama_1} tidak segan mengkomunikasikan apa yang sedang dikerjakan dan masalah yang dihadapi secara terbuka.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        data_1 = [nama_1, p1_1, p2_1, p3_1, p4_1, p5_1]
                    except:
                        st.warning(f'Anda telah memilih {nama_1}, silakan pilih pegawai lain.')

                st.write('---')

                st.subheader('👑 NOMINASI KEDUA')
                
                nama_2 = st.selectbox(
                    'Silakan pilih nama pegawai kedua',
                    list_nama)

                if nama_2 != '- Belum dipilih -':
                    try:
                        # p1
                        p1_2 = st.radio(f'Responsif – {nama_2} memahami kebutuhan tim kerja, mengerti apa yang haru dilakukan, cekatan dan solutif.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p2
                        p2_2 = st.radio(f'Kualitas – {nama_2} mengutamakan output yang berkualitas bukan “yang penting ada” atau “yang penting selesai”.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p3
                        p3_2 = st.radio(f'Integritas – {nama_2} memiliki sifat yang jujur, bertanggung jawab, dan disiplin dalam bekerja.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p4
                        p4_2 = st.radio(f'Dapat diandalkan – {nama_2} dapat diandalkan untuk menyelesaikan tugas dengan caranya sendiri secara tepat waktu.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p5
                        p5_2 = st.radio(f'Transparan – {nama_2} tidak segan mengkomunikasikan apa yang sedang dikerjakan dan masalah yang dihadapi secara terbuka.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        data_2 = [nama_2, p1_2, p2_2, p3_2, p4_2, p5_2]
                    except:
                        st.warning(f'Anda telah memilih {nama_2}, silakan pilih pegawai lain.')

                st.write('---')

                st.subheader('👑 NOMINASI KETIGA')
                
                nama_3 = st.selectbox(
                    'Silakan pilih nama pegawai ketiga',
                    list_nama)

                if nama_3 != '- Belum dipilih -':
                    try:
                        # p1
                        p1_3 = st.radio(f'Responsif – {nama_3} memahami kebutuhan tim kerja, mengerti apa yang haru dilakukan, cekatan dan solutif.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p2
                        p2_3 = st.radio(f'Kualitas – {nama_3} mengutamakan output yang berkualitas bukan “yang penting ada” atau “yang penting selesai”.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p3
                        p3_3 = st.radio(f'Integritas – {nama_3} memiliki sifat yang jujur, bertanggung jawab, dan disiplin dalam bekerja.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p4
                        p4_3 = st.radio(f'Dapat diandalkan – {nama_3} dapat diandalkan untuk menyelesaikan tugas dengan caranya sendiri secara tepat waktu.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        # p5
                        p5_3 = st.radio(f'Transparan – {nama_3} tidak segan mengkomunikasikan apa yang sedang dikerjakan dan masalah yang dihadapi secara terbuka.', ('0','1','2','3','4','5','6','7','8','9','10'))
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        data_3 = [nama_3, p1_3, p2_3, p3_3, p4_3, p5_3]
                    except:
                        st.warning(f'Anda telah memilih {nama_3}, silakan pilih pegawai lain.')

            
                if '- Belum dipilih -' not in [nama_1, nama_2, nama_3]:
                    data_all = [data_1, data_2, data_3]
                    inputNominasi = st.button('Simpan Penilaian')
                    if inputNominasi:
                        # Tambah kolom bulan
                        currentMonth = datetime.now().month
                        currentYear = datetime.now().year
                        bulan_penilaian =str(currentMonth) + '-' + str(currentYear)

                        # Masukin ke DETA
                        for data in data_all:
                            db.put({
                                        "nama": pilihNama,
                                        "tim": '-',
                                        "jabatan": '-' ,
                                        "nama_ternilai": data[0],
                                        "tim_ternilai": '-',
                                        "bulan_penilaian": bulan_penilaian,
                                        "p1": data[1],
                                        "p2": data[2],
                                        "p3": data[3],
                                        "p4": data[4],
                                        "p5": data[5]
                                    }
                                )
                        st.success('Berhasil Menyimpan Nominasi, Silakan Reload Halaman (atau Tekan Tombol F5).')
                        st.experimental_rerun()
                
            elif len(list_nama_ternilai) == 3:

                st.write(f'''
                    Hallo *{st.session_state["name"]}*,

                    Anda sebelumnya telah menominasikan 3 (tiga) pegawai yang telah dinilai:

                    ''')

                for nama_ternilai in list_nama_ternilai:
                    st.write(f'- **{nama_ternilai}**')

                st.write(f'''
                    Apabila anda ingin mengubah nominasi anda silakan tekan tombol dibawah ini.
                    ''')
                
                # st.write(df_penilaian[df_penilaian['nama'] == st.session_state["name"]]['key'].to_list())
                hapusNominasi = st.button('Hapus Nominasi')
                if hapusNominasi:
                    list_key = df_penilaian[df_penilaian['nama'] == st.session_state["name"]]['key'].to_list()
                    db.delete(list_key[0])
                    db.delete(list_key[1])
                    db.delete(list_key[2])
                    st.success('Berhasil menghapus nominasi, silakan reload halaman (atau tekan yombol F5) lalu pilih kembali nominasi anda.')
                    st.experimental_rerun()

        if selected == 'Perubahan Budaya Kerja':
            st.title('PERUBAHAN BUDAYA KERJA')

            db_budaya = deta.Base("data_budaya")

            # with st.form("form"):
            #     name = st.text_input("Your name")
            #     age = st.number_input("Your age")
            #     submitted = st.form_submit_button("Store in database")


            # If the user clicked the submit button,
            # write the data from the form to the database.
            # You can store any data you want here. Just modify that dictionary below (the entries between the {}).
            # if submitted:
            #     # Tambah kolom bulan
            #     currentMonth = datetime.now().month
            #     currentYear = datetime.now().year
            #     bulan_penilaian =str(currentMonth) + '-' + str(currentYear)
            #     db_budaya.put({
            #                 "nama": pilihNama,
            #                 "bulan_penilaian": bulan_penilaian,
            #                 "p1": 1,
            #                 "p2": 2,
            #                 "p3": 3,
            #                 "p4": 4,
            #                 "p5": 5,
            #                 "p6": 6,
            #                 "p7": 7,
            #                 "p8": 8,
            #                 "p9": 9,
            #                 "p10": 10
            #             }
            #         )


            # READ DATA HASIL PENILAIAN BUDAYA
            db_budaya = deta.Base("data_budaya")
            df_budaya = db_budaya.fetch().items
            df_budaya = pd.json_normalize(df_budaya)
            df_budaya = df_budaya[df_budaya['nama'] == pilihNama].reset_index(drop=True)
            st.session_state["df_budaya"] = df_budaya

            if len(df_budaya) == 0: # Belum menilai
                # st.warning('Anda belum memilih.')
                st.write(f'''
                    Hallo *{st.session_state["name"]}*,

                    Perubahan budaya kerja (*culture change*) adalah proses merubah kebiasaan atau pola pikir untuk mendorong performa kerja yang lebih baik. 
                    Performa kerja yang lebih baik dapat dicapai jika didukung oleh lingkungan kerja yang nyaman, 
                    diantaranya adalah adanya kepercayaan yang tinggi antar pegawai, ruang inovasi yang luas, tidak ada kebiasaan julid, dan tidak ada mental *silo*.
                    
                    Untuk mewujudkan hal tersebut, mohon berkenan mengisi pertanyaan di bawah ini untuk perbaikan/peningkatan budaya kerja di DAPS.

                    *Note: Merasa jawaban anda receh? Don’t worry, karena kita akan mulai perubahan dari hal-hal receh. Identitas anda pun akan dijaga kerahasiannya.*

                    ''')
                
                st.write('---')
                
                # p1
                p1 = st.radio('Secara umum, apakah anda nyaman bekerja di DAPS?', ('Sangat tidak nyaman','Tidak nyaman','Nyaman','Sangat nyaman'))
                st.write('')    
                # p2
                p2 = st.text_area('(Masih) adakah hal-hal yang membuat anda tidak nyaman bekerja di DAPS?')
                st.write('')  
                # p3
                p3 = st.radio('Bagaimana beban kerjamu memengaruhi kesehatan mentalmu?', ('Stress dan tertekan tiap hari','Kadang stress, tapi nggak tiap hari','Biasa aja','Ngerasa enjoy banget kalau bekerja'))
                st.write('')  
                # p4
                p4 = st.text_area('Adakah usulan terkait pembagian beban kerja yang lebih adil/lebih baik? Jelaskan!')
                st.write('')  
                # p5
                p5 = st.radio('Tahun ini, DAPS menerapkan skema tim kerja. Seberapa cocok anda dengan skema ini? ', ('Sangat tidak cocok', 'Kurang cocok sih, tapi ya ikut aja', 'Cocok-cocok aja', 'Skema terbaik yang pernah ada'))
                st.write('')  
                # p6
                p6 = st.text_area('Apakah anda punya usulan skema kolaborasi antar pegawai di DAPS yang lebih baik? Jelaskan!')
                st.write('')  
                # p7
                p7 = st.radio('Menurut anda, bagimana budaya kerja di DAPS? ', ('Sangat tidak baik', 'Tidak baik', 'Biasa saja', 'Sudah baik', 'Sangat baik'))
                st.write('')  
                # p8
                p8 = st.text_area('Apakah anda punya harapan khusus untuk DAPS supaya budaya kerja menjadi lebih baik lagi?')
                st.write('')  
                # p9
                p9 = st.text_area('Hal seperti apa atau budaya kerja yang mana yang masih layak dipertahankan di DAPS?')
                st.write('')  
                # p10
                p10 = st.text_area('Apakah anda mempunyai usulan praktek baik yang dapat diimplemetasikan di DAPS?')

                inputNilai = st.button('Simpan Penilaian')
                if inputNilai:
                    # Tambah kolom bulan
                    currentMonth = datetime.now().month
                    currentYear = datetime.now().year
                    bulan_penilaian =str(currentMonth) + '-' + str(currentYear)

                    # To DETA
                    db_budaya.put({
                                "nama": pilihNama,
                                "bulan_penilaian": bulan_penilaian,
                                "p1": p1,
                                "p2": p2,
                                "p3": p3,
                                "p4": p4,
                                "p5": p5,
                                "p6": p6,
                                "p7": p7,
                                "p8": p8,
                                "p9": p9,
                                "p10": p10
                            }
                        )
                    st.experimental_rerun()

            else: # Sudah menilai
                st.write(f'''
                    Hallo *{st.session_state["name"]}*,

                    Anda sebelumnya telah menilai budaya kerja di DAPS. Apabila anda ingin mengubah penilaian anda silakan tekan tombol dibawah ini.

                    ''')

                hapusNilai = st.button('Hapus Penilaian Budaya Kerja')
                if hapusNilai:
                    list_key = df_budaya[df_budaya['nama'] == pilihNama]['key'].to_list()
                    db_budaya.delete(list_key[0])                
                    st.success('Berhasil menghapus penilaian, silakan reload halaman (atau tekan yombol F5) lalu pilih kembali penilaian anda.')
                    st.experimental_rerun()

        if selected == 'Penilaian Anda':

            # READ DATA HASIL PENILAIAN
            df_hasil = db.fetch().items
            df_hasil = pd.json_normalize(df_hasil)
            df_hasil = df_hasil[df_hasil['nama_ternilai'] == pilihNama].reset_index(drop=True)
            df_hasil = df_hasil[~df_hasil['p5'].isna()]

            # st.table(df_hasil)

            if len(df_hasil) == 0:
                st.title(f'{selected} 🌟')
                st.warning('Belum ada penilaian tentang anda.')
            else:

                st.markdown("<h1 style='text-align: center; color: white;'>🌟 SELAMAT 🌟</h1>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: white;'>ANDA MENGINSPIRASI {len(df_hasil)} PEGAWAI DAPS</h2>", unsafe_allow_html=True)

                rerata_p1 = mean(df_hasil['p1'].astype(int).to_list())
                rerata_p2 = mean(df_hasil['p2'].astype(int).to_list())
                rerata_p3 = mean(df_hasil['p3'].astype(int).to_list())
                rerata_p4 = mean(df_hasil['p4'].astype(int).to_list())
                rerata_p5 = mean(df_hasil['p5'].astype(int).to_list())
                rerata_nilai = (rerata_p1 + rerata_p2 + rerata_p3 + rerata_p4 + rerata_p5) / 5
                
                st.write(f'Rata-rata Nilai Anda:')
                st.write('')
                st.write(f'1. Responsif: {round(rerata_p1,1)}')
                st.write('')
                st.write(f'2. Kualitas: {round(rerata_p2,1)}')
                st.write('')
                st.write(f'3. Integritas: {round(rerata_p3,1)}')
                st.write('')
                st.write(f'4. Dapat Diandalkan: {round(rerata_p4,1)}')
                st.write('')
                st.write(f'5. Transparan : {round(rerata_p5,1)}')


        if selected == 'Atur Profil':
            st.title(selected)
            # Tombol Logout
            authenticator.logout('Logout', 'main')
            
            # Fungsi ADMIN
            colpro1, colpro2 = st.columns(2)
            with colpro1:
                # Ganti Password
                with st.expander("Ganti Password"):
                    # st.write('Mohon maaf fitur ini sedang tidak dapat digunakan.')
                    pass
                    if authentication_status:
                        try:
                            if authenticator.reset_password(username, 'Ganti Password'):
                                st.success('Password berhasil diganti')
                                # Save data user to db
                                str_config = str(config)
                                drive_user.put('config.yaml', io.StringIO(str_config))
                        except Exception as e:
                            st.error(e)
            
            with colpro2:
                # Update Informasi
                with st.expander("Update Informasi"):
                    # st.write('Mohon maaf fitur ini sedang tidak dapat digunakan.')
                    st.write('Mohon tidak mengubah informasi *nama*')
                    if authentication_status:
                        try:
                            if authenticator.update_user_details(username, 'Update user details'):
                                st.success('Entries updated successfully')
                                # Save data user to db
                                str_config = str(config)
                                drive_user.put('config.yaml', io.StringIO(str_config))
                        except Exception as e:
                            st.error(e)


elif st.session_state["authentication_status"] == False:
    with col2:
        st.error('Username/password salah atau tidak terdaftar')

elif st.session_state["authentication_status"] == None:
    with col2:
        st.warning('Silakan masukan username dan password')
