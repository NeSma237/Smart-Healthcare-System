import numpy as np
# Rows = Hospital strategy (0=aggressive, 1=conservative)
# Cols = Insurance strategy (0=approve,   1=deny)
PAYOFF_H = np.array([
    [ 8, -2],   # aggressive vs (approve, deny)
    [ 5,  1],   # conservative vs (approve, deny)
])
PAYOFF_I = np.array([
    [-4,  6],   # Hospital aggressive vs (approve, deny)
    [ 3,  1],   # Hospital conservative vs (approve, deny)
])
STRATEGIES_H = ["aggressive", "conservative"]
STRATEGIES_I = ["approve",    "deny"]

def find_dominant_strategy(payoff, strategies_self, strategies_opp):
    """Return dominant strategy if one exists, else None."""
    n_self = len(strategies_self)
    n_opp  = len(strategies_opp)
    for i in range(n_self):
        dominated_by_i = []
        for k in range(n_self):
            if i == k: continue
            if all(payoff[i, j] > payoff[k, j] for j in range(n_opp)):
                dominated_by_i.append(k)
        if len(dominated_by_i) == n_self - 1:  # dominates all others
            return strategies_self[i]
    return None
# Usage:
dom_H = find_dominant_strategy(PAYOFF_H, STRATEGIES_H, STRATEGIES_I)
dom_I = find_dominant_strategy(PAYOFF_I, STRATEGIES_I, STRATEGIES_H)
print("Hospital dominant strategy  :", dom_H)
print("Insurance dominant strategy :", dom_I)


def iesds(payoff_A, payoff_B, strat_A, strat_B):
    rem_A = list(range(len(strat_A)))
    rem_B = list(range(len(strat_B)))
    log   = []
    changed = True
    while changed:
        changed = False
        # Eliminate dominated rows for A
        remove_A = []
        for i in rem_A:
            for k in rem_A:
                if i == k: continue
                if all(payoff_A[k,j] > payoff_A[i,j] for j in rem_B):
                    remove_A.append(i)
                    log.append(f"Hospital: {strat_A[i]} eliminated")
                    changed = True; break
        rem_A = [r for r in rem_A if r not in remove_A]
        # Eliminate dominated cols for B
        remove_B = []
        for j in rem_B:
            for l in rem_B:
                if j == l: continue
                if all(payoff_B[i,l] > payoff_B[i,j] for i in rem_A):
                    remove_B.append(j)
                    log.append(f"Insurance: {strat_B[j]} eliminated")
                    changed = True; break
        rem_B = [r for r in rem_B if r not in remove_B]
    return [strat_A[i] for i in rem_A], [strat_B[j] for j in rem_B], log


def best_response_H(p_approve):
    """Hospital best response given P(Insurance approves) = p_approve."""
    # Expected payoff for each Hospital strategy
    exp_aggressive    = p_approve*PAYOFF_H[0,0] + (1-p_approve)*PAYOFF_H[0,1]
    exp_conservative  = p_approve*PAYOFF_H[1,0] + (1-p_approve)*PAYOFF_H[1,1]
    if exp_aggressive >= exp_conservative:
        return "aggressive",   exp_aggressive
    return "conservative", exp_conservative
# Test it:
br, expected = best_response_H(p_approve=0.6)
print(f"Best response when P(approve)=0.6 : {br}  (E={expected:.2f})")



def pure_nash(payoff_H, payoff_I, strat_H, strat_I):
    """Find all Pure Nash Equilibria."""
    nash = []
    for i in range(len(strat_H)):
        for j in range(len(strat_I)):
            # Is row i best response to col j for Hospital?
            best_H = payoff_H[:,j].max() == payoff_H[i,j]
            # Is col j best response to row i for Insurance?
            best_I = payoff_I[i,:].max() == payoff_I[i,j]
            if best_H and best_I:
                nash.append((strat_H[i], strat_I[j],
                             payoff_H[i,j], payoff_I[i,j]))
    return nash
# Usage:
equilibria = pure_nash(PAYOFF_H, PAYOFF_I, STRATEGIES_H, STRATEGIES_I)
for h_s, i_s, ph, pi in equilibria:
    print(f"Nash: ({h_s}, {i_s})  ->  Hospital:{ph}  Insurance:{pi}")



def mixed_nash(payoff_H, payoff_I):
    """Compute Mixed Nash Equilibrium probabilities."""
    # Insurance indifference condition:
    # p_agg * payoff_H[0,0] + (1-p_agg)*payoff_H[1,0] =
    # p_agg * payoff_H[0,1] + (1-p_agg)*payoff_H[1,1]
    a00, a01 = payoff_H[0]   # aggressive row
    a10, a11 = payoff_H[1]   # conservative row
    denom = (a00 - a01 - a10 + a11)
    p_aggressive = (a11 - a01) / denom if denom != 0 else 0.5
    # Hospital indifference condition (symmetric):
    b00, b01 = payoff_I[0]
    b10, b11 = payoff_I[1]
    denom2 = (b00 - b01 - b10 + b11)
    p_approve = (b11 - b01) / denom2 if denom2 != 0 else 0.5
    p_aggressive = max(0, min(1, p_aggressive))
    p_approve    = max(0, min(1, p_approve))
    return p_aggressive, p_approve
# Usage:
p_agg, p_app = mixed_nash(PAYOFF_H, PAYOFF_I)
print(f"Mixed NE — Hospital: P(aggressive)={p_agg:.3f}")
print(f"Mixed NE — Insurance: P(approve)={p_app:.3f}")



def update_belief(history, target_strategy):
    """",
    Estimate P(opponent plays target_strategy) from history.
    history: list of (round, strategy, payoff) tuples
    """
    if not history:
        return 0.5   # uninformative prior
    recent = history[-10:]   # use last 10 rounds (sliding window)
    count  = sum(1 for _, s, _ in recent if s == target_strategy)
    return count / len(recent)
# Example:
hospital_history = [(0,"aggressive",8),(1,"conservative",5),(2,"aggressive",-2)]
p = update_belief(hospital_history, "aggressive")
print(f"Estimated P(Hospital aggressive) = {p:.2f}")



# The extensive-form game tree as a dictionary
TREE = {
    "root": {"player": "Hospital",   "children": ["H_agg", "H_cons"]},
    "H_agg":  {"player": "Insurance","children": ["AA_app","AA_den"]},
    "H_cons": {"player": "Insurance","children": ["HC_app","HC_den"]},
    # Terminal nodes — (Hospital payoff, Insurance payoff)
    "AA_app": {"player": "terminal", "payoff_H":  8, "payoff_I": -4},
    "AA_den": {"player": "terminal", "payoff_H": -2, "payoff_I":  6},
    "HC_app": {"player": "terminal", "payoff_H":  5, "payoff_I":  3},
    "HC_den": {"player": "terminal", "payoff_H":  1, "payoff_I":  1},
}



def backward_induction(tree):
    # Step 1: Insurance best response to each Hospital move
    # If Hospital plays aggressive:
    if tree["AA_app"]["payoff_I"] >= tree["AA_den"]["payoff_I"]:
        ins_if_agg  = ("approve", tree["AA_app"])
    else:
        ins_if_agg  = ("deny",    tree["AA_den"])
    # If Hospital plays conservative:
    if tree["HC_app"]["payoff_I"] >= tree["HC_den"]["payoff_I"]:
        ins_if_cons = ("approve", tree["HC_app"])
    else:
        ins_if_cons = ("deny",    tree["HC_den"])
    # Step 2: Hospital anticipates Insurance response and picks best
    payoff_H_if_agg  = ins_if_agg[1]["payoff_H"]
    payoff_H_if_cons = ins_if_cons[1]["payoff_H"]
    if payoff_H_if_agg >= payoff_H_if_cons:
        h_choice = "aggressive"
        outcome  = ins_if_agg
    else:
        h_choice = "conservative"
        outcome  = ins_if_cons
    return {
        "hospital_plays":  h_choice,
        "insurance_plays": outcome[0],
        "payoff_H":       outcome[1]["payoff_H"],
        "payoff_I":       outcome[1]["payoff_I"],
    }
# Usage:
result = backward_induction(TREE)
print(f"Subgame Perfect Eq: Hospital={result['hospital_plays']}")
print(f"                    Insurance={result['insurance_plays']}")
print(f"Payoffs: H={result['payoff_H']}  I={result['payoff_I']}")