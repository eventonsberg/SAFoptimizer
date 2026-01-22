from ortools.sat.python import cp_model
from optimizer_5 import minimize_production_capacity

def generate_model_inputs(potential_facilities, air_defense, restrictions):
    P_A = float(air_defense.loc[0, "Suksessrate"]) # Probability of successful interception by an air defense missile
    C_A = int(air_defense.loc[0, "Kostnad"]) # Cost of an air defense missile
    A_max = int(air_defense.loc[0, "Maks antall"]) # Maximum number of air defense missiles protecting a facility
    B_R = int(restrictions.loc[0, "Mengde"]) # Missile budget
    B_B = int(restrictions.loc[1, "Mengde"]) # Facility and air defense budget
    F = 0 # Number of potential facilities
    type_f = [] # Type of facility f
    K_f = [] # Production capacity of facility f
    H_f = [] # Number of hits required to destroy facility f
    C_f = [] # Cost of facility f
    for f_type in range(len(potential_facilities)):
        max_units = int(potential_facilities.loc[f_type, "Maks antall"])
        for _ in range(max_units):
            F += 1
            type_f.append(potential_facilities.loc[f_type, "Type"])
            K_f.append(int(potential_facilities.loc[f_type, "Kapasitet"]))
            H_f.append(float(potential_facilities.loc[f_type, "Hardhet"]))
            C_f.append(int(potential_facilities.loc[f_type, "Kostnad"]))
    return P_A, C_A, A_max, B_R, B_B, F, type_f, K_f, H_f, C_f

def maximize_remaining_production_capacity(C_A, A_max, B_B, F, K_f, C_f, scenarios):
    # Model
    model = cp_model.CpModel()

    # Variables
    K_tot_star = model.NewIntVar(0, sum(K_f), 'K_tot_star')  # Total remaining production capacity after worst possible attack
    e_f = [model.NewBoolVar(f'e_{f}') for f in range(F)]  # Boolean variable indicating if facility f is established
    a_f = [model.NewIntVar(0, A_max, f'a_{f}') for f in range(F)]  # Number of air defense missiles protecting facility f

    # Constraints
    if not scenarios:
        scenarios = [[0] * F]  # Default attack scenario where no facilities are destroyed
    for _, d_f_s in enumerate(scenarios):
        model.Add(
            K_tot_star <= sum(K_f[f] * e_f[f] * (1 - d_f_s[f]) for f in range(F))  # Remaining production capacity after attack scenario s
        )

    for f in range(F):
        model.Add(
            a_f[f] <= A_max * e_f[f]  # Air defense missiles can only be assigned to established facilities
        )
    
    model.Add(
        sum(C_f[f] * e_f[f] + C_A * a_f[f] for f in range(F)) <= B_B  # Facility and air defense budget constraint
    )

    # Objective
    model.Maximize(
        K_tot_star  # Maximize remaining production capacity after worst possible attack
    )

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    estblished_f = [bool(solver.Value(e_f[f])) for f in range(F)]
    air_defense_f = [int(solver.Value(a_f[f])) for f in range(F)]
    remaining_production_capacity = int(solver.ObjectiveValue())
    return estblished_f, air_defense_f, remaining_production_capacity, status

def solve_interdiction(P_A, C_A, A_max, B_R, B_B, F, K_f, H_f, C_f, max_iters=100):
    scenarios = [] # List of attack scenarios
    history = [] # Iteration history
    for it in range(max_iters):
        e_f, a_f, K_tot_star, status = maximize_remaining_production_capacity(C_A, A_max, B_B, F, K_f, C_f, scenarios)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"status": "INFEASABLE", "history": history}
        d_f, missile_cost_f, production_capacity = minimize_production_capacity(P_A, B_R, F, K_f, e_f, H_f, a_f)
        if d_f is None:
            return {"status": "SUBPROBLEM_INFEASABLE", "history": history}
        K_tot_gap = K_tot_star - production_capacity
        history.append({
            "iteration": it,
            "established_facilities": e_f,
            "air_defense_assignment": a_f,
            "attack_scenario": d_f,
            "missile_costs": missile_cost_f,
            "remaining_production_capacity_after_attack": production_capacity,
            "previous_remaining_production_capacity": K_tot_star,
            "optimality_gap": K_tot_gap
        })
        if K_tot_gap <= 0:
            return {
                "status": "OPTIMAL",
                "established_facilities": e_f,
                "air_defense_assignment": a_f,
                "attack_scenario": d_f,
                "missile_costs": missile_cost_f,
                "remaining_production_capacity_after_attack": production_capacity,
                "optimality_gap": K_tot_gap,
                "history": history
            }
        scenarios.append(d_f) # Add new attack scenario and repeat
    return {"status": "MAX_ITERS_EXCEEDED", "history": history}