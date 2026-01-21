import streamlit as st

def display_notes():
    st.subheader("Objektivfunksjon")
    st.latex(r"""
    \max_{x_f,\, y_f}\;\; \sum_{f\in F} K_f \big( H_f\, x_f + p_A\, y_f \big)
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $K_f$  | Produksjonskapasiteten til fabrikk $f$ |
    | $H_f$  | Antall treff som kreves for å ødelegge fabrikk $f$ |
    | $x_f$  | Boolsk variabel som indikerer om fabrikk $f$ er etablert eller ikke |
    | $p_A$  | Sannsynligheten for at et luftvernmissil slår ut et innkommende missil |
    | $y_f$  | Antall luftvernmissiler som beskytter fabrikk $f$ |
    | $F$    | Potensielle fabrikker |
    """
    )

    st.subheader("Begrensninger")
    st.latex(r"""
    y_f \leq Y^{\max} \, x_f \quad \forall f \in F
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $Y^{\max}$ | Maksimalt antall luftvernmissiler som kan beskytte en fabrikk |
    """
    )
    st.latex(r"""
    \sum_{f\in F} \big( C_f\, x_f + C_A\, y_f \big) \leq B
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $C_f$  | Kostnaden for fabrikk $f$ |
    | $C_A$  | Kostnaden for et luftvernmissil |
    | $B$    | Totalt budsjett |
    """
    )
    st.latex(r"""
    \sum_{f\in F} K_f\, x_f \leq K^{\max}
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $K^{\max}$ | Maksimal total produksjonskapasitet |
    """
    )
    


