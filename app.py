from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
from werkzeug.utils import secure_filename
from main import AccountManagementAnalyzer, BANK_CONFIGS
from flask import Flask, request, jsonify
import pickle
import tempfile
import numpy as np

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')  # Required for session management

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'  # Folder for graphs
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/')
def landing():
    return render_template('landing_page.html')

@app.route('/upload')
def index():
    return render_template('index.html', banks=BANK_CONFIGS)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    password = request.form.get('password', '')  # Get password input
    selected_bank = request.form.get('bank', 'HDFC')  # Get selected bank

    if not file or not file.filename:
        return redirect(request.url)

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the file using AccountManagementAnalyzer
        analyzer = AccountManagementAnalyzer()
        
        try:
            unprotected_pdf = analyzer.remove_pdf_password(filepath, password)  # Decrypt PDF
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        if unprotected_pdf:
            csv_file = analyzer.analyze(unprotected_pdf)  # Convert PDF to CSV
            if csv_file:
                # Validate bank selection before processing
                if selected_bank != 'auto':
                    # Load data to validate bank format
                    temp_df = pd.read_csv(csv_file)
                    from main import validate_bank_statement
                    is_valid, error_message = validate_bank_statement(temp_df, selected_bank)
                    if not is_valid:
                        return render_template("error.html", 
                                             error_message=f"Bank Statement Validation Error: {error_message}", 
                                             filename=filename)
                    
                    analyzer.bank_code = selected_bank
                    analyzer.bank_config = BANK_CONFIGS[selected_bank]
                
                try:
                    df = analyzer.show_data()
                    analyzer.preprocessing_and_analysis()
                    analyzer.classification()

                    # Store csv_file and bank info in session for later use in prediction
                    session['csv_file'] = csv_file
                    session['bank_code'] = analyzer.bank_code

                    table_html = df.to_html(classes='table table-striped')

                    return render_template("result.html", filename=filename, table_html=table_html, bank_name=analyzer.bank_config['name'], show_download=True)
                except ValueError as e:
                    # Handle validation errors
                    error_message = str(e)
                    return render_template("error.html", error_message=error_message, filename=filename)
                except Exception as e:
                    # Handle other errors
                    return render_template("error.html", error_message=f"An error occurred: {str(e)}", filename=filename)

    return redirect(url_for('index'))

@app.route('/simple_report')
def simple_report():
    if 'csv_file' not in session:
        return redirect(url_for('index'))
    
    analyzer = AccountManagementAnalyzer()
    analyzer.csv_file = session['csv_file']
    
    if 'bank_code' in session:
        analyzer.bank_code = session['bank_code']
        analyzer.bank_config = BANK_CONFIGS[session['bank_code']]
    
    analyzer.show_data()
    analyzer.preprocessing_and_analysis()
    analyzer.classification()
    
    # Generate report data
    df = analyzer.df
    total_withdrawals = df['Withdrawal Amount'].sum()
    total_deposits = df['Deposit Amount'].sum()
    current_balance = df['Closing Balance'].iloc[-1]
    
    # Category analysis
    category_counts = df['Category'].value_counts().to_dict()
    
    # Create simple HTML report
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
        </div>
        
        <div class="summary">
            <h2>Financial Summary</h2>
            <p><strong>Total Withdrawals:</strong> ₹{total_withdrawals:,.2f}</p>
            <p><strong>Total Deposits:</strong> ₹{total_deposits:,.2f}</p>
            <p><strong>Current Balance:</strong> ₹{current_balance:,.2f}</p>
            <p><strong>Net Flow:</strong> ₹{total_deposits - total_withdrawals:,.2f}</p>
        </div>
        
        <div class="summary">
            <h2>Transaction Categories</h2>
            {''.join([f'<div class="category"><strong>{cat}:</strong> {count} transactions</div>' for cat, count in category_counts.items()])}
        </div>
        
        <h2>Transaction Details</h2>
        {df.to_html(classes='table', table_id='transactions')}
    </body>
    </html>
    """
    
    from flask import make_response
    response = make_response(report_html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=spendify_report.html'
    return response

@app.route('/download_report')
def download_report():
    if 'csv_file' not in session:
        return redirect(url_for('index'))
    
    analyzer = AccountManagementAnalyzer()
    analyzer.csv_file = session['csv_file']
    
    if 'bank_code' in session:
        analyzer.bank_code = session['bank_code']
        analyzer.bank_config = BANK_CONFIGS[session['bank_code']]
    
    analyzer.show_data()
    analyzer.preprocessing_and_analysis()
    analyzer.classification()
    
    # Generate report data
    df = analyzer.df
    total_withdrawals = df['Withdrawal Amount'].sum()
    total_deposits = df['Deposit Amount'].sum()
    current_balance = df['Closing Balance'].iloc[-1]
    
    # Category analysis
    category_counts = df['Category'].value_counts().to_dict()
    
    # Monthly analysis
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_data = df.groupby(df['Date'].dt.to_period('M')).agg({
        'Withdrawal Amount': 'sum',
        'Deposit Amount': 'sum'
    }).reset_index()
    monthly_data['Month'] = monthly_data['Date'].astype(str)
    # Convert to JSON serializable format
    monthly_records = []
    for _, row in monthly_data.iterrows():
        monthly_records.append({
            'Month': row['Month'],
            'Withdrawal Amount': float(row['Withdrawal Amount']),
            'Deposit Amount': float(row['Deposit Amount'])
        })
    
    # Top transactions
    top_withdrawals = df.nlargest(5, 'Withdrawal Amount')[['Date', 'Narration', 'Withdrawal Amount']]
    top_deposits = df.nlargest(5, 'Deposit Amount')[['Date', 'Narration', 'Deposit Amount']]
    
    # Create interactive HTML report
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SPENDIFY - Interactive Financial Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #2c3e50; margin-bottom: 30px; }}
            .summary {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
            .stat-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .controls {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .filter-group {{ display: inline-block; margin-right: 15px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; cursor: pointer; }}
            th:hover {{ background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #e8f4f8; }}
            .chart-container {{ width: 100%; height: 400px; margin: 20px 0; }}
            input, select {{ padding: 8px; border: 1px solid #ddd; border-radius: 4px; margin: 5px; }}
            .btn {{ padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
            .btn:hover {{ background: #764ba2; }}
            .hidden {{ display: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 SPENDIFY Interactive Financial Report</h1>
                <h3>Bank: {analyzer.bank_config['name'] if analyzer.bank_config else 'Unknown'}</h3>
                <p>Generated on: {pd.Timestamp.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>₹{total_withdrawals:,.0f}</h3>
                    <p>Total Withdrawals</p>
                </div>
                <div class="stat-card">
                    <h3>₹{total_deposits:,.0f}</h3>
                    <p>Total Deposits</p>
                </div>
                <div class="stat-card">
                    <h3>₹{current_balance:,.0f}</h3>
                    <p>Current Balance</p>
                </div>
                <div class="stat-card">
                    <h3>₹{total_deposits - total_withdrawals:,.0f}</h3>
                    <p>Net Flow</p>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="categoryChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="monthlyChart"></canvas>
            </div>
            
            <div class="controls">
                <div class="filter-group">
                    <label>Search:</label>
                    <input type="text" id="searchInput" placeholder="Search transactions...">
                </div>
                <div class="filter-group">
                    <label>Category:</label>
                    <select id="categoryFilter">
                        <option value="">All Categories</option>
                        {''.join([f'<option value="{cat}">{cat}</option>' for cat in category_counts.keys()])}
                    </select>
                </div>
                <div class="filter-group">
                    <label>Amount Range:</label>
                    <input type="number" id="minAmount" placeholder="Min">
                    <input type="number" id="maxAmount" placeholder="Max">
                </div>
                <button class="btn" onclick="applyFilters()">Apply Filters</button>
                <button class="btn" onclick="clearFilters()">Clear</button>
            </div>
            
            <h2>📋 Transaction Details</h2>
            <div id="transactionTable">
                {df.to_html(classes='table', table_id='transactions', escape=False)}
            </div>
        </div>
        
        <script>
            // Category Chart
            const categoryData = {dict(category_counts)};
            const ctx1 = document.getElementById('categoryChart').getContext('2d');
            new Chart(ctx1, {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(categoryData),
                    datasets: [{{
                        data: Object.values(categoryData),
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Transaction Categories Distribution'
                        }}
                    }}
                }}
            }});
            
            // Monthly Chart
            const monthlyData = {monthly_records};
            const ctx2 = document.getElementById('monthlyChart').getContext('2d');
            new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: monthlyData.map(d => d.Month),
                    datasets: [{{
                        label: 'Withdrawals',
                        data: monthlyData.map(d => d['Withdrawal Amount']),
                        backgroundColor: '#FF6384'
                    }}, {{
                        label: 'Deposits',
                        data: monthlyData.map(d => d['Deposit Amount']),
                        backgroundColor: '#36A2EB'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Monthly Withdrawals vs Deposits'
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
            
            // Table sorting
            function sortTable(columnIndex) {{
                const table = document.getElementById('transactions');
                const rows = Array.from(table.rows).slice(1);
                const isNumeric = !isNaN(parseFloat(rows[0].cells[columnIndex].textContent));
                
                rows.sort((a, b) => {{
                    const aVal = a.cells[columnIndex].textContent;
                    const bVal = b.cells[columnIndex].textContent;
                    
                    if (isNumeric) {{
                        return parseFloat(aVal) - parseFloat(bVal);
                    }}
                    return aVal.localeCompare(bVal);
                }});
                
                rows.forEach(row => table.appendChild(row));
            }}
            
            // Add click handlers to table headers
            document.querySelectorAll('#transactions th').forEach((th, index) => {{
                th.onclick = () => sortTable(index);
            }});
            
            // Filter functions
            function applyFilters() {{
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                const categoryFilter = document.getElementById('categoryFilter').value;
                const minAmount = parseFloat(document.getElementById('minAmount').value) || 0;
                const maxAmount = parseFloat(document.getElementById('maxAmount').value) || Infinity;
                
                const rows = document.querySelectorAll('#transactions tbody tr');
                
                rows.forEach(row => {{
                    const cells = row.cells;
                    const narration = cells[1].textContent.toLowerCase();
                    const category = cells[cells.length-1].textContent;
                    const withdrawal = parseFloat(cells[3].textContent) || 0;
                    const deposit = parseFloat(cells[4].textContent) || 0;
                    const amount = Math.max(withdrawal, deposit);
                    
                    const matchesSearch = narration.includes(searchTerm);
                    const matchesCategory = !categoryFilter || category === categoryFilter;
                    const matchesAmount = amount >= minAmount && amount <= maxAmount;
                    
                    row.style.display = matchesSearch && matchesCategory && matchesAmount ? '' : 'none';
                }});
            }}
            
            function clearFilters() {{
                document.getElementById('searchInput').value = '';
                document.getElementById('categoryFilter').value = '';
                document.getElementById('minAmount').value = '';
                document.getElementById('maxAmount').value = '';
                
                document.querySelectorAll('#transactions tbody tr').forEach(row => {{
                    row.style.display = '';
                }});
            }}
            
            // Real-time search
            document.getElementById('searchInput').addEventListener('input', applyFilters);
        </script>
    </body>
    </html>
    """
    
    from flask import make_response
    response = make_response(report_html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=spendify_interactive_report.html'
    return response

@app.route('/predict', methods=['POST'])
def predict():
    prediction_days = request.form.get('days', '30')
    try:
        future_days = int(prediction_days)
    except ValueError:
        future_days = 30
    
    if 'csv_file' in session:
        analyzer = AccountManagementAnalyzer()
        analyzer.csv_file = session['csv_file']
        
        # Restore bank configuration from session
        if 'bank_code' in session:
            analyzer.bank_code = session['bank_code']
            analyzer.bank_config = BANK_CONFIGS[session['bank_code']]
        
        analyzer.show_data()
        analyzer.preprocessing_and_analysis()
        analyzer.classification()
        
        current_balance, prediction_df = analyzer.trans_pred(future_days)
        predicted_balance = prediction_df["ARIMA_Prediction"].iloc[-1]
        
        budget_data = analyzer.budget_system()
        
        session['future_days'] = future_days
        
        # Convert prediction_df to dict and ensure all values are JSON serializable
        prediction_data = prediction_df.to_dict(orient='records')
        
        # Convert NumPy types to native Python types in prediction_data
        for record in prediction_data:
            for key, value in record.items():
                if hasattr(value, 'item'):  # Check if it's a NumPy type
                    record[key] = value.item()
                elif isinstance(value, (np.integer, np.floating)):
                    record[key] = value.item()
        
        # Convert NumPy types in budget_data
        if budget_data:
            for key, value in budget_data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if hasattr(sub_value, 'item'):
                            budget_data[key][sub_key] = sub_value.item()
                        elif isinstance(sub_value, (np.integer, np.floating)):
                            budget_data[key][sub_key] = sub_value.item()
                elif hasattr(value, 'item'):
                    budget_data[key] = value.item()
                elif isinstance(value, (np.integer, np.floating)):
                    budget_data[key] = value.item()
        
        return jsonify({
            'success': True, 
            'days': future_days,
            'current_balance': f"₹{float(current_balance):.2f}",
            'predicted_balance': f"₹{float(predicted_balance):.2f}",
            'prediction_data': prediction_data,
            'budget_data': budget_data
        })
    
    return jsonify({'success': False, 'error': 'No data available for prediction'})

@app.route('/analysis')
def analysis():
    if 'csv_file' not in session:
        return redirect(url_for('index'))
    
    analyzer = AccountManagementAnalyzer()
    analyzer.csv_file = session['csv_file']
    
    if 'bank_code' in session:
        analyzer.bank_code = session['bank_code']
        analyzer.bank_config = BANK_CONFIGS[session['bank_code']]
    
    analyzer.show_data()
    analyzer.preprocessing_and_analysis()
    analyzer.classification()
    
    df = analyzer.df
    table_html = df.to_html(classes='table table-striped')
    bank_name = analyzer.bank_config['name'] if analyzer.bank_config else 'Unknown'
    
    return render_template("result.html", filename="Analysis Results", table_html=table_html, bank_name=bank_name, show_download=True)

@app.route('/assistant', methods=['POST'])
def assistant():
    if 'csv_file' not in session:
        return jsonify({'error': 'No data available'})
    
    question = request.json.get('question', '')
    
    try:
        from financial_agent import get_financial_advice
        
        analyzer = AccountManagementAnalyzer()
        analyzer.csv_file = session['csv_file']
        
        if 'bank_code' in session:
            analyzer.bank_code = session['bank_code']
            analyzer.bank_config = BANK_CONFIGS[session['bank_code']]
        
        analyzer.show_data()
        analyzer.preprocessing_and_analysis()
        analyzer.classification()
        
        # Use LangGraph agent for intelligent response
        response = get_financial_advice(question, analyzer.df)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

@app.route('/dashboard')
def dashboard():
    if 'csv_file' not in session:
        return redirect(url_for('index'))
    
    analyzer = AccountManagementAnalyzer()
    analyzer.csv_file = session['csv_file']
    
    if 'bank_code' in session:
        analyzer.bank_code = session['bank_code']
        analyzer.bank_config = BANK_CONFIGS[session['bank_code']]
    
    analyzer.show_data()
    analyzer.preprocessing_and_analysis()
    analyzer.classification()
    
    df = analyzer.df
    
    # Prepare data for dashboard
    dashboard_data = {
        'total_withdrawals': float(df['Withdrawal Amount'].sum()),
        'total_deposits': float(df['Deposit Amount'].sum()),
        'current_balance': float(df['Closing Balance'].iloc[-1]),
        'transaction_count': len(df),
        'categories': df['Category'].value_counts().to_dict(),
        'bank_name': analyzer.bank_config['name'] if analyzer.bank_config else 'Unknown'
    }
    
    # Monthly data
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_data = df.groupby(df['Date'].dt.to_period('M')).agg({
        'Withdrawal Amount': 'sum',
        'Deposit Amount': 'sum'
    }).reset_index()
    monthly_data['Month'] = monthly_data['Date'].astype(str)
    # Convert to dict and ensure JSON serializable
    monthly_records = []
    for _, row in monthly_data.iterrows():
        monthly_records.append({
            'Month': row['Month'],
            'Withdrawal Amount': float(row['Withdrawal Amount']),
            'Deposit Amount': float(row['Deposit Amount'])
        })
    dashboard_data['monthly_data'] = monthly_records
    
    # All transactions - ensure JSON serializable
    all_df = df[['Date', 'Narration', 'Withdrawal Amount', 'Deposit Amount', 'Category']].copy()
    all_transactions = []
    for _, row in all_df.iterrows():
        all_transactions.append({
            'Date': row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else '',
            'Narration': str(row['Narration']),
            'Withdrawal Amount': float(row['Withdrawal Amount']) if pd.notna(row['Withdrawal Amount']) else 0.0,
            'Deposit Amount': float(row['Deposit Amount']) if pd.notna(row['Deposit Amount']) else 0.0,
            'Category': str(row['Category'])
        })
    dashboard_data['all_transactions'] = all_transactions
    
    return render_template('dashboard.html', data=dashboard_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)