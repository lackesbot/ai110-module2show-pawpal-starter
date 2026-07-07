import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state initialization ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None

# -----------------------------------------------------------
# SECTION 1: Owner
# -----------------------------------------------------------
st.header("1. Owner")

with st.form("owner_form"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First name", value="Jordan")
    with col2:
        last_name = st.text_input("Last name", value="Smith")
    save_owner = st.form_submit_button("Save owner")

if save_owner:
    st.session_state.owner = Owner(first_name=first_name, last_name=last_name)
    st.success(f"Owner saved: {st.session_state.owner.full_name()}")

if st.session_state.owner:
    st.caption(f"Current owner: **{st.session_state.owner.full_name()}**")

st.divider()

# -----------------------------------------------------------
# SECTION 2: Pet
# -----------------------------------------------------------
st.header("2. Add a Pet")

with st.form("pet_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
        pet_breed = st.text_input("Breed", value="Shiba Inu")
    with col2:
        pet_sex = st.selectbox("Sex", ["female", "male"])
        pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    save_pet = st.form_submit_button("Save pet")

if save_pet:
    new_pet = Pet(
        name=pet_name,
        age=pet_age,
        sex=pet_sex,
        breed=pet_breed,
    )
    st.session_state.pet = new_pet
    if st.session_state.owner:
        st.session_state.owner.add_pet(new_pet)
    st.success(f"Pet saved: {pet_name} the {pet_breed}")

if st.session_state.pet:
    p = st.session_state.pet
    st.caption(f"Current pet: **{p.name}** | {p.breed} | Age {p.age} | {p.sex}")

st.divider()

# -----------------------------------------------------------
# SECTION 3: Tasks
# -----------------------------------------------------------
st.header("3. Schedule a Task")

with st.form("task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    description = st.text_input("Description (optional)", value="")
    frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
    add_task = st.form_submit_button("Add task")


if add_task:
    new_task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
        description=description,
        frequency=frequency,
    )
    if st.session_state.pet:
        st.session_state.pet.add_task(new_task)
    st.session_state.tasks.append(new_task)
    st.success(f"Task added: {task_title}")


if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
    if st.button("Clear all tasks"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# -----------------------------------------------------------
# SECTION 4: Generate Schedule
# -----------------------------------------------------------
st.header("4. Build Schedule")

available_minutes = st.number_input("Available time (minutes)", min_value=10, max_value=480, value=60)
start_time = st.text_input("Start time", value="08:00 AM")

scheduler = Scheduler()

# Pet selector — only shown when the owner has at least one pet
selected_pet = None
if st.session_state.owner and st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Select pet to schedule for", pet_names)
    tasks_for_pet = scheduler.filter_tasks_by_pet(
        st.session_state.owner.pets, selected_pet_name
    )
    selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
    if tasks_for_pet:
        st.caption(f"{len(tasks_for_pet)} task(s) found for {selected_pet_name}")
    else:
        st.info(f"No tasks added for {selected_pet_name} yet.")

if st.button("Generate schedule"):
    if not st.session_state.owner:
        st.error("Please save an owner first.")
    elif not selected_pet:
        st.error("Please save a pet first.")
    elif not tasks_for_pet:
        st.error("Please add at least one task for this pet.")
    else:
        # Conflict detection
        total_needed = sum(t.duration_minutes for t in tasks_for_pet)
        if total_needed > int(available_minutes):
            st.warning(
                f"Tasks total {total_needed} min but you only have {int(available_minutes)} min. "
                "Lower-priority tasks will be dropped to fit."
            )
        st.session_state.schedule = scheduler.generate_schedule(
            st.session_state.owner,
            selected_pet,
            tasks_for_pet,
            available_minutes=int(available_minutes),
            start_time=start_time,
        )


if "schedule" in st.session_state:
    st.text(st.session_state.schedule.display())
