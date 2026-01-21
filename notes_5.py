import streamlit as st

def display_notes():
    st.markdown(
        """
        Rød aktør ønsker å minimere blå sin produksjonskapasitet.
        Modellen beregner hvilke av de etablerte fabrikkene som bør ødelegges
        gitt et begrenset antall missiler til disposisjon.
    """
    )

    st.subheader("Objektivfunksjon")
    st.latex(r"""
    \min_d\;\; \sum_{f\in F} K_f\, e_f\, (1 - d_f)
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $K_f$  | Produksjonskapasiteten til fabrikk $f$ |
    | $e_f$  | Boolsk variabel som indikerer om fabrikk $f$ er etablert |
    | $d_f$  | Boolsk variabel som indikerer om fabrikk $f$ er ødelagt |
    | $F$    | Potensielle fabrikker |
    """
    )

    st.subheader("Begrensninger")
    st.latex(r"""
    d_f \leq e_f \quad \forall f \in F
    """)
    st.latex(r"""
    \sum_{f\in F} \big( H_f + P_A\, a_f \big) d_f \leq B_R
    """)
    st.markdown(
        """
    | Parameter | Forklaring |
    |--------|------------|
    | $H_f$  | Antall treff som kreves for å ødelegge fabrikk $f$ |
    | $P_A$  | Sannsynligheten for at et luftvernmissil slår ut et innkommende missil |
    | $a_f$  | Antall luftvernmissiler som beskytter fabrikk $f$ |
    | $B_R$  | Budsjettet til rød, i form av antall missiler til disposisjon |
    """
    )
    
    


