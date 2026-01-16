import streamlit as st
from ortools.linear_solver import pywraplp
import pandas as pd

def maximize_volume_weighted_missile_cost(prod_facilities, air_defense, restrictions):
    
    # Constants
    p_A = float(air_defense.loc[0, "Suksessrate"]) # Probability of successful interception by an air defense missile
    C_A = int(air_defense.loc[0, "Kostnad per enhet"]) # Cost per air defense missile
    Y_max = int(air_defense.loc[0, "Maks antall enheter per fabrikk"]) # Max number of air defense missiles per facility
    B = int(restrictions.loc[0, "Mengde"]) # Total budget
    K_max = int(restrictions.loc[1, "Mengde"]) # Maximum total production capacity
    F = 0 # Number of potential facilities
    K_f = [] # Production capacity of facility f
    H_f = [] # Number of hits required to destroy facility f
    C_f = [] # Cost of facility f
    type_f = [] # Type of facility f
    for f_type in range(len(prod_facilities)):
        max_units = int(prod_facilities.loc[f_type, "Maks antall enheter"])
        for i in range(max_units):
            F += 1
            K_f.append(float(prod_facilities.loc[f_type, "Produksjonskapasitet"]))
            H_f.append(float(prod_facilities.loc[f_type, "Hardhet"]))
            C_f.append(float(prod_facilities.loc[f_type, "Kostnad per enhet"]))
            type_f.append(prod_facilities.loc[f_type, "Type"])

    # Solver
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')

    # Variables
    x_f = []  # Boolean variable indicating if facility f is built
    y_f = []  # Number of air defense missiles protecting facility f
    for f in range(F):
        x_f.append(solver.BoolVar(f'x_{f}'))
        y_f.append(solver.IntVar(0, Y_max, f'y_{f}'))

    # Constraints
    for f in range(F):
        solver.Add(
            y_f[f] <= Y_max * x_f[f]
        )
    solver.Add(
        solver.Sum([C_f[f] * x_f[f] + C_A * y_f[f] for f in range(F)]) <= B
    )
    solver.Add(
        solver.Sum([K_f[f] * x_f[f] for f in range(F)]) <= K_max
    )

    # Objective:
    solver.Maximize(
        solver.Sum([K_f[f] * (H_f[f] * x_f[f] + p_A * y_f[f]) for f in range(F)])
    )

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        type_counters = {}
        results = []
        total_investment_cost = 0
        total_production_capacity = 0
        for f in range(F):
            factory_built = x_f[f].solution_value() > 0
            if factory_built:
                if type_f[f] not in type_counters:
                    type_counters[type_f[f]] = 0
                type_counters[type_f[f]] += 1
                type_name = f"{type_f[f]} #{type_counters[type_f[f]]}" if type_counters[type_f[f]] > 1 else type_f[f]
                number_of_air_defense_missiles = int(y_f[f].solution_value())
                investment_cost = C_f[f] + C_A * number_of_air_defense_missiles
                missile_cost = H_f[f] + p_A * number_of_air_defense_missiles
                results.append({
                    "Type fabrikk": type_name,
                    "Antall luftvernmissiler": number_of_air_defense_missiles,
                    "Investeringskostnad": investment_cost,
                    "Missilkostnad": missile_cost,
                    "Volumvektet missilkostnad": K_f[f] * missile_cost
                })
                total_investment_cost += investment_cost
                total_production_capacity += K_f[f]
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