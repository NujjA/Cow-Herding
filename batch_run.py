from model import CHModel
import movement_control
from collections import defaultdict
import movement_control

episodes = 3
steps = 100

random_agents = 1
cow_agents = 4
plan_agents = 0
monte_carlo_agents = 1
td_agents = 0
nA = len(movement_control.possible_action_space)

MC_Q_values = [] # Save Q values so MC agents can access each episode
for agent in range(monte_carlo_agents):
    MC_Q_values.append(defaultdict(lambda: np.zeros(nA)))

final_scores = []
for episode in range(episodes):
    model = CHModel(8, 8, random_n = random_agents, cow_n = cow_agents, plan_n = plan_agents, mc_n = monte_carlo_agents, td_n = td_agents, episode_number = episode, old_Q_values = MC_Q_values)
    print("Episode ", episode)
    for i in range(steps):
        model.step()
    final_scores.append(movement_control.compute_score(model))
    MC_Q_values = model.get_new_Q_values()

for ep, score in enumerate(final_scores):
    print("Final score for episode ", ep, ": ", score)

