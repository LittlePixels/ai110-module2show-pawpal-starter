import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="April")
pet_name = st.text_input("Pet name", value="Buddy")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize Owner and Pet once in the session vault — reuse on every rerun
if "owner" not in st.session_state:
    pet = Pet(name=pet_name, species=species, location="TBD",
              type_of_food="TBD", type_of_shampoo="TBD")
    owner = Owner(name=owner_name)
    owner.add_pet(pet)          # Owner.add_pet()
    st.session_state.owner = owner

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")
st.caption("Adds a real Task object to the first pet via pet.add_task().")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col3:
    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])

if st.button("Add task"):
    new_task = Task(description=task_title, time=task_time, frequency=frequency)
    # Call pet.add_task() on the first pet stored in the Owner
    st.session_state.owner.pets[0].add_task(new_task)
    st.success(f"Task '{task_title}' added to {st.session_state.owner.pets[0].name}.")

# Display current tasks from the real Pet object
current_tasks = st.session_state.owner.pets[0].get_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([
        {"Task": t.description, "Time": t.time, "Frequency": t.frequency, "Done": t.completed}
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")
st.caption("Calls Scheduler.prioritize_tasks() to sort and display today's plan.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)   # Scheduler(owner)
    schedule = scheduler.prioritize_tasks()          # prioritize_tasks()
    if not schedule:
        st.warning("No pending tasks to schedule.")
    else:
        st.success(f"Schedule for {st.session_state.owner.name}:")
        for pet_name, task in schedule:
            st.markdown(f"- **[{task.time}]** {pet_name} — {task.description} *({task.frequency})*")
