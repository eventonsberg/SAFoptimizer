import streamlit as st
import altair as alt
import pandas as pd

def plot_remaining_production_capacity_vs_missile_budget():
    results = st.session_state.varying_missile_budget_results
    missile_budgets = []
    remaining_capacities = []
    for budget, result in results.items():
        missile_budgets.append(budget)
        remaining_capacities.append(result["remaining_production_capacity_after_attack"])
    df = pd.DataFrame({
        "Missilbudsjett": missile_budgets,
        "Gjenværende produksjonskapasitet etter angrep": remaining_capacities
    })
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(
            "Missilbudsjett:Q",
            title="Missilbudsjett",
            axis=alt.Axis(format="d")
        ),
        y=alt.Y(
            "Gjenværende produksjonskapasitet etter angrep:Q",
            title="Produksjonskapasitet"
        ),
        tooltip=["Missilbudsjett", "Gjenværende produksjonskapasitet etter angrep"]
    )
    st.altair_chart(chart)

def plot_facility_configuration_vs_missile_budget(type_f):
    results = st.session_state.varying_missile_budget_results
    data = []
    for budget, result in results.items():
        established = result["established_facilities"]
        air_defense = result["air_defense_assignment"]
        destroyed = result["attack_scenario"]
        for idx, (t, est, ad, dest) in enumerate(zip(type_f, established, air_defense, destroyed)):
            if est:
                data.append({
                    "Missilbudsjett": budget,
                    "Fabrikktype": t,
                    "FabrikkID": f"{t} #{idx+1}",
                    "Antall etablert": 1,
                    "Luftvern": ad,
                    "Ødelagt": dest
                })
    df = pd.DataFrame(data)
    bar = alt.Chart(df).mark_bar(
        strokeWidth=2
    ).encode(
        x=alt.X(
            "Missilbudsjett:O",
            title="Missilbudsjett",
            axis=alt.Axis(labelAngle=0)
        ),
        xOffset=alt.XOffset("Fabrikktype:N"),
        y=alt.Y(
            "Antall etablert:Q",
            title="Antall etablerte fabrikker"
        ),
        color=alt.Color(
            "Fabrikktype:N",
            title="",
            legend=alt.Legend(orient="bottom")
        ),
        order=alt.Order("Ødelagt:O", sort="ascending"),
        stroke=alt.Stroke(
            "Ødelagt:N",
            scale=alt.Scale(domain=[True, False],
                            range=["red", "transparent"]
            ),
            legend=alt.Legend(title="",
                              orient="bottom",
                              values=[True],
                              labelExpr="'True' ? 'Fabrikk ødelagt' : ''"
            )
        ),
        tooltip=["Missilbudsjett", "Fabrikktype", "FabrikkID", "Luftvern", "Ødelagt"]
    )
    st.altair_chart(bar)
    