import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.cm as cm

# Sample temperature data (replace with your actual data)
days = range(1, 11)  # Assuming 10 days
max_temp = [25, 28, 32, 30, 27, 23, 20, 22, 24, 26]
min_temp = [18, 20, 22, 21, 19, 17, 15, 16, 18, 20]
avg_temp = [(max_temp[i] + min_temp[i]) / 2 for i in range(len(days))]

# Debug print statements
print("Min Temperature:", min(min_temp))
print("Max Temperature:", max(max_temp))

# Define a colormap that transitions from cool to warm temperature
cmap = plt.cm.RdYlBu_r

# Normalize temperature values for colormap (0 to 1)
norm = Normalize(vmin=min(min_temp), vmax=max(max_temp))

# Debug print statements
print("Normalized Avg Temperature:", [norm(x) for x in avg_temp])

# Plot the fill between for min and max temperature using colormap
plt.fill_between(days, max_temp, min_temp, color=cmap(norm(avg_temp)), alpha=0.7)

# Plot the average temperature line
plt.plot(days, avg_temp, color='white', marker='o', linewidth=2, label='Average Temperature')

# Set labels and title
plt.xlabel('Days')
plt.ylabel('Temperature (°C)')
plt.title('Daily Temperature Variation')

# Add legend
plt.legend()

# Customize the plot (optional)
plt.grid(True)
plt.xticks(days)  # Display days on x-axis

# Add colorbar to show the temperature range
cbar = plt.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), ax=plt.gca(), label='Temperature (°C)')
plt.show()
