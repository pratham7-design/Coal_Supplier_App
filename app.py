import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Global Coal Logistics & Supply", page_icon="🏭", layout="wide")

# Header Section
st.title("🏭 Premium Industrial Coal Logistics & Wholesale Supply")
st.caption("Supplying certified high-grade thermal, steam, and coking coal to power plants, cement factories, and industrial units.")

# Quick Contact Banner
st.info("💡 **Bulk Buyers Notice:** For orders above 5,000 MT, contact our dispatch team directly via WhatsApp for negotiated contract rates.")

st.divider()

# TAB 1: Product Catalog & Lab Specs
tab1, tab2, tab3 = st.tabs(["📦 Coal Inventory & Specs", "🧮 Price & Freight Calculator", "📝 Request Formal Quote"])

with tab1:
    st.header("Certified Coal Stock Inventory")
    
    # Dataset of Coal Products
    coal_data = [
        {"Grade": "Imported Indonesian Coal", "GCV (kcal/kg)": "5000 - 5800", "Ash %": "< 8%", "Moisture %": "15 - 25%", "Volatile Matter": "38 - 42%", "Target Industry": "Power Plants, Paper Mills"},
        {"Grade": "High-Calorific US Coal", "GCV (kcal/kg)": "6700 - 7200", "Ash %": "< 10%", "Moisture %": "< 8%", "Volatile Matter": "30 - 35%", "Target Industry": "Cement, Steel Plants"},
        {"Grade": "Domestic Steam Coal (G-10)", "GCV (kcal/kg)": "4300 - 4600", "Ash %": "20 - 24%", "Moisture %": "8 - 12%", "Volatile Matter": "25 - 30%", "Target Industry": "Brick Kilns, Textile Units"},
        {"Grade": "Low Ash Coking Coal", "GCV (kcal/kg)": "6400 - 6800", "Ash %": "< 12%", "Moisture %": "< 5%", "Volatile Matter": "20 - 24%", "Target Industry": "Metallurgical & Steel"},
    ]
    
    df = pd.DataFrame(coal_data)
    st.dataframe(df, use_container_width=True)
    
    st.subheader("📄 Technical Data Sheets")
    st.write("Download certified lab inspection reports (Certificate of Analysis) for quality assurance:")
    st.download_button(label="Download Sample Lab Report (PDF)", data="Sample Coal Analysis Report: GCV 5800 kcal/kg, Ash 9%", file_name="Coal_Lab_Report.txt")

# TAB 2: Cost Estimator
with tab2:
    st.header("Estimate Your Order")
    
    col_a, col_b = st.columns(2)
    with col_a:
        grade = st.selectbox("Select Coal Grade", ["Imported Indonesian Coal", "High-Calorific US Coal", "Domestic Steam Coal", "Coking Coal"])
        tonnage = st.number_input("Required Quantity (Metric Tons)", min_value=50, max_value=50000, value=500, step=50)
        transport = st.radio("Mode of Delivery", ["Railway Rake", "Road Transport (Trucks)", "Ex-Depot Pick Up"])
    
    with col_b:
        # Base pricing estimates
        base_prices = {"Imported Indonesian Coal": 6500, "High-Calorific US Coal": 11500, "Domestic Steam Coal": 4200, "Coking Coal": 14000}
        
        estimated_material_cost = base_prices[grade] * tonnage
        freight_rate = 800 if transport == "Road Transport (Trucks)" else (500 if transport == "Railway Rake" else 0)
        estimated_freight = freight_rate * tonnage
        total_estimate = estimated_material_cost + estimated_freight
        
        st.subheader("Estimated Cost Breakdown")
        st.metric("Material Cost Estimate", f"₹{estimated_material_cost:,.2f}")
        st.metric("Freight Charge Estimate", f"₹{estimated_freight:,.2f}")
        st.metric("Total Approximate Cost", f"₹{total_estimate:,.2f}")
        st.caption("*Note: Prices vary depending on daily port rates, GST, and exact delivery location.")

# TAB 3: Inquiry & Lead Generation
with tab3:
    st.header("Request an Official Proforma Invoice")
    
    with st.form("b2b_inquiry"):
        c1, c2 = st.columns(2)
        with c1:
            company = st.text_input("Company Name *")
            gst_no = st.text_input("GST / Tax Identification Number")
            contact_person = st.text_input("Contact Person Name *")
        with c2:
            phone = st.text_input("WhatsApp / Mobile Number *")
            email = st.text_input("Official Email Address")
            delivery_location = st.text_input("Plant / Factory Location *")
            
        notes = st.text_area("Specific Requirements (e.g., Size requirement in mm, delivery timeline)")
        
        submit = st.form_submit_button("Submit Formal RFP")
        
        if submit:
            if company and phone and delivery_location:
                st.success("Your RFQ (Request for Quotation) has been registered. Our sales director will contact you via WhatsApp/Email within 2 business hours.")
            else:
                st.error("Please fill in all mandatory fields marked with (*).")

# Footer
st.divider()
st.markdown("💬 **Direct Line:** [Chat with Sales Manager on WhatsApp](https://wa.me/919999999999?text=Hi,%20I%20visited%20your%20app%20and%20need%20a%20coal%20price%20quote)")
