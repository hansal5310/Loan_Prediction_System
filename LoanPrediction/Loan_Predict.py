import streamlit as st
import pandas as pd
import joblib
import io
import os

# =====================================================
# PATH CONFIG (IMPORTANT FOR DEPLOYMENT)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "loan_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "Loan_Prediction_model.pkl")

# =====================================================
# LOAD DATA & MODEL
# =====================================================
df = pd.read_csv(DATA_PATH)
Model = joblib.load(MODEL_PATH)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="LoanSphere | Loan Status Predictor",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>🏦 LoanSphere – Loan Approval Predictor</h1>", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("ℹ️ About")
    st.write("Predict loan approval using ML model")

    st.metric("Total Records", len(df))

    df["Loan Status"] = df["Loan Status"].map({
        "Rejected": 0,
        "Approved": 1
    })

    st.metric("Approved Loans", int(df["Loan Status"].sum()))
    st.write(f"Model Type: {type(Model).__name__}")

# =====================================================
# TABS
# =====================================================
tab1, tab2 = st.tabs(["🧪 Manual Prediction", "📦 Bulk Prediction"])

# =====================================================
# MANUAL TAB
# =====================================================
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        loan_amount = st.number_input("Current Loan Amount", min_value=0)
        term = st.selectbox("Term", ["Short", "Long"])
        credit_score = st.number_input("Credit Score", 300, 10000, 600)
        annual_income = st.number_input("Annual Income", min_value=0)

    with col2:
        home_ownership = st.selectbox("Home Ownership",
            ["Have Mortgage", "Rent", "Home Mortgage", "Own"])

        purpose = st.selectbox("Purpose",
            ["Business Loan","Buy a Car","Buy House",
             "Debt Consolidation","Educational Expenses",
             "Home Improvements","Major Purchase",
             "Medical Bills","Moving","Other",
             "Renewable Energy","Small Business",
             "Take a Trip","Vacation","Wedding"])

        monthly_debt = st.number_input("Monthly Debt", min_value=0.0)
        credit_history = st.number_input("Years of Credit History", min_value=0)
        months_delinquent = st.number_input("Months since last delinquent", min_value=0)

    open_accounts = st.number_input("Number of Open Accounts", min_value=0)
    credit_problems = st.number_input("Number of Credit Problems", min_value=0)
    current_balance = st.number_input("Current Credit Balance", min_value=0)
    max_credit = st.number_input("Maximum Open Credit", min_value=0)

    # Encoding maps (same as training)
    term_map = {"Short": 0, "Long": 1}
    home_map = {
        "Have Mortgage": 0,
        "Rent": 1,
        "Home Mortgage": 2,
        "Own": 3
    }

    purpose_map = {
        "Business Loan":1,"Buy a Car":2,"Buy House":3,
        "Debt Consolidation":4,"Educational Expenses":5,
        "Home Improvements":6,"Major Purchase":7,
        "Medical Bills":8,"Moving":9,"Other":10,
        "Renewable Energy":11,"Small Business":12,
        "Take a Trip":13,"Vacation":14,"Wedding":15
    }

    input_df = pd.DataFrame([{
        "Current Loan Amount": loan_amount,
        "Term": term_map[term],
        "Credit Score": credit_score,
        "Annual Income": annual_income,
        "Home Ownership": home_map[home_ownership],
        "Purpose": purpose_map[purpose],
        "Monthly Debt": monthly_debt,
        "Years of Credit History": credit_history,
        "Months since last delinquent": months_delinquent,
        "Number of Open Accounts": open_accounts,
        "Number of Credit Problems": credit_problems,
        "Current Credit Balance": current_balance,
        "Maximum Open Credit": max_credit
    }])

    if st.button("🚀 Predict Loan Status"):
        input_df = input_df[Model.feature_names_in_]
        prediction = Model.predict(input_df)[0]

        if prediction == 1:
            st.success("✅ Loan Approved")
        else:
            st.error("❌ Loan Not Approved")

# =====================================================
# BULK TAB
# =====================================================
with tab2:

    st.subheader("📦 Bulk Loan Prediction")

    # ============================================
    # SAMPLE DATA TEMPLATE
    # ============================================
    sample_df = pd.DataFrame({
        "Current Loan Amount": [25000, 15000],
        "Term": [0, 1],
        "Credit Score": [720, 580],
        "Annual Income": [60000, 35000],
        "Home Ownership": [3, 1],
        "Purpose": [4, 2],
        "Monthly Debt": [1200.5, 800.0],
        "Years of Credit History": [10, 5],
        "Months since last delinquent": [0, 12],
        "Number of Open Accounts": [5, 3],
        "Number of Credit Problems": [0, 1],
        "Current Credit Balance": [15000, 8000],
        "Maximum Open Credit": [30000, 20000]
    })

    col1, col2, col3 = st.columns(3)

    # ============================================
    # COLUMN 1: DOWNLOAD SAMPLE
    # ============================================
    with col1:
        st.markdown("### ⬇️ Download Sample File")

        sample_format = st.selectbox(
            "Select Format",
            ["CSV", "Excel", "JSON", "SQL"]
        )

        if sample_format == "CSV":
            st.download_button(
                "📥 Download CSV",
                sample_df.to_csv(index=False),
                "loan_sample.csv",
                "text/csv"
            )

        elif sample_format == "Excel":
            buffer = io.BytesIO()
            sample_df.to_excel(buffer, index=False)
            st.download_button(
                "📥 Download Excel",
                buffer.getvalue(),
                "loan_sample.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        elif sample_format == "JSON":
            st.download_button(
                "📥 Download JSON",
                sample_df.to_json(orient="records", indent=4),
                "loan_sample.json",
                "application/json"
            )

        elif sample_format == "SQL":
            sql_script = """CREATE TABLE loan_data (
Current Loan Amount INTEGER,
Term INTEGER,
Credit_Score INTEGER,
Annual_Income INTEGER,
Home_Ownership INTEGER,
Purpose INTEGER,
Monthly_Debt REAL,
Years_of_Credit_History INTEGER,
Months_since_last_delinquent INTEGER,
Number_of_Open_Accounts INTEGER,
Number_of_Credit_Problems INTEGER,
Current_Credit_Balance INTEGER,
Maximum_Open_Credit INTEGER
);

INSERT INTO loan_data VALUES
(25000,0,720,60000,3,4,1200.5,10,0,5,0,15000,30000),
(15000,1,580,35000,1,2,800.0,5,12,3,1,8000,20000);
"""
            st.download_button(
                "📥 Download SQL",
                sql_script,
                "loan_sample.sql",
                "application/sql"
            )

    # ============================================
    # COLUMN 2: UPLOAD FILE
    # ============================================
    with col2:
        st.markdown("### 📤 Upload File")

        uploaded_file = st.file_uploader(
            "Upload CSV, Excel, JSON or SQL",
            type=["csv", "xlsx", "json", "sql"]
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    bulk_df = pd.read_csv(uploaded_file)

                elif uploaded_file.name.endswith(".xlsx"):
                    bulk_df = pd.read_excel(uploaded_file)

                elif uploaded_file.name.endswith(".json"):
                    bulk_df = pd.read_json(uploaded_file)

                elif uploaded_file.name.endswith(".sql"):
                    import sqlite3
                    conn = sqlite3.connect(":memory:")
                    sql_script = uploaded_file.read().decode("utf-8")
                    conn.executescript(sql_script)
                    bulk_df = pd.read_sql("SELECT * FROM loan_data", conn)
                    conn.close()

                st.success("File Uploaded Successfully!")
                st.dataframe(bulk_df.head())

                if st.button("🚀 Run Bulk Prediction"):
                    bulk_df_model = bulk_df[Model.feature_names_in_]
                    bulk_df["Prediction"] = Model.predict(bulk_df_model)

                    st.session_state["bulk_result"] = bulk_df
                    st.success("Prediction Completed!")

            except Exception as e:
                st.error(f"Error: {e}")

    # ============================================
    # COLUMN 3: DOWNLOAD RESULTS
    # ============================================
    with col3:
        st.markdown("### 📊 Download Results")

        if "bulk_result" in st.session_state:
            result_df = st.session_state["bulk_result"]

            output_format = st.selectbox(
                "Select Output Format",
                ["CSV", "Excel", "JSON", "SQL"]
            )

            if output_format == "CSV":
                st.download_button(
                    "📥 Download CSV",
                    result_df.to_csv(index=False),
                    "loan_predictions.csv",
                    "text/csv"
                )

            elif output_format == "Excel":
                buffer = io.BytesIO()
                result_df.to_excel(buffer, index=False)
                st.download_button(
                    "📥 Download Excel",
                    buffer.getvalue(),
                    "loan_predictions.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            elif output_format == "JSON":
                st.download_button(
                    "📥 Download JSON",
                    result_df.to_json(orient="records", indent=4),
                    "loan_predictions.json",
                    "application/json"
                )

            elif output_format == "SQL":
                table_name = "loan_predictions"
                sql_script = f"CREATE TABLE {table_name} (\n"

                for col, dtype in result_df.dtypes.items():
                    if "int" in str(dtype):
                        sql_type = "INTEGER"
                    elif "float" in str(dtype):
                        sql_type = "REAL"
                    else:
                        sql_type = "TEXT"

                    sql_script += f"  {col.replace(' ','_')} {sql_type},\n"

                sql_script = sql_script.rstrip(",\n") + "\n);\n\n"

                for _, row in result_df.iterrows():
                    values = []
                    for val in row:
                        if pd.isna(val):
                            values.append("NULL")
                        elif isinstance(val, str):
                            values.append(f"'{val}'")
                        else:
                            values.append(str(val))
                    sql_script += f"INSERT INTO {table_name} VALUES ({', '.join(values)});\n"

                st.download_button(
                    "📥 Download SQL",
                    sql_script,
                    "loan_predictions.sql",
                    "application/sql"
                )
        else:
            st.info("Run prediction to download results")