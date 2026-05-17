import numpy as np
from agent import HospitalAgent, InsuranceAgent
from game_theory import PAYOFF_H, PAYOFF_I, pure_nash, iesds, mixed_nash, backward_induction, TREE
from simulation import simulate
from plot import generate_all_plots
from report import build_report

if __name__ == "__main__":
    np.random.seed(42)

    # ── 1. Game Theory Analysis ───────────────
    print("=" * 50)
    print("   Smart Healthcare — Game Theory Analysis")
    print("=" * 50)

    # Pure Nash
    nash = pure_nash(PAYOFF_H, PAYOFF_I, ["aggressive", "conservative"], ["approve", "deny"])
    print(f"\n[1] Pure Nash Equilibria: {nash}")

    # Mixed Nash
    p_agg, p_app = mixed_nash(PAYOFF_H, PAYOFF_I)
    print(f"\n[2] Mixed Nash Equilibrium:")
    print(f"    Hospital  : P(aggressive)  = {p_agg:.3f}")
    print(f"    Insurance : P(approve)     = {p_app:.3f}")

    # IESDS
    surv_H, surv_I, log = iesds(PAYOFF_H, PAYOFF_I, ["aggressive", "conservative"], ["approve", "deny"])
    print(f"\n[3] IESDS:")
    for line in log:
        print(f"    {line}")
    print(f"    Hospital  survives: {surv_H}")
    print(f"    Insurance survives: {surv_I}")

    # Backward Induction
    result = backward_induction(TREE)
    print(f"\n[4] Extensive Form (Backward Induction):")
    print(f"    Hospital  plays : {result['hospital_plays']}")
    print(f"    Insurance plays : {result['insurance_plays']}")
    print(f"    Payoffs → H: {result['payoff_H']}   I: {result['payoff_I']}")

    # ── 2. Simulation ─────────────────────────
    print(f"\n[5] Running simulation (50 rounds)...")
    H, I, log_data = simulate(rounds=50)

    print(f"\n    Hospital  total reward : {H.total_reward}")
    print(f"    Insurance total reward : {I.total_reward}")
    print(f"    Hospital  final queue  : {H.urgency:.1f} patients")
    print(f"    Hospital  final probs  : {H.strategy_prob}")
    print(f"    Insurance final probs  : {I.strategy_prob}")

    # ── 3. Plots ──────────────────────────────
    print(f"\n[6] Generating plots...")
    PLOT_PATH = r"C:\Users\nesma\Downloads\game\game\results.png"
    generate_all_plots(log_data, PAYOFF_H, save_path=PLOT_PATH)

    # ── 4. Report ─────────────────────────────
    print(f"\n[7] Building PDF report...")
    results_summary = {
        "nash":          nash,
        "p_aggressive":  round(p_agg, 3),
        "p_approve":     round(p_app, 3),
        "surv_H":        surv_H,
        "surv_I":        surv_I,
        "bi_result":     result,
        "H_reward":      H.total_reward,
        "I_reward":      I.total_reward,
        "H_queue":       round(H.urgency, 1),
        "H_final_probs": H.strategy_prob,
        "I_final_probs": I.strategy_prob,
    }
    REPORT_PATH = r"C:\Users\nesma\Downloads\game\game\report.pdf"
    build_report(PLOT_PATH, results_summary, output=REPORT_PATH)

    print("\n✓ Done! Check your folder for results.png and report.pdf")