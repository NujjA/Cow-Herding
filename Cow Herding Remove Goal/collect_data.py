from model import CHModel

# number of episodes
episodes = 5

# number of agents
random_agents = 2
cow_agents = 4
plan_agents = 2
trained_mc_agents = 2

# Collect times for random_agents

# Collect times for plan_agents
final_plan_scores = []
final_plan_times = []
for episode in range(episodes):
    model = CHModel(10, 10, cow_n = cow_agents, plan_n = plan_agents, episode_number = episode)
    print("Plan Episode ", episode)
    while True:
        model.step()
        if(model.done):
            print("all cows herded in plan run, breaking")
            break
    final_plan_scores.append(movement_control.compute_score(model))
    final_plan_times.append(model.schedule.time)
    MC_Q_values = model.get_new_Q_values()

# Collect times for trained monte carlo agents

