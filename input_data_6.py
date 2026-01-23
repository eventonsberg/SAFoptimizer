import pandas as pd

potential_facilities = pd.DataFrame([
    {
        "Type": "Mongstad",
        "Kapasitet": 500,
        "Kostnad": 0,
        "Hardhet": 3.0,
        "Maks antall": 1
    },
    
    {
        "Type": "SAF-anlegg (liten)",
        "Kapasitet": 20,
        "Kostnad": 20000000,
        "Hardhet": 3.0,
        "Maks antall": 12
    },
    {
        "Type": "SAF-anlegg (stor)",
        "Kapasitet": 200,
        "Kostnad": 100000000,
        "Hardhet": 3.0,
        "Maks antall": 2
    }
])

air_defense = pd.DataFrame([
    {
        "Type": "Luftvernmissil",
        "Kostnad": 5000000,
        "Suksessrate": 0.7,
        "Maks antall": 20
    }
])

restrictions = pd.DataFrame([
    {
        "Type": "Missilbudsjett",
        "Mengde": 5
    },
    {
        "Type": "Fabrikk- og luftvernbudsjett",
        "Mengde": 250000000
    }
])

