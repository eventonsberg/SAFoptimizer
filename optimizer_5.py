from ortools.sat.python import cp_model

def generate_model_inputs(potential_facilities, air_defense, restrictions):
    P_A = float(air_defense.loc[0, "Suksessrate"]) # Probability of successful interception by an air defense missile
    B_R = int(restrictions.loc[0, "Mengde"]) # Missile budget
    F = len(potential_facilities) # Number of potential facilities
    K_f = [] # Production capacity of facility f
    e_f = [] # Boolean indicating if facility f is established
    H_f = [] # Number of hits required to destroy facility f
    a_f = [] # Number of air defense missiles assigned to facility f
    for f in range(F):
        K_f.append(int(potential_facilities.loc[f, "Kapasitet"]))
        e_f.append(bool(potential_facilities.loc[f, "Etablert"]))
        H_f.append(float(potential_facilities.loc[f, "Hardhet"]))
        a_f.append(int(potential_facilities.loc[f, "Luftvern"]))
    return P_A, B_R, F, K_f, e_f, H_f, a_f

def scale_int(value, scale=100):
    # Help function to scale float to int for CP-SAT
    return int(round(value * scale))

def minimize_production_capacity(P_A, B_R, F, K_f, e_f, H_f, a_f):
    # Model
    model = cp_model.CpModel()

    # Variables
    d_f = [model.NewBoolVar(f'd_{f}') for f in range(F)] # Boolean indicating if facility f is destroyed

    # Constraints
    for f in range(F):
        model.Add(
            d_f[f] <= e_f[f] # Cannot destroy facilities that are not established
        )
    
    scaled_missile_cost_f = [scale_int(H_f[f] + P_A * a_f[f]) for f in range(F)]
    scaled_missile_budget = scale_int(B_R)
    model.Add(
        sum(scaled_missile_cost_f[f] * d_f[f] for f in range(F)) <= scaled_missile_budget # Missile budget constraint
    )

    # Objective
    model.Minimize(
        sum(K_f[f] * e_f[f] * (1 - d_f[f]) for f in range(F)) # Minimize total production capacity
    )

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None, None
    
    destroyed_f = [bool(solver.Value(d_f[f])) for f in range(F)]
    missile_cost_f = [float((H_f[f] + P_A * a_f[f]) * destroyed_f[f]) for f in range(F)]
    production_capacity = int(solver.ObjectiveValue())
    return destroyed_f, missile_cost_f, production_capacity