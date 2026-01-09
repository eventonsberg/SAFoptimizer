import pandas as pd

prod_facilities = pd.DataFrame([
    {"Type": "Mongstad", "Kostnad per enhet": 0, "Hardhet": 3.0},
    {"Type": "SAF-anlegg (liten)", "Kostnad per enhet": 20000000, "Hardhet": 3.0},
    {"Type": "SAF-anlegg (stor)", "Kostnad per enhet": 100000000, "Hardhet": 3.0}
])

air_defense = pd.DataFrame([
    {"Type": "Luftvernmissil", "Kostnad per enhet": 5000000, "Suksessrate": 0.7},
])

budget = pd.DataFrame([
    {"Type": "Totalbudsjett", "Beløp": 150000000}
])