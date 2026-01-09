import streamlit as st
from input_data import prod_facilities, air_defense, budget
from optimizer_1 import maximize_missile_cost
from notes_1 import display_notes_1

def display_tab_1():
    with st.expander("Vis notater"):
        display_notes_1()

    st.subheader("Fabrikker")
    prod_facilities_edited =st.data_editor(
        prod_facilities.reset_index(drop=True),
        num_rows="dynamic",
        column_config={
            "Kostnad per enhet": st.column_config.NumberColumn(format="localized")
        },
    )

    st.subheader("Luftvern")
    air_defense_edited = st.data_editor(
        air_defense,
        hide_index=True,
        column_config={
            "Kostnad per enhet": st.column_config.NumberColumn(format="localized")
        },
    )

    st.subheader("Budsjett")
    budget_edited = st.data_editor(
        budget,
        hide_index=True,
        column_config={
            "Beløp": st.column_config.NumberColumn(format="localized")
        },
    )

    if st.button("Kjør optimering", type="primary"):
        maximize_missile_cost(prod_facilities_edited, air_defense_edited, budget_edited)
