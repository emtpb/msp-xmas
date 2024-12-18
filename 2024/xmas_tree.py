import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon


def generate_star(center_x, center_y, radius, inner_radius, points=5):
    coords = []
    angle = 2 * np.pi / (2 * points)  # Angle between consecutive points
    rotation = np.pi / 2  # Rotate so one point faces directly upwards
    for i in range(2 * points):
        r = radius if i % 2 == 0 else inner_radius
        theta = i * angle + rotation
        x = center_x + r * np.cos(theta)
        y = center_y + r * np.sin(theta)
        coords.append((x, y))
    return coords


### Initial figure ###
fig, ax = plt.subplots(figsize=(6, 8))
fig.set_facecolor("xkcd:sky blue")
ax.set_aspect("equal")

# Leaves
tree_levels = [
    ([0, -1.5, 1.5], [0, -2, -2]),
    ([0, -1.2, 1.2], [0.5, -1, -1]),
    ([0, -0.8, 0.8], [1, 0, 0]),
]
for x, y in tree_levels:
    ax.fill(x, y, color="green", zorder=4)

# Trunk
trunk_x = [-0.3, 0.3, 0.3, -0.3]
trunk_y = [-2, -2, -2.5, -2.5]
ax.fill(trunk_x, trunk_y, color="saddlebrown")

# Christmas balls
color_palette = ["red", "blue", "gold", "purple", "white"]
ball_coords = [
    (0, 0.2),
    (-0.7, -0.4),
    (0.7, -0.4),
    (-1.0, -1.4),
    (1.0, -1.4),
    (0, -1.6),
]
balls = []
for x, y in ball_coords:
    ball = ax.scatter(x, y, color=color_palette[0], s=100, zorder=5)
    balls.append(ball)

# Star (initialized as a patch for dynamic updates)
star_coords = generate_star(
    center_x=0, center_y=1.1, radius=0.3, inner_radius=0.15, points=5
)
star = Polygon(star_coords, closed=True, facecolor="gold", edgecolor="black", zorder=6)
ax.add_patch(star)

ax.set_xlim(-2, 2)
ax.set_ylim(-3, 2)
ax.axis("off")
plt.title("Fröhliche Weihnachten!", fontsize=24, fontname="cursive")

# Snow flakes
num_snowflakes = 50
snow_x = np.random.uniform(-2, 2, num_snowflakes)
snow_y = np.random.uniform(-3, 2, num_snowflakes)
snow_speeds = np.random.uniform(0.01, 0.03, num_snowflakes)
snow_offsets = np.zeros(num_snowflakes)
snow_amplitudes = np.random.uniform(0.02, 0.1, num_snowflakes)
snow = ax.scatter(snow_x, snow_y, color="white", s=10, zorder=1)


## Animation
color_offset = [0]
star_colors = ["gold", "yellow"]


def update(frame):

    if frame % 20 == 0:
        # Update color offset
        color_offset[0] = (color_offset[0] + 1) % len(color_palette)

        # Update ball colors
        for i, ball in enumerate(balls):
            color = color_palette[(color_offset[0] + i) % len(color_palette)]
            ball.set_color(color)

        # Blink the star
        star.set_facecolor(star_colors[frame % len(star_colors)])

    # Update snowflake positions
    global snow_y, snow_offsets
    snow_y -= snow_speeds  # Schneeflocken nach unten bewegen
    snow_offsets = snow_amplitudes * np.sin(frame * 0.1)  # Hin-und-Her-Wehen
    snow_x_updated = snow_x + snow_offsets  # Aktuelle x-Positionen der Schneeflocken

    # Schneeflocken, die unten verschwinden, nach oben zurücksetzen
    snow_y[snow_y < -3] = 2

    # Aktualisiere Schneeflockenpositionen
    snow.set_offsets(np.c_[snow_x_updated, snow_y])

    return balls + [star, snow]


ani = FuncAnimation(fig, update, frames=np.arange(0, 200), interval=20, blit=True)

plt.show()
