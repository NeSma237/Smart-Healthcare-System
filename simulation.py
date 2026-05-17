import numpy as np
from agent import HospitalAgent, InsuranceAgent
from game_theory import PAYOFF_H, PAYOFF_I
def simulate(rounds=50, seed=42):
    np.random.seed(seed)
    hospital  = HospitalAgent("Hospital_A",  initial_urgency=30)
    insurance = InsuranceAgent("Insurance_B", initial_budget=100)
    log = []   # store every round result
    for r in range(rounds):
        # --- Learning: update strategies based on opponent history --
        hospital.update_strategy(PAYOFF_H,  insurance.history)
        insurance.update_strategy(PAYOFF_I, hospital.history)
        # --- Decision: sample from mixed strategy --
        sH = hospital.choose_strategy()   # "aggressive" or "conservative"
        sI = insurance.choose_strategy()  # "approve"    or "deny"
        # --- Payoff lookup --
        i = ["aggressive","conservative"].index(sH)
        j = ["approve","deny"].index(sI)
        pH = PAYOFF_H[i][j]
        pI = PAYOFF_I[i][j]
        # --- Update agent state --
        arrival = np.random.randint(2, 8)   # new patients
        hospital.urgency  = max(0, hospital.urgency - pH + arrival)
        insurance.budget -= pI               # negative = paid out
        hospital.total_reward  += pH
        insurance.total_reward += pI
        hospital.history.append((r, sH, pH))
        insurance.history.append((r, sI, pI))
        log.append({
            "round": r, "H_strategy": sH, "I_strategy": sI,
            "H_payoff": pH, "I_payoff": pI,
            "urgency": hospital.urgency,
            "p_aggressive": hospital.strategy_prob["aggressive"],
        })
    return hospital, insurance, log
# Run:
if __name__ == "__main__":
    hospital, insurance, log = simulate()
    print(f"Final Hospital urgency: {hospital.urgency}")
    print(f"Final Insurance budget: {insurance.budget}")
    H, I, results = simulate(rounds=50)
    print(f"Hospital total reward  : {H.total_reward}")
    print(f"Insurance total reward : {I.total_reward}")
