#!/usr/bin/env python
# coding: utf-8

# # Calculator with dropdowns of all banks

# In[2]:


#imports
import dash
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
from dash import Dash
import plotly.graph_objs as go
import os


# In[3]:


#App declaration and function calling
app = Dash("SIP-Financial_Calculator")
app.title = "Financial_Calculators"
# Bank-specific interest rates (example values)
bank_rates = {
    'SBI': {'SIP': 12, 'EMI': 8.5, 'FD': 6.5, 'RD': 7, 'Lumpsum': 10},
    'HDFC': {'SIP': 11.5, 'EMI': 9, 'FD': 6.75, 'RD': 7.25, 'Lumpsum': 10.5},
    'ICICI': {'SIP': 12, 'EMI': 9.2, 'FD': 6.8, 'RD': 7.4, 'Lumpsum': 10.25},
    'LIC': {'SIP': 11, 'EMI': 9.5, 'FD': 6.6, 'RD': 7.1, 'Lumpsum': 10},
    'Kotak': {'SIP': 12, 'EMI': 9.1, 'FD': 6.9, 'RD': 7.35, 'Lumpsum': 10.3},
    'PNB': {'SIP': 11.8, 'EMI': 8.9, 'FD': 6.55, 'RD': 7.2, 'Lumpsum': 10.1},
    'Axis': {'SIP': 11.9, 'EMI': 9.3, 'FD': 6.7, 'RD': 7.3, 'Lumpsum': 10.4},
    'IDBI': {'SIP': 11.6, 'EMI': 9.4, 'FD': 6.6, 'RD': 7.1, 'Lumpsum': 10.15},
    'Nippon': {'SIP': 12.2, 'EMI': 9.6, 'FD': 6.85, 'RD': 7.5, 'Lumpsum': 10.6},
}


# In[5]:


#Calculator Functions Declaration
def calculate_sip(rate, years, monthly_investment):
    r = rate/12/100
    years = int(years)
    n = years*12
    fv = monthly_investment*(((1+r)**n-1)/r)*(1+r)
    gain = fv-(n*monthly_investment)
    return fv, n, gain
def calculate_emi(principal, rate, years):
    r = rate / 12 / 100
    years = int(years)
    n = years * 12
    emi = principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    total_payment = emi * n
    total_interest = total_payment - principal
    return emi, total_payment, total_interest

def calculate_fd(principal, rate, years):
    fv = principal * ((1 + rate / 100) ** years)
    interest = fv - principal
    return fv, interest

def calculate_rd(monthly_investment, rate, years):
    r = rate / 4 / 100
    years = int(years)
    n = years * 4
    fv = monthly_investment * n + monthly_investment * (((1 + r) ** n - 1) / r)
    interest = fv - (monthly_investment * n)
    return fv, interest

def calculate_lumpsum(principal, rate, years):
    fv = principal * ((1 + rate / 100) ** years)
    gain = fv - principal
    return fv, gain

banks = list(bank_rates.keys())
Parameters = ['SIP', 'EMI', 'FD', 'RD', 'Lumpsum']


# In[6]:


#App layout and input-output 
app.layout = html.Div([
    html.H1("📊 Financial Calculators", style={'textAlign': 'center', 'fontSize': '48px', 'marginBottom': '30px'}),

    html.Div([
        html.Label("Select Bank:"),
        dcc.Dropdown(id='bank', options=[{'label': b, 'value': b} for b in banks], value='SBI'),

        html.Br(),
        html.Label("Select Parameter:"),
        dcc.Dropdown(id='calc-type', options=[{'label': c, 'value': c} for c in Parameters], value='SIP')
    ], style={'width': '40%', 'margin': 'auto'}),

    html.Div(id='input-area', style={'marginTop': '30px', 'padding': '20px'}),
    html.Div(id='output-area', style={'marginTop': '20px', 'backgroundColor': '#f0f0f0', 'padding': '10px'}),
])
@app.callback(
    Output('input-area', 'children'),
    [Input('calc-type', 'value'), Input('bank', 'value')]
)
def render_inputs(calc_type, bank):
    default_rate = bank_rates.get(bank,{}).get(calc_type,0)
    if calc_type == 'SIP':
        return html.Div([
            html.Label("Monthly Investment (₹):"),
            dcc.Input(id='input1', type='number', value=5000, min=500, step=500),
            html.Br(), html.Br(),
            html.Label(f"Expected Annual Return (%) [{default_rate}% suggested by {bank}]:"),
            dcc.Input(id='input2', type='number', value=default_rate),
            html.Br(), html.Br(),
            html.Label("Investment Duration (Years):"),
            dcc.Input(id='input3', type='number', value=10, min=1, max=40),
        ])
    elif calc_type == 'EMI':
        return html.Div([
            html.Label("Loan Amount (₹):"),
            dcc.Input(id='input1', type='number', value=100000, min=10000, step=1000),
            html.Br(), html.Br(),
            html.Label(f"Annual Interest Rate (%) [{default_rate}% suggested by {bank}]:"),
            dcc.Input(id='input2', type='number', value=default_rate),
            html.Br(), html.Br(),
            html.Label("Loan Tenure (Years):"),
            dcc.Input(id='input3', type='number', value=5),
        ])
    elif calc_type == 'FD':
        return html.Div([
            html.Label("Principal Amount (₹):"),
            dcc.Input(id='input1', type='number', value=100000),
            html.Br(), html.Br(),
            html.Label(f"Annual Interest Rate (%) [{default_rate}% suggested by {bank}]:"),
            dcc.Input(id='input2', type='number', value=default_rate),
            html.Br(), html.Br(),
            html.Label("Time Period (Years):"),
            dcc.Input(id='input3', type='number', value=5),
        ])
    elif calc_type == 'RD':
        return html.Div([
            html.Label("Monthly Investment (₹):"),
            dcc.Input(id='input1', type='number', value=2000),
            html.Br(), html.Br(),
            html.Label(f"Annual Interest Rate (%) [{default_rate}% suggested by {bank}]:"),
            dcc.Input(id='input2', type='number', value=default_rate),
            html.Br(), html.Br(),
            html.Label("Time Period (Years):"),
            dcc.Input(id='input3', type='number', value=5),
        ])
    elif calc_type == 'Lumpsum':
        return html.Div([
            html.Label("Principal Amount (₹):"),
            dcc.Input(id='input1', type='number', value=100000),
            html.Br(), html.Br(),
            html.Label(f"Expected Annual Return (%) [{default_rate}% suggested by {bank}]:"),
            dcc.Input(id='input2', type='number', value=default_rate),
            html.Br(), html.Br(),
            html.Label("Time Period (Years):"),
            dcc.Input(id='input3', type='number', value=5),
        ])

@app.callback(
    Output('output-area', 'children'),
    [Input('calc-type', 'value'),
     Input('input1', 'value'),
     Input('input2', 'value'),
     Input('input3', 'value')]
)
def update_output(calc_type, input1, input2, input3):
    if None in (input1, input2, input3):
        raise PreventUpdate

    if calc_type == 'SIP':
        fv, n_months, gain = calculate_sip(input2, input3, input1)
        return [
            html.P(f"💰 Total Investment: ₹{input1 * n_months:,.0f}"),
            html.P(f"📈 Estimated Returns: ₹{gain:,.0f}"),
            html.P(f"🧮 Total Value: ₹{fv:,.0f}")
        ]
    elif calc_type == 'EMI':
        emi, total_payment, total_interest = calculate_emi(input1, input2, input3)
        return [
            html.P(f"📆 EMI per month: ₹{emi:,.0f}"),
            html.P(f"💸 Total Payment: ₹{total_payment:,.0f}"),
            html.P(f"📊 Interest Paid: ₹{total_interest:,.0f}")
        ]
    elif calc_type == 'FD':
        fv, interest = calculate_fd(input1, input2, input3)
        return [
            html.P(f"💰 Maturity Amount: ₹{fv:,.0f}"),
            html.P(f"📈 Interest Earned: ₹{interest:,.0f}")
        ]
    elif calc_type == 'RD':
        fv, interest = calculate_rd(input1, input2, input3)
        return [
            html.P(f"💰 Maturity Amount: ₹{fv:,.0f}"),
            html.P(f"📈 Interest Earned: ₹{interest:,.0f}")
        ]
    elif calc_type == 'Lumpsum':
        fv, gain = calculate_lumpsum(input1, input2, input3)
        return [
            html.P(f"💰 Future Value: ₹{fv:,.0f}"),
            html.P(f"📈 Gain: ₹{gain:,.0f}")
        ]



# In[ ]:


# Running the App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))

