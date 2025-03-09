import os
import streamlit as st
import shutil
import atexit
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns



# Load the Text file
text_file_name = "intelligence_report.txt" # Name of the Text file

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) # Find the root directory of the project dynamically
file_path = os.path.join(project_root, "Goodwing-Timetabler", "Outputs", text_file_name) # Construct the correct absolute path
file_path = file_path.replace("\\", "/") # Ensure forward slashes for Windows compatibility


# Define storage folder for previous reports
history_folder = os.path.join(project_root, "Frontend", "Intelligence-Report", "Reports-History")


# Define lock file to prevent duplicate execution
lock_file = os.path.join(history_folder, "current_session.lock")

# Function to remove the lock file when Streamlit stops
def cleanup_lock_file():
    if os.path.exists(lock_file):
        os.remove(lock_file)
atexit.register(cleanup_lock_file)


# Function to get the latest report version
def get_latest_version():
    """Returns the latest version number of intelligence reports."""
    existing_files = [f for f in os.listdir(history_folder) if f.startswith("intelligence_report_v") and f.endswith(".txt")]
    version_numbers = [int(f.split("_v")[-1].split(".txt")[0]) for f in existing_files if f.split("_v")[-1].split(".txt")[0].isdigit()]
    return max(version_numbers) if version_numbers else 0


# Function to store the report with versioning
def store_previous_report():
    """Saves intelligence_report.txt as intelligence_report_vX.txt if not already stored in this session."""

    if os.path.exists(lock_file):
        return None  # If lock file exists, DO NOT create a new report (prevents duplication)

    latest_version = get_latest_version()
    new_version = latest_version + 1
    new_file_name = f"intelligence_report_v{new_version}.txt"
    new_file_path = os.path.join(history_folder, new_file_name)

    # Create new report version
    shutil.copy(file_path, new_file_path)

    # Create lock file to prevent multiple report creations in this session
    with open(lock_file, "w") as lock:
        lock.write(f"Session Report Version: {new_version}")

# Store report only once per execution using lock file
store_previous_report()


# Function to load a selected report
def load_intelligence_report(report_file):
    """Reads the selected intelligence report file."""
    if os.path.exists(report_file):
        with open(report_file, "r") as file:
            return file.read()
    else:
        return "Intelligence Report not found!"


# Get list of available reports DESCENDING order
available_reports = sorted(
    [f for f in os.listdir(history_folder) if f.startswith("intelligence_report_v") and f.endswith(".txt")],
    key=lambda x: int(x.split("_v")[-1].split(".txt")[0]),
    reverse=True  # Show the latest report first
)

# Get list of available reports ASCENDING order
available_reports_asc = sorted(
    [f for f in os.listdir(history_folder) if f.startswith("intelligence_report_v") and f.endswith(".txt")],
    key=lambda x: int(x.split("_v")[-1].split(".txt")[0]),
    reverse=False  # Show the latest report last
)



# Streamlit UI
st.set_page_config(page_title="Scheduling Intelligence Report", layout="wide")

st.title("Scheduling Intelligence Report")
st.markdown("---")


# Sidebar Navigation
pages = {
    "📜 **Overview**": "==== SCHEDULING INTELLIGENCE REPORT ====",
    "⚠️ Conflict Analysis": "1. CONFLICT ANALYSIS",
    "📈 Resource Utilization": "2. RESOURCE UTILIZATION",
    "⏳ Timeslot Distribution": "3. TIMESLOT DISTRIBUTION",
    "🚨 Penalty Breakdown": "4. PENALTY BREAKDOWN",
    "🌐 Online-Physical Transitions": "5. ONLINE-PHYSICAL TRANSITIONS",
    "🌙 Late Timeslot Analysis": "6. LATE TIMESLOT ANALYSIS",
    "✅ **Summary**": "==== END OF INTELLIGENCE REPORT ====",
    "📂 **View Past Reports**": None  
}

selected_page = st.sidebar.radio("🔍 Select a section:", list(pages.keys()))


# Overview section
if selected_page == "📜 **Overview**":
    st.subheader("📜 **Overview**")
    st.markdown(
        """
        The **Scheduling Intelligence Report** is designed to analyze and evaluate the generated university schedules.
        This report helps to **identify conflicts, optimize resource usage, and ensure a balanced timetable**.

         🛠️ **Key Objectives:**
        - ✅ Detect schedule conflicts (room/teacher overlaps)
        - ✅ Analyze resource utilization (rooms, teachers, timeslots)
        - ✅ Optimize scheduling efficiency (balance, penalties)
        - ✅ Ensure fairness in timetable distribution

        You can also view the previous reports.
        
        **Use the sidebar menu to explore different sections of this report.**
        """
    )
    st.markdown("---")
    st.stop()  # Prevents further execution to keep Overview at the top


# Past Reports Section
if selected_page == "📂 **View Past Reports**":
    st.subheader("📂 **View Past Reports**")
    
    if available_reports:

        # 1. Get report names and their creation times
        report_data = []
        for report in available_reports:
            report_path = os.path.join(history_folder, report)
            creation_time = os.path.getctime(report_path)  # Get file creation timestamp
            formatted_time = datetime.fromtimestamp(creation_time).strftime("%d/%m/%Y %H:%M")
            report_data.append((report, formatted_time))

        # Convert to DataFrame
        df_reports = pd.DataFrame(report_data, columns=["Report Name", "Generated On"])

        # Display in Streamlit as a table
        st.markdown("##### Past Reports History")  
        st.dataframe(df_reports, use_container_width=True)  # Display as a responsive table



        # 2. Metrics Evolution Over Reports
        comp_times, obj_values, sol_counts = [], [], []

        for report in available_reports_asc:
            report_path = os.path.join(history_folder, report)
            with open(report_path, "r") as file:
                content = file.readlines()
            
            # Extract key values
            comp_time, obj_value, sol_count = None, None, None
            for line in content:
                if "Computational time" in line:
                    comp_time = float(line.split(":")[1].split("s")[0].strip())
                elif "Best objective value" in line:
                    obj_value = int(line.split(":")[1].strip())
                elif "Total solutions found" in line:
                    sol_count = int(line.split(":")[1].strip())

            if comp_time is not None and obj_value is not None and sol_count is not None:
                comp_times.append(comp_time)
                obj_values.append(obj_value)
                sol_counts.append(sol_count)

        # Create shorter x-axis labels (v1, v2, v3...)
        x_labels = [f"v{r.split('_v')[-1].split('.txt')[0]}" for r in available_reports_asc]

        # Use Seaborn theme for a cleaner look
        sns.set_theme(style="whitegrid")

        # Define figure size
        fig_size = (6, 3)

        # Plot Computational Time
        fig1, ax1 = plt.subplots(figsize=fig_size)
        sns.lineplot(x=x_labels, y=comp_times, marker='o', color='#1f77b4', ax=ax1)
        ax1.set_title("Computational Time", fontsize=9, fontweight='bold')
        ax1.set_xlabel("Report Version", fontsize=6)
        ax1.set_ylabel("Time (s)", fontsize=6)
        ax1.set_xticklabels(x_labels, rotation=30, fontsize=4)  
        ax1.tick_params(axis='y', labelsize=4) 
        st.pyplot(fig1)

        # Plot Best Objective Value
        fig2, ax2 = plt.subplots(figsize=fig_size)
        sns.lineplot(x=x_labels, y=obj_values, marker='s', color='#2ca02c', ax=ax2)
        ax2.set_title("Best Objective Value", fontsize=9, fontweight='bold')
        ax2.set_xlabel("Report Version", fontsize=6)
        ax2.set_ylabel("Objective Value", fontsize=6)
        ax2.set_xticklabels(x_labels, rotation=30, fontsize=4) 
        ax2.tick_params(axis='y', labelsize=4)
        st.pyplot(fig2)

        # Plot Total Solutions Found
        fig3, ax3 = plt.subplots(figsize=fig_size)
        sns.lineplot(x=x_labels, y=sol_counts, marker='d', color='#d62728', ax=ax3)
        ax3.set_title("Total Solutions Found", fontsize=9, fontweight='bold')
        ax3.set_xlabel("Report Version", fontsize=6)
        ax3.set_ylabel("Solutions Count", fontsize=6)
        ax3.set_xticklabels(x_labels, rotation=30, fontsize=4) 
        ax3.tick_params(axis='y', labelsize=4)
        st.pyplot(fig3)



        # 3. Select and load a report
        selected_report = st.selectbox("Select a report:", available_reports)
        
        if st.button("Load Report"):
            # Load and display the selected report
            selected_report_path = os.path.join(history_folder, selected_report)
            past_report_content = load_intelligence_report(selected_report_path)

            st.markdown(f"##### **Displaying** *{selected_report}*")
            st.text_area("Report Content", past_report_content, height=500)



    else:
        st.info("No previous reports found.")
    st.stop()  # Stop execution after loading past reports


# Process content into sections
sections = load_intelligence_report(file_path).split("\n")
current_section = pages[selected_page]
display_lines = []
found_section = False

for line in sections:
    stripped_line = line.strip()

    # Detect the start of the selected section
    if stripped_line == current_section:
        found_section = True
        display_lines.append(f"### {selected_page}")  # Add title

    # Stop at the next section header
    elif found_section and stripped_line in pages.values():
        break

    # Collect content
    elif found_section:
        display_lines.append(stripped_line)

# Render content nicely
for line in display_lines:
    if line.startswith("-"):
        st.markdown(f"✅ {line[1:].strip()}")  # Bullet points
    elif line.startswith("*"):
        st.markdown(f"🔹 {line[1:].strip()}")  # Sub-items
    elif "Elapsed time" in line or "Total solutions" in line or "Objective" in line:
        st.markdown(f"🕒 **{line}**")  # Highlight important values
    else:
        st.write(line)  # Default display


st.markdown("---")
st.markdown("📌 *Generated by Goodwing-Timetabler*")