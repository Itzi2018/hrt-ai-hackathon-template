import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Smiles By Alex — Patient Monitor", layout="wide", page_icon="🦷")

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


def generate_acquisition_data():
    os.makedirs("data_ai", exist_ok=True)
    random.seed(99)
    today_d = datetime.today()

    segments = [
        {"segment": "Vietnamese Families",       "population": 14000, "pct_insured": 58,  "avg_household_income": 82000,  "primary_language": "Vietnamese/English", "annual_dental_visit_rate": 45, "best_channel": "Vietnamese Community Media"},
        {"segment": "Korean Community",           "population": 4500,  "pct_insured": 72,  "avg_household_income": 105000, "primary_language": "Korean/English",     "annual_dental_visit_rate": 55, "best_channel": "Korean Language Outreach"},
        {"segment": "Caucasian Families",       "population": 19000, "pct_insured": 75,  "avg_household_income": 110000, "primary_language": "English",            "annual_dental_visit_rate": 68, "best_channel": "Nextdoor / Google Ads"},
        {"segment": "Hispanic/Latino Families",   "population": 8500,  "pct_insured": 45,  "avg_household_income": 65000,  "primary_language": "Spanish/English",    "annual_dental_visit_rate": 38, "best_channel": "Facebook / Spanish Outreach"},
        {"segment": "Seniors 65+",                "population": 11000, "pct_insured": 85,  "avg_household_income": 55000,  "primary_language": "English",            "annual_dental_visit_rate": 72, "best_channel": "Senior Center Outreach"},
        {"segment": "Young Adults 25-34",         "population": 9500,  "pct_insured": 52,  "avg_household_income": 75000,  "primary_language": "English",            "annual_dental_visit_rate": 42, "best_channel": "Instagram / Yelp"},
        {"segment": "Families with Young Children","population": 7500, "pct_insured": 65,  "avg_household_income": 95000,  "primary_language": "English",            "annual_dental_visit_rate": 60, "best_channel": "School Partnerships (FVUSD)"},
    ]
    for s in segments:
        s["est_unserved_residents"] = round(s["population"] * (1 - s["annual_dental_visit_rate"] / 100))
        s["opportunity_score"]      = round(s["est_unserved_residents"] * (s["pct_insured"] / 100))
    fv_demo_df = pd.DataFrame(segments)
    fv_demo_df.to_csv("data_ai/fv_demographics.csv", index=False)

    channels = [
        {"channel": "Google Business Optimization",       "monthly_cost": 200, "monthly_reach": 3500, "est_new_patients_monthly": 8, "best_segment": "All",                      "roi_score": 9,  "notes": "High-intent searches; free with setup cost"},
        {"channel": "Nextdoor Advertising",               "monthly_cost": 300, "monthly_reach": 2800, "est_new_patients_monthly": 6, "best_segment": "Caucasian Families",     "roi_score": 8,  "notes": "Hyper-local; neighbors trust recommendations"},
        {"channel": "Facebook/Instagram Ads",             "monthly_cost": 500, "monthly_reach": 5000, "est_new_patients_monthly": 9, "best_segment": "Hispanic / Young Adults",  "roi_score": 8,  "notes": "Targeted by zip code; multilingual options"},
        {"channel": "Yelp Premium",                       "monthly_cost": 400, "monthly_reach": 2200, "est_new_patients_monthly": 5, "best_segment": "Young Adults / All",       "roi_score": 7,  "notes": "High conversion for comparison shoppers"},
        {"channel": "Vietnamese Community Media",         "monthly_cost": 350, "monthly_reach": 4500, "est_new_patients_monthly": 7, "best_segment": "Vietnamese Families",      "roi_score": 9,  "notes": "Little Saigon radio, newspapers, Zalo/WeChat"},
        {"channel": "School Partnerships (FVUSD)",        "monthly_cost": 150, "monthly_reach": 1800, "est_new_patients_monthly": 4, "best_segment": "Families w/ Children",     "roi_score": 8,  "notes": "Back-to-school dental checkup campaigns"},
        {"channel": "Senior Center Outreach",             "monthly_cost": 100, "monthly_reach": 800,  "est_new_patients_monthly": 3, "best_segment": "Seniors 65+",              "roi_score": 9,  "notes": "Low cost; high trust; Medicare/Medi-Cal referrals"},
        {"channel": "Referral Program",                   "monthly_cost": 250, "monthly_reach": 0,    "est_new_patients_monthly": 5, "best_segment": "All",                      "roi_score": 10, "notes": "Incentivize current patients — highest conversion"},
        {"channel": "Community Events (Mile Square Park)","monthly_cost": 400, "monthly_reach": 3000, "est_new_patients_monthly": 6, "best_segment": "Vietnamese/Hispanic Families","roi_score": 7,"notes": "Health fair booths; free screenings build trust"},
        {"channel": "Korean Language Outreach",           "monthly_cost": 200, "monthly_reach": 1500, "est_new_patients_monthly": 4, "best_segment": "Korean Community",         "roi_score": 9,  "notes": "KakaoTalk groups, Korean church bulletin boards"},
    ]
    for c in channels:
        c["cost_per_patient"]         = round(c["monthly_cost"] / c["est_new_patients_monthly"], 2)
        c["monthly_revenue_potential"] = c["est_new_patients_monthly"] * 350
    mktg_df = pd.DataFrame(channels)
    mktg_df.to_csv("data_ai/marketing_channels.csv", index=False)

    lead_names = [
        ("Linh","Nguyen"),("David","Kim"),("Maria","Flores"),("James","Anderson"),
        ("Mei","Chen"),("Rosa","Martinez"),("Kevin","Park"),("Jennifer","Tran"),
        ("Michael","Lopez"),("Susan","Lee"),("Carlos","Ramirez"),("Emily","Pham"),
        ("Robert","Johnson"),("Anh","Le"),("Jessica","Wong"),("Thomas","Garcia"),
        ("Yuna","Choi"),("Patricia","Hernandez"),("Daniel","Nguyen"),("Sarah","Smith"),
    ]
    sources   = ["Google Search","Nextdoor","Facebook Ad","Vietnamese Media","Patient Referral",
                 "Yelp","Community Event","School Flyer","Walk-In","Korean Church"]
    seg_names = [s["segment"] for s in segments]
    statuses  = ["New Lead","Contacted","Appointment Set","Converted","Not Interested"]
    leads = []
    for i, (fn, ln) in enumerate(lead_names, 1):
        src = random.choice(sources)
        if "Vietnamese" in src:
            seg = "Vietnamese Families"
        elif "Korean" in src:
            seg = "Korean Community"
        elif "School" in src:
            seg = "Families with Young Children"
        else:
            seg = random.choice(seg_names)
        leads.append({
            "lead_id":    f"L{i:03d}",
            "first_name": fn, "last_name": ln,
            "phone":      f"({random.randint(700,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
            "email":      f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@email.com",
            "source":     src, "segment": seg,
            "status":     random.choices(statuses, [0.25, 0.30, 0.20, 0.15, 0.10])[0],
            "date_added": (today_d - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            "notes":      random.choice(["Interested in whitening","Family looking for dentist",
                                          "Needs cleaning","Moving to FV soon","Saw us at community event",
                                          "Referred by existing patient","","",""]),
        })
    leads_df = pd.DataFrame(leads)
    leads_df.to_csv("data_ai/leads.csv", index=False)
    return fv_demo_df, mktg_df, leads_df


def load_acquisition_data():
    if not os.path.exists("data_ai/fv_demographics.csv"):
        return generate_acquisition_data()
    return (
        pd.read_csv("data_ai/fv_demographics.csv"),
        pd.read_csv("data_ai/marketing_channels.csv"),
        pd.read_csv("data_ai/leads.csv"),
    )


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

if "fv_demo_df" not in st.session_state:
    fd, mkt, ld = load_acquisition_data()
    st.session_state.fv_demo_df = fd
    st.session_state.mktg_df    = mkt
    st.session_state.leads_df   = ld

fv_demo_df = st.session_state.fv_demo_df
mktg_df    = st.session_state.mktg_df
leads_df   = st.session_state.leads_df
today_str  = datetime.today().strftime("%Y-%m-%d")

# ─── Sidebar Navigation ───────────────────────────────────────────────────────

st.sidebar.image("https://img.icons8.com/emoji/96/tooth-emoji.png", width=64)
st.sidebar.title("🦷 Smiles By Alex")
st.sidebar.caption("Patient Monitoring System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "👥 Patients", "📅 Appointments", "🚨 Alerts", "🏘️ Grow Practice", "➕ Add Data"],
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

    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Patients by Insurance Provider")
        ins_counts = patients_df["insurance"].value_counts().rename_axis("Insurance").reset_index(name="Patients")
        st.bar_chart(ins_counts.set_index("Insurance"), height=260, use_container_width=True)
    with col6:
        st.subheader("Revenue Summary")
        total_billed = treatments_df["cost_usd"].sum()
        total_covered = treatments_df["insurance_covered_usd"].sum()
        total_owed = treatments_df["patient_owes_usd"].sum()
        r1, r2, r3 = st.columns(3)
        r1.metric("Total Billed", f"${total_billed:,.0f}")
        r2.metric("Insurance Paid", f"${total_covered:,.0f}")
        r3.metric("Patient Balance", f"${total_owed:,.0f}")
        rev_df = pd.DataFrame({"Category": ["Insurance Covered","Patient Owes"],
                               "Amount": [total_covered, total_owed]})
        st.bar_chart(rev_df.set_index("Category"), height=170, use_container_width=True)


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
        st.dataframe(p_treats[["date","procedure","tooth_number","cost_usd",
                                "insurance_covered_usd","patient_owes_usd"]].rename(
            columns={"date":"Date","procedure":"Procedure","tooth_number":"Tooth #",
                     "cost_usd":"Cost ($)","insurance_covered_usd":"Covered ($)",
                     "patient_owes_usd":"Patient Owes ($)"}),
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
# PAGE: GROW PRACTICE
# ══════════════════════════════════════════════════════════════════════════════

elif page == "🏘️ Grow Practice":
    st.title("🏘️ Grow Your Practice")
    st.markdown("Attract new patients by targeting Fountain Valley's key community segments with the right outreach strategy.")
    st.markdown("---")

    total_leads = len(leads_df)
    converted   = len(leads_df[leads_df["status"] == "Converted"])
    in_pipeline = len(leads_df[leads_df["status"].isin(["New Lead","Contacted","Appointment Set"])])
    conv_rate   = round(converted / total_leads * 100, 1) if total_leads > 0 else 0
    best_ch     = mktg_df.sort_values("roi_score", ascending=False).iloc[0]["channel"]

    gk1, gk2, gk3, gk4 = st.columns(4)
    gk1.metric("Active Leads", total_leads)
    gk2.metric("Converted to Patients", converted, delta=f"{conv_rate}% conversion")
    gk3.metric("In Pipeline", in_pipeline)
    gk4.metric("Highest ROI Channel", best_ch[:22] + "…" if len(best_ch) > 22 else best_ch)

    st.markdown("---")

    gt1, gt2, gt3, gt4 = st.tabs(["📊 FV Demographics", "🎯 Target Segments", "📣 Marketing Channels", "👤 Lead Tracker"])

    # ── TAB 1: Demographics ───────────────────────────────────────────────────
    with gt1:
        st.subheader("Fountain Valley, CA — Community Snapshot")
        st.caption("Population ≈ 57,000 · Median Age 41 · Median HH Income ~$93,000 · ~42% Asian, ~35% White, ~15% Hispanic")

        da1, da2 = st.columns(2)
        with da1:
            st.markdown("**Population by Community Segment**")
            st.bar_chart(fv_demo_df[["segment","population"]].set_index("segment"), height=300, use_container_width=True)
        with da2:
            st.markdown("**Estimated Residents Without a Regular Dentist**")
            st.bar_chart(fv_demo_df[["segment","est_unserved_residents"]].set_index("segment"), height=300, use_container_width=True)

        st.markdown("---")
        st.subheader("Annual Dental Visit Rate by Segment (%)")
        st.caption("Lower % = more residents not seeing a dentist regularly = larger growth opportunity for your practice.")
        st.bar_chart(fv_demo_df[["segment","annual_dental_visit_rate"]].set_index("segment"), height=250, use_container_width=True)

        st.markdown("---")
        disp = fv_demo_df[["segment","population","pct_insured","avg_household_income",
                             "annual_dental_visit_rate","est_unserved_residents","best_channel"]].copy()
        disp.columns = ["Segment","Population","% Insured","Avg HH Income ($)","Dental Visit Rate (%)","Est. Unserved","Best Outreach Channel"]
        st.dataframe(disp, use_container_width=True, hide_index=True)

    # ── TAB 2: Target Segments ────────────────────────────────────────────────
    with gt2:
        st.subheader("Patient Acquisition Opportunity Score")
        st.caption("Score = Est. Unserved Residents × (% Insured ÷ 100). Higher = more reachable, insured prospects in that community.")

        top_segs = fv_demo_df.sort_values("opportunity_score", ascending=False).reset_index(drop=True)
        st.bar_chart(top_segs[["segment","opportunity_score"]].set_index("segment"), height=280, use_container_width=True)

        st.markdown("---")
        st.subheader("Recommendations by Segment")
        for idx, row in top_segs.iterrows():
            icon = "🥇" if idx == 0 else ("🥈" if idx == 1 else ("🥉" if idx == 2 else "📌"))
            with st.expander(f"{icon} {row['segment']}  —  Opportunity Score: {int(row['opportunity_score']):,}"):
                sc1, sc2, sc3 = st.columns(3)
                sc1.metric("Est. Unserved Residents", f"{int(row['est_unserved_residents']):,}")
                sc2.metric("% with Dental Insurance", f"{int(row['pct_insured'])}%")
                sc3.metric("Avg Household Income",    f"${int(row['avg_household_income']):,}")
                st.info(f"**Recommended Channel:** {row['best_channel']}  ·  **Primary Language:** {row['primary_language']}")

    # ── TAB 3: Marketing Channels ─────────────────────────────────────────────
    with gt3:
        st.subheader("Marketing Channel Comparison — Fountain Valley")
        budget = st.slider("Monthly Marketing Budget ($)", min_value=100, max_value=3000, value=1500, step=50)

        mktg_sorted = mktg_df.sort_values("roi_score", ascending=False).copy()
        affordable  = mktg_sorted[mktg_sorted["monthly_cost"] <= budget]

        if not affordable.empty:
            bm1, bm2, bm3 = st.columns(3)
            bm1.metric("Channels Within Budget",  len(affordable))
            bm2.metric("Est. New Patients/Month", int(affordable["est_new_patients_monthly"].sum()),
                       delta=f"${int(affordable['monthly_cost'].sum()):,}/mo spent")
            bm3.metric("Est. Revenue Potential",  f"${int(affordable['monthly_revenue_potential'].sum()):,}")

        st.markdown("---")
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("**New Patients per Month (by Channel)**")
            st.bar_chart(mktg_sorted[["channel","est_new_patients_monthly"]].set_index("channel"), height=300, use_container_width=True)
        with mc2:
            st.markdown("**ROI Score (1–10, higher is better)**")
            st.bar_chart(mktg_sorted[["channel","roi_score"]].set_index("channel"), height=300, use_container_width=True)

        st.markdown("---")
        disp_mktg = mktg_sorted[["channel","monthly_cost","est_new_patients_monthly",
                                   "cost_per_patient","roi_score","best_segment","notes"]].copy()
        disp_mktg.columns = ["Channel","Monthly Cost ($)","New Patients/Mo",
                               "Cost per Patient ($)","ROI Score","Best For","Notes"]

        def color_roi(row):
            if row["ROI Score"] >= 9:
                return ["background-color: #e0ffe8"] * len(row)
            elif row["ROI Score"] == 8:
                return ["background-color: #fff9e0"] * len(row)
            return [""] * len(row)

        st.dataframe(disp_mktg.style.apply(color_roi, axis=1), use_container_width=True, hide_index=True)

    # ── TAB 4: Lead Tracker ───────────────────────────────────────────────────
    with gt4:
        st.subheader("Prospective Patient Lead Tracker")

        funnel  = ["New Lead","Contacted","Appointment Set","Converted","Not Interested"]
        scounts = leads_df["status"].value_counts()
        lk1, lk2, lk3, lk4, lk5 = st.columns(5)
        for col, s in zip([lk1, lk2, lk3, lk4, lk5], funnel):
            col.metric(s, int(scounts.get(s, 0)))

        st.markdown("---")

        lfc1, lfc2 = st.columns(2)
        lead_st_f  = lfc1.selectbox("Filter by Status", ["All"] + funnel, key="lt_status")
        lead_src_f = lfc2.selectbox("Filter by Source", ["All"] + sorted(leads_df["source"].unique().tolist()), key="lt_src")

        flt_leads = leads_df.copy()
        if lead_st_f != "All":
            flt_leads = flt_leads[flt_leads["status"] == lead_st_f]
        if lead_src_f != "All":
            flt_leads = flt_leads[flt_leads["source"] == lead_src_f]

        disp_leads = flt_leads[["lead_id","first_name","last_name","phone","email",
                                  "source","segment","status","date_added","notes"]].copy()
        disp_leads.columns = ["ID","First","Last","Phone","Email","Source","Segment","Status","Date Added","Notes"]

        def color_lead(row):
            c = {"Converted":"#e0ffe8","Appointment Set":"#e0f0ff",
                 "Contacted":"#fff9e0","New Lead":"#f5f5f5","Not Interested":"#ffe0e0"}.get(row["Status"],"")
            return [f"background-color: {c}" if c else "" for _ in row]

        st.dataframe(disp_leads.style.apply(color_lead, axis=1),
                     use_container_width=True, height=300, hide_index=True)

        st.markdown("---")
        st.subheader("Add New Lead")
        with st.form("add_lead_form", clear_on_submit=True):
            fl1, fl2, fl3 = st.columns(3)
            l_first  = fl1.text_input("First Name *")
            l_last   = fl2.text_input("Last Name *")
            l_phone  = fl3.text_input("Phone", placeholder="(714) 555-1234")
            fl4, fl5, fl6 = st.columns(3)
            l_email  = fl4.text_input("Email")
            l_source = fl5.selectbox("How did they find us?",
                ["Google Search","Nextdoor","Facebook Ad","Vietnamese Media","Patient Referral",
                 "Yelp","Community Event","School Flyer","Walk-In","Korean Church","Other"])
            l_seg    = fl6.selectbox("Community Segment", fv_demo_df["segment"].tolist())
            fl7, fl8 = st.columns([1, 2])
            l_status = fl7.selectbox("Status", ["New Lead","Contacted","Appointment Set"])
            l_notes  = fl8.text_input("Notes", placeholder="Optional notes about this lead")

            if st.form_submit_button("➕ Add Lead", type="primary"):
                if not l_first.strip() or not l_last.strip():
                    st.error("First and last name are required.")
                else:
                    new_lid  = len(st.session_state.leads_df) + 1
                    new_lead = pd.DataFrame([{
                        "lead_id":    f"L{new_lid:03d}",
                        "first_name": l_first.strip(), "last_name": l_last.strip(),
                        "phone":      l_phone, "email": l_email,
                        "source":     l_source, "segment": l_seg,
                        "status":     l_status,
                        "date_added": datetime.today().strftime("%Y-%m-%d"),
                        "notes":      l_notes.strip(),
                    }])
                    updated = pd.concat([st.session_state.leads_df, new_lead], ignore_index=True)
                    updated.to_csv("data_ai/leads.csv", index=False)
                    st.session_state.leads_df = updated
                    st.success(f"Lead **{l_first} {l_last}** added successfully!")
                    st.rerun()
