import json
import os
from datetime import datetime

LOG_PATH = os.path.join("logs", "history.json")


def _initialize_log():
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)


def save_scan(query, detection, risk):

    _initialize_log()

    try:
        with open(LOG_PATH, "r") as f:
            content = f.read().strip()
            history = json.loads(content) if content else []
    except:
        history = []
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "search_type": detection.get("type"),
        "records_found": len(detection.get("records", [])),
        "risk_level": risk.get("level"),
        "risk_score": risk.get("score")
    }

    history.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(history, f, indent=4)


def load_history():
    _initialize_log()

    try:
        with open(LOG_PATH, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except:
        return []