import streamlit as st
import os
import pandas as pd
from main import AccountManagementAnalyzer, BANK_CONFIGS

st.set_page_config(page_title="Account Analyzer", layout="wide")

# Session state setup
if "analyzer" not in st.session_state:
    st.session_state.analyzer = AccountManagementAnalyzer()
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "classified" not in st.session_state:
    st.session_state.classified = False
if "predicted" not in st.session_state:
    st.session_state.predicted = False
if "budgeted" not in st.session_state:
    st.session_state.budgeted = False
if "show_data" not in st.session_state:
    st.session_state.show_data = False

analyzer = st.session_state.analyzer

st.title("📊 Account Management Analyzer")

# Step 1: Bank Selection and Upload
st.subheader("🏦 Select Your Bank")
bank_options = {
    'auto': 'Auto Detect Bank',
    'HDFC': 'HDFC Bank',
    'SBI': 'State Bank of India (SBI)',
    'KOTAK': 'Kotak Mahindra Bank',
    'PNB': 'Punjab National Bank (PNB)',

}
selected_bank = st.selectbox("Choose your bank:", list(bank_options.keys()), format_func=lambda x: bank_options[x])

uploaded_file = st.file_uploader("📄 Upload your bank statement PDF", type="pdf")
password = st.text_input("🔒 If your PDF is password protected, enter password (optional)", type="password")

# Step 2: Process file
if uploaded_file:
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ File uploaded!")

    if st.button("🔐 Process PDF"):
        pdf_path = "uploaded.pdf"

        if password:
            pdf_path = analyzer.remove_pdf_password(pdf_path, password)
            if pdf_path is None:
                st.error("❌ Incorrect password or decryption failed.")
                st.stop()
            else:
                st.success("🔓 Password correct. File decrypted!")

        csv_path = analyzer.analyze(pdf_path)
        if csv_path is None or not os.path.exists(csv_path) or os.path.getsize(csv_path) < 10:
            st.error("❌ Failed to extract CSV from PDF.")
            st.stop()

        # Override detected bank if user selected one
        if selected_bank != 'auto':
            analyzer.bank_code = selected_bank
            analyzer.bank_config = BANK_CONFIGS[selected_bank]
            st.info(f"🎯 Using {analyzer.bank_config['name']} format")

        try:
            analyzer.show_data()
            st.session_state.data_loaded = True
            st.success(f"📄 Data successfully extracted for {analyzer.bank_config['name']}.")
        except ValueError as e:
            st.error(f"❌ Bank Statement Validation Error: {str(e)}")
            st.info("💡 Try using 'Auto Detect Bank' or select the correct bank for your statement.")
            st.stop()
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.stop()

# Step 3: Full Analysis
if st.session_state.data_loaded:
    if st.button("🔍 Run Full Analysis"):
        analyzer.preprocessing_and_analysis()
        st.session_state.analysis_done = True
        st.session_state.show_data = True
        st.success("✅ Full analysis completed.")

# Show cleaned data (with narration)
if st.session_state.show_data:
    st.subheader("🧼 Cleaned Transaction Data")
    st.dataframe(analyzer.df, use_container_width=True)

# Show graphs after analysis
if st.session_state.analysis_done:
    st.subheader("📊 Insights from Bank Statement")
    cols = st.columns(2)
    for i in range(1, 7):
        with cols[i % 2]:
            st.image(f"static/graph{i}.png", use_column_width=True)
    for i in range(7, 8):  # Show daily deposit/withdrawals chart separately
        st.image(f"static/graph{i}.png", use_column_width=True)

# Classification
if st.session_state.analysis_done:
    if st.button("🏷️ Classify Transactions"):
        analyzer.classification()
        st.session_state.classified = True
        st.success("✅ Transactions classified and saved.")

if st.session_state.classified:
    st.image("static/graph9.png", caption="Transaction Category Distribution")

# Prediction
if st.session_state.analysis_done:
    st.subheader("🔮 Predict Future Balance")
    days = st.number_input("Enter number of days to forecast", min_value=1, max_value=90, value=30)
    if st.button("📈 Predict"):
        analyzer.trans_pred()
        st.session_state.predicted = True
        st.session_state.forecast_days = days
        st.success("✅ Prediction completed.")

if st.session_state.predicted:
    pred_df = analyzer.prediction_df
    current_balance = analyzer.df["Closing Balance"].iloc[-1]
    predicted_balance = pred_df["ARIMA_Prediction"].iloc[st.session_state.forecast_days - 1]
    
    st.markdown(f"💰 **Current Balance:** ₹{current_balance:.2f}")
    st.markdown(f"📅 **Predicted Balance (in {st.session_state.forecast_days} days):** ₹{predicted_balance:.2f}")
    st.markdown("### 🔢 Forecast Table (ARIMA & LSTM)")
    st.dataframe(pred_df[["Date", "ARIMA_Prediction", "LSTM_Prediction"]].head(st.session_state.forecast_days), use_container_width=True)

# Budgeting
if st.session_state.predicted:
    if st.button("💸 Generate Budget Suggestion"):
        analyzer.budget_system()
        st.session_state.budgeted = True
        st.success("✅ Budget system generated.")

# Download Report Section (available after analysis)
if st.session_state.analysis_done:
    st.subheader("📄 Download Analysis Report")
    if st.button("📄 Generate & Download Report"):
        df = analyzer.df
        total_withdrawals = df['Withdrawal Amount'].sum()
        total_deposits = df['Deposit Amount'].sum()
        current_balance = df['Closing Balance'].iloc[-1]
        
        # Get category data if classified
        category_data = ""
        if st.session_state.classified:
            category_counts = df['Category'].value_counts().to_dict()
            category_data = ''.join([f'<div class="category"><strong>{cat}:</strong> {count} transactions</div>' for cat, count in category_counts.items()])
        
        # Get prediction data if available
        prediction_data = ""
        if st.session_state.predicted:
            pred_df = analyzer.prediction_df
            predicted_balance = pred_df["ARIMA_Prediction"].iloc[st.session_state.forecast_days - 1]
            prediction_data = f"""
            <div class="summary">
                <h2>Balance Prediction</h2>
                <p><strong>Predicted Balance (in {st.session_state.forecast_days} days):</strong> ₹{predicted_balance:,.2f}</p>
            </div>
            """
        
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SPENDIFY - Financial Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; color: #2c3e50; }}
                .summary {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .category {{ margin: 10px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>SPENDIFY Financial Analysis Report</h1>
                <h3>Bank: {analyzer.bank_config['name'] if analyzer.bank_config else 'Unknown'}</h3>
                <p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>Financial Summary</h2>
                <p><strong>Total Withdrawals:</strong> ₹{total_withdrawals:,.2f}</p>
                <p><strong>Total Deposits:</strong> ₹{total_deposits:,.2f}</p>
                <p><strong>Current Balance:</strong> ₹{current_balance:,.2f}</p>
                <p><strong>Net Flow:</strong> ₹{total_deposits - total_withdrawals:,.2f}</p>
            </div>
            
            {prediction_data}
            
            <div class="summary">
                <h2>Transaction Categories</h2>
                {category_data if category_data else '<p>Transaction classification not performed.</p>'}
            </div>
            
            <h2>Transaction Details</h2>
            {df.to_html(classes='table', table_id='transactions')}
        </body>
        </html>
        """
        
        st.download_button(
            label="📄 Download HTML Report",
            data=report_html,
            file_name="spendify_analysis_report.html",
            mime="text/html"
        )
        st.success("✅ Report generated! Click the download button above.")

if st.session_state.budgeted:
    pred_df = analyzer.prediction_df
    predicted_income = pred_df["LSTM_Prediction"].mean()
    predicted_expense = pred_df["ARIMA_Prediction"].mean()
    savings_ratio = 0.1 if predicted_expense > predicted_income * 0.8 else 0.2
    dynamic_savings = predicted_income * savings_ratio
    essential_expense = predicted_expense * 0.7
    non_essential_expense = predicted_expense * 0.3

    st.subheader("📊 AI-Based Budget Suggestion for Next Month")
    st.markdown(f"- **Predicted Income:** ₹{predicted_income:.2f}")
    st.markdown(f"- **Predicted Expenses:** ₹{predicted_expense:.2f}")
    st.markdown(f"- **Recommended Savings ({int(savings_ratio * 100)}%):** ₹{dynamic_savings:.2f}")
    st.markdown(f"- **Essential Expenses (70%):** ₹{essential_expense:.2f}")
    st.markdown(f"- **Non-Essential Expenses (30%):** ₹{non_essential_expense:.2f}")

    st.image("static/graph10.png", caption="Expense Breakdown by Category")
    st.image("static/graph11.png", caption="Budget Allocation")
