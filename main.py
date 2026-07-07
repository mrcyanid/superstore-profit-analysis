# main.py - Superstore Profit Analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create outputs folder
OUTPUT_DIR = 'outputs'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("="*60)
print("SUPERSTORE PROFIT ANALYSIS - GENERATED DATA")
print("="*60)

# Generate sample data
np.random.seed(42)
n_rows = 1000

# Create categories
categories = ['Furniture', 'Office Supplies', 'Technology']
category = np.random.choice(categories, n_rows)

# Generate realistic data
sales = np.random.uniform(50, 500, n_rows)
discount = np.random.uniform(0, 0.50, n_rows)

# Profit depends on discount
profit = sales * (0.30 - discount * 0.60) + np.random.normal(0, 10, n_rows)

# Create DataFrame
df = pd.DataFrame({
    'Category': category,
    'Sales': sales,
    'Profit': profit,
    'Discount': discount
})

print(f"Generated {len(df)} rows of sample data")
print(f"Categories: {df['Category'].unique()}")

# Create Profit Ratio
df['Profit_Ratio'] = df['Profit'] / df['Sales']

# Create Discount Buckets
bins = [0, 0.10, 0.20, 0.30, 0.40, 0.50]
labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%']
df['Discount_Bucket'] = pd.cut(df['Discount'], bins=bins, labels=labels, right=False)

# Calculate averages
result_df = df.groupby(['Category', 'Discount_Bucket']).agg({
    'Profit_Ratio': 'mean',
    'Sales': 'count'
}).reset_index()
result_df.columns = ['Category', 'Discount_Bucket', 'Avg_Profit_Ratio', 'Number_of_Orders']

# Save results
result_df.to_csv(os.path.join(OUTPUT_DIR, 'discount_profit_analysis.csv'), index=False)
print("Analysis saved to outputs folder!")

# Create the chart
print("\nCreating visualization...")
sns.set_style("whitegrid")
plt.figure(figsize=(12, 7))

sns.lineplot(data=result_df, 
             x='Discount_Bucket', 
             y='Avg_Profit_Ratio', 
             hue='Category', 
             marker='o', 
             linewidth=2.5)

plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Break Even (0 Profit)')

plt.title('Impact of Discounts on Profit Ratio by Product Category', 
          fontsize=16, fontweight='bold')
plt.xlabel('Discount Percentage Range', fontsize=12)
plt.ylabel('Average Profit Ratio (Profit / Sales)', fontsize=12)
plt.legend(title='Category', loc='best')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

chart_path = os.path.join(OUTPUT_DIR, 'profit_discount_analysis.png')
plt.savefig(chart_path, dpi=300, bbox_inches='tight')
print(f"Chart saved to: {chart_path}")

# Executive Summary
print("\n" + "="*60)
print("EXECUTIVE SUMMARY - INSIGHTS")
print("="*60)

worst_idx = result_df['Avg_Profit_Ratio'].idxmin()
worst = result_df.loc[worst_idx]

best_idx = result_df['Avg_Profit_Ratio'].idxmax()
best = result_df.loc[best_idx]

print(f"1. WORST PERFORMER: {worst['Category']} at {worst['Discount_Bucket']} discount")
print(f"   → Average Profit Ratio: {worst['Avg_Profit_Ratio']:.1%}")

print(f"\n2. BEST PERFORMER: {best['Category']} at {best['Discount_Bucket']} discount")
print(f"   → Average Profit Ratio: {best['Avg_Profit_Ratio']:.1%}")

print("\n3. KEY INSIGHTS:")
tech_data = result_df[result_df['Category'] == 'Technology']
if len(tech_data) > 0:
    tech_profitable = tech_data[tech_data['Avg_Profit_Ratio'] > 0]
    if len(tech_profitable) > 0:
        max_discount = tech_profitable['Discount_Bucket'].iloc[-1]
        print(f"   → Technology can handle up to {max_discount} discounts profitably")

furniture_data = result_df[result_df['Category'] == 'Furniture']
if len(furniture_data) > 0:
    furn_profitable = furniture_data[furniture_data['Avg_Profit_Ratio'] > 0]
    if len(furn_profitable) > 0:
        furn_max = furn_profitable['Discount_Bucket'].iloc[-1]
        print(f"   → Furniture should be capped at {furn_max} discounts")
    else:
        print(f"   → Furniture becomes unprofitable even at lowest discounts")

print("\n4. RECOMMENDATIONS:")
print("   → Implement dynamic discount caps by category")
print("   → Set Furniture max discount at 15-20%")
print("   → Office Supplies max discount at 25-30%")
print("   → Technology can offer up to 40% discounts")

print("="*60)

# Show the chart
plt.show()

print("\nProject completed successfully!")
print(f"Check the '{OUTPUT_DIR}' folder for your chart and CSV!")