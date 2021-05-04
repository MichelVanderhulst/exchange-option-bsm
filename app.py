# Dash app libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Importing app header, body and graphs from the other .py scripts
from appHeader import header
from appBody import body, graphs

# Rep strat math
from Exchange_Option_BSM_GBM import *

# Excel export
import pandas as pd
import urllib.parse

# Creating dash object 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], #modern-looking buttons, sliders, etc
	                      external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML', "./assets/mathjax.js"],#LaTeX in app
	                      meta_tags=[{"content": "width=device-width"}] #app width adapts itself to user device
	                      )
server = app.server

# Building the app from imported header, body and graphs
app.layout = html.Div(
                id='main_page',
                children=[
                    dcc.Store(id='memory-output'),
                    header(),
                    body(),
                    graphs(),
                         ],
                     )

# App interactivity: calling the rep strat everytime the user changes an input
@app.callback(
    Output('memory-output', 'data'),
    [Input("S1","value"),
     Input("S2", "value"),
     Input("Rf", "value"),
     Input("T","value"),
     Input("mu1","value"),
     Input("vol1", "value"),
     Input("mu2", "value"),
     Input("vol2","value"),
     Input('corr',"value"),
     Input("dt", "value"),
     Input("dt_p", "value"),
     Input("TransactionCosts", "value"),
     Input("FixedOrPropor", "value"),
     Input("seed", "value")])
def get_rep_strat_data(S1, S2, Rf,T,mu1,vol1,mu2, vol2, corr, dt,dt_p, TransactionCosts, FixedOrPropor, seed):
    StockPrice1, StockPrice2, dt, a, OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, Portfolio, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft = RepStrat_Exchange_Option_BSM_GBM(S1, S2, Rf, T, mu1, mu2, vol1, vol2, corr, dt, dt_p, TransactionCosts, FixedOrPropor, seed)
    return StockPrice1, StockPrice2, dt, list(a), OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, Portfolio, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft

# Plot of stock simulation, intrinsic value, option price and rep portfolio
@app.callback(
    Output('replication', 'figure'),
    [Input('memory-output', 'data'),])
def graph_rep_strat(data):
    StockPrice1, StockPrice2, dt, discre_matu, OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, Portfolio, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft= data

    return{
    'data': [
        go.Scatter(
            x=discre_matu,
            y=StockPrice1,
            mode='lines',
            line={'dash': 'solid', 'color': 'light blue'},
            opacity=0.7,
            name="Stock price 1 simulation (GBM)"),
        go.Scatter(
            x=discre_matu,
            y=StockPrice2,
            mode='lines',
            line={'dash': 'solid', 'color': 'dark blue'},
            opacity=0.7,
            name="Stock price 2 simulation (GBM)"),
        # go.Scatter(
        #   x=discre_matu,
        #   y=OptionIntrinsicValue,
        #   mode="lines",
        #   line={'dash': 'dash', 'color': 'green'},
        #   opacity=0.7,
        #   name="Option intrinsic value"),
        go.Scatter(
            x=discre_matu,
            y=OptionPrice,
            mode="lines",
            line={'dash': 'solid', 'color': 'green'},
            opacity=0.7,
            name="Option price"),
        go.Scatter(
            x=discre_matu,
            y=Portfolio,
            mode="lines",
            line={'dash': 'solid', 'color': 'red'},
            opacity=0.7,
            name="Portfolio"),
        go.Scatter(
            x=[None], 
            y=[None], 
            mode='markers',
            name=f'Payoff - Portfolio: {round(OptionIntrinsicValue[-1]-EquityAccount[-1]-CashAccount[-1],2)}'),
    ],
    'layout': go.Layout(
        title={'yref':"paper",
                'y':1,
                "yanchor":"bottom"},
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Currency"},
        legend=dict(
            x=0,
            y=1,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)'),
    )
}

# Plot of portfolio cash account & equity account
@app.callback(
    Output('port_details', 'figure'),
    [Input('memory-output', 'data'),])
def graph_portf_details(data):
    StockPrice1, StockPrice2, dt, discre_matu, OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, Portfolio, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft= data
    return{
    'data': [
        go.Scatter(
            x=discre_matu,
            y=EquityAccount1,
            mode='lines',
            line={'dash': 'solid', 'color': 'orange'},
            opacity=0.7,
            name="Equity account 1"),
        go.Scatter(
            x=discre_matu,
            y=EquityAccount2,
            mode='lines',
            line={'dash': 'solid', 'color': 'dark orange'},
            opacity=0.7,
            name="Equity account 2"),
        go.Scatter(
            x=discre_matu,
            y=CashAccount,
            mode='lines',
            line={'dash': 'solid', 'color': 'yellow'},
            opacity=0.7,
            name="Cash account",
            ),
        go.Scatter(
            x=discre_matu,
            y=Portfolio,
            mode="lines",
            line={'dash': 'solid', 'color': 'red'},
            opacity=0.7,
            name="Portfolio"),
    ],
    'layout': go.Layout(
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Currency"},
        legend=dict(
            x=0,
            y=1,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)'),
    )
}

# Plot of number of shares to hold
@app.callback(
    Output('held_shares', 'figure'),
    [Input('memory-output', 'data'),])
def graph_held_shares(data):
    StockPrice1, StockPrice2, dt, discre_matu, OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, Portfolio, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft = data
    return{
    'data': [
        go.Scatter(
            x=discre_matu,
            y=Delta1,
            mode='lines',
            line={'dash': 'solid', 'color': 'light blue'},
            opacity=0.7,
            name="Held shares stock 1",
            ),
        go.Scatter(
            x=discre_matu,
            y=Delta2,
            mode='lines',
            line={'dash': 'solid', 'color': 'dark blue'},
            opacity=0.7,
            name="Held shares stock 2",
            ),
    ],
    'layout': go.Layout(
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Shares"},
        legend=dict(
            x=0,
            y=1,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)'),
    )
}


# User input checks
@app.callback(Output('message_S1', 'children'),
              [Input('S1', 'value')])
def check_input_S1(S1):
    if S1<0:
        return f'Cannot be lower than 0.'
    else:
        return ""


@app.callback(Output('message_S2', 'children'),
              [Input('S2', 'value')])
def check_input_S2(S2):
    if S2<0:
        return f'Cannot be lower than 0.'
    else:
        return ""


@app.callback(Output('message_dt', 'children'),
              [Input('T', 'value'),
              Input("dt", "value")])
def check_input_dt(T, dt):
    if dt<0.001:
        return f'Lower than 0.001 will be very slow.'
    elif dt > T:
        return f"Cannot be higher than {T}"
    else:
        return ""   


@app.callback(Output('message_dt_p', 'children'),
              [Input('T', 'value'),
              Input("dt", "value"),
              Input("dt_p","value")])
def check_input_dt_p(T, dt, dt_p):
    if dt_p<=0 or dt_p==None:
        return f'Cannot be lower than 1.'
    elif dt_p > (T/dt):
        return f"Cannot be higher than {T/dt}"
    else:
        return ""   

# Input visuals
@app.callback(Output('correlation', 'children'),
              [Input('corr', 'value')])
def display_value_corr(value):
    return f': {value}'


@app.callback(Output('drift1', 'children'),
              [Input('mu1', 'value')])
def display_value_mu1(value):
    return f': {int(value*100)}%'


@app.callback(Output('sigma1', 'children'),
              [Input('vol1', 'value')])
def display_value_vol(value):
    return f': {int(value*100)}%'

@app.callback(Output('drift2', 'children'),
              [Input('mu2', 'value')])
def display_value_mu1(value):
    return f': {int(value*100)}%'


@app.callback(Output('sigma2', 'children'),
              [Input('vol2', 'value')])
def display_value_vol(value):
    return f': {int(value*100)}%'


@app.callback(Output('riskfree', 'children'),
              [Input('Rf', 'value')])
def display_value_Rf(value):
    return f': {int(value*100)}%'


@app.callback(Output('matu', 'children'),
              [Input('T', 'value')])
def display_value_T(value):
    if value==0.25 or value==0.5 or value==0.75:
        return f": {int(value*12)} months"
    elif value == 1:
        return f': {value} year'
    else:
        return f': {value} years'       

                
@app.callback(Output('TransactionCosts', 'value'),
              [Input('FixedOrPropor', 'value')])
def display_value_TC(value):
    if value=="NTC":
        return 0

@app.callback(Output('unit_TC', 'children'),
              [Input('FixedOrPropor', 'value')])
def display_unit_TC(value):
    if value == "FTC":
        return "$"
    elif value == "PTC":
        return "%"
    else:
        return ""

# Excel export
@app.callback(Output('download-link', 'href'), 
             [Input('memory-output', 'data')])
def update_download_link(data):
    StockPrice1, StockPrice2, dt, discre_matu, OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, Portfolio, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft = data
    cash_bfr, cash_aft, equi1_bfr, equi1_aft, t, equi2_bfr, equi2_aft = np.array(cash_bfr), np.array(cash_aft), np.array(equi1_bfr), np.array(equi1_aft), np.array(t), np.array(equi2_bfr), np.array(equi2_aft)

    df = pd.DataFrame({"Time (in dt)":t,"Stock price 1":StockPrice1, "Stock price 2":StockPrice2, "Option intrinsic value":OptionIntrinsicValue, "Option price":OptionPrice,
                               "Cash before":cash_bfr, "Equity 1 before":equi1_bfr, "Equity 2 before":equi2_bfr, "Portfolio before":cash_bfr+equi1_bfr+equi2_bfr,
                               "Delta 1":Delta1, "Delta 2":Delta2, "Cash after":cash_aft, "Equity 1 after":equi1_aft, "Equity 2 after":equi2_aft, "Portfolio after":cash_aft+equi1_aft+equi2_aft, "Replication strategy error":OptionPrice-cash_aft-equi1_aft-equi2_aft})
    df = df.round(6)
    csv_string = df.to_csv(index=False, encoding="utf-8")
    csv_string = 'data:text/csv;charset=utf-8,' + urllib.parse.quote(csv_string)
    return csv_string


# Opening/Closing "About" Top-right button
@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


# Main function, runs the app
if __name__ == '__main__':
    app.run_server(debug=True)
