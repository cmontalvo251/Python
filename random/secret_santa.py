import numpy as np
import matplotlib.pyplot as plt

PEOPLE = 20

bottom_phrase_ = 'You are number '
top_phrase_ = 'Buy a present for number '

# Generate assignments (Derangement)
givers = np.arange(1, PEOPLE + 1)
receivers = np.copy(givers)

while True:
    np.random.shuffle(receivers)
    if not np.any(givers == receivers):
        break

# Plotting
cols = 4
rows = int(np.ceil(PEOPLE / cols))

fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 2))
axes = axes.flatten()

for i in range(PEOPLE):
    ax = axes[i]
    bottom_phrase = bottom_phrase_ + str(givers[i])
    top_phrase = top_phrase_ + str(receivers[i])
    
    ax.text(0.5, 0.3, bottom_phrase, fontsize=12, ha='center')
    ax.text(0.5, 0.7, top_phrase, fontsize=12, ha='center')
    ax.set_xticks([])
    ax.set_yticks([])

# Hide unused axes
for i in range(PEOPLE, len(axes)):
    axes[i].axis('off')

plt.tight_layout()
plt.savefig('secret_santa_all.png')
plt.close()