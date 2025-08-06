import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="📅 Smart To-Do Calendar", layout="centered")
st.title("🗓️ Smart Calendar-Based To-Do List")

# --- Initialize ---
if "tasks" not in st.session_state:
    st.session_state.tasks = {}

# --- Select Date ---
selected_date = st.date_input("📌 Select Date", date.today())
date_key = str(selected_date)

# --- Add Multiple Tasks ---
st.subheader("📝 Add Multiple Tasks")

with st.form("task_form"):
    tasks_input = st.text_area("Enter tasks (one per line)")
    repeat_type = st.selectbox("Repeat", ["Only Once", "Daily for 7 Days", "Weekly (Same Weekday for 1 Month)"])
    submitted = st.form_submit_button("Add Tasks")

    if submitted and tasks_input.strip():
        lines = [line.strip() for line in tasks_input.split("\n") if line.strip()]
        repeat_dates = []

        if repeat_type == "Only Once":
            repeat_dates = [selected_date]
        elif repeat_type == "Daily for 7 Days":
            repeat_dates = [selected_date + timedelta(days=i) for i in range(7)]
        elif repeat_type == "Weekly (Same Weekday for 1 Month)":
            weekday = selected_date.weekday()
            current = selected_date
            while current.month == selected_date.month:
                if current.weekday() == weekday:
                    repeat_dates.append(current)
                current += timedelta(days=1)

        for rd in repeat_dates:
            rd_key = str(rd)
            if rd_key not in st.session_state.tasks:
                st.session_state.tasks[rd_key] = []
            for line in lines:
                st.session_state.tasks[rd_key].append({"task": line, "done": False})

        st.success(f"✅ Added {len(lines)} task(s) on {len(repeat_dates)} date(s)")

# --- Show Tasks ---
st.markdown("---")
st.subheader(f"📋 Tasks for {selected_date.strftime('%A, %d %B %Y')}")

if date_key in st.session_state.tasks and st.session_state.tasks[date_key]:
    new_tasks = []
    done_count = 0
    total = len(st.session_state.tasks[date_key])

    for i, task in enumerate(st.session_state.tasks[date_key]):
        cols = st.columns([0.07, 0.75, 0.18])
        with cols[0]:
            is_done = st.checkbox("", value=task["done"], key=f"{date_key}_{i}")
        with cols[1]:
            st.write(f"✅ ~~{task['task']}~~" if is_done else f"🔲 {task['task']}")
        with cols[2]:
            delete = st.button("🗑️ Delete", key=f"del_{date_key}_{i}")
        if not delete:
            task["done"] = is_done
            new_tasks.append(task)
        else:
            total -= 1  # adjust total if deleted
        if is_done and not delete:
            done_count += 1

    st.session_state.tasks[date_key] = new_tasks

    # Progress bar
    if total > 0:
        st.markdown("### 📊 Progress")
        st.progress(done_count / total)
        st.write(f"✅ {done_count} of {total} task(s) completed")
else:
    st.info("No tasks added for this date.")

# --- Expand: Summary of All Tasks ---
with st.expander("📖 View Summary for All Dates"):
    if st.session_state.tasks:
        for k in sorted(st.session_state.tasks.keys()):
            tlist = st.session_state.tasks[k]
            done = sum(1 for t in tlist if t["done"])
            total = len(tlist)
            st.write(f"**{k}**: ✅ {done}/{total} tasks")
    else:
        st.write("No tasks yet.")
