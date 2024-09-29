import json
import matplotlib.pyplot as plt
from tqdm import tqdm

# Load data from the JSON file
with open("asin_num_reviews_map.json", "r") as f:
    data = json.load(f)


# Use tqdm to show progress while filtering
filtered_data = {k: v for k, v in tqdm(data.items(), desc="Filtering data") if v >= 50}

# Extract product IDs (keys) and review counts (values) from the filtered data
product_ids = list(filtered_data.keys())
review_counts = list(filtered_data.values())

print(len(product_ids))
print(len(review_counts))

# Create a bar chart
plt.figure(figsize=(60, 6))
plt.bar(product_ids, review_counts, color="skyblue")

# Add titles and labels
plt.title("Number of Reviews per Product (Reviews >= 50)", fontsize=16)
plt.xlabel("Product ID", fontsize=12)
plt.ylabel("Number of Reviews", fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(product_ids[::50], rotation="vertical")


# Show the plot
plt.tight_layout()
plt.grid(True, axis="y")
plt.show()
plt.savefig("reviews_bar_chart.png", dpi=300)  # Save with high resolution (300 dpi)
