import numpy as np
STRATEGIES_H = ["aggressive", "conservative"]   # Hospital
STRATEGIES_I = ["approve", "deny"]              # Insurance
class HospitalAgent:
    def __init__(self, agent_id, initial_urgency=20):
        self.agent_id   = agent_id
        self.urgency    = initial_urgency   # patients waiting
        self.strategy_prob = {"aggressive": 0.5, "conservative": 0.5}
        self.history    = []                # (round, strategy, payoff)
        self.total_reward = 0
    # --- Belief (Game Theory Topic 3) --
    def predict_opponent(self, opp_history):
        """Bayesian: estimate P(Insurance plays Approve)."""
        if not opp_history:
            return 0.5
        approvals = sum(1 for _, s, _ in opp_history if s == "approve")
        return approvals / len(opp_history)
    # --- Best Response (Game Theory Topic 6) --
    def best_response(self, p_approve, payoff_matrix):
        """Given P(approve), find my best strategy."""
        exp = {}
        for i, s in enumerate(STRATEGIES_H):
            exp[s] = (p_approve        * payoff_matrix[i][0] +   # approve col
                      (1-p_approve)    * payoff_matrix[i][1])    # deny col
        return max(exp, key=exp.get)
    # --- Mixed Strategy Decision (Topic 4) --
    def choose_strategy(self):
        strategies = list(self.strategy_prob.keys())
        probs      = list(self.strategy_prob.values())
        return np.random.choice(strategies, p=probs)
    # --- Learning / Adaptation --
    def update_strategy(self, payoff_matrix, opp_history, lr=0.1):
        p = self.predict_opponent(opp_history)
        br = self.best_response(p, payoff_matrix)
        for s in self.strategy_prob:
            if s == br:
               self.strategy_prob[s] += lr * (1 - self.strategy_prob[s])
            else:
               self.strategy_prob[s] -= lr * self.strategy_prob[s]
        total = sum(self.strategy_prob.values())
        self.strategy_prob = {k: v/total
                              for k, v in self.strategy_prob.items()}

class InsuranceAgent:
    def __init__(self, agent_id, initial_budget=100):
        self.agent_id   = agent_id
        self.budget     = initial_budget    # money available
        self.strategy_prob = {"approve": 0.5, "deny": 0.5}
        self.history    = []                # (round, strategy, payoff)
        self.total_reward = 0
    def predict_opponent(self, opp_history):
        if not opp_history:
            return 0.5
        aggressive = sum(1 for _, s, _ in opp_history if s == "aggressive")
        return aggressive / len(opp_history)
    def best_response(self, p_aggressive, payoff_matrix):
        exp = {}
        for j, s in enumerate(STRATEGIES_I):
            exp[s] = (p_aggressive      * payoff_matrix[0][j] +   # aggressive row
                      (1-p_aggressive)  * payoff_matrix[1][j])    # conservative row
        return max(exp, key=exp.get)
    def choose_strategy(self):
        strategies = list(self.strategy_prob.keys())
        probs      = list(self.strategy_prob.values())
        return np.random.choice(strategies, p=probs)
    def update_strategy(self, payoff_matrix, opp_history, lr=0.1):
        p = self.predict_opponent(opp_history)
        br = self.best_response(p, payoff_matrix)
        for s in self.strategy_prob:
            if s == br:
               self.strategy_prob[s] += lr * (1 - self.strategy_prob[s])
            else:
               self.strategy_prob[s] -= lr * self.strategy_prob[s]
        total = sum(self.strategy_prob.values())
        self.strategy_prob = {k: v/total
                              for k, v in self.strategy_prob.items()}