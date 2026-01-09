import streamlit as st

def display_notes_1():
    st.markdown("""
        Ønsker å maksimere kostnaden -- i form av antall missiler -- som kreves for å ødelegge samtlige drivstoffabrikker
    """)
    
    st.subheader("Objektivfunksjon")
    st.latex(r"""
    \max_{x_f,\, y_f}\;\; \sum_{f=1}^{F} x_f \,\big( H_f + p_A\, y_f \big)
    """)

    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $x_f$  | Antall fabrikker av typen $f$ |
    | $H_f$  | Antall treff som kreves for å ødelegge en fabrikk av typen $f$ |
    | $p_A$  | Sannsynligheten for at et luftvernmissil slår ut et innkommende missil |
    | $y_f$  | Antall luftvernmissiler som beskytter en fabrikk av typen $f$ |
    | $F$    | Antall ulike typer fabrikker |
    """
    )

    st.subheader("Begrensninger")
    st.latex(r"""
    \sum_{f=1}^{F} x_f \,\big( C_f + C_A\, y_f \big) \;\le\; B
    """)

    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $C_f$ | Kostnaden til fabrikker av typen $f$  |
    | $C_A$ | Kostnaden til luftvernmissiler  |
    | $B$   | Totalt budsjett |
    """
    )

    st.warning(
        """
        Utfordringen over er at dette er et ikke-lineært problem, på grunn av produktet $x_f \\cdot y_f$.
        Ønsker å linearisere problemet for å kunne løse det med en lineær solver fra OR-Tools i Python.
    """)

    st.markdown("For å linearisere problemet introduserer vi variabelen:")
    st.latex(r"""
    z_f = x_f\, y_f
    """)
    st.markdown("Da kan objektivfunksjonen og begrensninger formuleres som følger:")

    st.subheader("Objektivfunksjon")
    st.latex(r"""
    \max_{x_f,\, z_f}\;\; \sum_{f=1}^{F} \Big( H_f\, x_f + p_A\, z_f \Big)
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $z_f$  | Totalt antall luftvernmissiler som beskytter fabrikker av typen $f$ |
    """
    )

    st.subheader("Begrensninger")
    st.latex(r"""
    \sum_{f=1}^{F} \Big( C_f\, x_f + C_A\, z_f \Big) \;\le\; B
    """)

    st.markdown("Vi lineariserer $z_f$ med bruk av 'McCormick envelopes':")
    st.latex(r"""
    0 \le x_f \le X_f^{\max}
    """)
    st.latex(r"""
    0 \le y_f \le Y_f^{\max}
    """)
    st.latex(r"""
    z_f \ge 0
    """)
    st.latex(r"""
    z_f \le x_f\, Y_f^{\max}
    """)
    st.latex(r"""
    z_f \le X_f^{\max}\, y_f
    """)
    st.latex(r"""
    z_f \ge X_f^{\max}\, y_f + x_f\, Y_f^{\max} - X_f^{\max}\, Y_f^{\max}
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $X_f^{\\max}$  | Maksimalt antall fabrikker av typen $f$ |
    | $Y_f^{\\max}$  | Maksimalt antall luftvernmissiler som kan beskytte en fabrikk av typen $f$ |
    """
    )

    st.markdown(
        """
    Valg av $X_f^{\\max}$ og $Y_f^{\\max}$ er kritisk.
    Jo strammere og mer realistiske de er, jo raskere og bedre vil modellen fungere.
    En enkel måte å sette verdiene på er:
    """
    )
    st.latex(r"""
    X_f^{\max} \;=\; \left\lfloor \frac{B}{C_f} \right\rfloor
    """)
    st.latex(r"""
    Y_f^{\max} \;=\; \left\lfloor \frac{B - C_f}{C_A} \right\rfloor
    """)


