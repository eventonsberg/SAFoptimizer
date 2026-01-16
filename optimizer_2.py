import streamlit as st
from ortools.linear_solver import pywraplp
import pandas as pd

def maximize_volume_weighted_missile_cost(prod_facilities, air_defense, restrictions):
    
    # Constants
    p_A = float(air_defense.loc[0, "Suksessrate"]) # Probability of successful interception by an air defense missile
    C_A = int(air_defense.loc[0, "Kostnad per enhet"]) # Cost per air defense missile
    B = int(restrictions.loc[0, "Mengde"]) # Total budget
    K_max = int(restrictions.loc[1, "Mengde"]) # Maximum total production capacity
    F = len(prod_facilities) # Number of production facility types
    K_f = [] # Production capacity for a facility of type f
    H_f = [] # Number of hits required to destroy a facility of type f
    C_f = [] # Cost per facility of type f
    X_max_f = [] # Maximum number of facilities of type f
    Y_max_f = [] # Maximum number of air defense missiles protecting a facility of type f
    for f in range(F):
        K_f.append(float(prod_facilities.loc[f, "Produksjonskapasitet"]))
        H_f.append(float(prod_facilities.loc[f, "Hardhet"]))
        facility_cost = float(prod_facilities.loc[f, "Kostnad per enhet"])
        C_f.append(facility_cost)
        X_max_f.append(B // facility_cost if facility_cost > 0 else 1) # Handle special case for zero cost facilities, i.e., facilities that already exist (Mongstad)
        Y_max_f.append((B - facility_cost) // C_A if C_A > 0 and B >= facility_cost else 0) # Zero cost air defense is not valid
    Z_max = B // C_A if C_A > 0 else 0 # Maximum total number of air defense missiles

    constans_dict = {
        'p_A': p_A,
        'C_A': C_A,
        'B': B,
        'K_max': K_max,
        'F': F,
        'K_f': K_f,
        'H_f': H_f,
        'C_f': C_f,
        'X_max_f': X_max_f,
        'Y_max_f': Y_max_f,
        'Z_max': Z_max
    }
    #st.write(constans_dict) # Uncomment this to display constant values

    # Solver
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')

    # Variables
    x_f = []  # Number of production facilities of type f
    y_f = []  # Number of air defense missiles protecting a facility of type f
    z_f = []  # Total number of air defense missiles protecting facilities of type f
    for f in range(F):
        x = solver.IntVar(0, X_max_f[f], f'x_{f}')
        y = solver.IntVar(0, Y_max_f[f], f'y_{f}')
        z = solver.IntVar(0, Z_max, f'z_{f}')
        x_f.append(x)
        y_f.append(y)
        z_f.append(z)

    # Constraints
    solver.Add(
        solver.Sum([C_f[f] * x_f[f] + C_A * z_f[f] for f in range(F)]) <= B
    )
    solver.Add(
        solver.Sum([K_f[f] * x_f[f] for f in range(F)]) <= K_max
    )
    for f in range(F):
        solver.Add(
            z_f[f] <= x_f[f] * Y_max_f[f]
        )
        solver.Add(
            z_f[f] <= X_max_f[f] * y_f[f]
        )
        solver.Add(
            z_f[f] >= x_f[f] * Y_max_f[f] + X_max_f[f] * y_f[f] - X_max_f[f] * Y_max_f[f]
        )

    # Objective:
    solver.Maximize(
        solver.Sum([K_f[f] * (H_f[f] * x_f[f] + p_A * z_f[f]) for f in range(F)])
    )

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        results = []
        total_investment_cost = 0
        total_production_capacity = 0
        for f in range(F):
            facility = prod_facilities.loc[f, "Type"]
            number_of_facilities = int(x_f[f].solution_value())
            air_defense_missiles_total = int(z_f[f].solution_value())
            investment_cost = C_f[f] * number_of_facilities + C_A * air_defense_missiles_total
            missile_cost_total = H_f[f] * number_of_facilities + p_A * air_defense_missiles_total
            production_capacity = K_f[f] * number_of_facilities
            volume_weighted_missile_cost = production_capacity * missile_cost_total
            results.append({
                "Type fabrikk": facility,
                "Antall fabrikker": number_of_facilities,
                "Totalt antall luftvernmissiler": air_defense_missiles_total,
                "Investeringskostnad": investment_cost,
                "Missilkostnad": missile_cost_total,
                "Produksjonskapasitet": production_capacity,
                "Volumvektet missilkostnad": volume_weighted_missile_cost
            })
            total_investment_cost += investment_cost
            total_production_capacity += K_f[f] * number_of_facilities
        results_df = pd.DataFrame(results)
        st.subheader("Optimal løsning")
        st.dataframe(
            results_df,
            hide_index=True,
            column_config={
                "Investeringskostnad": st.column_config.NumberColumn(format="localized")
            }
        )
        if total_investment_cost < B:
            leftover_budget = B - total_investment_cost
            st.write(f'Total investeringskostnad: {total_investment_cost:,.0f} :orange-badge[Ubrukte midler: {leftover_budget:,.0f}]')
        else:
            st.write(f'Total investeringskostnad: {total_investment_cost:,.0f}')
        st.write(f'Total produksjonskapasitet: {total_production_capacity:,.0f}')
        st.write(f'Total volumvektet missilkostnad: {solver.Objective().Value():,.1f}')