import streamlit as st
import pandas as pd
from input_data_6 import potential_facilities, air_defense, restrictions
from optimizer_6 import generate_model_inputs, solve_interdiction
from visualizations import (
    plot_remaining_production_capacity_vs_missile_budget,
    plot_facility_configuration_vs_missile_budget
)

def display_tab_7():
    st.subheader("Potensielle fabrikker")
    potential_facilities_edited =st.data_editor(
        potential_facilities,
        num_rows="dynamic",
        column_config={
            "Kostnad": st.column_config.NumberColumn(format="localized")
        },
        key="prod_facilities_7"
    )

    st.subheader("Luftvern")
    air_defense_edited = st.data_editor(
        air_defense,
        hide_index=True,
        column_config={
            "Kostnad": st.column_config.NumberColumn(format="localized")
        },
        key="air_defense_7"
    )

    st.subheader("Begrensninger")
    restrictions_copy = restrictions.copy()
    restrictions_copy.iloc[0, 0] = "Missilbudsjett (SETTES MED SLIDER NEDENFOR)"
    restrictions_copy.iloc[0, 1] = None # Given by slider input
    restrictions_edited = st.data_editor(
        restrictions_copy,
        hide_index=True,
        column_config={
            "Mengde": st.column_config.NumberColumn(format="localized")
        },
        key="restrictions_7"
    )
    restrictions_edited.iloc[0, 0] = "Missilbudsjett"

    st.subheader("Missilbudsjett")
    missile_budget_range = st.slider(
        "Velg variasjon for missilbudsjett:",
        min_value=0,
        max_value=50,
        value=(0, 10)
    )

    if "current_iteration" not in st.session_state:
        st.session_state.current_iteration = 0
    if "varying_missile_budget_results" not in st.session_state:
        st.session_state.varying_missile_budget_results = {}

    if st.button("Kjør optimering", type="primary", key="run_optimization_7"):
        st.session_state.varying_missile_budget_results = {}
        iteration_placeholder = st.empty()
        st.subheader("Gjenværende produksjonskapasitet etter angrep")
        chart1_placeholder = st.empty()
        st.subheader("Fabrikkonfigurasjon")
        chart2_placeholder = st.empty()
        for missile_budget in range(missile_budget_range[0], missile_budget_range[1] + 1):
            restrictions_edited.loc[0, "Mengde"] = missile_budget
            P_A, C_A, A_max, B_R, B_B, F, type_f, K_f, H_f, C_f = generate_model_inputs(potential_facilities_edited, air_defense_edited, restrictions_edited)
            result = solve_interdiction(P_A, C_A, A_max, B_R, B_B, F, type_f, K_f, H_f, C_f, iteration_placeholder=iteration_placeholder)
            if result["status"] != "OPTIMAL":
                st.warning(f"Løsningen for missilbudsjett {missile_budget} ikke funnet. Status: {result['status']}")
                return
            st.session_state.varying_missile_budget_results[missile_budget] = result
            with chart1_placeholder:
                plot_remaining_production_capacity_vs_missile_budget()
            with chart2_placeholder:
                plot_facility_configuration_vs_missile_budget(type_f)

