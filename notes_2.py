import streamlit as st

def display_notes_2():
    st.markdown(
        """
        Et naturlig neste steg er å maksimere volumvektet missilkostnad,
        for å gjøre det så kostbart som mulig å sette store produksjonsmengder ut av spill.
        Dette oppnås ved å gange med produksjonskapasiteten til hver fabrikk i objektivfunksjonen.
        """
    )

    st.subheader("Objektivfunksjon")
    st.latex(r"""
    \max_{x_f,\, z_f}\;\; \sum_{f=1}^{F} K_f \,\big( H_f\, x_f + p_A\, z_f \big)
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $K_f$  | Produksjonskapasiteten til en fabrikk av typen $f$ |
    | $H_f$  | Antall treff som kreves for å ødelegge en fabrikk av typen $f$ |
    | $x_f$  | Antall fabrikker av typen $f$ |
    | $p_A$  | Sannsynligheten for at et luftvernmissil slår ut et innkommende missil |
    | $z_f$  | Totalt antall luftvernmissiler som beskytter fabrikker av typen $f$ |
    | $F$    | Antall ulike typer fabrikker |
    """
    )

    st.subheader("Begrensninger")
    st.latex(r"""
    \sum_{f=1}^{F} \Big( C_f\, x_f + C_A\, z_f \Big) \;\le\; B
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

    st.latex(r"""
    \sum_{f=1}^{F} K_f \, x_f \;\le\; K^{\max}
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $K^{\max}$ | Maksimal total produksjonskapasitet |
    """
    )

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
    | $y_f$  | Antall luftvernmissiler som beskytter en fabrikk av typen $f$ |
    | $Y_f^{\\max}$  | Maksimalt antall luftvernmissiler som kan beskytte en fabrikk av typen $f$ |
    """
    )