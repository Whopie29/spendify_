# 💸 SPENDIFY – Your Multi-Bank AI Financial Companion

**Spend smarter, save better.**  
SPENDIFY brings all your Indian bank statements together, analyzes them, predicts your balances, and helps you budget with the power of AI.

---

## 🚀 Why SPENDIFY?

Managing multiple bank accounts is messy. SPENDIFY makes it effortless:
- 📥 Upload statements from **HDFC, SBI, Kotak** (more banks coming soon)
- 🤖 Get **AI-powered insights, predictions & budget suggestions**
- 📊 See your money through **beautiful, interactive charts**
- 💬 Chat with an **AI chatbot** to understand your financial health
- 📑 Export **downloadable reports** anytime

---

## 🏦 Supported Banks

✔ **HDFC Bank**  
✔ **State Bank of India (SBI)**  
✔ **Kotak Mahindra Bank**  
*(Easily extendable to more banks)*

---

## 🌟 Core Features

### 🔹 Landing Page
A clean, modern entry point introducing SPENDIFY with quick navigation.

### 🔹 Upload Page
- Upload **password-protected/unprotected PDFs**
- Auto-detects bank type
- Manual bank selection if needed

### 🔹 Analysis Page + AI Chatbot
- Smart **transaction analysis**
- **AI chatbot** answers queries like
  - *"Where did I spend the most last month?"*
  - *"What percentage of my income went to bills?"*
- Auto-categorizes expenses: Food, Bills, Transport, Entertainment, etc.

### 🔹 Interactive Dashboard
- Balance trends over time
- Daily/weekly/monthly summaries
- Income vs. expense ratio
- Overspending alerts

### 🔹 Downloadable Reports
- Export insights to **PDF / Excel**
- Share with advisors or keep for records

### 🔹 Interactive Graphs & Visuals
- Daily deposits vs withdrawals
- Expense category breakdown
- Most frequent transactions
- Predictive balance curve (**LSTM + ARIMA**)
- Budget allocation pie charts

---

## 🔮 Predictive & AI Features

- **Future Balance Prediction**:
  - LSTM (deep learning)
  - ARIMA (time series forecasting)
- **Smart Budget Suggestions**: AI generates personalized budget plans
- **Spending Insights**: Identify unusual spending patterns instantly

---

## 🛠️ Installation

```bash
git clone <repo-url>
cd spendify
pip install -r requirements.txt
cp .env.example .env   # Add your GROQ_API_KEY
```

Run it in two ways:

### Flask (Web Interface)
```bash
python app.py
```
→ Open http://localhost:5000

### Streamlit (Interactive Interface)
```bash
streamlit run web.py
```

---

## 📊 Supported Column Formats

### HDFC Bank
- Date, Narration, Chq. / Ref No., Withdrawal Amount, Deposit Amount, Closing Balance*

### SBI (State Bank of India)
- Value Dt, Transaction Remarks, Cheque Number, Withdrawal Amt., Deposit Amt., Balance

### Kotak Mahindra Bank
- DATE, TRANSACTION DETAILS, CHEQUE/REFERENCE#, DEBIT, CREDIT, BALANCE

---

## 🎯 Use Cases

- Personal finance tracking
- Multi-bank expense comparison
- Budget planning with AI suggestions
- Predicting future account balances
- Categorizing and analyzing spending habits

---

## 🔒 Security

- Local-only processing (no external servers)
- Secure handling of password-protected PDFs
- Session-based privacy controls

---

## 📸 Pages Flow

1️⃣ **Landing Page**  
2️⃣ **Upload Statement**  
3️⃣ **AI Analysis + Chatbot**  
4️⃣ **Dashboard (Interactive)**  
5️⃣ **Download Reports**

---

## 📈 Analysis Features

### Transaction Analysis
- Daily withdrawal vs deposit trends
- Total withdrawal vs deposit comparison
- Closing balance over time
- Transaction amount distribution
- Most frequent transactions
- Top withdrawal amounts

### Transaction Classification
- Food/Clothing
- Entertainment
- Recharge
- Rent/Bills
- Transport
- Emergency
- Banking
- Gaming
- Trading
- Personal Transfer

### Predictive Analytics
- **LSTM Model**: Deep learning-based balance prediction
- **ARIMA Model**: Statistical time series forecasting
- **Model Comparison**: Both models provide different perspectives

### Budget System
- AI-based budget allocation
- Category-wise expense breakdown
- Adaptive budget suggestions
- Overspending alerts
- Income-expense ratio analysis

---

## 🔧 Technical Details

### Bank Detection Algorithm
The system uses multiple strategies to detect the bank:
1. **Keyword Matching**: Looks for bank-specific terms in column headers
2. **Column Pattern Matching**: Matches column names to known bank formats
3. **Fallback**: Defaults to HDFC format if no match is found

### Data Standardization
All bank formats are standardized to a common format:
- Date → Date
- Narration → Narration
- Cheque/Reference → Chq. / Ref No.
- Withdrawal → Withdrawal Amount
- Deposit → Deposit Amount
- Balance → Closing Balance*

---

## 🐛 Troubleshooting

### Common Issues

1. **PDF Not Processing**
   - Ensure the PDF is a bank statement
   - Check if the PDF is corrupted
   - Try with a different PDF reader

2. **Wrong Bank Detected**
   - Manually select your bank from the dropdown
   - Check if your statement format matches the expected format

3. **AI Features Not Working**
   - Ensure GROQ_API_KEY is set in your .env file
   - Check your internet connection

### Adding New Banks

To add support for a new bank:

1. Add bank configuration to `BANK_CONFIGS` in `main.py`
2. Update the `detect_bank()` function
3. Test with sample statements
4. Update documentation

---

## 📝 License

MIT License – free to use, modify, and share.

---

## 🤝 Contributing

Open to PRs! Add support for more banks, improve AI models, or enhance dashboards.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📞 Support

- Open an issue on GitHub
- Check the troubleshooting guide
- Review the [deployment documentation](DEPLOYMENT.md)

---

## 🔥 With SPENDIFY, your money finally makes sense.

**Note**: This application is designed for educational and personal use. Always verify financial calculations and consult with financial advisors for important financial decisions.
