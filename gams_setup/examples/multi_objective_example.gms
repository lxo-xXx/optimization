$title Multi-Objective Optimization Example
$ontext
Multi-objective optimization problem with two conflicting objectives
Demonstrates weighted sum approach and epsilon-constraint method
$offtext

Sets
    i       'decision variables'  / x1*x5 /
    obj     'objectives'          / obj1, obj2 /;

Parameters
    w(obj)  'weights for objectives'
            / obj1  0.6
              obj2  0.4 /
              
    eps     'epsilon value for constraint method' / 10 /;

Variables
    x(i)    'decision variables'
    z(obj)  'objective function values'
    z_total 'weighted sum objective';

* Variable bounds
x.lo(i) = 0;
x.up(i) = 10;

Equations
    objective1      'first objective function'
    objective2      'second objective function'
    weighted_sum    'weighted sum of objectives'
    constraint1     'problem constraint 1'
    constraint2     'problem constraint 2'
    epsilon_constr  'epsilon constraint for multi-objective';

* Define objectives (example: minimize cost vs maximize quality)
objective1..    z('obj1') =e= sum(i, power(x(i) - 3, 2));
objective2..    z('obj2') =e= sum(i, x(i)) - 2*sum(i, sqrt(x(i) + 1));

* Weighted sum approach
weighted_sum..  z_total =e= sum(obj, w(obj) * z(obj));

* Problem constraints
constraint1..   sum(i, x(i)) =l= 25;
constraint2..   sum(i, power(x(i), 2)) =l= 100;

* Epsilon constraint (for epsilon-constraint method)
epsilon_constr.. z('obj2') =l= eps;

* Models
Model weighted_model /objective1, objective2, weighted_sum, constraint1, constraint2/;
Model epsilon_model /objective1, objective2, constraint1, constraint2, epsilon_constr/;

* Solve weighted sum approach
Solve weighted_model using nlp minimizing z_total;

Display x.l, z.l, z_total.l;

* Store weighted sum results
Parameter
    x_weighted(i)   'solution from weighted sum'
    z_weighted(obj) 'objectives from weighted sum';

x_weighted(i) = x.l(i);
z_weighted(obj) = z.l(obj);

* Solve epsilon-constraint method for different epsilon values
Set eps_values /eps1*eps5/;

Parameter
    epsilon_table(eps_values) 'epsilon values to test'
    / eps1  5
      eps2  10
      eps3  15
      eps4  20
      eps5  25 /;

Parameter
    pareto_solutions(eps_values, i)   'Pareto optimal solutions'
    pareto_objectives(eps_values, obj) 'Pareto optimal objectives';

Loop(eps_values,
    eps = epsilon_table(eps_values);
    Solve epsilon_model using nlp minimizing z('obj1');
    
    pareto_solutions(eps_values, i) = x.l(i);
    pareto_objectives(eps_values, obj) = z.l(obj);
);

Display pareto_solutions, pareto_objectives;

* Analysis
Parameter
    hypervolume     'approximate hypervolume'
    diversity       'solution diversity measure';

* Simple hypervolume approximation (for demonstration)
hypervolume = sum(eps_values, 
    pareto_objectives(eps_values, 'obj1') * pareto_objectives(eps_values, 'obj2'));

* Diversity measure
diversity = sum(eps_values, 
    sqrt(sum(obj, power(pareto_objectives(eps_values, obj) - 
                       sum(eps_values, pareto_objectives(eps_values, obj))/card(eps_values), 2))));

Display hypervolume, diversity;

* Export results for Python integration
File results_file /multi_obj_results.txt/;
Put results_file;
Put "# Multi-objective optimization results"/;
Put "# Format: solution_id, x1, x2, x3, x4, x5, obj1, obj2"/;
Loop(eps_values,
    Put eps_values.tl:0:0;
    Loop(i, Put pareto_solutions(eps_values, i):8:4);
    Loop(obj, Put pareto_objectives(eps_values, obj):8:4);
    Put /;
);
Putclose results_file;