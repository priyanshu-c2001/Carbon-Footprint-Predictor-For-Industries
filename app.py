import streamlit as st
import pandas as pd
import altair as alt

# Define emission factors for different industries (example values, replace with accurate data)
EMISSION_FACTORS = {
    "Walmart": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Supply Chain": 1.5,  # kgCO2/unit
        "Waste": 0.1  # kgCO2/kg
    },
    "Amazon": {
        "Transportation": 0.12,  # kgCO2/km
        "Electricity": 0.75,  # kgCO2/kWh
        "Supply Chain": 1.7,  # kgCO2/unit
        "Waste": 0.08  # kgCO2/kg
    },
    "Tesla": {
        "Transportation": 0.1,  # kgCO2/km
        "Electricity": 0.65,  # kgCO2/kWh
        "Supply Chain": 2.0,  # kgCO2/unit
        "Waste": 0.07  # kgCO2/kg
    }
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Carbon Footprint Data Visualization")

# Streamlit app code
st.title("Carbon Footprint Data Visualization ⚠️")

# User inputs
st.subheader("🌍 Your Industry")
industry = st.selectbox("Select", ["Walmart", "Amazon", "Tesla"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Daily commute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, key="distance_input")

    st.subheader("💡 Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

with col2:
    st.subheader("🗑️ Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

    st.subheader("🔗 Supply chain units handled per year")
    supply_chain = st.number_input("Units", 0, key="supply_chain_input")

# Normalize inputs
if distance > 0:
    distance = distance * 365  # Convert daily distance to yearly
if electricity > 0:
    electricity = electricity * 12  # Convert monthly electricity to yearly
if waste > 0:
    waste = waste * 52  # Convert weekly waste to yearly

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[industry]["Transportation"] * distance
electricity_emissions = EMISSION_FACTORS[industry]["Electricity"] * electricity
supply_chain_emissions = EMISSION_FACTORS[industry]["Supply Chain"] * supply_chain
waste_emissions = EMISSION_FACTORS[industry]["Waste"] * waste

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
supply_chain_emissions = round(supply_chain_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + supply_chain_emissions + waste_emissions, 2
)

# Prediction for 2025 (assumed growth rates)
GROWTH_RATE = 0.05  # 5% increase in emissions for 2025 (adjust as necessary)

predicted_transportation_emissions = round(transportation_emissions * (1 + GROWTH_RATE), 2)
predicted_electricity_emissions = round(electricity_emissions * (1 + GROWTH_RATE), 2)
predicted_supply_chain_emissions = round(supply_chain_emissions * (1 + GROWTH_RATE), 2)
predicted_waste_emissions = round(waste_emissions * (1 + GROWTH_RATE), 2)

predicted_total_emissions = round(
    predicted_transportation_emissions + predicted_electricity_emissions + predicted_supply_chain_emissions + predicted_waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):

    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year (2024)")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year (2024)")
        st.info(f"🔗 Supply Chain: {supply_chain_emissions} tonnes CO2 per year (2024)")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year (2024)")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year (2024)")
        st.warning("Predicted 2025 Emissions:")
        st.info(f"🚗 Transportation: {predicted_transportation_emissions} tonnes CO2")
        st.info(f"💡 Electricity: {predicted_electricity_emissions} tonnes CO2")
        st.info(f"🔗 Supply Chain: {predicted_supply_chain_emissions} tonnes CO2")
        st.info(f"🗑️ Waste: {predicted_waste_emissions} tonnes CO2")
        st.success(f"🌍 Your total predicted carbon footprint for 2025 is: {predicted_total_emissions} tonnes CO2")

        industry_warnings = {
            "Walmart": "In 2024, CO2 emissions per capita for Walmart were estimated to be 2.3 tons. Walmart has been working towards reducing emissions, but its supply chain still contributes significantly to its carbon footprint.",
            "Amazon": "In 2024, Amazon's CO2 emissions per capita were estimated at 3.1 tons, with major contributions from transportation and its global supply chain network.",
            "Tesla": "In 2024, Tesla's CO2 emissions per capita were estimated at 1.2 tons, primarily driven by electricity consumption in production facilities, although the company's focus on renewable energy helps mitigate its overall footprint."
        }
        st.warning(industry_warnings[industry])

    # Create a dataframe for the bar chart
    data = {
        "Category": ["Transportation (2024)", "Electricity (2024)", "Supply Chain (2024)", "Waste (2024)",
                     "Transportation (2025)", "Electricity (2025)", "Supply Chain (2025)", "Waste (2025)"],
        "CO2 Emissions (tonnes)": [
            transportation_emissions,
            electricity_emissions,
            supply_chain_emissions,
            waste_emissions,
            predicted_transportation_emissions,
            predicted_electricity_emissions,
            predicted_supply_chain_emissions,
            predicted_waste_emissions,
        ]
    }

    df = pd.DataFrame(data)

    # Create a bar chart using Altair
    st.subheader("Carbon Emissions Comparison by Category")
    chart = alt.Chart(df).mark_bar().encode(
        x="Category",
        y="CO2 Emissions (tonnes)",
        color="Category"
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
