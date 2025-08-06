import streamlit as st
from datetime import date

st.set_page_config(page_title="📆 Calendar To-Do List", layout="centered")
st.title("🗓️ Calendar-based Daily To-Do List with Progress")

# Initialize task storage
if "tasks" not in st.session_state:
    st.session_state.tasks = {}

# --- Calendar Date Picker ---
selected_date = st.date_input("📅 Select a date", date.today())

# --- Add Multiple Tasks ---
st.subheader("📝 Add Tasks for Selected Date")
with st.form("task_form"):
    tasks_input = st.text_area("Enter multiple tasks (one per line)")
    add_tasks = st.form_submit_button("Add Tasks")

    if add_tasks and tasks_input.strip():
        task_lines = [line.strip() for line in tasks_input.strip().split("\n") if line.strip()]
        date_key = str(selected_date)
        if date_key not in st.session_state.tasks:
            st.session_state.tasks[date_key] = []
        for line in task_lines:
            st.session_state.tasks[date_key].append({"task": line, "done": False})
        st.success(f"{len(task_lines)} task(s) added for {selected_date.strftime('%A, %d %B %Y')}")

# --- Show Tasks ---
date_key = str(selected_date)
st.subheader(f"📌 Tasks for {selected_date.strftime('%A, %d %B %Y')}")

if date_key in st.session_state.tasks and st.session_state.tasks[date_key]:
    updated = []
    done_count = 0
    total_tasks = len(st.session_state.tasks[date_key])

    for i, task_data in enumerate(st.session_state.tasks[date_key]):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            done = st.checkbox("", value=task_data["done"], key=f"{date_key}_{i}")
        with col2:
            st.write(f"✅ ~~{task_data['task']}~~" if done else f"🔲 {task_data['task']}")
        task_data["done"] = done
        updated.append(task_data)
        if done:
            done_count += 1

    st.session_state.tasks[date_key] = updated

    # --- Progress Bar ---
    st.markdown("### 🟢 Progress")
    st.progress(done_count / total_tasks)
    st.write(f"✅ {done_count} of {total_tasks} task(s) completed")
else:
    st.info("No tasks added for this date.")

# --- Summary of All Dates ---
with st.expander("📖 View Task Summary (All Dates)"):
    if st.session_state.tasks:
        for k in sorted(st.session_state.tasks.keys()):
            task_list = st.session_state.tasks[k]
            pending = sum(not t["done"] for t in task_list)
            completed = sum(t["done"] for t in task_list)
            st.write(f"**{k}**: ✅ {completed} / 🔲 {pending + completed} tasks")
    else:
        st.write("No tasks added yet.")
