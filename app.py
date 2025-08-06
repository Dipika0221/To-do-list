import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="🗓️ Repeating To-Do Tasks", layout="centered")
st.title("🔁 Add Repeating Daily or Weekly Tasks")

# Initialize task storage
if "tasks" not in st.session_state:
    st.session_state.tasks = {}

# --- Task Input Section ---
st.subheader("📝 Add a Recurring Task")

task_text = st.text_input("Enter a task")
start_date = st.date_input("Start Date", date.today())

repeat_type = st.selectbox("Repeat Task", ["Only Once", "Daily for 7 Days", "Weekly (Same Weekday for 1 Month)"])

add_task = st.button("Add Task")

# --- Repeat Logic ---
if add_task and task_text.strip():
    dates_to_add = []

    if repeat_type == "Only Once":
        dates_to_add = [start_date]
    elif repeat_type == "Daily for 7 Days":
        dates_to_add = [start_date + timedelta(days=i) for i in range(7)]
    elif repeat_type == "Weekly (Same Weekday for 1 Month)":
        weekday = start_date.weekday()
        current_date = start_date
        while current_date.month == start_date.month:
            if current_date.weekday() == weekday:
                dates_to_add.append(current_date)
            current_date += timedelta(days=1)

    # Add to session_state
    for d in dates_to_add:
        key = str(d)
        if key not in st.session_state.tasks:
            st.session_state.tasks[key] = []
        st.session_state.tasks[key].append({"task": task_text.strip(), "done": False})

    st.success(f"✅ Task added on {len(dates_to_add)} date(s)!")

# --- View All Tasks by Date ---
st.markdown("---")
st.subheader("📅 Tasks Added")

if st.session_state.tasks:
    for k in sorted(st.session_state.tasks.keys()):
        task_list = st.session_state.tasks[k]
        st.write(f"**{k}**:")
        for task in task_list:
            st.write(f"- {'✅' if task['done'] else '🔲'} {task['task']}")
else:
    st.info("No tasks added yet.")
