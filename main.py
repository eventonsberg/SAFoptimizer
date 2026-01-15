import streamlit as st
from tab_1 import display_tab_1
from tab_2 import display_tab_2
from tab_3 import display_tab_3

st.set_page_config(
    page_title="SAF optimizer",
    page_icon=":material/travel:"
)

tab1, tab2, tab3 = st.tabs(
    ["Missilkostnad", "Volumvektet missilkostnad", "Missilkostnad - Revidert"],
    default="Missilkostnad - Revidert"
)

with tab1:
    display_tab_1()

with tab2:
    display_tab_2()

with tab3:
    display_tab_3()