import streamlit as st
import pandas as pd
import mysql.connector as mysql
import all_func
from statistics import mean

def app(selected, pilihNama, conn):
    st.title(selected)

    # READ DATA HASIL PENILAIAN
    df_hasil = pd.read_sql(f'SELECT * FROM data_penilaian WHERE nama_ternilai = "{pilihNama}"', con=conn)
    df_hasil = df_hasil[~df_hasil['p5'].isna()]

    # st.table(df_hasil)

    if len(df_hasil) == 0:
        st.warning('Belum ada penilaian tentang anda.')
    else:
        rerata_p1 = mean(df_hasil['p1'].astype(int).to_list())
        rerata_p2 = mean(df_hasil['p2'].astype(int).to_list())
        rerata_p3 = mean(df_hasil['p3'].astype(int).to_list())
        rerata_p4 = mean(df_hasil['p4'].astype(int).to_list())
        rerata_p5 = mean(df_hasil['p5'].astype(int).to_list())
        # list_p5 = df_hasil['p5'].to_list()
        # list_p6 = df_hasil['p6'].to_list()

        st.write(f'1. Nasionalisme: {rerata_p1}')
        st.write('')
        st.write(f'2. pengabdian dan dedikasi: {rerata_p2}')
        st.write('')
        st.write(f'3. Komitmen: {rerata_p3}')
        st.write('')
        st.write(f'4. Inovatif: {rerata_p4}')
        st.write('')
        st.write(f'5. Antusias: {rerata_p5}')
        # for isi in list_p5:
        #     st.write(f'- {isi}')
        # st.write('')
        # st.write(f'6. Saran dan masukan:')
        # for isi in list_p6:
        #     st.write(f'- {isi}')