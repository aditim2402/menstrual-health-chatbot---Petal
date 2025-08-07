import matplotlib.pyplot as plt
from datetime import timedelta

def plot_cycle_timeline(logged_days=[], predicted_days=[], ovulation_days=[], start_date=None, total_days=35):
    fig, ax = plt.subplots(figsize=(14, 2.8))

    for i in range(total_days):
        # 🗓️ Date label or fallback
        date_label = (start_date + timedelta(days=i)).strftime("%b %d") if start_date else f"Day {i+1}"

        # 🟥 Determine color
        color = "white"
        edge = "gray"

        if i in logged_days:
            color = "darkred"
        elif i in predicted_days:
            color = "lightcoral"

        # 🟣 Ovulation marker
        if i in ovulation_days:
            ax.plot(i + 0.5, 0.5, "o", color="purple", markersize=10, zorder=2)

        # 🟡 Draw day circle
        circle = plt.Circle((i + 0.5, 0.5), 0.4, color=color, ec=edge)
        ax.add_patch(circle)

        # 🏷️ Date label under each
        ax.text(i + 0.5, 0.1, date_label, ha="center", va="top", fontsize=7, rotation=60)

    ax.set_xlim(0, total_days)
    ax.set_ylim(0, 1.2)
    ax.axis("off")
    return fig
