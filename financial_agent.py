from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
import pandas as pd
import os

class FinancialState(TypedDict):
    question: str
    financial_data: dict
    response: str

def create_financial_agent():
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is required")
    
    llm = ChatGroq(
        temperature=0.3,
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant"
    )
    
    prompt_template = ChatPromptTemplate.from_template("""
You are SPENDIFY's financial assistant. Help users with financial questions and bank statement insights.

User's Financial Data:
- Current Balance: ₹{current_balance:,.2f}
- Total Spent: ₹{total_withdrawals:,.2f} 
- Total Earned: ₹{total_deposits:,.2f}
- Top Spending Categories: {top_categories}
- Total Transactions: {transaction_count}

User Question: {question}

RULES:
1. ONLY answer finance-related questions (budgeting, saving, investing, spending analysis, financial terms)
2. If question is NOT about finance/money/banking, respond: "I'm here to help with financial questions and your spending analysis. Ask me about budgeting, savings, or your transaction patterns!"
3. Keep responses helpful but concise (2-3 sentences max)
4. Use user's actual data when relevant
5. Provide actionable financial advice
6. Use <b>bold</b> for important numbers (not **)
7. Be friendly but professional

For financial questions, provide:
- Direct answer using their data when possible
- One practical tip or suggestion
- Encourage good financial habits
""")
    
    def analyze_finances(state: FinancialState):
        data = state["financial_data"]
        formatted_prompt = prompt_template.format(
            current_balance=data.get("current_balance", 0),
            total_deposits=data.get("total_deposits", 0),
            total_withdrawals=data.get("total_withdrawals", 0),
            transaction_count=data.get("transaction_count", 0),
            top_categories=", ".join(data.get("top_categories", [])),
            question=state["question"]
        )
        
        response = llm.invoke(formatted_prompt)
        return {"question": state["question"], "financial_data": data, "response": response.content}
    
    
    builder = StateGraph(FinancialState)
    builder.add_node("analyze", analyze_finances)
    builder.set_entry_point("analyze")
    builder.set_finish_point("analyze")
    
    return builder.compile()

def is_finance_related(question: str) -> bool:
    # Always return True for now since we want to handle all questions
    # The LLM will handle filtering non-financial topics
    return True

def get_financial_advice(question: str, df: pd.DataFrame):
    try:
       
        # Let the LLM handle all questions now
        # if not is_finance_related(question):
        #     return "I'm here to help with <b>financial questions</b> and your spending analysis. Ask me about budgeting, savings, investments, or your transaction patterns! 💰"
        
        
        financial_data = {
            "current_balance": float(df['Closing Balance'].iloc[-1]),
            "total_deposits": float(df['Deposit Amount'].sum()),
            "total_withdrawals": float(df['Withdrawal Amount'].sum()),
            "transaction_count": len(df),
            "top_categories": df['Category'].value_counts().head(3).index.tolist()
        }
        
        
        agent = create_financial_agent()
        result = agent.invoke({
            "question": question,
            "financial_data": financial_data,
            "response": ""
        })
        
        
        response = result["response"].replace('**', '')
        return response
    except ValueError as e:
        if "GROQ_API_KEY" in str(e):
            return "⚠️ AI features require GROQ_API_KEY environment variable. Please configure it to use financial assistant."
        return "Unable to analyze data. Please try again."
    except Exception as e:
        return "Unable to analyze data. Please try again."