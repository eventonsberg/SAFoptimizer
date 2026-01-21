import pandas as pd

potential_facilities = pd.DataFrame([
    {
        "Type": "Mongstad",
        "Etablert": True,
        "Kapasitet": 500,
        "Kostnad": 0,
        "Hardhet": 3.0,
        "Luftvern": 6
    },
    {
        "Type": "SAF-anlegg (liten)",
        "Etablert": True,
        "Kapasitet": 20,
        "Kostnad": 20000000,
        "Hardhet": 3.0,
        "Luftvern": 0
    },
    {
        "Type": "SAF-anlegg (liten) #2",
        "Etablert": True,
        "Kapasitet": 20,
        "Kostnad": 20000000,
        "Hardhet": 3.0,
        "Luftvern": 0
    },
    {
        "Type": "SAF-anlegg (liten) #3",
        "Etablert": False,
        "Kapasitet": 20,
        "Kostnad": 20000000,
        "Hardhet": 3.0,
        "Luftvern": 0
    },
    {
        "Type": "SAF-anlegg (stor)",
        "Etablert": False,
        "Kapasitet": 200,
        "Kostnad": 100000000,
        "Hardhet": 3.0,
        "Luftvern": 0
    }
])

air_defense = pd.DataFrame([
    {
        "Type": "Luftvernmissil",
        "Kostnad": 5000000,
        "Suksessrate": 0.7
    },
])

restrictions = pd.DataFrame([
    {
        "Type": "Missilbudsjett",
        "Mengde": 5
    }
])

