import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# -------------------------------------------------------------
# PAGE CONFIGURATION & SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="Global Coal Logistics & Supply", page_icon="🏭", layout="wide")

# Admin Password
ADMIN_PASSWORD = "coaladmin123"

# Google Sheet URL (Replace with your actual public Google Sheet link)
GSHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit#gid=0"

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        df = conn.read(spreadsheet=GSHEET_URL, ttl="0")
        return df
    except Exception:
        # Fallback default data if sheet URL isn't configured yet
        return pd.DataFrame([
            {"Coal Grade": "Imported Indonesian Coal", "Available Stock (Tons)": 10000, "Base Rate (₹/Ton)": 6500, "Location / Depot": "Vizag Port", "Status": "Available"},
            {"Coal Grade": "High-Calorific US Coal", "Available Stock (Tons)": 5000, "Base Rate (₹/Ton)": 11500, "Location / Depot": "Mundra Port", "Status": "Available"},
            {"Coal Grade": "Domestic Steam Coal (G-10)", "Available Stock (Tons)": 25000, "Base Rate (₹/Ton)": 4200, "Location / Depot": "Bilaspur Depot", "Status": "Available"}
        ])

inventory_df = load_data()

# -------------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------------
st.sidebar.title("📌 Portal Navigation")
user_role = st.sidebar.radio("View Mode:", ["Buyer Portal", "Seller Admin Panel"])

# -------------------------------------------------------------
# 1. BUYER PORTAL (Customer View)
# -------------------------------------------------------------
if user_role == "Buyer Portal":
    st.title("🏭 Premium Industrial Coal Logistics & Wholesale Supply")
    st.caption("Supplying certified high-grade thermal, steam, and coking coal to industrial plants.")
    
    st.info("💡 **Bulk Buyers Notice:** For orders above 5,000 MT, contact dispatch directly via WhatsApp.")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📦 Live Inventory & Specs", "🧮 Price Calculator", "📝 Request Formal Quote"])

    # TAB 1: Live Inventory
    with tab1:
        st.header("Certified Coal Stock Inventory")
        
        # Location Filter
        locations = ["All"] + list(inventory_df["Location / Depot"].unique())
        selected_loc = st.selectbox("Filter Stock by Location:", locations)

        if selected_loc != "All":
            filtered_df = inventory_df[inventory_df["Location / Depot"] == selected_loc]
        else:
            filtered_df = inventory_df

        st.dataframe(filtered_df, use_container_width=True)
        
        st.subheader("📄 Technical Data Sheets")
        st.download_button(
            label="Download Sample Lab Report (PDF)",
            data="Sample Coal Analysis Report: GCV 5800 kcal/kg, Ash 9%",
            file_name="Coal_Lab_Report.txt"
        )

    # TAB 2: Cost Estimator
    with tab2:
        st.header("Estimate Your Order")
        c_a, c_b = st.columns(2)
        
        with c_a:
            selected_grade = st.selectbox("Select Coal Grade", inventory_df["Coal Grade"].tolist())
            tonnage = st.number_input("Required Quantity (Metric Tons)", min_value=10, value=500, step=50)
            transport = st.radio("Delivery Mode", ["Railway Rake", "Road Transport (Trucks)", "Ex-Depot Pick Up"])
        
        with c_b:
            # Match selected grade price from current database
            match = inventory_df[inventory_df["Coal Grade"] == selected_grade]
            base_rate = float(match["Base Rate (₹/Ton)"].values[0]) if not match.empty else 5000.0
            
            material_cost = base_rate * tonnage
            freight_rate = 800 if transport == "Road Transport (Trucks)" else (500 if transport == "Railway Rake" else 0)
            freight_cost = freight_rate * tonnage
            total_estimate = material_cost + freight_cost
            
            st.subheader("Estimated Cost Breakdown")
            st.metric("Material Cost", f"₹{material_cost:,.2f}")
            st.metric("Freight Cost", f"₹{freight_cost:,.2f}")
            st.metric("Total Estimate", f"₹{total_estimate:,.2f}")

    # TAB 3: Direct Inquiry
    with tab3:
        st.header("Request an Official Proforma Invoice")
        with st.form("b2b_inquiry"):
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input("Company Name *")
                gst_no = st.text_input("GST / Tax ID")
                contact_person = st.text_input("Contact Person Name *")
            with col2:
                phone = st.text_input("WhatsApp / Mobile Number *")
                email = st.text_input("Official Email")
                delivery_location = st.text_input("Plant / Delivery Location *")
                
            submit = st.form_submit_button("Submit Formal Request")
            if submit:
                if company and phone and delivery_location:
                    st.success("Your RFQ has been logged. Our sales team will reach out shortly.")
                else:
                    st.error("Please fill in required fields (*).")

    st.divider()
    # Replace 919876543210 with your actual phone number below
    st.markdown("💬 **Direct Line:** [Chat with Sales Manager on WhatsApp](https://wa.me/919335277466?text=Hi,%20I%20visited%20your%20Coal%20App%20and%20need%20a%20quote)")

# -------------------------------------------------------------
# 2. SELLER ADMIN PANEL (Protected Updates)
# -------------------------------------------------------------
elif user_role == "Seller Admin Panel":
    st.title("🔐 Seller Admin Dashboard")
    st.caption("Update stock quantities, location rates, and product availability.")
    
    pwd = st.text_input("Enter Admin Password:", type="password")

    if pwd == ADMIN_PASSWORD:
        st.success("Authenticated Successfully.")
        st.divider()

        st.subheader("⚙️ Live Database Manager")
        st.info("Edit values directly below and click save. Updates sync with Google Sheets live.")

        # Interactive Data Editor
        edited_df = st.data_editor(inventory_df, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Push Updates to Live Database"):
            try:
                conn.update(spreadsheet=GSHEET_URL, data=edited_df)
                st.success("Database updated! Customers can now see the updated rates.")
            except Exception as e:
                st.error(f"Error saving to database: {e}")
                
    elif pwd != "":
        st.error("Incorrect password!")




