# Goodwing-Timetabler-Mailer 📅✉️

## 📌 Overview
This folder `Send-Mail-To-Teachers` is an **automated email system** that extracts university timetables from an Excel file and sends personalized emails to professors with their schedules attached. The system **preserves the original Excel formatting**, ensuring a clean and professional timetable delivery.
This functionality can be seen as a **plugin** for the **Goodwing-Timetabler** project, which generates university timetables.

## 🚀 Features
- **Automated professor detection** → Extracts professor names and generates their email.
- **Email generation** → Converts names to email format (`firstname.lastname@devinci.fr`).
- **Accent removal** → Ensures correct email formatting by removing special characters.
- **Timetable extraction** → Filters the Excel file to send only the relevant weeks.
- **Excel formatting preservation** → Keeps styles, colors, and structure.
- **Email automation** → Sends personalized emails with the correct attachments.

---

## To run the code
Please know that for now, **Google service** is used. This means that you can **ONLY** send emails from a **Google account**. 
It can be changed later to Outlook service. 

### **1- Set up your email credentials**
You need to enable "App Passwords" on your Google account to be able to send emails automatically: 
- Go to Google Security
- Enable "2-Step Verification"
- Generate an App Password for "Mail"
- Save this password for later

### **2- Update the code** (`send_emails.py`)
    EMAIL_SENDER = "your.email@gmail.com"  # Replace with your email
    EMAIL_PASSWORD = "your_app_password"  # Replace with your generated app password
