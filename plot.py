import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def generate_all_plots(log, payoff_H, save_path=r"C:\Users\nesma\Downloads\game\game\results.png"):
    rounds  = [r["round"]        for r in log]
    pH      = [r["H_payoff"]     for r in log]
    pI      = [r["I_payoff"]     for r in log]
    urgency = [r["urgency"]      for r in log]
    p_agg   = [r["p_aggressive"] for r in log]
    h_strat = [r["H_strategy"]   for r in log]
    i_strat = [r["I_strategy"]   for r in log]

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Game Theory — Smart Healthcare System",
                 fontsize=16, fontweight="bold")

    # ── Plot 1: Payoff Matrix ─────────────────
    im = axes[0,0].imshow(payoff_H, cmap="RdYlGn", vmin=-4, vmax=8)
    for i in range(2):
        for j in range(2):
            axes[0,0].text(j, i, str(payoff_H[i,j]),
                           ha="center", va="center",
                           fontsize=14, fontweight="bold")
    axes[0,0].set_xticks([0,1])
    axes[0,0].set_xticklabels(["Approve", "Deny"])
    axes[0,0].set_yticks([0,1])
    axes[0,0].set_yticklabels(["Aggressive", "Conservative"])
    axes[0,0].set_title("Normal Form — Hospital Payoff Matrix")
    plt.colorbar(im, ax=axes[0,0])

    # ── Plot 2: Payoffs Over Rounds ───────────
    axes[0,1].plot(rounds, pH, label="Hospital",  color="#1976D2", lw=2)
    axes[0,1].plot(rounds, pI, label="Insurance", color="#00796B", lw=2)
    axes[0,1].set_title("Payoffs Over Rounds")
    axes[0,1].set_xlabel("Round")
    axes[0,1].set_ylabel("Payoff")
    axes[0,1].legend()
    axes[0,1].grid(alpha=0.3)

    # ── Plot 3: Strategy Frequency ────────────
    strat_count = defaultdict(int)
    for s in h_strat: strat_count[f"H_{s}"] += 1
    for s in i_strat: strat_count[f"I_{s}"] += 1

    labels = ["H-Aggressive", "H-Conservative", "I-Approve", "I-Deny"]
    values = [
        strat_count["H_aggressive"],
        strat_count["H_conservative"],
        strat_count["I_approve"],
        strat_count["I_deny"],
    ]
    bar_colors = ["#E74C3C", "#2ECC71", "#3498DB", "#E67E22"]
    axes[0,2].bar(labels, values, color=bar_colors, edgecolor="black", alpha=0.8)
    axes[0,2].set_title("Strategy Frequency")
    axes[0,2].set_ylabel("Count")
    axes[0,2].grid(axis="y", alpha=0.3)
    for bar, val in zip(axes[0,2].patches, values):
        axes[0,2].text(bar.get_x() + bar.get_width()/2,
                       bar.get_height() + 0.3,
                       str(val), ha="center", fontsize=10)

    # ── Plot 4: Patient Urgency Over Time ─────
    axes[1,0].fill_between(rounds, urgency, alpha=0.3, color="#E74C3C")
    axes[1,0].plot(rounds, urgency, color="#E74C3C", lw=2)
    axes[1,0].set_title("Patient Urgency Over Time")
    axes[1,0].set_xlabel("Round")
    axes[1,0].set_ylabel("Patients Waiting")
    axes[1,0].grid(alpha=0.3)

    # ── Plot 5: Mixed Strategy Convergence ────
    axes[1,1].plot(rounds, p_agg, color="purple", lw=2)
    axes[1,1].axhline(0.5, color="gray",  linestyle="--", alpha=0.5, label="50-50")
    axes[1,1].axhline(0.3, color="red",   linestyle=":",  lw=2,      label="Nash p=0.30")
    axes[1,1].set_title("Mixed Strategy Convergence")
    axes[1,1].set_xlabel("Round")
    axes[1,1].set_ylabel("P(aggressive)")
    axes[1,1].set_ylim(0, 1)
    axes[1,1].legend()
    axes[1,1].grid(alpha=0.3)

    # ── Plot 6: Extensive Form Tree ───────────
    ax = axes[1,2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Extensive Form Game Tree")

    node_style = dict(boxstyle="round,pad=0.4", facecolor="#AED6F1", edgecolor="black")
    term_style = dict(boxstyle="round,pad=0.4", facecolor="#A9DFBF", edgecolor="black")

    positions = {
        "H_root":    (5,   9),
        "I_agg":     (2.5, 6.5),
        "I_cons":    (7.5, 6.5),
        "T_AA_app":  (1,   4),
        "T_AA_den":  (4,   4),
        "T_AC_app":  (6,   4),
        "T_AC_den":  (9,   4),
    }
    terminal_payoffs = {
        "T_AA_app": "(8,-4)",
        "T_AA_den": "(-2,6)",
        "T_AC_app": "(5, 3)",
        "T_AC_den": "(1, 1)",
    }
    edges = [
        ("H_root", "I_agg",    "Aggressive"),
        ("H_root", "I_cons",   "Conservative"),
        ("I_agg",  "T_AA_app", "Approve"),
        ("I_agg",  "T_AA_den", "Deny"),
        ("I_cons", "T_AC_app", "Approve"),
        ("I_cons", "T_AC_den", "Deny"),
    ]
    for src, dst, lbl in edges:
        sx, sy = positions[src]
        dx, dy = positions[dst]
        ax.annotate("", xy=(dx, dy), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
        ax.text((sx+dx)/2 + 0.2, (sy+dy)/2, lbl, fontsize=7, color="#2C3E50")

    ax.text(*positions["H_root"], "Hospital",  ha="center", va="center",
            fontsize=9, fontweight="bold", bbox=node_style)
    for k in ["I_agg", "I_cons"]:
        ax.text(*positions[k], "Insurance", ha="center", va="center",
                fontsize=9, fontweight="bold", bbox=node_style)
    for k, pf in terminal_payoffs.items():
        ax.text(*positions[k], pf, ha="center", va="center",
                fontsize=9, bbox=term_style)

    # ── Save ──────────────────────────────────
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")  # ← الحفظ الأول
    plt.show()                                              # ← العرض بعد الحفظ
    plt.close()
    print(f"Saved -> {save_path}")