import streamlit as st
import pickle
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="NPA Dashboard", layout="wide")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: white;
}

.metric-box {
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    font-size: 20px;
    text-align: center;
    font-weight: bold;
}

.low { background-color: #1abc9c; }
.medium { background-color: #f39c12; }
.high { background-color: #e74c3c; }

.sidebar .sidebar-content {
    background-color: #111;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load model
# -----------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

FEATURES = ['Loan_Growth', 'Net_Profit', 'Retail_Agri', 'CASA', 'Cost_Income']

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.title("📊 Input Panel")

loan_growth = st.sidebar.slider("Loan Growth (%)", 5.0, 25.0, 14.0)
net_profit = st.sidebar.number_input("Net Profit (Cr)", 100.0, 5000.0, 700.0)
retail_agri = st.sidebar.slider("Retail + Agri (%)", 55.0, 70.0, 63.0)
casa = st.sidebar.slider("CASA Ratio (%)", 20.0, 50.0, 33.0)
cost_income = st.sidebar.slider("Cost to Income (%)", 40.0, 60.0, 48.0)

# -----------------------------
# Header
# -----------------------------
st.title("📊 NPA Risk Dashboard")
st.write("Analyze credit risk using financial indicators")

# -----------------------------
# Metric Cards
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(f"<div class='metric-box'>Loan Growth<br><b>{loan_growth}%</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'>Net Profit<br><b>{net_profit}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'>Retail+Agri<br><b>{retail_agri}%</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box'>CASA<br><b>{casa}%</b></div>", unsafe_allow_html=True)
col5.markdown(f"<div class='metric-box'>Cost/Income<br><b>{cost_income}%</b></div>", unsafe_allow_html=True)

# -----------------------------
# Prediction
# -----------------------------
if st.button("🚀 Analyze Risk"):

    input_df = pd.DataFrame([[
        loan_growth,
        net_profit,
        retail_agri,
        casa,
        cost_income
    ]], columns=FEATURES)

    prediction = model.predict(input_df)[0]

    # Risk classification
    if prediction < 2:
        risk = "Low Risk"
        cls = "low"
    elif prediction < 3:
        risk = "Moderate Risk"
        cls = "medium"
    else:
        risk = "High Risk"
        cls = "high"

    # Result box
    st.markdown(
        f"<div class='result-box {cls}'>Predicted NPA: {prediction:.2f}%<br>{risk}</div>",
        unsafe_allow_html=True
    )