import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="April")
pet_name = st.text_input("Pet name", value="Buddy")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize Owner and Pet once in the session vault — reuse on every rerun
if "owner" not in st.session_state:
    pet = Pet(name=pet_name, species=species, location="TBD",
              type_of_food="TBD", type_of_shampoo="TBD")
    owner = Owner(name=owner_name)
    owner.add_pet(pet)
    st.session_state.owner = owner

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col3:
    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])

if st.button("Add task"):
    new_task = Task(description=task_title, time=task_time, frequency=frequency)
    st.session_state.owner.pets[0].add_task(new_task)
    st.success(f"Task '{task_title}' added to {st.session_state.owner.pets[0].name}.")

# Display all current tasks from the pet
current_tasks = st.session_state.owner.pets[0].get_tasks()
if current_tasks:
    st.write("All tasks for this pet:")
    st.table([
        {
            "Task": t.description,
            "Time": t.time,
            "Frequency": t.frequency,
            "Due": str(t.due_date),
            "Done": "✅" if t.completed else "⬜",
        }
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Daily Schedule ---
st.subheader("Today's Schedule")

scheduler = Scheduler(st.session_state.owner)
schedule = scheduler.prioritize_tasks()   # sorted by time, pending only
conflicts = scheduler.detect_conflicts()  # plain-English warning strings

if not schedule:
    st.info("No pending tasks for today. All done or nothing added yet!")
else:
    st.success(f"{len(schedule)} task(s) pending — sorted by start time.")
    st.table([
        {
            "Time": task.time,
            "Pet": pet_name,
            "Task": task.description,
            "Frequency": task.frequency,
            "Due": str(task.due_date),
        }
        for pet_name, task in schedule
    ])

# Show conflict warnings below the schedule so the owner sees context first
if conflicts:
    st.markdown("**Scheduling Conflicts Detected**")
    for warning in conflicts:
        st.warning(warning)
else:
    if schedule:
        st.success("No scheduling conflicts — your plan looks good!")

st.divider()

# --- Mark a Task Complete ---
st.subheader("Mark a Task Complete")

pending = scheduler.get_pending_tasks()   # filter_by_status is used internally

if not pending:
    st.info("No pending tasks to mark complete.")
else:
    task_labels = [
        f"{task.description} ({pet_name} @ {task.time})"
        for pet_name, task in pending
    ]
    selected_label = st.selectbox("Select a task to mark done", task_labels)
    selected_index = task_labels.index(selected_label)
    selected_pet_name, selected_task = pending[selected_index]

    if st.button("Mark complete"):
        scheduler.mark_task_complete(selected_pet_name, selected_task)
        st.success(
            f"'{selected_task.description}' marked complete! "
            f"Next {selected_task.frequency.lower()} occurrence scheduled automatically."
        )
        st.rerun()
