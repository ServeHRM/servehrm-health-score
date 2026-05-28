import streamlit as st
import pandas as pd
import os

query_params = st.query_params
show_admin = query_params.get("admin") == "true"

admin_password = ""

if show_admin:
    with st.sidebar:
        st.header("Admin Access")
        admin_password = st.text_input(
            "Enter Admin Password",
            type="password"
        )

import tempfile
import urllib.parse
import smtplib
from email.message import EmailMessage

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def send_email_with_pdf(to_email, company, pdf_path):
    sender_email = "a9cc57001@smtp-brevo.com"
    brevo_smtp_key = "xsmtpsib-f1313fa970cfd34d85ae67686a9e2dad42472c4a93f016be8fd7091bd65bdd71-7PdP1fV2OZsFvrm3"

    subject = "Your Preliminary HR Health Report - ServeHRM"    
    body = f"""
Dear {company} Team,

Thank you for completing the Phase-1 Preliminary HR Health Checkup.

Please find attached your Preliminary HR Health Report.

This is only a preliminary report. To identify hidden HR, payroll, labour law, compliance, employee documentation, and productivity risks, we recommend booking a Phase-2 Comprehensive HR Health Checkup.

Regards,
MVS HR Advisory Solutions
ServeHRM
Website: servehrm.com
"""

    msg = EmailMessage()
    msg["From"] = "support@servehrm.com"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(pdf_path, "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype="application",
            subtype="pdf",
            filename=f"{company}_Preliminary_HR_Health_Report.pdf",
        )

    with smtplib.SMTP("smtp-relay.brevo.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, brevo_smtp_key)
        smtp.send_message(msg)


st.title("ServeHRM Preliminary HR Health Score")
st.write("Powered by MVS HR Advisory Solutions")
st.header("Phase-1: Free Preliminary HR Health Check for Startups & MSMEs")

st.info(
    "This is a quick preliminary HR health check. "
    "For detailed labour law, payroll, compliance, documentation, and productivity risks, "
    "book a Phase-2 Comprehensive HR Health Checkup call."
)

st.header("Company Details")

company = st.text_input("Enter Company Name")
contact_person = st.text_input("Contact Person Name")
mobile = st.text_input("Mobile Number")
email = st.text_input("Email ID")
city = st.text_input("City / Location")
employees = st.number_input("Number of Employees", min_value=1, step=1)

industry = st.selectbox(
    "Select Industry",
    ["Manufacturing", "Pharma", "IT", "Retail", "Construction", "Services", "Other"],
)

st.header("Phase-1 Preliminary HR Parameters")

appointment_letters = st.slider("Appointment Letters / Offer Letters", 0, 10)
attendance = st.slider("Attendance & Leave Tracking", 0, 10)
payroll = st.slider("Payroll Accuracy", 0, 10)
compliance = st.slider("PF / ESI / Labour Law Awareness", 0, 10)
employee_records = st.slider("Employee Records & Documentation", 0, 10)

total = appointment_letters + attendance + payroll + compliance + employee_records
score_percentage = int((total / 50) * 100)

st.subheader(f"Preliminary HR Health Score: {score_percentage}/100")
st.progress(score_percentage / 100)

if score_percentage >= 80:
    risk_level = "Low Preliminary HR Risk"
    recommendation = (
        "Your basic HR systems appear reasonably strong. However, a Phase-2 Comprehensive "
        "HR Health Checkup can identify hidden risks and improvement opportunities."
    )
    st.success(risk_level)

elif score_percentage >= 50:
    risk_level = "Moderate Preliminary HR Risk"
    recommendation = (
        "Your HR system needs improvement in documentation, compliance tracking, payroll discipline, "
        "and structured HR processes. A Phase-2 Comprehensive HR Health Checkup is recommended."
    )
    st.warning(risk_level)

else:
    risk_level = "High Preliminary HR Risk"
    recommendation = (
        "Your organization may have serious HR, payroll, documentation, and compliance risks. "
        "Please book a Phase-2 Comprehensive HR Health Checkup immediately."
    )
    st.error(risk_level)

st.info(recommendation)

dynamic_recommendations = []

if appointment_letters < 5:
    dynamic_recommendations.append(
        "Appointment letters and offer letters need improvement. Ensure every employee has a properly issued appointment letter with role, salary, working hours, leave, notice period, and compliance terms."
    )

if attendance < 5:
    dynamic_recommendations.append(
        "Attendance and leave tracking require immediate attention. Maintain accurate attendance records, leave balances, approvals, and monthly reconciliation before payroll processing."
    )

if payroll < 5:
    dynamic_recommendations.append(
        "Payroll accuracy needs improvement. Salary structure, attendance linkage, deductions, PF/ESI applicability, and monthly payroll checking should be reviewed."
    )

if compliance < 5:
    dynamic_recommendations.append(
        "PF, ESI, and labour law compliance awareness appears weak. Review statutory applicability, due dates, employee eligibility, contribution records, and compliance documentation."
    )

if employee_records < 5:
    dynamic_recommendations.append(
        "Employee records and documentation need strengthening. Maintain KYC, education records, appointment letters, salary details, attendance, leave, increments, warnings, and exit documents."
    )

if not dynamic_recommendations:
    dynamic_recommendations.append(
        "No major weakness is identified in the preliminary check. However, a Phase-2 Comprehensive HR Health Checkup is recommended to identify hidden HR and compliance risks."
    )

st.header("Preliminary HR Recommendations")

for rec in dynamic_recommendations:
    st.warning(rec)

phase2_cta = (
    "This is only a Phase-1 Preliminary HR Health Score. "
    "Book a Phase-2 Comprehensive HR Health Checkup with MVS HR Advisory Solutions "
    "to identify hidden HR, labour law, payroll, compliance, employee documentation, "
    "and productivity risks."
)

st.header("Next Step")
st.success(phase2_cta)

if st.button("Generate Preliminary HR Health Report"):

    if (
        company.strip() == ""
        or contact_person.strip() == ""
        or mobile.strip() == ""
        or email.strip() == ""
        or city.strip() == ""
    ):
        st.error("Please enter complete company records to get the HR Health Report.")

    else:
        st.success("Preliminary HR Health Report Generated Successfully.")

        st.header("Company Summary")
        st.write(f"Company Name: {company}")
        st.write(f"Contact Person: {contact_person}")
        st.write(f"Mobile: {mobile}")
        st.write(f"Email: {email}")
        st.write(f"City / Location: {city}")
        st.write(f"Employees: {employees}")
        st.write(f"Industry: {industry}")
        st.write(f"Preliminary HR Health Score: {score_percentage}/100")
        st.write(f"Risk Level: {risk_level}")
        st.write(f"Recommendation: {recommendation}")

        st.subheader("Dynamic HR Improvement Recommendations")
        for rec in dynamic_recommendations:
            st.write(f"- {rec}")

        lead_data = {
            "Company Name": [company],
            "Contact Person": [contact_person],
            "Mobile": [mobile],
            "Email": [email],
            "City": [city],
            "Employees": [employees],
            "Industry": [industry],
            "HR Score": [score_percentage],
            "Risk Level": [risk_level],
            "Recommendation": [recommendation],
            "Dynamic Recommendations": [" | ".join(dynamic_recommendations)],
            "Lead Status": ["New Lead"],
            "Follow-up Date": [""],
            "Consultation Booked": ["No"],
            "Remarks": [""],
        }

        df = pd.DataFrame(lead_data)
        file_name = "hr_leads.csv"

        if os.path.exists(file_name):
            df.to_csv(file_name, mode="a", header=False, index=False)
        else:
            df.to_csv(file_name, index=False)

        whatsapp_message = f"""
Hello MVS HR Advisory Solutions,

We completed the Phase-1 Preliminary HR Health Score.

Company Name: {company}
Contact Person: {contact_person}
Industry: {industry}
Employees: {employees}
Preliminary HR Health Score: {score_percentage}/100
Risk Level: {risk_level}

We would like to book a Phase-2 Comprehensive HR Health Checkup consultation.
"""

        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_number = "919951451466"
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

        st.link_button("Book Phase-2 HR Health Checkup on WhatsApp", whatsapp_url)

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        doc = SimpleDocTemplate(temp_pdf.name, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("ServeHR Preliminary HR Health Report", styles["Title"]))
        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                "Phase-1 Free Preliminary HR Health Score for Startups & MSMEs",
                styles["Heading2"],
            )
        )
        content.append(Spacer(1, 12))

        details = [
            f"<b>Company Name:</b> {company}",
            f"<b>Contact Person:</b> {contact_person}",
            f"<b>Mobile:</b> {mobile}",
            f"<b>Email:</b> {email}",
            f"<b>City:</b> {city}",
            f"<b>Employees:</b> {employees}",
            f"<b>Industry:</b> {industry}",
            f"<b>Preliminary HR Health Score:</b> {score_percentage}/100",
            f"<b>Risk Level:</b> {risk_level}",
            f"<b>Overall Recommendation:</b> {recommendation}",
        ]

        for item in details:
            content.append(Paragraph(item, styles["BodyText"]))
            content.append(Spacer(1, 10))

        content.append(Spacer(1, 16))
        content.append(Paragraph("Dynamic HR Improvement Recommendations", styles["Heading2"]))

        for rec in dynamic_recommendations:
            content.append(Paragraph(f"- {rec}", styles["BodyText"]))
            content.append(Spacer(1, 8))

        content.append(Spacer(1, 16))
        content.append(Paragraph("Next Step", styles["Heading2"]))
        content.append(Paragraph(phase2_cta, styles["BodyText"]))

        content.append(Spacer(1, 20))
        content.append(
            Paragraph(
                "<b>MVS HR Advisory Solutions</b><br/>"
                "Book Phase-2 Comprehensive HR Health Checkup<br/>"
                "Website: mvshradvisory.com | ServeHRM: servehrm.com",
                styles["BodyText"],
            )
        )

        doc.build(content)

        try:
            send_email_with_pdf(email, company, temp_pdf.name)
            st.success("Preliminary HR Health Report has been emailed successfully.")

        except Exception as e:
            st.warning("PDF generated successfully, but email could not be sent.")
            st.write(e)

        with open(temp_pdf.name, "rb") as pdf_file:
            st.download_button(
                label="Download Preliminary HR Health Report PDF",
                data=pdf_file,
                file_name=f"{company}_Preliminary_HR_Health_Report.pdf",
                mime="application/pdf",
            )

st.divider()

if admin_password == "mvs123":

    st.header("Internal HR Lead Analytics Dashboard")

    if os.path.exists("hr_leads.csv"):
        leads_df = pd.read_csv("hr_leads.csv", on_bad_lines="skip")

        required_columns = {
            "Lead Status": "New Lead",
            "Follow-up Date": "",
            "Consultation Booked": "No",
            "Remarks": "",
        }

        for column, default_value in required_columns.items():
            if column not in leads_df.columns:
                leads_df[column] = default_value

        st.subheader("Lead Summary")

        total_leads = len(leads_df)
        average_score = round(leads_df["HR Score"].mean(), 2)

        high_risk = len(leads_df[leads_df["Risk Level"] == "High Preliminary HR Risk"])
        moderate_risk = len(leads_df[leads_df["Risk Level"] == "Moderate Preliminary HR Risk"])
        consultation_booked = len(leads_df[leads_df["Consultation Booked"] == "Yes"])

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Leads", total_leads)
        col2.metric("Average Score", average_score)
        col3.metric("High Risk", high_risk)
        col4.metric("Moderate Risk", moderate_risk)
        col5.metric("Consultations", consultation_booked)

        st.subheader("Lead Management CRM")

        edited_df = st.data_editor(
            leads_df,
            width="stretch",
            num_rows="dynamic",
            column_config={
                "Lead Status": st.column_config.SelectboxColumn(
                    "Lead Status",
                    options=[
                        "New Lead",
                        "Contacted",
                        "Follow-up Pending",
                        "Consultation Booked",
                        "Converted Client",
                        "Not Interested",
                    ],
                ),
                "Consultation Booked": st.column_config.SelectboxColumn(
                    "Consultation Booked",
                    options=["Yes", "No"],
                ),
            },
        )

        if st.button("Save Lead Updates"):
            edited_df.to_csv("hr_leads.csv", index=False)
            st.success("Lead updates saved successfully.")

        st.subheader("Industry-wise Leads")
        industry_count = leads_df["Industry"].value_counts().sort_values(ascending=False)
        st.bar_chart(industry_count)

        st.subheader("Risk-wise Leads")
        risk_count = leads_df["Risk Level"].value_counts().sort_values(ascending=False)
        st.bar_chart(risk_count)

        st.subheader("Lead Status-wise Summary")
        status_count = leads_df["Lead Status"].value_counts().sort_values(ascending=False)
        st.bar_chart(status_count)

    else:
        st.info("No leads found yet. Generate HR Health Reports to create lead records.")

elif admin_password != "":
    st.error("Invalid admin password.")