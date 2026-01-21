import streamlit as st
from input_data_1 import prod_facilities, air_defense, restrictions
from notes_2 import display_notes
from optimizer_2 import maximize_volume_weighted_missile_cost

def display_tab_2():
    with st.expander("Vis notater"):
        display_notes()

    st.subheader("Fabrikker")
    relevant_prod_facilities_columns = ["Type", "Kostnad per enhet", "Hardhet", "Produksjonskapasitet"]
    prod_facilities_edited =st.data_editor(
        prod_facilities[relevant_prod_facilities_columns],
        num_rows="dynamic",
        column_config={
            "Kostnad per enhet": st.column_config.NumberColumn(format="localized")
        },
        key="prod_facilities_2"
    )

    st.subheader("Luftvern")
    relevant_air_defense_columns = ["Type", "Kostnad per enhet", "Suksessrate"]
    air_defense_edited = st.data_editor(
        air_defense[relevant_air_defense_columns],
        hide_index=True,
        column_config={
            "Kostnad per enhet": st.column_config.NumberColumn(format="localized")
        },
        key="air_defense_2"
    )

    st.subheader("Begrensninger")
    relevant_restrictions_rows = [0, 1]
    restrictions_edited = st.data_editor(
        restrictions.loc[relevant_restrictions_rows],
        hide_index=True,
        column_config={
            "Mengde": st.column_config.NumberColumn(format="localized")
        },
        key="restrictions_2"
    )

    if st.button("Kjør optimering", type="primary", key="optimize_2"):
        maximize_volume_weighted_missile_cost(
            prod_facilities_edited,
            air_defense_edited,
            restrictions_edited
        )