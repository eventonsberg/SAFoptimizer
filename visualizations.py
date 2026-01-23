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
        for idx, (t, est) in enumerate(zip(type_f, established)):
            if est:
                data.append({
                    "Missilbudsjett": budget,
                    "Fabrikktype": t,
                    "FabrikkID": f"{t} #{idx+1}",
                    "Antall etablert": 1
                })
    df = pd.DataFrame(data)
    chart = alt.Chart(df).mark_bar().encode(
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
            "FabrikkID:N",
            title="FabrikkID",
            legend=None
        ),
        tooltip=["Missilbudsjett", "Fabrikktype", "FabrikkID"]
    )
    st.altair_chart(chart)
    