from modules.detector import detect_query
from modules.risk_engine import calculate_risk

query = input("Enter email or domain: ")

detection = detect_query(query)
risk = calculate_risk(detection)

print("\nDetection:")
print(detection)

print("\nRisk Analysis:")
print(risk)