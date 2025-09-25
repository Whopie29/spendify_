💸 SPENDIFY – Your Multi-Bank AI Financial Companion

Spend smarter, save better.
SPENDIFY brings all your Indian bank statements together, analyzes them, predicts your balances, and helps you budget with the power of AI.

🚀 Why SPENDIFY?

Managing multiple bank accounts is messy. SPENDIFY makes it effortless:

📥 Upload statements from HDFC, SBI, Kotak (more coming soon)

🤖 Get AI-powered insights, predictions & budget suggestions

📊 See your money through beautiful, interactive charts

💬 Chat with an AI chatbot to understand your financial health

📑 Export downloadable reports anytime

🏦 Supported Banks

✔ HDFC Bank
✔ State Bank of India (SBI)
✔ Kotak Mahindra Bank
(Easily extendable to more banks)

🌟 Core Features
🔹 Landing Page

A clean, modern entry point introducing SPENDIFY with quick navigation.

🔹 Upload Page

Upload password-protected/unprotected PDFs

Auto-detects bank type

Manual bank selection if needed

🔹 Analysis Page + AI Chatbot

Smart transaction analysis

AI chatbot answers queries like “Where did I spend most last month?”

Auto-categorizes expenses: Food, Bills, Transport, Entertainment, etc.

🔹 Interactive Dashboard

Balance trends over time

Daily/weekly/monthly summaries

Income vs. expense ratio

Overspending alerts

🔹 Downloadable Reports

Export insights to PDF / Excel

Ready to share with advisors or keep for records

🔹 Interactive Graphs & Visuals

Daily deposits vs withdrawals

Expense category breakdown

Most frequent transactions

Predictive balance curve (LSTM + ARIMA)

Budget allocation pie charts

🔮 Predictive & AI Features

Future Balance Prediction: LSTM (deep learning) + ARIMA (time series)

Smart Budget Suggestions: AI generates personalized budget plans

Spending Insights: Identify unusual spending patterns instantly

🛠️ Installation
git clone <repo-url>
cd spendify
pip install -r requirements.txt
cp .env.example .env   # Add your GROQ_API_KEY


Run it in two ways:

Flask (Web)
python app.py


→ Open http://localhost:5000

Streamlit (Interactive)
streamlit run web.py

🎯 Use Cases

Personal finance tracking

Multi-bank expense comparison

Budget planning with AI suggestions

Predicting future account balances

Categorizing and analyzing spending habits

🔒 Security

Local-only processing (no external servers)

Secure handling of password-protected PDFs

Session-based privacy controls

📸 Sneak Peek (Pages Flow)

1️⃣ Landing Page → 2️⃣ Upload Statement → 3️⃣ AI Analysis + Chatbot → 4️⃣ Dashboard → 5️⃣ Download Reports

📝 License

MIT License – free to use, modify, and share.

🤝 Contributing

Open to PRs! Add support for more banks, improve AI models, or enhance dashboards.

📞 Support

Open an issue on GitHub

Check the troubleshooting guide

🔥 With SPENDIFY, your money finally makes sense.
