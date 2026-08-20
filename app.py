import streamlit as st

# Page Title & Branding
st.set_page_config(page_title="Coal Supply Business", page_icon="🧱")
st.title("🏭 Premium Industrial Coal Supplier")
st.write("Connecting power plants, brick kilns, and manufacturing industries directly with high-grade coal.")

st.divider()

# Section 1: Display Coal Products
st.header("📦 Available Coal Grades")

col1, col2 = st.columns(2)

with col1:
    st.subheader("High GCV Thermal Coal")
    st.markdown("""
    * **Gross Calorific Value (GCV):** 5500–6000 kcal/kg
    * **Ash Content:** < 12%
    * **Moisture:** < 10%
    * **Best For:** Power Plants, Paper Mills
    """)

with col2:
    st.subheader("Low Moisture Steam Coal")
    st.markdown("""
    * **Gross Calorific Value (GCV):** 4200–4800 kcal/kg
    * **Ash Content:** < 18%
    * **Moisture:** < 8%
    * **Best For:** Brick Kilns, Textile Units
    """)

st.divider()

# Section 2: Direct Contact Form for Buyers
st.header("📞 Request a Quote / Direct Inquiry")
st.write("Fill out the details below to receive direct pricing and specs.")

with st.form("inquiry_form"):
    company_name = st.text_input("Your Company / Industry Name")
    contact_number = st.text_input("Phone / WhatsApp Number")
    coal_type = st.selectbox("Select Coal Grade Needed", ["Thermal Coal", "Steam Coal", "Anthracite", "Petcoke"])
    quantity = st.number_input("Required Quantity (in Metric Tons)", min_value=10, step=10)
    
    submitted = st.form_submit_button("Submit Requirement")
    
    if submitted:
        st.success(f"Thank you, {company_name}! Your inquiry for {quantity} MT of {coal_type} has been recorded. We will contact you at {contact_number} shortly.")
        
# Section 3: Direct WhatsApp Link
st.markdown("---")
st.subheader("💬 Need Immediate Quotes?")
st.markdown("[Click here to Chat directly on WhatsApp](https://wa.me/91XXXXXXXXXX?text=Hi,%20I%20am%20interested%20in%20buying%20coal)")
