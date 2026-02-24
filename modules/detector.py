import pandas as pd

def search_breaches(query):
    data = pd.read_csv("data/breaches.csv")

    matches = data[data['email'].str.contains(query, case=False, na=False)]

    if matches.empty:
        return None

    return matches.to_dict(orient="records")