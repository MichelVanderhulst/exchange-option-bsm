#####################################################################################
# Exchange Option
# Stocks follow a Geometric Brownian Motion
### SOURCES:
## THE VALUE OF AN OPTION TO EXCHANGE ONE ASSET FOR ANOTHER WILLIAM MARGRABE 1978 
## Lecture notes LLSMS 2226- Derivatives Pricing: Pricing an exchange option 2017-2018 Prof. Frédéric Vrins
#####################################################################################

import numpy as np
from scipy.stats import norm

def d1(S1, S2, T, t, vol):
    return (np.log(S1 / S2) + (T - t) * 0.5 * (vol**2)) / (vol * np.sqrt(T - t))

def d2(dd1, T, t, vol):
    return dd1 - vol*np.sqrt(T-t)

def p_eo(S1, S2, T, t, vol):
    dd1 = d1(S1, S2, T, t, vol)
    dd2 = d2(dd1, T,t,vol)
    return S1*norm.cdf(dd1)-S2*norm.cdf(dd2)

def RepStrat_Exchange_Option_BSM(S1, S2, Rf, T, mu1, mu2, vol1, vol2, corr, dt, RebalancingSteps, TransactionCosts, FixedOrPropor, seed):

	# Problematic input from webapp, returns nothing
    arguments = [S1, S2, Rf, T, mu1, mu2, vol1, vol2, corr, dt, RebalancingSteps, FixedOrPropor] #transaction costs skipped bc assumed 0
    for arg in arguments:
        if arg == None:
            return [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]

    if S1 < 0 or S2 < 0 or dt <= 0 or RebalancingSteps < 1 or RebalancingSteps > T/dt:
        return [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
	
    if TransactionCosts == None:
        TransactionCosts = 0

    ####################################################################################################################
    #####################  START derivative/model strings specifics, user input transformation,    #####################
    #####################        discretization of continuous [0,T] period and rebalancing period  #####################
    #####################        computation

    # transaction costs
    Fixed, Propor = 0, 0
    if FixedOrPropor == "NTC" or FixedOrPropor == []:
        Fixed, Propor = 0, 0

    elif FixedOrPropor == "FTC":
        Fixed, Propor = 1, 0
        TransactionCosts = TransactionCosts

    elif FixedOrPropor == "PTC":
        Fixed, Propor = 0, 1 
        TransactionCosts = TransactionCosts / 100

    # Seed is always fixed. 
    np.random.seed(1)
    # unless user wants new seed everytime
    if seed == ["seed"]:
        np.random.seed(np.random.randint(low=2, high=50000))
    
    # volatility whilst considering correlation
    volcarre = (vol1**2)+(vol2**2) -2*corr*vol1*vol2
    vol=np.sqrt(volcarre)

    # Discretization of maturity period
    ### The matrix length depends on T and dt chosen by user.
    t = np.arange(0, T + dt, dt)
    nt = len(t)
    a = range(nt)

    # Rebalancing period computation
    ### t_rebal is the rebalancing time.
    ### If rebalancing steps = 1, then dt_rebal = dt, and therefore t_rebal = t.
    ### If rebalancing steps > 1, then dt_rebal =/= dt, and therefore t_rebal =/= t.
    ### It will be used for the portfolio rebalancing, given that in the later case, its timeline will be different
    ### than the stock's, i.e. the portfolio will be rebalanced at different moments that the stock is priced.
    dt_rebal = dt * RebalancingSteps
    t_rebal = np.arange(0, T + dt_rebal, dt_rebal)

    #####################    END derivative/model strings specifics, user input transformation,    #####################
    #####################        discretization of continuous [0,T] period and rebalancing period  #####################
    #####################        computation

    ####################################################################################################################
    #####################                  START accounts initialization                           #####################

    StockPrice1, StockPrice2, OptionIntrinsicValue, OptionPrice, W1, W2, Z = np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt)
    EquityAccount, EquityAccount1, EquityAccount2, Delta1, Delta2, CashAccount = np.zeros(nt),np.zeros(nt),np.zeros(nt),np.zeros(nt), np.zeros(nt), np.zeros(nt) 

    dW1 = np.sqrt(dt) * np.random.randn(nt - 1)     # increments brownian motion stock 1
    dZ = np.sqrt(dt) * np.random.randn(nt - 1)      # increments independent brownian motion
    # dW2 = corr * dW1 + np.sqrt(1 - corr ** 2) * dZ  # increments BM correlated to stock 1
        
    # for the excel
    cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft = np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt), np.zeros(nt)
    #####################                      END accounts initialization                         #####################
    ####################################################################################################################



    ####################################################################################################################
    #####################                  START replication strategy                              #####################
    # t = 0.
    StockPrice1[0] = S1
    StockPrice2[0] = S2
    OptionIntrinsicValue[0] = max(0, StockPrice1[0] - StockPrice2[0])
    OptionPrice[0] = p_eo(S1, S2, T, 0, vol)
    W1[0], W2[0], Z[0] = 0, 0, 0 #brownian motions are grounded to 0
    dd1 = d1(S1, S2,T,0,vol)
    Delta1[0] = norm.cdf(dd1)
    Delta2[0] = - norm.cdf(d2(dd1,T,0,vol))
    EquityAccount1[0] = Delta1[0]*StockPrice1[0]
    EquityAccount2[0] = Delta2[0]*StockPrice2[0]
    EquityAccount[0] = EquityAccount1[0] + EquityAccount2[0]
    CashAccount[0] = OptionPrice[0] - EquityAccount[0] - abs(Delta1[0]) * (Fixed*TransactionCosts + StockPrice1[0]*Propor*TransactionCosts) - abs(Delta2[0]) * (Fixed*TransactionCosts+StockPrice2[0]*Propor*TransactionCosts)

    cash_bfr[0], cash_aft[0], equi1_bfr[0], equi1_aft[0], equi2_bfr[0], equi2_aft[0] = OptionPrice[0], CashAccount[0], 0, EquityAccount1[0], 0, EquityAccount2[0]

    # 0 < t <= T
    # Reminder : nt = len(np.arange(0,T+dt,dt))
    #           function range() is [1,nt[. 1 included, last of nt not included.
    #           This loop stops at maturity T.
    for i in range(1, nt):
        # Stock price simulation
        W1[i] = W1[i - 1] + dW1[i - 1]
        Z[i] = Z[i - 1] + dZ[i - 1]
        W2[i] = corr*W1[i] + np.sqrt(1-(corr**2))*Z[i] # constructing correlated BM
        # W2[i] = W2[i - 1] + dW2[i - 1]			 # previous method, also working

        StockPrice1[i] = StockPrice1[0] * np.exp((mu1 - 0.5 * (vol1 **2)) * t[i] + vol1 * W1[i])
        StockPrice2[i] = StockPrice2[0] * np.exp((mu2 - 0.5 * (vol2 **2)) * t[i] + vol2 * W2[i])

        # Option intrinsic value & price
        OptionIntrinsicValue[i] = max(0, StockPrice1[i] - StockPrice2[i])
        OptionPrice[i] = p_eo(StockPrice1[i], StockPrice2[i], T, t[i], vol)

        # Replication strategy
        ### i = rebalancing step
        ### Portfolio is rebalanced every Rebalancing Step, so in order to recognize them we take the modulus of i, the
        ### discretization step, and if it is equal to zero then i is an rebalancing step:
        if i % RebalancingSteps == 0:
        	# Before rebalancing
        	### accrued interest on cash account & updating both equity account to stock prices evolution
            CashAccount[i] = CashAccount[i-1] * (1 + Rf * dt_rebal)

            EquityAccount1[i] = Delta1[i-1] * StockPrice1[i]
            EquityAccount2[i] = Delta2[i-1]*StockPrice2[i]
            EquityAccount[i] = EquityAccount1[i]+EquityAccount2[i]

            cash_bfr[i], equi1_bfr[i], equi2_bfr[i] = CashAccount[i], EquityAccount1[i], EquityAccount2[i]

            # After reblancing
            ### computing delta (# of shares to hold at this time t), ensuring equivalence of portfolio and selling/buying
            ### shares to get delta and updating EquityAccount value with current Delta
            dd1 = d1(StockPrice1[i], StockPrice2[i], T, t_rebal[int(i/RebalancingSteps)], vol)
            Delta1[i] = norm.cdf(dd1)
            Delta2[i] = -norm.cdf(d2(dd1,T,t_rebal[int(i/RebalancingSteps)],vol))
            EquityAccount1[i] = Delta1[i] * StockPrice1[i]
            EquityAccount2[i] = Delta2[i] * StockPrice2[i]
            EquityAccount[i] = EquityAccount1[i] + EquityAccount2[i]
            CashAccount[i] = CashAccount[i] + EquityAccount[i] - Delta1[i]*StockPrice1[i] - Delta2[i]*StockPrice2[i] - abs(Delta1[i]-Delta1[i-1]) * (Fixed*TransactionCosts + StockPrice1[0]*Propor*TransactionCosts) - abs(Delta2[i]-Delta2[i-1]) * (Fixed*TransactionCosts+StockPrice2[0]*Propor*TransactionCosts)

            cash_aft[i], equi1_aft[i], equi2_aft[i] = CashAccount[i], EquityAccount1[i], EquityAccount2[i]

        # i is not a rebalancing step, portfolio is not rebalanced and thus takes its previous value
        else:
            Delta1[i] = Delta1[i - 1]
            Delta2[i] = Delta2[i-1]
            CashAccount[i] = CashAccount[i - 1]
            EquityAccount1[i] = EquityAccount1[i-1]
            EquityAccount2[i] = EquityAccount2[i-1]
            EquityAccount[i] = EquityAccount[i - 1]
            cash_bfr[i], cash_aft[i], equi1_bfr[i], equi1_aft[i], equi2_bfr[i], equi2_aft[i] = cash_bfr[i-1], cash_aft[i-1], equi1_bfr[i-1], equi1_aft[i-1], equi2_bfr[i-1], equi2_aft[i-1]

    #####################                  END replication strategy                                #####################
    ####################################################################################################################
    
    return StockPrice1, StockPrice2, dt, a, OptionIntrinsicValue, OptionPrice, EquityAccount, EquityAccount1, EquityAccount2,CashAccount, EquityAccount+CashAccount, t, Delta1, Delta2, cash_bfr, cash_aft, equi1_bfr, equi1_aft, equi2_bfr, equi2_aft
#                        #   (S1,  S2,  Rf,T, mu1, mu2, vol1, vol2, corr, dt,   RebalancingSteps, TransactionCosts, Fixed, Propor)
# RepStrat_Exchange_Option_BSM(100, 100, 5, 5.2, 5,   5,   10,   5,    0.2,  0.01, 1, 0, 0, 0)