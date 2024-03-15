import json
import matplotlib.pyplot as plt
import pandas as pd

# Load crop data from JSON file
with open('intents.json') as file:
    intents_data = json.load(file)

# Extract crop data from intents
crops_data = intents_data['intents'][1]['patterns']  # Assuming crop data is stored in the second intent (modify as needed)

# Create DataFrame
df = pd.DataFrame({"Crops": crops_data})

# Create table plot
plt.figure(figsize=(10, 6))
plt.axis('off')  # Turn off axis
table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Scale table size

# Save table as image
plt.savefig('crop_sowing_schedule.png', bbox_inches='tight', pad_inches=0.05)
plt.close()

