import streamlit as st
from tab_1 import display_tab_1
from tab_2 import display_tab_2
from tab_3 import display_tab_3
from tab_4 import display_tab_4
from tab_5 import display_tab_5
from tab_6 import display_tab_6
from tab_7 import display_tab_7

st.set_page_config(
    page_title="SAF optimizer",
    page_icon=":material/travel:"
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Missilkostnad",
        "Volumvektet missilkostnad",
        "Missilkostnad - Revidert",
        "Volumvektet missilkostnad - Revidert",
        "Produksjonskapasitet - RØD",
        "Produksjonskapasitet - BLÅ",
        "Varierende missilbudsjett"
    ],
    default="Varierende missilbudsjett"
)

with tab1:
    display_tab_1()

with tab2:
    display_tab_2()

with tab3:
    display_tab_3()

with tab4:
    display_tab_4()

with tab5:
    display_tab_5()

with tab6:
    display_tab_6()

with tab7:
    display_tab_7()