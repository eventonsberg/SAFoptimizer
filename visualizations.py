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
    # For each missile budget, count established facilities per type
    for budget, result in results.items():
        established = result["established_facilities"]
        type_counts = {}
        for t, est in zip(type_f, established):
            if est:
                type_counts[t] = type_counts.get(t, 0) + 1
        for t in set(type_f):
            data.append({
                "Missilbudsjett": budget,
                "Fabrikktype": t,
                "Antall etablert": type_counts.get(t, 0)
            })

    df = pd.DataFrame(data)
    max_y = int(df["Antall etablert"].max()) if not df.empty else 1
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(
            "Missilbudsjett:O",
            title="Missilbudsjett",
            axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y(
            "Antall etablert:Q",
            title="Antall etablerte fabrikker",
            axis=alt.Axis(
                values=list(range(0, max_y + 1)),
                format='d'
            )
        ),
        color=alt.Color(
            "Fabrikktype:N",
            title="Fabrikktype",
            legend=alt.Legend(orient="bottom")
        ),
        xOffset="Fabrikktype:N",
        tooltip=["Missilbudsjett", "Fabrikktype", "Antall etablert"]
    )
    st.altair_chart(chart)
    