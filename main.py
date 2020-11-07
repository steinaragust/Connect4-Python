from connect4_with_ai_vs_ai import MC_AI, AI, play_game

scores = [0, 0]

games = 5

for i in range(games):
    winner = play_game(i % 2)
    scores[winner] += 1

print("MC_AI final score: %d" %  (scores[MC_AI]))
print("AI final score: %d" % (scores[AI]))
