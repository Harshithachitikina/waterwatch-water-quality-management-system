import streamlit as st
import pyodbc
import pandas as pd
from datetime import date

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=HARSHI\\SQLEXPRESS;"   # change this
        "DATABASE=WaterWatchDB;"
        "Trusted_Connection=yes;"
    )

conn = get_connection()
cursor = conn.cursor()

# -----------------------------
# LOGIN SECTION
# -----------------------------
st.sidebar.title("🔐 Login (Admin/Officer/Analyst)")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    query = "SELECT * FROM Users WHERE username=? AND password=?"
    user = pd.read_sql(query, conn, params=(username, password))

    if not user.empty:
        st.session_state["login"] = True
        st.session_state["role"] = user['role'][0]
        st.success(f"Logged in as {user['role'][0]}")
    else:
        st.error("Invalid Credentials")

# -----------------------------
# ROLE HANDLING
# -----------------------------
if "login" in st.session_state:
    role = st.session_state["role"]
else:
    role = "Public"

st.title("💧 WaterWatch - Water Quality Monitoring System")

# -----------------------------
# ROLE-BASED MENU
# -----------------------------
if role == "Admin":
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Add Location", "Add Water Record", "View Reports", "View Alerts"]
    )

elif role == "Officer":
    menu = st.sidebar.selectbox(
        "Menu",
        ["Add Water Record", "View Reports"]
    )

elif role == "Analyst":
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "View Reports", "View Alerts"]
    )

else:  # PUBLIC USER (NO LOGIN)
    st.sidebar.info("Public Access: View Water Reports Only")
    menu = st.sidebar.selectbox(
        "Menu",
        ["View Reports"]
    )

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":
    st.subheader("📊 Dashboard")

    total_locations = pd.read_sql("SELECT COUNT(*) as c FROM Locations", conn)
    total_records = pd.read_sql("SELECT COUNT(*) as c FROM WaterQuality", conn)
    unsafe_count = pd.read_sql("SELECT COUNT(*) as c FROM WaterQuality WHERE status='Unsafe'", conn)

    st.metric("Total Locations", total_locations['c'][0])
    st.metric("Total Records", total_records['c'][0])
    st.metric("Unsafe Cases", unsafe_count['c'][0])

# -----------------------------
# ADD LOCATION (ADMIN)
# -----------------------------
elif menu == "Add Location":
    st.subheader("📍 Add Location")

    area = st.text_input("Area Name")
    district = st.text_input("District")
    state = st.text_input("State")

    if st.button("Save Location"):
        cursor.execute(
            "INSERT INTO Locations(area_name,district,state) VALUES (?,?,?)",
            (area, district, state)
        )
        conn.commit()
        st.success("Location Added Successfully")

# -----------------------------
# ADD WATER RECORD
# -----------------------------
elif menu == "Add Water Record":
    st.subheader("💧 Add Water Record")

    locations = pd.read_sql("SELECT * FROM Locations", conn)

    if locations.empty:
        st.warning("No locations available. Add location first.")
    else:
        location = st.selectbox("Select Location", locations['area_name'])

        ph = st.number_input("pH Value", 0.0, 14.0)
        tds = st.number_input("TDS")
        turbidity = st.number_input("Turbidity")
        hardness = st.number_input("Hardness")

        loc_id = int(
            locations[locations['area_name'] == location]['location_id'].values[0]
        )

        status = "Safe"
        if ph < 6.5 or ph > 8.5 or tds > 500 or turbidity > 5 or hardness > 300:
            status = "Unsafe"

        if st.button("Submit Record"):

            try:
                conn.autocommit = False

                cursor.execute("""
                    INSERT INTO WaterQuality(location_id,ph,tds,turbidity,hardness,status,test_date)
                    OUTPUT INSERTED.record_id
                    VALUES (?,?,?,?,?,?,?)
                """, (loc_id, ph, tds, turbidity, hardness, status, date.today()))

                record_id = cursor.fetchone()[0]

                # ALERT INSERT
                if status == "Unsafe":
                    cursor.execute(
                        "INSERT INTO Alerts(record_id,message) VALUES (?,?)",
                        (record_id, "Unsafe water detected")
                    )

                conn.commit()
                st.success(f"Record Saved Successfully - {status}")

            except:
                conn.rollback()
                st.error("Transaction Failed")

# -----------------------------
# VIEW REPORTS (ALL USERS)
# -----------------------------
elif menu == "View Reports":
    st.subheader("📋 Water Quality Reports")

    query = """
    SELECT L.area_name, W.ph, W.tds, W.turbidity, W.hardness, W.status, W.test_date
    FROM WaterQuality W
    JOIN Locations L ON W.location_id = L.location_id
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.info("No records found")
    else:
        # -----------------------------
        # DATE FILTER
        # -----------------------------
        unique_dates = sorted(df['test_date'].unique())

        selected_date = st.selectbox("Select Date", ["All"] + list(unique_dates))

        if selected_date != "All":
            df = df[df['test_date'] == selected_date]
        
        
        # -----------------------------
        # AREA FILTER (optional)
        # -----------------------------
        areas = ["All"] + list(df['area_name'].unique())
        selected_area = st.selectbox("Select Area", areas)

        if selected_area != "All":
            df = df[df['area_name'] == selected_area]

        # -----------------------------
        # DISPLAY DATA
        # -----------------------------
        st.dataframe(df)

        st.write("### 📊 Graph")
        st.bar_chart(df[['ph','tds','turbidity','hardness']])
# -----------------------------
# VIEW ALERTS (ADMIN + ANALYST)
# -----------------------------
elif menu == "View Alerts":
    st.subheader("⚠️ Unsafe Water Alerts")

    query = """
    SELECT A.alert_id, L.area_name, A.message, W.test_date
    FROM Alerts A
    JOIN WaterQuality W ON A.record_id = W.record_id
    JOIN Locations L ON W.location_id = L.location_id
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.info("No alerts available")
    else:
        st.dataframe(df)
    