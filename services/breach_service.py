from services.breach_loader import load_data
from services.password_utils import mask_password

def detect_query(query):
    """
    Detects breach records for an email or domain.
    """

    if not query:
        raise ValueError("Query cannot be empty.")

    query = query.lower().strip()

    df = load_data()

    # Determine search type
    if "@" in query:
        # Email search
        results = df[df["email"] == query]
        search_type = "email"
    else:
        # Domain search
        results = df[df["domain"] == query]
        search_type = "domain"

    if results.empty:
        return {
            "found": False,
            "type": search_type,
            "records": []
        }

    formatted_records = []

    for _, row in results.iterrows():
        password_info = mask_password(
            row["password_hint"],
            row["password_exposed"]
        )
        
        formatted_records.append({
            "email": row["email"],
            "domain": row["domain"],
            "breach": row["breach"],
            "breach_date": row["breach_date"],
            "attack_type": row["attack_type"],
            "data_exposed": row["data_exposed"],
            "password_status": password_info["status"],
            "password_display": password_info["display"]
        })

    return {
        "found": True,
        "type": search_type,
        "count": len(formatted_records),
        "records": formatted_records
    }