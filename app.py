import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Dentaflow — Patient Monitor", layout="wide", page_icon="🦷")

st.markdown("""
<style>
    .stApp { background-color: #fffde7; }
    [data-testid="stSidebar"] { background-color: #fff9c4; }
</style>
""", unsafe_allow_html=True)

# ─── Data Generation ──────────────────────────────────────────────────────────

def generate_data():
    os.makedirs("data_ai", exist_ok=True)
    random.seed(42)
    today = datetime.today()

    first_names = ["Maria","James","Linda","Robert","Patricia","Michael","Barbara",
                   "William","Jennifer","David","Susan","Richard","Jessica","Thomas",
                   "Sarah","Charles","Karen","Joseph","Nancy","Daniel","Lisa","Mark",
                   "Betty","Paul","Dorothy","Steven","Sandra","Andrew","Ashley","Kenneth"]
    last_names = ["Garcia","Smith","Johnson","Williams","Brown","Jones","Miller",
                  "Davis","Wilson","Moore","Taylor","Anderson","Thomas","Jackson",
                  "White","Harris","Martin","Thompson","Martinez","Robinson"]
    insurances = ["Delta Dental","MetLife Dental","Cigna Dental","Aetna Dental","BlueCross Dental","Self-Pay"]
    risk_levels = ["Low","Medium","High"]

    patients = []
    for i in range(1, 51):
        last_visit_days = random.randint(30, 730)
        last_visit = today - timedelta(days=last_visit_days)
        next_offset = random.choice([-15, -7, 7, 14, 21, 30, 45, 60, 90])
        next_appt = today + timedelta(days=next_offset)
        risk = random.choices(risk_levels, [0.50, 0.35, 0.15])[0]
        patients.append({
            "patient_id": f"P{i:03d}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "age": random.randint(8, 78),
            "gender": random.choice(["Male","Female"]),
            "phone": f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
            "email": f"patient{i}@email.com",
            "insurance": random.choice(insurances),
            "risk_level": risk,
            "last_visit": last_visit.strftime("%Y-%m-%d"),
            "next_appointment": next_appt.strftime("%Y-%m-%d"),
            "days_since_last_visit": last_visit_days,
        })
    patients_df = pd.DataFrame(patients)
    patients_df.to_csv("data_ai/patients.csv", index=False)

    appt_types = ["Checkup & Cleaning","Filling","Root Canal","Extraction",
                  "Orthodontic Consult","Whitening","Crown Prep","Periodontal Scaling"]
    dentists = ["Dr. Patel","Dr. Kim","Dr. Rodriguez","Dr. Thompson"]
    appointments = []
    appt_id = 1
    for p in patients:
        for _ in range(random.randint(2, 8)):
            appt_date = today - timedelta(days=random.randint(-30, 730))
            status = "Scheduled" if appt_date > today else random.choices(
                ["Completed","Cancelled","No-Show"], [0.78, 0.15, 0.07])[0]
            appointments.append({
                "appointment_id": f"A{appt_id:04d}",
                "patient_id": p["patient_id"],
                "date": appt_date.strftime("%Y-%m-%d"),
                "type": random.choice(appt_types),
                "status": status,
                "dentist": random.choice(dentists),
                "duration_min": random.choice([30, 45, 60, 90]),
                "notes": random.choice(["Routine visit","Patient reports sensitivity",
                                        "Follow-up required","Good oral hygiene","",""]),
            })
            appt_id += 1
    appt_df = pd.DataFrame(appointments)
    appt_df.to_csv("data_ai/appointments.csv", index=False)

    metrics = []
    met_id = 1
    completed = appt_df[appt_df["status"] == "Completed"]
    for _, row in completed.iterrows():
        metrics.append({
            "metric_id": f"M{met_id:04d}",
            "patient_id": row["patient_id"],
            "appointment_id": row["appointment_id"],
            "date": row["date"],
            "plaque_score": round(random.uniform(0, 5), 1),
            "gum_bleeding_sites": random.randint(0, 15),
            "cavity_count": random.choices([0,1,2,3,4], [0.45,0.25,0.15,0.10,0.05])[0],
            "pocket_depth_avg_mm": round(random.uniform(1.5, 6.0), 1),
            "xray_taken": random.choice(["Yes","Yes","No"]),
            "oral_hygiene_score": random.randint(1, 10),
        })
        met_id += 1
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv("data_ai/health_metrics.csv", index=False)

    procedures = ["Amalgam Filling","Composite Filling","Root Canal Treatment",
                  "Tooth Extraction","Crown Placement","Periodontal Scaling",
                  "Teeth Cleaning","Fluoride Treatment","Dental Sealant",
                  "Invisalign","Whitening Treatment"]
    treatments = []
    tr_id = 1
    for _, row in completed.iterrows():
        for _ in range(random.randint(1, 2)):
            cost = random.choice([75,100,150,200,250,350,500,800,1200])
            covered = round(cost * random.uniform(0.5, 0.9), 2) if random.random() > 0.2 else 0
            treatments.append({
                "treatment_id": f"T{tr_id:04d}",
                "patient_id": row["patient_id"],
                "appointment_id": row["appointment_id"],
                "date": row["date"],
                "procedure": random.choice(procedures),
                "tooth_number": random.randint(1,32) if random.random() > 0.3 else None,
                "cost_usd": cost,
                "insurance_covered_usd": covered,
                "patient_owes_usd": round(cost - covered, 2),
            })
            tr_id += 1
    treatments_df = pd.DataFrame(treatments)
    treatments_df.to_csv("data_ai/treatments.csv", index=False)

    return patients_df, appt_df, metrics_df, treatments_df


def generate_health_history(patient_ids):
    os.makedirs("data_ai", exist_ok=True)
    random.seed(77)
    conditions_pool = ["None","Diabetes Type 2","Hypertension","Heart Disease",
                       "Asthma","Osteoporosis","Thyroid Disorder","Diabetes Type 1"]
    allergies_pool  = ["None","Penicillin","Latex","Aspirin","Sulfa Drugs","Codeine","Ibuprofen"]
    meds_pool       = ["None","Metformin","Lisinopril","Atorvastatin","Warfarin",
                       "Levothyroxine","Amlodipine","Aspirin Daily"]
    blood_types     = ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
    smoking         = ["Non-Smoker","Non-Smoker","Non-Smoker","Former Smoker","Current Smoker"]

    records = []
    for pid in patient_ids:
        cond = random.choice(conditions_pool)
        med  = "None" if cond == "None" else random.choice([m for m in meds_pool if m != "None"])
        records.append({
            "patient_id":          pid,
            "medical_conditions":  cond,
            "allergies":           random.choice(allergies_pool),
            "current_medications": med,
            "blood_type":          random.choice(blood_types),
            "smoking_status":      random.choice(smoking),
            "last_updated":        (datetime.today() - timedelta(days=random.randint(30,365))).strftime("%Y-%m-%d"),
        })
    hh_df = pd.DataFrame(records)
    hh_df.to_csv("data_ai/health_history.csv", index=False)
    return hh_df


def load_health_history(patient_ids):
    if not os.path.exists("data_ai/health_history.csv"):
        return generate_health_history(patient_ids)
    return pd.read_csv("data_ai/health_history.csv")


def load_data():
    if not os.path.exists("data_ai/patients.csv"):
        return generate_data()
    return (
        pd.read_csv("data_ai/patients.csv"),
        pd.read_csv("data_ai/appointments.csv"),
        pd.read_csv("data_ai/health_metrics.csv"),
        pd.read_csv("data_ai/treatments.csv"),
    )


# ─── Session State ────────────────────────────────────────────────────────────

if "patients_df" not in st.session_state:
    p, a, m, t = load_data()
    st.session_state.patients_df = p
    st.session_state.appt_df = a
    st.session_state.metrics_df = m
    st.session_state.treatments_df = t

patients_df    = st.session_state.patients_df
appt_df        = st.session_state.appt_df
metrics_df     = st.session_state.metrics_df
treatments_df  = st.session_state.treatments_df

if "health_history_df" not in st.session_state:
    st.session_state.health_history_df = load_health_history(patients_df["patient_id"].tolist())

health_history_df = st.session_state.health_history_df
today_str  = datetime.today().strftime("%Y-%m-%d")

# ─── Sidebar Navigation ───────────────────────────────────────────────────────

st.sidebar.image("https://img.icons8.com/emoji/96/tooth-emoji.png", width=64)
st.sidebar.title("🦷 Dentaflow")
st.sidebar.caption("Patient Monitoring System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "👥 Patients", "📅 Appointments", "🚨 Alerts", "🏥 Health History", "➕ Add Data"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Today: {today_str}")
st.sidebar.caption(f"Total Patients: {len(patients_df)}")


def risk_badge(risk):
    colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    return f"{colors.get(risk, '')} {risk}"


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

if page == "📊 Overview":
    st.title("📊 Practice Overview")
    st.markdown("A snapshot of your dental practice at a glance.")
    st.markdown("---")

    total_patients = len(patients_df)
    high_risk = len(patients_df[patients_df["risk_level"] == "High"])
    upcoming = len(appt_df[(appt_df["date"] >= today_str) & (appt_df["status"] == "Scheduled")])
    overdue = len(patients_df[patients_df["days_since_last_visit"] > 365])
    no_shows = len(appt_df[appt_df["status"] == "No-Show"])
    avg_hygiene = round(metrics_df["oral_hygiene_score"].mean(), 1)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Patients", total_patients)
    c2.metric("High-Risk Patients", high_risk, delta=f"{round(high_risk/total_patients*100)}%", delta_color="inverse")
    c3.metric("Upcoming Appts", upcoming)
    c4.metric("Overdue (>1 yr)", overdue, delta_color="inverse")
    c5.metric("No-Shows", no_shows, delta_color="inverse")
    c6.metric("Avg Hygiene Score", f"{avg_hygiene}/10")

    st.markdown("---")

    st.subheader("Appointments by Status")
    status_counts = appt_df["status"].value_counts().rename_axis("Status").reset_index(name="Count")
    st.bar_chart(status_counts.set_index("Status"), height=280, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Completed Appointments (Last 12 Months)")
        appt_df["date"] = pd.to_datetime(appt_df["date"])
        cutoff = datetime.today() - timedelta(days=365)
        monthly = (appt_df[(appt_df["status"] == "Completed") & (appt_df["date"] >= cutoff)]
                   .groupby(appt_df["date"].dt.to_period("M"))
                   .size()
                   .rename_axis("Month")
                   .reset_index(name="Appointments"))
        monthly["Month"] = monthly["Month"].astype(str)
        st.bar_chart(monthly.set_index("Month"), height=280, use_container_width=True)
    with col4:
        st.subheader("Top 5 Procedures Performed")
        top_proc = treatments_df["procedure"].value_counts().head(5).rename_axis("Procedure").reset_index(name="Count")
        st.bar_chart(top_proc.set_index("Procedure"), height=280, use_container_width=True)

    st.markdown("---")

    st.subheader("Patients by Insurance Provider")
    ins_counts = patients_df["insurance"].value_counts().rename_axis("Insurance").reset_index(name="Patients")
    st.bar_chart(ins_counts.set_index("Insurance"), height=260, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PATIENTS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "👥 Patients":
    st.title("👥 Patient Directory")
    st.markdown("---")

    fc1, fc2, fc3 = st.columns([2, 1, 1])
    search = fc1.text_input("🔍 Search by name", placeholder="e.g. Maria Garcia")
    risk_filter = fc2.selectbox("Risk Level", ["All","High","Medium","Low"])
    ins_filter = fc3.selectbox("Insurance", ["All"] + sorted(patients_df["insurance"].unique().tolist()))

    filtered = patients_df.copy()
    if search:
        filtered = filtered[filtered["name"].str.contains(search, case=False)]
    if risk_filter != "All":
        filtered = filtered[filtered["risk_level"] == risk_filter]
    if ins_filter != "All":
        filtered = filtered[filtered["insurance"] == ins_filter]

    st.caption(f"Showing {len(filtered)} of {len(patients_df)} patients")

    display = filtered[["patient_id","name","age","gender","risk_level","insurance",
                         "last_visit","next_appointment","days_since_last_visit"]].copy()
    display.columns = ["ID","Name","Age","Gender","Risk","Insurance",
                       "Last Visit","Next Appt","Days Since Visit"]

    def highlight_risk(row):
        color = {"High":"#ffe0e0","Medium":"#fff9e0","Low":"#e0ffe8"}.get(row["Risk"],"")
        return [f"background-color: {color}" if color else "" for _ in row]

    st.dataframe(display.style.apply(highlight_risk, axis=1),
                 use_container_width=True, height=380)

    st.markdown("---")
    st.subheader("Patient Detail View")
    patient_names = patients_df["name"].sort_values().tolist()
    selected_name = st.selectbox("Select a patient", patient_names)
    patient = patients_df[patients_df["name"] == selected_name].iloc[0]

    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        st.markdown("**Patient Info**")
        st.write(f"**ID:** {patient['patient_id']}")
        st.write(f"**Name:** {patient['name']}")
        st.write(f"**Age:** {patient['age']}   |   **Gender:** {patient['gender']}")
        st.write(f"**Phone:** {patient['phone']}")
        st.write(f"**Email:** {patient['email']}")
    with dc2:
        st.markdown("**Coverage & Risk**")
        st.write(f"**Insurance:** {patient['insurance']}")
        st.write(f"**Risk Level:** {risk_badge(patient['risk_level'])}")
        st.write(f"**Last Visit:** {patient['last_visit']}")
        st.write(f"**Next Appointment:** {patient['next_appointment']}")
        st.write(f"**Days Since Last Visit:** {patient['days_since_last_visit']}")
    with dc3:
        p_metrics = metrics_df[metrics_df["patient_id"] == patient["patient_id"]].sort_values("date")
        if not p_metrics.empty:
            latest = p_metrics.iloc[-1]
            st.markdown("**Latest Health Metrics**")
            st.write(f"**Plaque Score:** {latest['plaque_score']} / 5.0")
            st.write(f"**Gum Bleeding Sites:** {int(latest['gum_bleeding_sites'])}")
            st.write(f"**Cavities:** {int(latest['cavity_count'])}")
            st.write(f"**Pocket Depth Avg:** {latest['pocket_depth_avg_mm']} mm")
            st.write(f"**Oral Hygiene Score:** {int(latest['oral_hygiene_score'])} / 10")
        else:
            st.info("No health metrics recorded yet.")

    st.markdown("**Appointment History**")
    p_appts = appt_df[appt_df["patient_id"] == patient["patient_id"]].sort_values("date", ascending=False)
    if not p_appts.empty:
        p_appts["date"] = p_appts["date"].astype(str)
        st.dataframe(p_appts[["date","type","status","dentist","duration_min","notes"]].rename(
            columns={"date":"Date","type":"Type","status":"Status","dentist":"Dentist",
                     "duration_min":"Duration (min)","notes":"Notes"}),
            use_container_width=True, height=200)
    else:
        st.info("No appointments on record.")

    st.markdown("**Treatment History**")
    p_treats = treatments_df[treatments_df["patient_id"] == patient["patient_id"]].sort_values("date", ascending=False)
    if not p_treats.empty:
        st.dataframe(p_treats[["date","procedure","tooth_number"]].rename(
            columns={"date":"Date","procedure":"Procedure","tooth_number":"Tooth #"}),
            use_container_width=True, height=200)
    else:
        st.info("No treatments on record.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: APPOINTMENTS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "📅 Appointments":
    st.title("📅 Appointment Manager")
    st.markdown("---")

    appt_df["date"] = appt_df["date"].astype(str)

    af1, af2, af3, af4 = st.columns(4)
    status_f  = af1.selectbox("Status", ["All","Scheduled","Completed","Cancelled","No-Show"])
    dentist_f = af2.selectbox("Dentist", ["All"] + sorted(appt_df["dentist"].unique().tolist()))
    type_f    = af3.selectbox("Type", ["All"] + sorted(appt_df["type"].unique().tolist()))
    date_range = af4.selectbox("Date Range", ["All Time","Next 30 Days","Last 30 Days","Last 90 Days"])

    fdf = appt_df.copy()
    if status_f != "All":
        fdf = fdf[fdf["status"] == status_f]
    if dentist_f != "All":
        fdf = fdf[fdf["dentist"] == dentist_f]
    if type_f != "All":
        fdf = fdf[fdf["type"] == type_f]

    ref = datetime.today()
    if date_range == "Next 30 Days":
        fdf = fdf[(fdf["date"] >= today_str) & (fdf["date"] <= (ref + timedelta(days=30)).strftime("%Y-%m-%d"))]
    elif date_range == "Last 30 Days":
        fdf = fdf[(fdf["date"] >= (ref - timedelta(days=30)).strftime("%Y-%m-%d")) & (fdf["date"] <= today_str)]
    elif date_range == "Last 90 Days":
        fdf = fdf[(fdf["date"] >= (ref - timedelta(days=90)).strftime("%Y-%m-%d")) & (fdf["date"] <= today_str)]

    fdf = fdf.merge(patients_df[["patient_id","name","risk_level"]], on="patient_id", how="left")
    st.caption(f"Showing {len(fdf)} appointments")
    st.dataframe(
        fdf[["date","appointment_id","name","risk_level","type","status","dentist","duration_min","notes"]]
        .sort_values("date", ascending=False)
        .rename(columns={"date":"Date","appointment_id":"Appt ID","name":"Patient",
                         "risk_level":"Risk","type":"Type","status":"Status",
                         "dentist":"Dentist","duration_min":"Duration (min)","notes":"Notes"}),
        use_container_width=True, height=500)

    st.markdown("---")
    st.subheader("Appointments by Dentist (All Time)")
    by_dentist = appt_df[appt_df["status"] == "Completed"]["dentist"].value_counts().rename_axis("Dentist").reset_index(name="Completed")
    st.bar_chart(by_dentist.set_index("Dentist"), height=250, use_container_width=True)



# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALERTS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "🚨 Alerts":
    st.title("🚨 Patient Alerts & Follow-Ups")
    st.markdown("---")

    st.subheader("🕐 Overdue for Checkup (180+ Days Since Last Visit)")
    overdue_df = patients_df[patients_df["days_since_last_visit"] >= 180].sort_values("days_since_last_visit", ascending=False)
    if overdue_df.empty:
        st.success("No overdue patients.")
    else:
        st.warning(f"{len(overdue_df)} patients have not been seen in 180+ days.")
        st.dataframe(overdue_df[["patient_id","name","age","risk_level","insurance","last_visit","days_since_last_visit"]]
                     .rename(columns={"patient_id":"ID","name":"Name","age":"Age","risk_level":"Risk",
                                      "insurance":"Insurance","last_visit":"Last Visit","days_since_last_visit":"Days Overdue"}),
                     use_container_width=True, height=280)


    st.markdown("---")

    st.subheader("📆 Appointments in the Next 7 Days")
    week_end = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    appt_df["date"] = appt_df["date"].astype(str)
    upcoming_df = appt_df[(appt_df["date"] >= today_str) & (appt_df["date"] <= week_end) & (appt_df["status"] == "Scheduled")]
    upcoming_df = upcoming_df.merge(patients_df[["patient_id","name","risk_level"]], on="patient_id", how="left")
    if upcoming_df.empty:
        st.info("No appointments in the next 7 days.")
    else:
        st.info(f"{len(upcoming_df)} appointments coming up this week.")
        st.dataframe(upcoming_df[["date","name","risk_level","type","dentist","duration_min"]]
                     .sort_values("date")
                     .rename(columns={"date":"Date","name":"Patient","risk_level":"Risk",
                                      "type":"Type","dentist":"Dentist","duration_min":"Duration (min)"}),
                     use_container_width=True, height=250)

    st.markdown("---")

    st.subheader("📵 Patients with No-Shows")
    no_show_ids = appt_df[appt_df["status"] == "No-Show"]["patient_id"].value_counts().reset_index()
    no_show_ids.columns = ["patient_id","no_show_count"]
    ns_df = no_show_ids.merge(patients_df[["patient_id","name","risk_level","phone","email"]], on="patient_id", how="left")
    if ns_df.empty:
        st.success("No no-shows recorded.")
    else:
        st.dataframe(ns_df[["name","risk_level","no_show_count","phone","email"]]
                     .rename(columns={"name":"Patient","risk_level":"Risk","no_show_count":"No-Shows",
                                      "phone":"Phone","email":"Email"}),
                     use_container_width=True, height=250)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ADD DATA
# ══════════════════════════════════════════════════════════════════════════════

elif page == "➕ Add Data":
    st.title("➕ Add Data")
    st.markdown("Upload a CSV file or manually enter records below.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📂 Upload CSV", "🧑 Add Patient", "📅 Add Appointment"])

    # ── TAB 1: Upload CSV ─────────────────────────────────────────────────────
    with tab1:
        st.subheader("Drag & Drop a CSV File")
        st.markdown("Upload a CSV to add new **patients**, **appointments**, **health metrics**, or **treatments**.")

        uploaded_file = st.file_uploader(
            "Drop your CSV file here, or click to browse",
            type=["csv"],
            help="Accepted file types: .csv"
        )

        if uploaded_file is not None:
            try:
                upload_df = pd.read_csv(uploaded_file)
                st.success(f"File loaded: **{uploaded_file.name}** — {len(upload_df)} rows, {len(upload_df.columns)} columns")
                st.markdown("**Preview (first 5 rows):**")
                st.dataframe(upload_df.head(), use_container_width=True)

                # Auto-detect table type by columns
                cols = set(upload_df.columns.str.lower())
                if "plaque_score" in cols or "gum_bleeding_sites" in cols:
                    detected = "Health Metrics"
                elif "procedure" in cols or "tooth_number" in cols:
                    detected = "Treatments"
                elif "dentist" in cols or "duration_min" in cols:
                    detected = "Appointments"
                else:
                    detected = "Patients"

                data_type = st.selectbox(
                    "What type of data is this?",
                    ["Patients", "Appointments", "Health Metrics", "Treatments"],
                    index=["Patients","Appointments","Health Metrics","Treatments"].index(detected)
                )
                st.caption(f"Auto-detected as: **{detected}**")

                if st.button("✅ Import Data", type="primary"):
                    os.makedirs("data_ai", exist_ok=True)
                    if data_type == "Patients":
                        merged = pd.concat([st.session_state.patients_df, upload_df], ignore_index=True).drop_duplicates()
                        merged.to_csv("data_ai/patients.csv", index=False)
                        st.session_state.patients_df = merged
                    elif data_type == "Appointments":
                        merged = pd.concat([st.session_state.appt_df, upload_df], ignore_index=True).drop_duplicates()
                        merged.to_csv("data_ai/appointments.csv", index=False)
                        st.session_state.appt_df = merged
                    elif data_type == "Health Metrics":
                        merged = pd.concat([st.session_state.metrics_df, upload_df], ignore_index=True).drop_duplicates()
                        merged.to_csv("data_ai/health_metrics.csv", index=False)
                        st.session_state.metrics_df = merged
                    elif data_type == "Treatments":
                        merged = pd.concat([st.session_state.treatments_df, upload_df], ignore_index=True).drop_duplicates()
                        merged.to_csv("data_ai/treatments.csv", index=False)
                        st.session_state.treatments_df = merged
                    st.success(f"✅ {len(upload_df)} rows added to {data_type}!")
                    st.rerun()

            except Exception as e:
                st.error(f"Could not read file: {e}")

        st.markdown("---")
        st.markdown("**Expected CSV columns by data type:**")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Patients:** `patient_id, name, age, gender, phone, email, insurance, risk_level, last_visit, next_appointment, days_since_last_visit`")
            st.markdown("**Appointments:** `appointment_id, patient_id, date, type, status, dentist, duration_min, notes`")
        with col_b:
            st.markdown("**Health Metrics:** `metric_id, patient_id, appointment_id, date, plaque_score, gum_bleeding_sites, cavity_count, pocket_depth_avg_mm, xray_taken, oral_hygiene_score`")
            st.markdown("**Treatments:** `treatment_id, patient_id, appointment_id, date, procedure, tooth_number, cost_usd, insurance_covered_usd, patient_owes_usd`")

    # ── TAB 2: Add Patient ────────────────────────────────────────────────────
    with tab2:
        st.subheader("Add a New Patient")
        with st.form("add_patient_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            p_name     = f1.text_input("Full Name *", placeholder="e.g. John Doe")
            p_age      = f2.number_input("Age *", min_value=1, max_value=120, value=30)
            f3, f4 = st.columns(2)
            p_gender   = f3.selectbox("Gender", ["Male","Female","Other","Prefer not to say"])
            p_risk     = f4.selectbox("Risk Level", ["Low","Medium","High"])
            f5, f6 = st.columns(2)
            p_phone    = f5.text_input("Phone", placeholder="(555) 123-4567")
            p_email    = f6.text_input("Email", placeholder="patient@email.com")
            f7, f8 = st.columns(2)
            p_insurance = f7.selectbox("Insurance", ["Delta Dental","MetLife Dental","Cigna Dental",
                                                      "Aetna Dental","BlueCross Dental","Self-Pay"])
            p_last_visit = f8.date_input("Last Visit Date", value=datetime.today())
            f9, f10 = st.columns(2)
            p_next_appt = f9.date_input("Next Appointment", value=datetime.today() + timedelta(days=180))

            submitted = st.form_submit_button("➕ Add Patient", type="primary")
            if submitted:
                if not p_name.strip():
                    st.error("Patient name is required.")
                else:
                    existing = st.session_state.patients_df
                    new_id_num = int(existing["patient_id"].str.replace("P","").astype(int).max()) + 1
                    days_since = (datetime.today() - datetime.combine(p_last_visit, datetime.min.time())).days
                    new_row = pd.DataFrame([{
                        "patient_id": f"P{new_id_num:03d}",
                        "name": p_name.strip(),
                        "age": int(p_age),
                        "gender": p_gender,
                        "phone": p_phone,
                        "email": p_email,
                        "insurance": p_insurance,
                        "risk_level": p_risk,
                        "last_visit": p_last_visit.strftime("%Y-%m-%d"),
                        "next_appointment": p_next_appt.strftime("%Y-%m-%d"),
                        "days_since_last_visit": days_since,
                    }])
                    updated = pd.concat([existing, new_row], ignore_index=True)
                    updated.to_csv("data_ai/patients.csv", index=False)
                    st.session_state.patients_df = updated
                    st.success(f"✅ Patient **{p_name}** added successfully! (ID: P{new_id_num:03d})")
                    st.rerun()

    # ── TAB 3: Add Appointment ────────────────────────────────────────────────
    with tab3:
        st.subheader("Add a New Appointment")
        with st.form("add_appt_form", clear_on_submit=True):
            patient_list = patients_df["name"].sort_values().tolist()
            a1, a2 = st.columns(2)
            a_patient  = a1.selectbox("Patient *", patient_list)
            a_date     = a2.date_input("Appointment Date *", value=datetime.today() + timedelta(days=7))
            a3, a4 = st.columns(2)
            a_type     = a3.selectbox("Type", ["Checkup & Cleaning","Filling","Root Canal","Extraction",
                                               "Orthodontic Consult","Whitening","Crown Prep","Periodontal Scaling"])
            a_dentist  = a4.selectbox("Dentist", ["Dr. Patel","Dr. Kim","Dr. Rodriguez","Dr. Thompson"])
            a5, a6 = st.columns(2)
            a_status   = a5.selectbox("Status", ["Scheduled","Completed","Cancelled","No-Show"])
            a_duration = a6.selectbox("Duration (min)", [30, 45, 60, 90])
            a_notes    = st.text_area("Notes", placeholder="Optional notes about this appointment", height=80)

            submitted2 = st.form_submit_button("➕ Add Appointment", type="primary")
            if submitted2:
                pid = patients_df[patients_df["name"] == a_patient]["patient_id"].values[0]
                existing_appts = st.session_state.appt_df
                new_appt_num = len(existing_appts) + 1
                new_appt = pd.DataFrame([{
                    "appointment_id": f"A{new_appt_num:04d}",
                    "patient_id": pid,
                    "date": a_date.strftime("%Y-%m-%d"),
                    "type": a_type,
                    "status": a_status,
                    "dentist": a_dentist,
                    "duration_min": a_duration,
                    "notes": a_notes.strip(),
                }])
                updated_appts = pd.concat([existing_appts, new_appt], ignore_index=True)
                updated_appts.to_csv("data_ai/appointments.csv", index=False)
                st.session_state.appt_df = updated_appts
                st.success(f"✅ Appointment for **{a_patient}** on **{a_date}** added!")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HEALTH HISTORY
# ══════════════════════════════════════════════════════════════════════════════

elif page == "🏥 Health History":
    st.title("🏥 Patient Health History")
    st.markdown("Medical background and dental health trends for each patient.")
    st.markdown("---")

    selected_name = st.selectbox("Select a Patient", patients_df["name"].sort_values().tolist())
    patient  = patients_df[patients_df["name"] == selected_name].iloc[0]
    pid      = patient["patient_id"]
    hh       = health_history_df[health_history_df["patient_id"] == pid]

    st.markdown("---")

    # ── Medical Background ────────────────────────────────────────────────────
    st.subheader("Medical Background")
    hh1, hh2, hh3, hh4, hh5 = st.columns(5)
    if not hh.empty:
        row = hh.iloc[0]
        hh1.metric("Medical Conditions", row["medical_conditions"])
        hh2.metric("Allergies",          row["allergies"])
        hh3.metric("Medications",        row["current_medications"])
        hh4.metric("Blood Type",         row["blood_type"])
        hh5.metric("Smoking Status",     row["smoking_status"])

        if row["medical_conditions"] not in ["None", ""]:
            st.warning(f"⚠️ Note: Patient has **{row['medical_conditions']}** — may affect treatment planning and medication choices.")
        if row["allergies"] not in ["None", ""]:
            st.error(f"🚨 Allergy Alert: **{row['allergies']}** — verify before prescribing.")
    else:
        st.info("No health history on file for this patient.")

    st.markdown("---")

    # ── Dental Health Trends ──────────────────────────────────────────────────
    st.subheader("Dental Health Trends Over Time")
    pt_metrics = (metrics_df[metrics_df["patient_id"] == pid]
                  .copy()
                  .sort_values("date"))

    if len(pt_metrics) < 2:
        st.info("Not enough visit data to show trends — need at least 2 completed visits.")
    else:
        pt_metrics["date"] = pd.to_datetime(pt_metrics["date"]).dt.strftime("%Y-%m-%d")
        pt_metrics = pt_metrics.set_index("date")

        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown("**Plaque Score** (lower is better)")
            st.line_chart(pt_metrics[["plaque_score"]], height=200, use_container_width=True)
        with tc2:
            st.markdown("**Oral Hygiene Score** (higher is better)")
            st.line_chart(pt_metrics[["oral_hygiene_score"]], height=200, use_container_width=True)
        with tc3:
            st.markdown("**Cavity Count**")
            st.line_chart(pt_metrics[["cavity_count"]], height=200, use_container_width=True)

        tc4, tc5 = st.columns(2)
        with tc4:
            st.markdown("**Gum Bleeding Sites** (lower is better)")
            st.line_chart(pt_metrics[["gum_bleeding_sites"]], height=200, use_container_width=True)
        with tc5:
            st.markdown("**Pocket Depth (mm)** (lower is better)")
            st.line_chart(pt_metrics[["pocket_depth_avg_mm"]], height=200, use_container_width=True)

    st.markdown("---")

    # ── Visit Notes Timeline ──────────────────────────────────────────────────
    st.subheader("Visit Notes Timeline")
    pt_appts = (appt_df[appt_df["patient_id"] == pid]
                .copy()
                .sort_values("date", ascending=False))
    pt_appts = pt_appts[pt_appts["status"] == "Completed"]

    if pt_appts.empty:
        st.info("No completed visits on record.")
    else:
        for _, appt in pt_appts.iterrows():
            with st.expander(f"📅 {appt['date']}  —  {appt['type']}  ({appt['dentist']})"):
                if appt["notes"]:
                    st.write(appt["notes"])
                else:
                    st.caption("No notes recorded for this visit.")

    st.markdown("---")

    # ── Edit Health Record ────────────────────────────────────────────────────
    st.subheader("Update Health Record")
    existing = hh.iloc[0] if not hh.empty else None
    with st.form("edit_health_form", clear_on_submit=False):
        ef1, ef2, ef3 = st.columns(3)
        conditions_list = ["None","Diabetes Type 2","Hypertension","Heart Disease",
                           "Asthma","Osteoporosis","Thyroid Disorder","Diabetes Type 1"]
        allergies_list  = ["None","Penicillin","Latex","Aspirin","Sulfa Drugs","Codeine","Ibuprofen"]
        meds_list       = ["None","Metformin","Lisinopril","Atorvastatin","Warfarin",
                           "Levothyroxine","Amlodipine","Aspirin Daily"]
        smoking_list    = ["Non-Smoker","Former Smoker","Current Smoker"]
        blood_list      = ["A+","A-","B+","B-","O+","O-","AB+","AB-"]

        def idx(lst, val):
            return lst.index(val) if val in lst else 0

        e_cond    = ef1.selectbox("Medical Conditions", conditions_list,
                                   index=idx(conditions_list, existing["medical_conditions"]) if existing is not None else 0)
        e_allergy = ef2.selectbox("Allergies", allergies_list,
                                   index=idx(allergies_list, existing["allergies"]) if existing is not None else 0)
        e_med     = ef3.selectbox("Current Medications", meds_list,
                                   index=idx(meds_list, existing["current_medications"]) if existing is not None else 0)
        ef4, ef5 = st.columns(2)
        e_blood   = ef4.selectbox("Blood Type", blood_list,
                                   index=idx(blood_list, existing["blood_type"]) if existing is not None else 0)
        e_smoke   = ef5.selectbox("Smoking Status", smoking_list,
                                   index=idx(smoking_list, existing["smoking_status"]) if existing is not None else 0)

        if st.form_submit_button("💾 Save Health Record", type="primary"):
            updated_hh = health_history_df.copy()
            new_row = {
                "patient_id":          pid,
                "medical_conditions":  e_cond,
                "allergies":           e_allergy,
                "current_medications": e_med,
                "blood_type":          e_blood,
                "smoking_status":      e_smoke,
                "last_updated":        datetime.today().strftime("%Y-%m-%d"),
            }
            if pid in updated_hh["patient_id"].values:
                updated_hh.loc[updated_hh["patient_id"] == pid, list(new_row.keys())] = list(new_row.values())
            else:
                updated_hh = pd.concat([updated_hh, pd.DataFrame([new_row])], ignore_index=True)
            updated_hh.to_csv("data_ai/health_history.csv", index=False)
            st.session_state.health_history_df = updated_hh
            st.success(f"✅ Health record for **{selected_name}** updated!")
            st.rerun()

