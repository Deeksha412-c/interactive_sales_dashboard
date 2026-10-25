
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "visualizations"

# Create output folder if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Set a consistent visual theme
sns.set_theme(style="whitegrid", palette="deep")

# Display dataset information
print("INTERACTIVE SALES DASHBOARD")
print("=" * 40)
print(f"Total records: {len(df)}")
print(f"Total revenue: ${df['Total_Sales'].sum():,.2f}")
print(f"Total units sold: {df['Quantity'].sum():,}")
print(f"Unique products: {df['Product'].nunique()}")
print(f"Regions covered: {df['Region'].nunique()}")
print("\nDataset loaded successfully!")



# ----------------------------------------
# Chart 1: Sales Revenue by Product
# ----------------------------------------

product_sales = (
    df.groupby("Product", as_index=False)["Total_Sales"]
    .sum()
    .sort_values("Total_Sales", ascending=False)
)

plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=product_sales,
    x="Product",
    y="Total_Sales",
    hue="Product",
    legend=False
)

ax.set_title("Sales Revenue by Product", fontsize=16, fontweight="bold")
ax.set_xlabel("Product", fontsize=12)
ax.set_ylabel("Total Revenue ($)", fontsize=12)

# Add revenue labels above the bars
for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"${value:,.0f}" for value in container.datavalues],
        padding=3,
        fontsize=9
    )

plt.xticks(rotation=15)
plt.tight_layout()

# Save the chart
chart_path = OUTPUT_DIR / "sales_by_product.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"\nChart saved to: {chart_path}")
print("\nRevenue by product:")
print(product_sales.to_string(index=False))



# ----------------------------------------
# Chart 2: Sales Distribution by Product
# ----------------------------------------

plt.figure(figsize=(10, 6))

ax = sns.boxplot(
    data=df,
    x="Product",
    y="Total_Sales",
    hue="Product",
    legend=False
)

ax.set_title(
    "Sales Distribution by Product",
    fontsize=16,
    fontweight="bold"
)
ax.set_xlabel("Product", fontsize=12)
ax.set_ylabel("Sale Amount ($)", fontsize=12)

plt.xticks(rotation=15)
plt.tight_layout()

# Save the chart
chart_path = OUTPUT_DIR / "sales_distribution_boxplot.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"\nBox plot saved to: {chart_path}")



# ----------------------------------------
# Chart 3: Correlation Heatmap
# ----------------------------------------

numeric_columns = ["Quantity", "Price", "Total_Sales"]
correlation_matrix = df[numeric_columns].corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="YlGnBu",
    fmt=".2f",
    vmin=-1,
    vmax=1,
    linewidths=0.5
)

plt.title("Sales Data Correlation Heatmap", fontsize=15, fontweight="bold")
plt.tight_layout()

chart_path = OUTPUT_DIR / "correlation_heatmap.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"\nCorrelation heatmap saved to: {chart_path}")
print("\nCorrelation matrix:")
print(correlation_matrix.round(2))



# ----------------------------------------
# Chart 4: Daily Sales Trend
# ----------------------------------------

daily_sales = (
    df.groupby("Date", as_index=False)["Total_Sales"]
    .sum()
    .sort_values("Date")
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=daily_sales,
    x="Date",
    y="Total_Sales",
    marker="o"
)

plt.title("Daily Sales Revenue Trend", fontsize=16, fontweight="bold")
plt.xlabel("Date", fontsize=12)
plt.ylabel("Total Revenue ($)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

chart_path = OUTPUT_DIR / "daily_sales_trend.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"\nDaily sales trend saved to: {chart_path}")
print("\nDaily sales summary:")
print(daily_sales.head())



# ----------------------------------------
# Chart 5: Sales Revenue by Region
# ----------------------------------------

region_sales = (
    df.groupby("Region", as_index=False)["Total_Sales"]
    .sum()
    .sort_values("Total_Sales", ascending=False)
)

plt.figure(figsize=(9, 6))

ax = sns.barplot(
    data=region_sales,
    x="Region",
    y="Total_Sales",
    hue="Region",
    legend=False
)

ax.set_title("Sales Revenue by Region", fontsize=16, fontweight="bold")
ax.set_xlabel("Region", fontsize=12)
ax.set_ylabel("Total Revenue ($)", fontsize=12)

for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"${value:,.0f}" for value in container.datavalues],
        padding=3,
        fontsize=9
    )

plt.tight_layout()

chart_path = OUTPUT_DIR / "sales_by_region.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"\nSales by region chart saved to: {chart_path}")
print("\nRevenue by region:")
print(region_sales.to_string(index=False))




# ----------------------------------------
# Chart 6: Interactive Sales by Product
# ----------------------------------------

import plotly.express as px

interactive_chart = px.bar(
    product_sales,
    x="Product",
    y="Total_Sales",
    title="Interactive Sales Revenue by Product",
    labels={
        "Product": "Product",
        "Total_Sales": "Revenue ($)"
    },
    hover_data={"Total_Sales": ":,.2f"},
    color="Product"
)

interactive_chart.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Product",
    yaxis_title="Revenue ($)"
)

html_path = OUTPUT_DIR / "interactive_sales_by_product.html"
interactive_chart.write_html(html_path)

print(f"\nInteractive Plotly chart saved to: {html_path}")




# ----------------------------------------
# Complete Interactive Sales Dashboard
# ----------------------------------------

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Create KPI values
total_revenue = df["Total_Sales"].sum()
total_units = df["Quantity"].sum()
total_products = df["Product"].nunique()
total_regions = df["Region"].nunique()

# Create dashboard with multiple charts
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Revenue by Product",
        "Revenue by Region",
        "Daily Sales Trend",
        "Sales Distribution by Product"
    ),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "box"}]
    ],
    vertical_spacing=0.15
)

# Chart 1: Revenue by product
for product in product_sales["Product"]:
    product_row = product_sales[product_sales["Product"] == product]
    fig.add_trace(
        go.Bar(
            x=product_row["Product"],
            y=product_row["Total_Sales"],
            name=product,
            hovertemplate="%{x}<br>Revenue: $%{y:,.2f}<extra></extra>"
        ),
        row=1, col=1
    )

# Chart 2: Revenue by region
fig.add_trace(
    go.Bar(
        x=region_sales["Region"],
        y=region_sales["Total_Sales"],
        name="Region Revenue",
        marker_color="teal",
        hovertemplate="%{x}<br>Revenue: $%{y:,.2f}<extra></extra>"
    ),
    row=1, col=2
)

# Chart 3: Daily sales trend
fig.add_trace(
    go.Scatter(
        x=daily_sales["Date"],
        y=daily_sales["Total_Sales"],
        mode="lines+markers",
        name="Daily Revenue",
        line=dict(color="royalblue"),
        hovertemplate="%{x|%Y-%m-%d}<br>Revenue: $%{y:,.2f}<extra></extra>"
    ),
    row=2, col=1
)

# Chart 4: Sales distribution by product
for product in df["Product"].unique():
    product_data = df[df["Product"] == product]
    fig.add_trace(
        go.Box(
            x=product_data["Product"],
            y=product_data["Total_Sales"],
            name=product,
            boxpoints="outliers",
            showlegend=False
        ),
        row=2, col=2
    )

# Add dashboard title and layout
fig.update_layout(
    title={
        "text": (
            "Interactive Sales Dashboard"
            "<br><sup>"
            f"Revenue: ${total_revenue:,.2f} | "
            f"Units Sold: {total_units:,} | "
            f"Products: {total_products} | "
            f"Regions: {total_regions}"
            "</sup>"
        ),
        "x": 0.5
    },
    template="plotly_white",
    height=850,
    width=1300,
    hovermode="closest",
    barmode="group"
)

fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
fig.update_yaxes(title_text="Sale Amount ($)", row=2, col=2)

# Save dashboard as interactive HTML
dashboard_path = OUTPUT_DIR / "interactive_dashboard.html"
fig.write_html(dashboard_path)

print(f"\nComplete interactive dashboard saved to: {dashboard_path}")
