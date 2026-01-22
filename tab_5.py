import streamlit as st
import pandas as pd
from input_data_5 import potential_facilities, air_defense, restrictions
from optimizer_5 import generate_model_inputs, minimize_production_capacity
from notes_5 import display_notes

def display_tab_5():
    with st.expander("Vis notater"):
        display_notes()
        
    st.subheader("Potensielle fabrikker")
    relevant_potential_facilities_columns = ["Type", "Etablert", "Kapasitet", "Hardhet", "Luftvern"]
    potential_facilities_edited =st.data_editor(
        potential_facilities[relevant_potential_facilities_columns],
        num_rows="dynamic",
        column_config={
            "Kostnad": st.column_config.NumberColumn(format="localized")
        },
        key="prod_facilities_5"
    )

    st.subheader("Luftvern")
    relevant_air_defense_columns = ["Type", "Suksessrate"]
    air_defense_edited = st.data_editor(
        air_defense[relevant_air_defense_columns],
        hide_index=True,
        column_config={
            "Kostnad": st.column_config.NumberColumn(format="localized")
        },
        key="air_defense_5"
    )

    st.subheader("Begrensninger")
    restrictions_edited = st.data_editor(
        restrictions,
        hide_index=True,
        column_config={
            "Mengde": st.column_config.NumberColumn(format="localized")
        },
        key="restrictions_5"
    )

    if st.button("Kjør optimering", type="primary", key="optimize_5"):
        P_A, B_R, F, K_f, e_f, H_f, a_f = generate_model_inputs(potential_facilities_edited, air_defense_edited, restrictions_edited)
        destroyed_f, missile_cost_f, production_capacity = minimize_production_capacity(P_A, B_R, F, K_f, e_f, H_f, a_f)
        if destroyed_f is None:
            st.error("Ingen løsning funnet")
            return
        results = []
        for f in range(len(destroyed_f)):
            results.append({
                "Type": potential_facilities_edited.loc[f, "Type"],
                "Ødelagt": destroyed_f[f],
                "Missilkostnad": missile_cost_f[f]
            })
        results_df = pd.DataFrame(results)
        st.subheader("Optimal løsning")
        st.dataframe(
            results_df,
            hide_index=True,
            column_config={
                "Missilkostnad": st.column_config.NumberColumn(format="localized")
            }
        )
        st.write(f"Gjenværende produksjonskapasitet: {production_capacity}")