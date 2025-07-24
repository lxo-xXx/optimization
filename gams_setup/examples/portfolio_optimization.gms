$title Portfolio Optimization with Risk Management
$ontext
Mean-variance portfolio optimization with additional constraints
Demonstrates integration with metaheuristic initialization
$offtext

Sets
    i       'assets'        / asset1*asset10 /
    t       'time periods'  / t1*t12 /;

Table returns(i,t) 'historical returns for assets'
           t1     t2     t3     t4     t5     t6     t7     t8     t9    t10    t11    t12
asset1   0.05   0.03  -0.02   0.08   0.04   0.06  -0.01   0.07   0.02   0.05   0.03   0.04
asset2   0.08   0.06   0.02   0.12   0.07   0.09   0.03   0.11   0.05   0.08   0.06   0.07
asset3   0.03   0.02  -0.01   0.05   0.02   0.04  -0.02   0.04   0.01   0.03   0.02   0.02
asset4   0.12   0.10   0.05   0.18   0.11   0.15   0.07   0.16   0.09   0.12   0.10   0.11
asset5   0.06   0.04   0.01   0.09   0.05   0.07   0.02   0.08   0.03   0.06   0.04   0.05
asset6   0.04   0.03  -0.01   0.06   0.03   0.05  -0.01   0.05   0.02   0.04   0.03   0.03
asset7   0.10   0.08   0.04   0.15   0.09   0.12   0.05   0.13   0.07   0.10   0.08   0.09
asset8   0.07   0.05   0.02   0.10   0.06   0.08   0.03   0.09   0.04   0.07   0.05   0.06
asset9   0.02   0.01  -0.02   0.03   0.01   0.02  -0.03   0.02   0.00   0.02   0.01   0.01
asset10  0.09   0.07   0.03   0.13   0.08   0.11   0.04   0.12   0.06   0.09   0.07   0.08;

Parameters
    mu(i)           'expected return for asset i'
    target_return   'target portfolio return' / 0.08 /
    risk_aversion   'risk aversion parameter' / 2.0 /;

* Calculate expected returns
mu(i) = sum(t, returns(i,t)) / card(t);

* Calculate covariance matrix
Parameter sigma(i,i) 'covariance matrix';

Loop((i,i),
    sigma(i,i) = sum(t, power(returns(i,t) - mu(i), 2)) / (card(t) - 1);
);

* For simplicity, assume zero covariance between different assets
* In practice, you would calculate full covariance matrix

Variables
    x(i)            'portfolio weights'
    portfolio_return 'expected portfolio return'
    portfolio_risk  'portfolio variance'
    utility         'utility function (return - risk penalty)';

* Constraints
x.lo(i) = 0;        * No short selling
x.up(i) = 0.4;      * Maximum 40% in any single asset

Equations
    budget_constraint       'weights sum to 1'
    return_calculation     'calculate expected return'
    risk_calculation       'calculate portfolio variance'
    utility_function       'utility maximization'
    min_return_constraint  'minimum return requirement';

budget_constraint..     sum(i, x(i)) =e= 1;
return_calculation..    portfolio_return =e= sum(i, mu(i) * x(i));
risk_calculation..      portfolio_risk =e= sum(i, sigma(i,i) * power(x(i), 2));
utility_function..      utility =e= portfolio_return - risk_aversion * portfolio_risk;
min_return_constraint.. portfolio_return =g= target_return;

* Models
Model mean_variance /budget_constraint, return_calculation, risk_calculation, 
                     utility_function, min_return_constraint/;

Model max_return /budget_constraint, return_calculation, risk_calculation/;

* Solve for maximum utility
Solve mean_variance using nlp maximizing utility;

Display x.l, portfolio_return.l, portfolio_risk.l, utility.l;

* Store optimal solution
Parameter
    optimal_weights(i)      'optimal portfolio weights'
    optimal_return         'optimal portfolio return'
    optimal_risk           'optimal portfolio risk'
    optimal_utility        'optimal utility';

optimal_weights(i) = x.l(i);
optimal_return = portfolio_return.l;
optimal_risk = portfolio_risk.l;
optimal_utility = utility.l;

* Efficient frontier calculation
Set return_levels /r1*r10/;

Parameter
    return_targets(return_levels) 'target return levels'
    / r1  0.03, r2  0.04, r3  0.05, r4  0.06, r5  0.07
      r6  0.08, r7  0.09, r8  0.10, r9  0.11, r10 0.12 /;

Parameter
    efficient_weights(return_levels, i) 'efficient portfolio weights'
    efficient_risk(return_levels)       'efficient portfolio risks'
    efficient_return(return_levels)     'efficient portfolio returns';

Loop(return_levels,
    target_return = return_targets(return_levels);
    Solve mean_variance using nlp minimizing portfolio_risk;
    
    efficient_weights(return_levels, i) = x.l(i);
    efficient_risk(return_levels) = portfolio_risk.l;
    efficient_return(return_levels) = portfolio_return.l;
);

Display efficient_weights, efficient_risk, efficient_return;

* Risk budgeting analysis
Parameter
    risk_contribution(i)    'risk contribution by asset'
    risk_budget(i)         'target risk budget' / #i 0.1 /;

Loop(i,
    risk_contribution(i) = optimal_weights(i) * sigma(i,i) * optimal_weights(i) / optimal_risk;
);

Display risk_contribution, risk_budget;

* Scenario analysis
Set scenarios /bull, bear, normal/;

Parameter
    scenario_returns(scenarios, i) 'returns under different scenarios'
    scenario_prob(scenarios)       'scenario probabilities'
    / bull   0.3
      bear   0.2  
      normal 0.5 /;

* Define scenario returns (multipliers of expected returns)
scenario_returns('bull', i) = 1.5 * mu(i);
scenario_returns('bear', i) = -0.5 * mu(i);
scenario_returns('normal', i) = mu(i);

Parameter
    scenario_portfolio_return(scenarios) 'portfolio return under scenarios'
    expected_scenario_return             'expected return across scenarios'
    scenario_risk                        'risk measured as standard deviation';

Loop(scenarios,
    scenario_portfolio_return(scenarios) = 
        sum(i, optimal_weights(i) * scenario_returns(scenarios, i));
);

expected_scenario_return = sum(scenarios, 
    scenario_prob(scenarios) * scenario_portfolio_return(scenarios));

scenario_risk = sqrt(sum(scenarios, 
    scenario_prob(scenarios) * 
    power(scenario_portfolio_return(scenarios) - expected_scenario_return, 2)));

Display scenario_portfolio_return, expected_scenario_return, scenario_risk;

* Export results for Python integration
File portfolio_results /portfolio_results.txt/;
Put portfolio_results;
Put "# Portfolio Optimization Results"/;
Put "# Asset weights:"/;
Loop(i,
    Put i.tl:0, optimal_weights(i):10:6/;
);
Put "# Performance metrics:"/;
Put "Return: ", optimal_return:8:4/;
Put "Risk: ", optimal_risk:8:4/;
Put "Utility: ", optimal_utility:8:4/;
Put "# Efficient frontier:"/;
Put "# Return, Risk"/;
Loop(return_levels,
    Put efficient_return(return_levels):8:4, efficient_risk(return_levels):8:4/;
);
Putclose portfolio_results;