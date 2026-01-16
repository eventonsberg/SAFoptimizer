import streamlit as st
from tab_1 import display_tab_1
from tab_2 import display_tab_2
from tab_3 import display_tab_3
from tab_4 import display_tab_4

st.set_page_config(
    page_title="SAF optimizer",
    page_icon=":material/travel:"
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Missilkostnad", "Volumvektet missilkostnad", "Missilkostnad - Revidert", "Volumvektet missilkostnad - Revidert"],
    default="Missilkostnad - Revidert"
)

with tab1:
    display_tab_1()

with tab2:
    display_tab_2()

with tab3:
    display_tab_3()

with tab4:
    display_tab_4()