import streamlit as st
import pandas as pd
import mysql.connector as mysql
import all_func

def app(selected, conn):
    st.title(f'Penilaian: {selected}')

    # Data dari cache
    df_penilaian = st.session_state["df_penilaian"]
    pilihNama = st.session_state["name"]

    # Cek apakah sudah dinilai atau belum
    df_penilaian_cek = df_penilaian[df_penilaian['nama_ternilai'] == selected].reset_index(drop=True)

    if df_penilaian_cek['p5'][0] is not None:
        st.success(f'Anda sudah mengisi penilaian untuk {selected}.')

        nilaiUlang = st.button('Nilai Ulang')
        if nilaiUlang:
            all_func.insert_nilai(None, None, None, None, None, None, pilihNama, selected, conn)
            # st.success('Berhasil Input Nilai')

    elif df_penilaian_cek['p5'][0] is None:

        # p1
        p1 = st.radio(f'Responsif – pegawai memahami kebutuhan tim kerja, mengerti apa yang haru dilakukan, cekatan dan solutif.', ('0','1','2','3','4','5','6','7','8','9','10'))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # p2
        p2 = st.radio(f'Kualitas – Pegawai mengutamakan output yang berkualitas bukan “yang penting ada” atau “yang penting selesai”.', ('0','1','2','3','4','5','6','7','8','9','10'))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # p3
        p3 = st.radio(f'Integritas – Pegawai memiliki sifat yang jujur, bertanggung jawab, dan disiplin dalam bekerja.', ('0','1','2','3','4','5','6','7','8','9','10'))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # p4
        p4 = st.radio(f'Dapat diandalkan – Pegawai dapat diandalkan untuk menyelesaikan tugas dengan caranya sendiri secara tepat waktu.', ('0','1','2','3','4','5','6','7','8','9','10'))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # p5
        p5 = st.radio(f'Transparan – Pegawai tidak segan mengkomunikasikan apa yang sedang dikerjakan dan masalah yang dihadapi secara terbuka.', ('0','1','2','3','4','5','6','7','8','9','10'))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # p5
        # p5 = st.text_input(f'Satu Kata Tentang {selected}.')

        # p6
        # p6 = st.text_input(f'Saran dan Masukkan untuk {selected}.')

        # INPUT NILAI
        # if p1 and p2 and p3 and p4 and p5 and p6:
        inputPenilaian = st.button('Input Nilai')
        if inputPenilaian:
            all_func.insert_nilai(p1, p2, p3, p4, p5, pilihNama, selected, conn)
            st.success('Berhasil Input Nilai')