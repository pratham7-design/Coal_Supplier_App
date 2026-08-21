import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Coal Supply Portal", page_icon="🏭", layout="wide")

# Secret Admin Password (Change "coaladmin123" to your preferred password)
ADMIN_PASSWORD = "coaladmin123"

# Initialize live inventory in session memory if not already loaded
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {
            "Coal Grade": "Imported Indonesian Coal",
            "Available Stock (Tons)": 10000,
            "Base Rate (₹/Ton)": 6500,
            "Location / Depot": "Vizag Port",
            "Status": "Available"
        },
        {
            "Coal Grade": "High-Calorific US Coal",
            "Available Stock (Tons)": 5000,
            "Base Rate (₹/Ton)": 11500,
            "Location / Depot": "Mundra Port",
            "Status": "Available"
        },
        {
            "Coal Grade": "Domestic Steam Coal (G-10)",
            "Available Stock (Tons)": 25000,
            "Base Rate (₹/Ton)": 4200,
            "Location / Depot": "Bilaspur Depot",
            "Status": "Available"
        }
    ])

# Navigation sidebar
st.sidebar.title("📌 Portal Navigation")
user_role = st.sidebar.radio("Select View:", ["Buyer / Customer View", "Seller Admin Panel"])

# -------------------------------------------------------------
# 1. BUYER / CUSTOMER VIEW
# -------------------------------------------------------------
if user_role == "Buyer / Customer View":
    st.title("🏭 Premium Industrial Coal Supplier")
    st.caption("Live Inventory, Location-based Rates, and Direct Orders")
    st.divider()

    st.header("📦 Available Live Stock & Rates")
    
    # Filter by location
    locations = ["All"] + list(st.session_state.inventory["Location / Depot"].unique())
    selected_loc = st.selectbox("Filter Stock by Port / Depot Location:", locations)

    if selected_loc != "All":
        display_df = st.session_state.inventory[st.session_state.inventory["Location / Depot"] == selected_loc]
    else:
        display_df = st.session_state.inventory

    # Show inventory table to buyers
    st.dataframe(display_df, use_container_width=True)

    st.divider()

    # Direct Inquiry Form
    st.header("📝 Request Price Quote / Order Coal")
    with st.form("customer_order_form"):
        c1, c2 = st.columns(2)
        with c1:
            company_name = st.text_input("Company / Industry Name *")
            whatsapp_no = st.text_input("WhatsApp / Mobile Number *")
            delivery_city = st.text_input("Delivery Location (City/State) *")
        with c2:
            selected_coal = st.selectbox("Select Coal Grade", st.session_state.inventory["Coal Grade"].tolist())
            qty_needed = st.number_input("Required Tonnage (MT)", min_value=10, step=50)

        submit = st.form_submit_button("Submit Requirements")
        if submit:
            if company_name and whatsapp_no and delivery_city:
                st.success(f"Thank you {company_name}! Your request for {qty_needed} MT of {selected_coal} has been sent to the supplier.")
            else:
                st.error("Please fill in all required fields.")

    # WhatsApp Direct Button
    st.markdown("---")
    st.subheader("💬 Immediate Purchase?")
    st.markdown("[Click here to Chat directly on WhatsApp](https://wa.me/91XXXXXXXXXX?text=Hi,%20I%20want%20to%20buy%20coal)")

# -------------------------------------------------------------
# 2. SELLER ADMIN PANEL (PROTECTED)
# -------------------------------------------------------------
elif user_role == "Seller Admin Panel":
    st.title("🔐 Seller Admin Dashboard")
    st.caption("Only authorized business owners can update rates and stock here.")
    
    # Password verification
    password_input = st.text_input("Enter Admin Password:", type="password")

    if password_input == ADMIN_PASSWORD:
        st.success("Access Granted! You can now update stock details below.")
        st.divider()

        st.subheader("⚙️ Edit Live Stock & Rates Data")
        st.info("Make changes directly in the table below. Values will update for buyers instantly.")

        # Editable dataframe for the admin
        updated_df = st.data_editor(st.session_state.inventory, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Save All Changes"):
            st.session_state.inventory = updated_df
            st.success("Stock and rates updated successfully!")
            
    elif password_input != "":
        st.error("Incorrect password! Access denied.")



