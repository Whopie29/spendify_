import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Enhanced styling configuration
def setup_enhanced_style():
    """Configure matplotlib and seaborn for better-looking graphs"""
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Global font settings
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
        'axes.titlesize': 16,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11,
        'figure.titlesize': 18,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white'
    })

def format_currency(amount):
    """Format amount as Indian currency"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.1f}Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.1f}L"
    elif amount >= 1000:  # 1 thousand
        return f"₹{amount/1000:.1f}K"
    else:
        return f"₹{amount:.0f}"

def create_enhanced_graphs(analyzer):
    """Create all enhanced graphs for the analyzer"""
    setup_enhanced_style()
    
    df = analyzer.df
    df_summary = df.groupby("Date").agg({
        "Withdrawal Amount": "sum", 
        "Deposit Amount": "sum", 
        "Closing Balance": "last"
    }).reset_index()
    
    # Graph 1: Daily Withdrawals vs Deposits (Enhanced)
    plt.figure(figsize=(12, 6))
    plt.plot(df_summary["Date"], df_summary["Withdrawal Amount"], 
             marker="o", linewidth=3, markersize=6, label="Withdrawals", 
             color="#e74c3c", alpha=0.8)
    plt.plot(df_summary["Date"], df_summary["Deposit Amount"], 
             marker="s", linewidth=3, markersize=6, label="Deposits", 
             color="#27ae60", alpha=0.8)
    
    plt.fill_between(df_summary["Date"], df_summary["Withdrawal Amount"], 
                     alpha=0.2, color="#e74c3c")
    plt.fill_between(df_summary["Date"], df_summary["Deposit Amount"], 
                     alpha=0.2, color="#27ae60")
    
    plt.xlabel("Date", fontweight='bold')
    plt.ylabel("Amount (₹)", fontweight='bold')
    plt.title("Daily Withdrawals and Deposits Trend", fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.xticks(rotation=45, fontsize=8)
    plt.subplots_adjust(bottom=0.35)
    plt.savefig("static/graph1.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Graph 2: Total Withdrawals vs Deposits (Enhanced Pie)
    plt.figure(figsize=(12, 6))
    total_withdrawal = df_summary["Withdrawal Amount"].sum()
    total_deposit = df_summary["Deposit Amount"].sum()
    
    colors = ['#e74c3c', '#27ae60']
    wedges, texts, autotexts = plt.pie(
        [total_withdrawal, total_deposit],
        labels=["Withdrawals", "Deposits"],
        autopct=lambda pct: f'{pct:.1f}%\n{format_currency(pct/100 * (total_withdrawal + total_deposit))}',
        colors=colors,
        startangle=90,
        explode=(0.05, 0.05),
        shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    plt.title("Total Withdrawals vs Deposits", fontweight='bold', pad=20)
    plt.axis('equal')
    plt.savefig("static/graph2.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Graph 3: Closing Balance Over Time (Enhanced)
    plt.figure(figsize=(12, 6))
    plt.plot(df_summary["Date"], df_summary["Closing Balance"], 
             marker="o", linewidth=3, markersize=6, color="#3498db", alpha=0.8)
    plt.fill_between(df_summary["Date"], df_summary["Closing Balance"], 
                     alpha=0.3, color="#3498db")
    
    # Add trend line
    x_numeric = np.arange(len(df_summary))
    z = np.polyfit(x_numeric, df_summary["Closing Balance"], 1)
    p = np.poly1d(z)
    plt.plot(df_summary["Date"], p(x_numeric), "--", 
             color="#2c3e50", alpha=0.8, linewidth=2, label="Trend")
    
    plt.xlabel("Date", fontweight='bold')
    plt.ylabel("Closing Balance (₹)", fontweight='bold')
    plt.title("Account Balance Trend Over Time", fontweight='bold', pad=20)
    plt.legend()
    plt.xticks(rotation=45, fontsize=8)
    plt.subplots_adjust(bottom=0.35)
    plt.savefig("static/graph3.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Graph 4: Transaction Amount Distribution (Enhanced)
    plt.figure(figsize=(12, 6))
    
    # Filter out zero values for better visualization
    withdrawals = df[df["Withdrawal Amount"] > 0]["Withdrawal Amount"]
    deposits = df[df["Deposit Amount"] > 0]["Deposit Amount"]
    
    plt.hist(withdrawals, bins=30, alpha=0.7, color="#e74c3c", 
             label=f"Withdrawals (n={len(withdrawals)})", density=True)
    plt.hist(deposits, bins=30, alpha=0.7, color="#27ae60", 
             label=f"Deposits (n={len(deposits)})", density=True)
    
    plt.xlabel("Transaction Amount (₹)", fontweight='bold')
    plt.ylabel("Density", fontweight='bold')
    plt.title("Distribution of Transaction Amounts", fontweight='bold', pad=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig("static/graph4.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Graph 5: Most Frequent Transactions (Enhanced)
    top_narrations = df["Narration"].value_counts().nlargest(10).sort_values()
    
    plt.figure(figsize=(6, 2))
    colors = sns.color_palette("viridis", len(top_narrations))
    bars = plt.barh(range(len(top_narrations)), top_narrations.values, color=colors)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, top_narrations.values)):
        plt.text(bar.get_width() + max(top_narrations.values) * 0.02, 
                bar.get_y() + bar.get_height()/2, 
                str(value), va='center', fontweight='bold', fontsize=6)
    
    # Truncate long labels and adjust layout
    labels = [label[:30] + '...' if len(label) > 30 else label for label in top_narrations.index]
    plt.yticks(range(len(top_narrations)), labels, fontsize=6)
    plt.xticks(fontsize=6)
    plt.xlabel("Frequency", fontweight='bold', fontsize=6)
    plt.ylabel("Transaction Type", fontweight='bold', fontsize=6)
    plt.title("Most Frequent Transactions (Top 10)", fontweight='bold', pad=10, fontsize=6)
    plt.subplots_adjust(left=0.6, right=0.95, top=0.92, bottom=0.08)
    plt.savefig("static/graph5.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Graph 6: Top Withdrawal Amounts (Enhanced)
    narration_amounts = df.groupby("Narration")["Withdrawal Amount"].sum()
    top_narrations = narration_amounts.nlargest(10).sort_values()
    
    plt.figure(figsize=(6, 2))
    colors = sns.color_palette("plasma", len(top_narrations))
    bars = plt.barh(range(len(top_narrations)), top_narrations.values, color=colors)
    
    # Add formatted currency labels
    for i, (bar, value) in enumerate(zip(bars, top_narrations.values)):
        plt.text(bar.get_width() + max(top_narrations.values) * 0.02, 
                bar.get_y() + bar.get_height()/2, 
                format_currency(value), va='center', fontweight='bold', fontsize=6)
    
    # Truncate long labels and adjust layout
    labels = [label[:30] + '...' if len(label) > 30 else label for label in top_narrations.index]
    plt.yticks(range(len(top_narrations)), labels, fontsize=6)
    plt.xticks(fontsize=6)
    plt.xlabel("Total Withdrawal Amount (₹)", fontweight='bold', fontsize=6)
    plt.ylabel("Transaction Type", fontweight='bold', fontsize=6)
    plt.title("Top 10 Transactions by Total Withdrawal Amount", fontweight='bold', pad=10, fontsize=6)
    plt.subplots_adjust(left=0.6, right=0.95, top=0.92, bottom=0.08)
    plt.savefig("static/graph6.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Graph 7: Daily Deposits and Withdrawals (Enhanced Waterfall)
    plt.figure(figsize=(16, 10))
    
    # Create the bar chart
    bars_deposit = plt.bar(df_summary["Date"], df_summary["Deposit Amount"], 
                          color="#27ae60", label="Deposits", alpha=0.8, width=0.8)
    bars_withdrawal = plt.bar(df_summary["Date"], -df_summary["Withdrawal Amount"], 
                             color="#e74c3c", label="Withdrawals", alpha=0.8, width=0.8)
    
    plt.axhline(0, color="black", linewidth=2, alpha=0.8)
    
    # Enhanced annotations
    for bar in bars_deposit:
        height = bar.get_height()
        if height > df_summary["Deposit Amount"].max() * 0.1:  # Only annotate significant amounts
            plt.text(bar.get_x() + bar.get_width()/2, height + df_summary["Deposit Amount"].max() * 0.02,
                    format_currency(height), ha='center', va='bottom', 
                    fontweight='bold', fontsize=9, color='#27ae60')
    
    for bar in bars_withdrawal:
        height = bar.get_height()
        if abs(height) > df_summary["Withdrawal Amount"].max() * 0.1:
            plt.text(bar.get_x() + bar.get_width()/2, height - df_summary["Withdrawal Amount"].max() * 0.02,
                    format_currency(abs(height)), ha='center', va='top', 
                    fontweight='bold', fontsize=9, color='#e74c3c')
    
    plt.xlabel("Date", fontweight='bold')
    plt.ylabel("Amount (₹)", fontweight='bold')
    plt.title("Daily Cash Flow Analysis", fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.xticks(rotation=45, fontsize=8)
    plt.subplots_adjust(bottom=0.4)
    plt.savefig("static/graph7.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Graph 8: Financial Summary (Enhanced)
    summary = df[["Withdrawal Amount", "Deposit Amount", "Closing Balance"]].describe()
    
    categories = ["Withdrawals", "Deposits", "Closing Balance"]
    averages = [summary.loc['mean', 'Withdrawal Amount'], 
               summary.loc['mean', 'Deposit Amount'], 
               summary.loc['mean', 'Closing Balance']]
    maximums = [summary.loc['max', 'Withdrawal Amount'], 
               summary.loc['max', 'Deposit Amount'], 
               summary.loc['max', 'Closing Balance']]
    minimums = [summary.loc['min', 'Withdrawal Amount'], 
               summary.loc['min', 'Deposit Amount'], 
               summary.loc['min', 'Closing Balance']]
    
    x = np.arange(len(categories))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - width, averages, width, label='Average', 
                   color='#3498db', alpha=0.8)
    bars2 = ax.bar(x, maximums, width, label='Maximum', 
                   color='#27ae60', alpha=0.8)
    bars3 = ax.bar(x + width, minimums, width, label='Minimum', 
                   color='#e74c3c', alpha=0.8)
    
    # Add value labels
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + max(maximums) * 0.01,
                   format_currency(height), ha='center', va='bottom', 
                   fontweight='bold', fontsize=10)
    
    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)
    
    ax.set_xlabel('Categories', fontweight='bold', fontsize=12)
    ax.set_ylabel('Amount (₹)', fontweight='bold', fontsize=12)
    ax.set_title('Financial Summary - Statistical Overview', fontweight='bold', pad=20, fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.legend(frameon=True, shadow=True, fontsize=11)
    
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
    plt.savefig("static/graph8.png", dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()

    # Graph 9: Transaction Category Distribution (Enhanced)
    if 'Category' in df.columns:
        category_counts = df['Category'].value_counts()
        
        plt.figure(figsize=(12, 6))
        colors = sns.color_palette("Set3", len(category_counts))
        
        wedges, texts, autotexts = plt.pie(
            category_counts.values,
            labels=category_counts.index,
            autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
            colors=colors,
            startangle=90,
            explode=[0.05 if i == 0 else 0 for i in range(len(category_counts))],
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        plt.title("Transaction Category Distribution", fontweight='bold', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig("static/graph9.png", dpi=300, bbox_inches='tight')
        plt.close()

def create_budget_graphs(category_expense, dynamic_savings, essential_expense, non_essential_expense):
    """Create enhanced budget-related graphs"""
    setup_enhanced_style()
    
    # Graph 10: Expense Breakdown by Category (Enhanced)
    category_expense_sorted = category_expense.sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("viridis", len(category_expense_sorted))
    bars = plt.bar(range(len(category_expense_sorted)), category_expense_sorted.values, color=colors, alpha=0.8)
    
    # Add value labels
    for bar, value in zip(bars, category_expense_sorted.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(category_expense_sorted.values) * 0.01,
                format_currency(value), ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Truncate long category names
    labels = [label[:18] + '...' if len(label) > 18 else label for label in category_expense_sorted.index]
    plt.xticks(range(len(category_expense_sorted)), labels, rotation=45, ha='right', fontsize=9)
    plt.xlabel("Category", fontweight='bold', fontsize=12)
    plt.ylabel("Amount (₹)", fontweight='bold', fontsize=12)
    plt.title("Expense Breakdown by Category", fontweight='bold', pad=20, fontsize=14)
    plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.45)
    plt.savefig("static/graph10.png", dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    
    # Graph 11: Budget Allocation (Enhanced)
    plt.figure(figsize=(12, 6))
    sizes = [dynamic_savings, essential_expense, non_essential_expense]
    labels = ["Savings", "Essentials", "Non-Essentials"]
    colors = ['#27ae60', '#e74c3c', '#f39c12']
    
    wedges, texts, autotexts = plt.pie(
        sizes, labels=labels,
        autopct=lambda pct: f'{pct:.1f}%\n{format_currency(pct/100 * sum(sizes))}',
        colors=colors, startangle=90,
        explode=(0.1, 0, 0), shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    plt.title("Recommended Budget Allocation", fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("static/graph11.png", dpi=300, bbox_inches='tight')
    plt.close()