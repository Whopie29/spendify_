# SPENDIFY - Multi-Bank Financial Analyzer

SPENDIFY is a comprehensive financial analysis tool that supports multiple Indian banks for analyzing bank statements, predicting future balances, and generating AI-based budget suggestions.

## 🏦 Supported Banks

The application now supports the following banks:

1. **HDFC Bank** - Default support with original column format
2. **State Bank of India (SBI)** - Supports SBI statement format
3. **Kotak Mahindra Bank** - Supports Kotak statement format

## 🚀 Features

### Multi-Bank Support
- **Auto-Detection**: Automatically detects your bank based on statement format
- **Manual Selection**: Choose your bank manually if auto-detection fails
- **Standardized Processing**: All banks are processed using a unified format

### Core Features
- **PDF Processing**: Upload password-protected or unprotected PDF statements
- **Transaction Analysis**: Comprehensive analysis of spending patterns
- **Visual Analytics**: 11 different charts and visualizations
- **Transaction Classification**: AI-powered categorization of transactions
- **Balance Prediction**: LSTM and ARIMA-based future balance forecasting
- **Budget Suggestions**: AI-generated budget recommendations

## 📊 Supported Column Formats

### HDFC Bank
- Date, Narration, Chq. / Ref No., Withdrawal Amount, Deposit Amount, Closing Balance*

### SBI (State Bank of India)
- Value Dt, Transaction Remarks, Cheque Number, Withdrawal Amt., Deposit Amt., Balance

### Kotak Mahindra Bank
- DATE, TRANSACTION DETAILS, CHEQUE/REFERENCE#, DEBIT, CREDIT, BALANCE



## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spendify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment (for AI features):
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

4. Run the application:

### Flask Version (Web Interface)
```bash
python app.py
```
Then open http://localhost:5000 in your browser.

### Streamlit Version (Interactive Interface)
```bash
streamlit run web.py
```

## 📖 Usage

### Step 1: Select Your Bank
- Choose your bank from the dropdown menu
- Or select "Auto Detect Bank" for automatic detection

### Step 2: Upload Statement
- Upload your bank statement PDF
- Enter password if the PDF is password-protected

### Step 3: Analysis
- The system will automatically process your statement
- View extracted transactions and analysis charts

### Step 4: Predictions
- Generate future balance predictions
- Get AI-based budget suggestions

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

### Error Handling
- Robust error handling for different PDF formats
- Graceful fallback for unsupported banks
- Detailed error messages for troubleshooting

## 🎯 Use Cases

1. **Personal Finance Management**: Track spending patterns across multiple accounts
2. **Budget Planning**: Get AI-powered budget suggestions
3. **Financial Forecasting**: Predict future account balances
4. **Expense Categorization**: Automatically categorize transactions
5. **Multi-Bank Analysis**: Compare spending across different banks

## 🔒 Security

- Password-protected PDF support
- Local processing (no data sent to external servers)
- Session-based data management
- Secure file handling

## 🐛 Troubleshooting

### Common Issues

1. **PDF Not Processing**
   - Ensure the PDF is a bank statement
   - Check if the PDF is corrupted
   - Try with a different PDF reader

2. **Wrong Bank Detected**
   - Manually select your bank from the dropdown
   - Check if your statement format matches the expected format

3. **Columns Not Recognized**
   - Verify that your statement has the expected column headers
   - Contact support if your bank format is not supported

### Adding New Banks

To add support for a new bank:

1. Add bank configuration to `BANK_CONFIGS` in `main.py`
2. Update the `detect_bank()` function
3. Test with sample statements
4. Update documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Note**: This application is designed for educational and personal use. Always verify financial calculations and consult with financial advisors for important financial decisions.
