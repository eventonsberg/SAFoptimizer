import streamlit as st
import pandas as pd
from input_data_6 import potential_facilities, air_defense, restrictions
from optimizer_6 import generate_model_inputs, solve_interdiction
from notes_5 import display_notes

def display_tab_6():
    with st.expander("Vis notater"):
        display_notes()
        
    st.subheader("Potensielle fabrikker")
    potential_facilities_edited =st.data_editor(
        potential_facilities,
        num_rows="dynamic",
        column_config={
            "Kostnad": st.column_config.NumberColumn(format="localized")
        },
        key="prod_facilities_6"
    )

    st.subheader("Luftvern")
    air_defense_edited = st.data_editor(
        air_defense,
        hide_index=True,
        column_config={
            "Kostnad": st.column_config.NumberColumn(format="localized")
        },
        key="air_defense_6"
    )

    st.subheader("Begrensninger")
    restrictions_edited = st.data_editor(
        restrictions,
        hide_index=True,
        column_config={
            "Mengde": st.column_config.NumberColumn(format="localized")
        },
        key="restrictions_6"
    )

    if st.button("Kjør optimering", type="primary", key="optimize_6"):
        P_A, C_A, A_max, B_R, B_B, F, type_f, K_f, H_f, C_f = generate_model_inputs(potential_facilities_edited, air_defense_edited, restrictions_edited)
        results_dict = solve_interdiction(P_A, C_A, A_max, B_R, B_B, F, K_f, H_f, C_f)
        if results_dict["status"] == "OPTIMAL":
            results = []
            type_counters = {}
            for f in range(F):
                if results_dict["established_facilities"][f]:
                    if type_f[f] not in type_counters:
                        type_counters[type_f[f]] = 0
                    type_counters[type_f[f]] += 1
                    type_name = f"{type_f[f]} #{type_counters[type_f[f]]}" if type_counters[type_f[f]] > 1 else type_f[f]
                    number_of_air_defense_missiles = results_dict["air_defense_assignment"][f]
                    facility_and_air_defense_cost = C_f[f] + C_A * number_of_air_defense_missiles
                    results.append({
                        "Type fabrikk": type_name,
                        "Antall luftvernmissiler": number_of_air_defense_missiles,
                        "Fabrikk- og luftvernkostnad": facility_and_air_defense_cost,
                        "Ødelagt": results_dict["attack_scenario"][f],
                        "Missilkostnad": results_dict["missile_costs"][f]
                    })
            results_df = pd.DataFrame(results)
            st.subheader("Optimal løsning")
            st.dataframe(
                results_df,
                hide_index=True,
                column_config={
                    "Fabrikk- og luftvernkostnad": st.column_config.NumberColumn(format="localized")
                }
            )
            st.write(f"Gjenværende produksjonskapasitet etter angrep: {results_dict['remaining_production_capacity_after_attack']}")