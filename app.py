import streamlit as st
from datetime import date

st.set_page_config(page_title="📝 Day-wise To-Do List", layout="centered")

st.title("📅 Daily To-Do List")

# Initialize task store
if "tasks" not in st.session_state:
    st.session_state.tasks = {}

# Date selection
selected_date = st.date_input("Select a date", date.today())

# Add new task
with st.form("Add Task"):
    task_input = st.text_input("Enter task")
    submitted = st.form_submit_button("Add Task")
    if submitted and task_input:
        day_key = str(selected_date)
        if day_key not in st.session_state.tasks:
            st.session_state.tasks[day_key] = []
        st.session_state.tasks[day_key].append({"task": task_input, "done": False})
        st.success("Task added!")

# Display tasks
day_key = str(selected_date)
if day_key in st.session_state.tasks and st.session_state.tasks[day_key]:
    st.subheader(f"Tasks for {selected_date.strftime('%A, %d %B %Y')}:")
    updated_tasks = []
    for i, task_data in enumerate(st.session_state.tasks[day_key]):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            done = st.checkbox("", value=task_data["done"], key=f"{day_key}_{i}")
        with col2:
            st.write(f"~~{task_data['task']}~~" if done else task_data["task"])
        task_data["done"] = done
        updated_tasks.append(task_data)
    st.session_state.tasks[day_key] = updated_tasks
else:
    st.info("No tasks added for this date.")

