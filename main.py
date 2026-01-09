import streamlit as st
from tab_1 import display_tab_1
from tab_2 import display_tab_2

tab1, tab2 = st.tabs(["Missilkostnad", "Missilkostnad per kubikk drivstoff"])

with tab1:
    display_tab_1()

with tab2:
    display_tab_2()
