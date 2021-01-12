import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from descriptions import list_input
import base64



def body():
  return html.Div(children=[
            html.Div(id='left-column', children=[
                dcc.Tabs(
                    id='tabs', value='About this App',
                    children=[
                        dcc.Tab(
                            label='About this App',
                            value='About this App',
                            children=html.Div(children=[
                              html.Br(),
                                html.H4('What is this app?', style={"text-align":"center"}),
                                html.P(
                                    """
                                    This app computes the replication strategy of exchange options (also known as Margrabe options) on a set of given inputs, in the Black-Scholes-Merton (BSM) framework.
                                    """
                                      ),
                                html.P(
                                    """
                                    The goal is to showcase that under the BSM model's assumptions (see "Model" tab), the price \(V_0\) given by the BSM formula is "arbitrage-free". Indeed, we show that in this case, 
                                    it is possible to build a strategy that 
                                    """
                                      ),
                                html.Ul([html.Li("Can be initiated with \(V_0\) cash at time \(0\)."), 
                                         html.Li('Is self-financing (i.e., no need to "feed" the strategy  with extra cash later'),
                                         html.Li("Will deliver exactly the payoff of the option at maturity")
                                        ]),
                                html.Hr(),
                                html.P(
                                    """
                                    Read more about options : 
                                    https://en.wikipedia.org/wiki/Option_(finance)
                                    
                                    """
                                      ),
                                                        ])
                                 ),
                        dcc.Tab(
                          label="Model",
                          value="Model",
                          children=[html.Div(children=[
                            html.Br(),
                            html.H4("Model assumptions", style={"text-align":"center"}),
                            "The BSM main assumptions are:",
                            html.Ul([html.Li("It does not consider dividends and transaction costs"), 
                                 html.Li("The volatility and risk-free rate are assumed constant"),
                                 html.Li("Fraction of shares can be traded")]),
                            html.P([
                              """Under BSM, the underlying asset's dynamics are modeled with a geometric Brownian motion: 
                              $$dS_t = \mu S_tdt+\sigma S_tdW_t$$ Where \(\mu\) is the drift, \(\sigma\) the volatility, and \(dW_t\) the increment of a Brownian motion."""]),
                            html.Hr(),
                            html.H4("Type of options", style={"text-align":"center"}),
                            html.P([
                              """
                              The considered options are exchange options paying \(\psi(S^1_T,S^2_T)=max(0,S^1_T-S^2_T)\) (for exchange calls).
                              """]),
                            html.Hr(),
                            html.H4("Option price", style={"text-align":"center"}),
                            html.P([
                              """
                              The exchange option BSM price was derived by Margrabe in his 1978 paper:
                              $$V_t = S^1_t\Phi(d_1)-S^2_t\Phi(d_2)$$ Where \(\Phi(.)\) is the standard normal cumulative distribution function, 
                              \(d_1\) and \(d_2\) constants $$d_1=\\frac{1}{\hat{\sigma}\sqrt{T-t}}\left[ln(\\frac{S^1_t}{S^2_t})+\\frac{\hat{\sigma^2}}{2}(T-t)\\right]$$$$d_2=d_1-\hat{\sigma}\\sqrt{T-t}$$$$\hat{\sigma^2}=\sigma^2_1+\sigma_2^2-2\\rho\sigma_1\sigma_2$$
                              This pricing formula originate from the BSM partial differential equation, which is valid for any type of European option:
                              $$\\frac{\partial V_t}{\partial t}+\\frac{\sigma^{2}S^{2}_t}{2}\\frac{\partial^{2}V_t}{\partial S^{2}}+rS_t\\frac{\partial V_t}{\partial S} = rV_t$$
                              Where \(V_t=f(t,S_t)\) the price of the option at time t. To get the pricing formulas, solve the PDE with terminal condition the payoff \(\psi(X)\) of the desired European-type option.
                              """]),
                              html.Hr(),
                              html.H4("Academical references", style={"text-align":"center"}),
                              "The main academical references used were:",
                              html.Ul([html.Li("Vrins, F.  (2017-2018). Course notes for Derivatives Pricing. (Financial Engineering Program, Louvain School of Management, Université catholique de Louvain)"), 
                                       html.Li("Margrabe, W. (1978). The Value of an Option to Exchange One Asset for Another. Journal of Finance, 33, 177-186."),]),
                            ])]),
                        # Where \(S_t\) is the price of the underlying asset at time t, \(\sigma\) the standard deviation of the underlying asset, \(r\) the risk-free rate. 
                        #
                        dcc.Tab(
                          label="Approach",
                          value="Methodology",
                          children=[html.Div(children=[
                            html.Br(),
                            html.H4("Methodology followed", style={"text-align":"center"}),
                            html.P([
                              """
                              To prove that the BSM price is arbitrage-free, let us try to perfectly replicate it with a strategy. If the strategy is successfull, then 
                              the BSM price is unique and therefore arbitrage-free.
                              """]),
                            html.Hr(),
                            html.H4("Stock simulation", style={"text-align":"center"}),
                            html.P([
                              """
                              We use the analytical solution to the GBM SDE, using Îto: \(S_t=S_0exp((\mu-\\frac{\sigma^2}{2})t+\sigma W_t)\). Then, suppose that the stock price
                              observations are equally spaced: \(t_i=i\delta, i \in \{1,2,\dots,n\}, n=T/\delta\)\(,\\forall \delta>0\)
                              This corresponds to $$S_{t+\delta}=S_texp((\mu-\\frac{\sigma^2}{2})\delta+\sigma\sqrt{\delta}Z), Z\sim \mathcal{N}(0,1)$$
                              """]),
                            html.Hr(),
                            html.H4("Replicating portfolio", style={"text-align":"center"}),
                            html.Label("Step 1", style={'font-weight': 'bold'}),
                            html.P([
                              """
                              We infer the dynamics of the option price by applying Ito's lemma to the BSM PDE. Complying with Ito \(V_t=f(t,S_t)\):
                              $$dV_t=\\left(f_t(t,S_t)+\\frac{\sigma^2S_t^2}{2}f_{xx}(t,S_t)\\right)dt+f_x(t,S_t)dS_t$$ Where \(f_i(t,S_t)\) are the partial derivatives.
                              """]),
                            html.Label("Step 2", style={'font-weight': 'bold'}),
                            html.P([
                              """
                              The randomness embedded in \(S_t\), i.e. not knowing \(f(t,x)\), is taken care of by hedging \(dS_t\). This is better understood later on. Let us now  
                              create a portfolio \(\Pi\) composed of a cash account and an equity account. At inception, we buy \(\Delta_0\) shares at cost \(\Delta_0S_0\). The reminder \(\Pi_0-\Delta_0S_0\) is cash.
                              If the strategy is financially self-sufficiant, then 
                              $$d\Pi_t=r(\Pi_t-\Delta_tS_t)dt+\Delta_tdS_t$$ 
                              This means that the change in portfolio value results from the interests earned on the cash account and the gains/losses obtained by holding the stock. When we rebalance the portfolio to hold more
                              (resp. less) shares, the cash is taken from (resp. placed on) the cash account. Notice that the cash account can go negative, in which case the interests will have to be paid (not received).                 
                              """]),
                            # In other words, the only variation in the portfolio value is the risk-free received on the cash account and the underlying asset price variation.
                            html.Label("Step 3", style={'font-weight': 'bold'}),
                            html.P([
                              """
                              In other words, the created portfolio \(\Pi\) will perfectly replicate the option price if \(\Delta_t=f_x(t,S_t)\). Indeed, the BSM PDE can be found from equating the two equations with that.
                              """]),
                            html.P([
                              """
                              \(\Delta_t=f_x(t,S_t)\) indicates the number of shares to hold at any instant in order to replicate the BSM price. 
                              Deriving it, it is equal to \(\Delta_t = \nu\Phi(\nu d_1)\) Where \(\nu\) equals 1 for a call and -1 for a put.
                              """]),
                            html.P([
                              """
                              Holding \(\Delta_t = \nu\Phi(\nu d_1(t,S_t))\) at all times, we have found a strategy that perfectly replicates the BSM price, therefore proving it is the unique 
                              price that prevents arbitrage opportunities. 
                              """]),
                            html.P([
                              """ 
                              Indeed, because it is possible to generate the option’s payoff by being given exactly the cash amount \(V_0\) given by the BSM 
                              formula, the option price must agree with \(V_0\). Otherwise, for \(k>0\), if the price of the option is \(V_0+k\), you can sell the option at \(V_0+k\), launch the strategy (which only requires \(V_0\)), and get a 
                              profit of \(k\) today. At maturity, the strategy will deliver exactly the amount that you have to pay to the option’s buyer. If \(k<0\), do the opposite (buy the option, sell the strategy).
                              """]),
                           #  html.P([
                           #    """
                           #    The delta-hedging strategy is visually summarized in this table by Prof. Vrins (LSM, 2020). 
                           #    """]),
                           #  dbc.Button("Show me the table", id="bsm-table-target", color="primary", className="mr-1",),
                           #  dbc.Popover(children=[dbc.PopoverHeader("delta-hedging strategy table"),
                           #        dbc.PopoverBody([html.Img(src="data:image/png;base64,{}".format(base64.b64encode(open("bsm-math.png",'rb').read()).decode())    , style={"width": "250%"})]),
                           #       ],
                           #   id="bsm-table",
                           #   is_open=False,
                           # target="bsm-table-target",),
                            ])]),
                      #
                      #
                        dcc.Tab(
                            label='Inputs',
                            value='Inputs',
                            children=html.Div(children=[
                                      html.Br(),
                                      #
                                      html.P(
                                            """
                                            Place your mouse over any input to get its definition. 
                                            """
                                             ),
                            #
                            html.Div(children=[html.Label('Spot price 1', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="S1", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                               html.P("",id="message_S1", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ]
                                    ),

                            html.Div(children=[html.Label("Spot price 2", title=list_input["Spot price"], style={'font-weight': 'bold',"text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="S2", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                               html.P("",id="message_S2", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ],
                                    ),               
                          #
                          html.Div([html.Label('Stocks correlation', title=list_input["Correlation"], style={'font-weight': 'bold', "display":"inline-block"}),
                                    html.Label(id="correlation", style={"display":"inline-block"}),]),  
                          #
                          dcc.Slider(id='corr', min=-1, max=1, step=0.01, value=0.30, marks={-1:"-1", 0:"0", 1:"1"}),
                          #
                          html.Div(children=[html.Label("Drift stock 1", title=list_input["Drift"], style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="drift1", style={'display': 'inline-block'}),
                                             ]
                                  ),
                          #
                          dcc.Slider(id='mu1', min=-0.40, max=0.40, value=0.10, step=0.01, marks={-0.40: '-40%', 0:"0%", 0.40: '40%'}),
                          #
                          html.Div([html.Label('Volatility stock 1', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
                                    html.Label(id="sigma1", style={"display":"inline-block"}),]),  
                          #
                          dcc.Slider(id='vol1', min=0, max=1, step=0.01, value=0.25, marks={0:"0%", 0.5:"50%", 1:"100%"}),
                          #
                          html.Div(children=[html.Label("Drift stock 2", title=list_input["Drift"], style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="drift2", style={'display': 'inline-block'}),
                                             ]
                                  ),
                          #
                          dcc.Slider(id='mu2', min=-0.40, max=0.40, value=-0.10, step=0.01, marks={-0.40: '-40%', 0:"0%", 0.40: '40%'}),
                          #
                          html.Div([html.Label('Volatility stock 2', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
                                    html.Label(id="sigma2", style={"display":"inline-block"}),]),  
                          #
                          dcc.Slider(id='vol2', min=0, max=1, step=0.01, value=0.10,marks={0:"0%", 0.5:"50%",  1:"100%"}),
                          #
                          html.Div([html.Label('Risk-free rate', title=list_input["Risk-free rate"], style={'font-weight': 'bold', "display":"inline-block"}),
                                      html.Label(id="riskfree", style={"display":"inline-block"}),]),  
                          dcc.Slider(id='Rf', min=0, max=0.1, step=0.01, value=0.03, marks={0:"0%",  0.05:"5%", 0.1:"10%"}),
                          #
                          html.Div([html.Label('Maturity', title=list_input["Maturity"], style={'font-weight':'bold', "display":"inline-block"}),
                                    html.Label(id="matu", style={"display":"inline-block"}),]),                    
                          dcc.Slider(id='T', min=0.25, max=5, # marks={i: '{}'.format(i) for i in range(6)},
                                     marks={0.25:"3 months", 2.5:"2.5 years", 5:"5 years"}, step=0.25, value=3.5),
                          #
                          html.Br(),
                            html.Div([
                                  html.Label('Discretization step (dt)', title=list_input["Discretization step"], style={'font-weight': 'bold', "text-align":"left",'width': '50%', 'display': 'inline-block'}),
                                  dcc.Input(id="dt", value=0.01, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                  html.P("",id="message_dt", style={"font-size":12, "color":"red", 'width': '34%', "text-align":"left", 'display': 'inline-block'})
                                ]),
                            #                     
                            html.Div([
                                  html.Label("Time between two rebalancing (in dt unit)", title=list_input["Rebalancing frequency"], style={'font-weight': 'bold', 'width': '50%', "text-align":"left", 'display': 'inline-block'}),
                                  dcc.Input(id="dt_p", value=1, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                  html.P("",id="message_dt_p", style={"font-size":12, "color":"red", 'width': '34%', "text-align":"left", 'display': 'inline-block'})
                                    ]),
                            #
                          html.Div([html.Label('Transaction costs', title=list_input["Transaction costs"], style={'font-weight': 'bold', "text-align":"left",'width': '50%', 'display': 'inline-block'}),
                                    dcc.Input(id="TransactionCosts", value=0, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                    html.Label(id="unit_TC", style={"padding":5, "display":"inline-block"})
                              ]),
                          #
                          dcc.RadioItems(id="FixedOrPropor",
                                         options=[{'label': 'No TC', 'value': 'NTC'},
                                                  {'label': 'Fixed TC', 'value': 'FTC'},
                                                  {'label': 'Proportional TC', 'value': 'PTC'}
                                                 ],
                                         value='NTC',
                                         labelStyle={'padding':5, 'font-weight': 'bold', 'display': 'inline-block'}
                                        ),  
                          #
                          html.Label(children=[dcc.Checklist(id = "seed",
                                                   options=[{'label': 'New Brownian motion', 'value': "seed"}],
                                                   value=[], 
                                                   labelStyle={'font-weight': 'bold', "text-align":"left", 'display': 'inline-block'}
                                                   )], 
                                     title=list_input["Seed"]),
                          #
                          html.Br(),
                          html.A('Download Data', id='download-link', download="rawdata.csv", href="", target="_blank"),
                          # html.P("""Note: requires excel decimal separator to be a dot.""", style={"font-size":12}),

                          ])),
    ],),], style={'float': 'left', 'width': '25%', 'margin':"30px"}),
  ])



def graphs():
  return html.Div(id='right-column', 
          children=[
            html.Br(),
            html.Div([
                  # html.Div(children=[dcc.Markdown(children=''' #### Portfolio composition'''),
                  #            dcc.Graph(id='port_details'),],
                  #      style={"float":"right", "width":"45%", "display":"inline-block"}),
                  html.Div(children=[dcc.Markdown(children=''' #### Replication strategy '''),
                            dcc.Graph(id='replication'),],
                       style={"float":"right", "width":"100%", "display":"inline-block"}),
                    ]),
            html.Div([
                  # html.Div(children=[dcc.Markdown(children=''' #### Option greeks '''),
                  #            dcc.Graph(id='sde_deriv'),],
                  #      style={"float":"right", "width":"45%", "display":"inline-block"}),
                  html.Div(children=[dcc.Markdown(children=''' #### Held shares'''),
                             dcc.Graph(id='held_shares'),],
                       style={"float":"right", "width":"45%", "display":"inline-block"}),
                  html.Div(children=[dcc.Markdown(children=''' #### Portfolio composition'''),
                             dcc.Graph(id='port_details'),],
                       style={"float":"right", "width":"55%", "display":"inline-block"}),
                    ]),
                   ], 
          style={'float': 'right', 'width': '70%'})
