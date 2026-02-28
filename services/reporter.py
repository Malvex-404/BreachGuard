from fpdf import FPDF
import os
from datetime import datetime

REPORT_DIR = "reports"


def generate_report(query, detection, risk):
    """
    Generates a PDF breach intelligence report.
    """

    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    filename = f"report_{query.replace('@','_').replace('.','_')}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BreachGuard Intelligence Report", ln=True)

    pdf.ln(5)

    # Metadata
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Query: {query}", ln=True)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(8)

    # Detection Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Breach Summary", ln=True)

    pdf.set_font("Arial", size=12)

    if not detection["found"]:
        pdf.cell(0, 8, "No breach records detected.", ln=True)
    else:
        for record in detection["records"]:
            pdf.cell(0, 8, f"Email: {record['email']}", ln=True)
            pdf.cell(0, 8, f"Breach: {record['breach']}", ln=True)
            pdf.cell(0, 8, f"Date: {record['breach_date']}", ln=True)
            pdf.cell(0, 8, f"Attack Type: {record['attack_type']}", ln=True)
            pdf.cell(0, 8, f"Data Exposed: {record['data_exposed']}", ln=True)
            pdf.cell(0, 8, f"Password Status: {record['password_status']}", ln=True)

            if record["password_display"]:
                pdf.cell(0, 8, f"Password Hint: {record['password_display']}", ln=True)

            pdf.ln(4)

    pdf.ln(5)

    # Risk Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Risk Assessment", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Risk Level: {risk['level']}", ln=True)
    pdf.cell(0, 8, f"Risk Score: {risk['score']}", ln=True)

    pdf.ln(5)

    for reason in risk["reasons"]:
        pdf.multi_cell(0, 8, f"- {reason}")

    pdf.output(filepath)

    return filepath