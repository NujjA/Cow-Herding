from model import CHModel
import movement_control

episodes = 3
steps = 100

final_scores = []
for episode in range(episodes):
    model = CHModel(50, 8, 8)
    print("Episode ", episode)
    for i in range(steps):
        model.step()
    final_scores.append(movement_control.compute_score(model))
    #print("Final score for episode ", episode, ": ", movement_control.compute_score(model))

for ep, score in enumerate(final_scores):
    print("Final score for episode ", ep, ": ", score)

#score = model.datacollector.get_model_vars_dataframe()
#score.plot()
