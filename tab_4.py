import streamlit as st
from input_data_1 import prod_facilities, air_defense, restrictions
from optimizer_4 import maximize_volume_weighted_missile_cost
from notes_4 import display_notes

def display_tab_4():
    with st.expander("Vis notater"):
        display_notes()
        
    st.subheader("Fabrikker")
    relevant_prod_facilities_columns = ["Type", "Kostnad per enhet", "Hardhet", "Maks antall enheter", "Produksjonskapasitet"]
    prod_facilities_edited =st.data_editor(
        prod_facilities[relevant_prod_facilities_columns],
        num_rows="dynamic",
        column_config={
            "Kostnad per enhet": st.column_config.NumberColumn(format="localized")
        },
        key="prod_facilities_4"
    )

    st.subheader("Luftvern")
    relevant_air_defense_columns = ["Type", "Kostnad per enhet", "Suksessrate", "Maks antall enheter per fabrikk"]
    air_defense_edited = st.data_editor(
        air_defense[relevant_air_defense_columns],
        hide_index=True,
        column_config={
            "Kostnad per enhet": st.column_config.NumberColumn(format="localized")
        },
        key="air_defense_4"
    )

    st.subheader("Begrensninger")
    relevant_restrictions_rows = [0, 1]
    restrictions_edited = st.data_editor(
        restrictions.loc[relevant_restrictions_rows],
        hide_index=True,
        column_config={
            "Mengde": st.column_config.NumberColumn(format="localized")
        },
        key="restrictions_4"
    )

    if st.button("Kjør optimering", type="primary", key="optimize_4"):
        maximize_volume_weighted_missile_cost(prod_facilities_edited, air_defense_edited, restrictions_edited)
