import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)
categories = {
    "Food": (80, 400),
    "Transport": (30, 250),
    "Shopping": (200, 2500),
    "Bills": (300, 1500),
    "Entertainment": (100, 800),
}

rows = []
start = date(2026, 1, 1)
for i in range(240):
    cat = random.choice(list(categories))
    low, high = categories[cat]
    rows.append({
        "date": start + timedelta(days=random.randint(0, 179)),
        "category": cat,
        "amount": random.randint(low, high),
    })

df = pd.DataFrame(rows)
df.to_csv("expenses.csv", index=False)
print(df.head())

df = pd.read_csv("expenses.csv", parse_dates=["date"])
df["month"] = df["date"].dt.to_period("M")
print(df.info())
print(df.isna().sum())   # check for missing values
print("Total spent:", df["amount"].sum())
print(df.groupby("category")["amount"].sum().sort_values(ascending=False))
print(df.groupby("month")["amount"].sum())
import matplotlib.pyplot as plt

df.groupby("category")["amount"].sum().plot(kind="bar", title="Spending by Category")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("by_category.png")
plt.show()

df.groupby("month")["amount"].sum().plot(kind="line", marker="o", title="Monthly Spending")
plt.savefig("by_month.png")
plt.show()

total = df["amount"].sum()
by_cat = df.groupby("category")["amount"].sum().sort_values(ascending=False)
by_month = df.groupby("month")["amount"].sum()

print("Number of transactions:", len(df))
print("Date range:", df["date"].min().date(), "to", df["date"].max().date())
print("Total spent:", total)
print("Biggest category:", by_cat.index[0], "-", round(by_cat.iloc[0] / total * 100, 1), "%")
print("Smallest category:", by_cat.index[-1], "-", round(by_cat.iloc[-1] / total * 100, 1), "%")
print("Highest month:", by_month.idxmax(), "-", by_month.max())
print("Lowest month:", by_month.idxmin(), "-", by_month.min())
print("Average per transaction:", round(df["amount"].mean(), 1))