import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = "."
OUT_DIR = "output"
os.makedirs(f"{OUT_DIR}/charts", exist_ok=True)

MAIN_FILE = "Video_Games_Sales_as_at_22_Dec_2016.csv"
PS4_FILE = "PS4_GamesSales.csv"
XONE_FILE = "XboxOne_GameSales.csv"

plt.rcParams.update({"figure.figsize": (10, 6), "axes.grid": True, "grid.alpha": .3})


def read_csv_safe(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")


main_raw = read_csv_safe(f"{DATA_DIR}/{MAIN_FILE}")
ps4_raw = read_csv_safe(f"{DATA_DIR}/{PS4_FILE}")
xone_raw = read_csv_safe(f"{DATA_DIR}/{XONE_FILE}")

for name, d in [("MAIN", main_raw), ("PS4", ps4_raw), ("XONE", xone_raw)]:
    print("=" * 80)
    print(name, d.shape)
    print(d.dtypes.to_string())
    print("\nMissing values:\n", d.isna().sum()[d.isna().sum() > 0].to_string())
    print("Full duplicate rows:", d.duplicated().sum())

print("\nMAIN duplicates on Name+Platform:", main_raw.duplicated(["Name", "Platform"]).sum())
print("MAIN years outside 1980-2016:", (main_raw["Year_of_Release"] > 2016).sum())
print("PS4 rows with missing Year & Publisher:", (ps4_raw["Year"].isna() & ps4_raw["Publisher"].isna()).sum())
print("XONE rows with missing Year & Publisher:", (xone_raw["Year"].isna() & xone_raw["Publisher"].isna()).sum())

COLS = ["Name", "Platform", "Year", "Genre", "Publisher",
        "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales",
        "Critic_Score", "Critic_Count", "User_Score", "User_Count", "Developer", "Rating"]

main = main_raw.rename(columns={"Year_of_Release": "Year"}).copy()

small_map = {"Game": "Name", "North America": "NA_Sales", "Europe": "EU_Sales",
             "Japan": "JP_Sales", "Rest of World": "Other_Sales", "Global": "Global_Sales"}


def prep_small(df, platform):
    d = df.rename(columns=small_map).drop(columns=["Pos"], errors="ignore").copy()
    d["Platform"] = platform
    return d


ps4 = prep_small(ps4_raw, "PS4")
xone = prep_small(xone_raw, "XOne")

main = main.dropna(subset=["Name", "Genre"])
main.loc[main["Year"] > 2016, "Year"] = np.nan
main["User_Score"] = pd.to_numeric(main["User_Score"], errors="coerce")

ps4 = ps4.dropna(subset=["Year", "Publisher"])
xone = xone.dropna(subset=["Year", "Publisher"])

def key(df):
    return df["Name"].str.lower().str.strip() + "|" + df["Platform"]

score_cols = ["Critic_Score", "Critic_Count", "User_Score", "User_Count", "Developer", "Rating"]
score_lookup = main.assign(_k=key(main)).drop_duplicates("_k").set_index("_k")[score_cols]

new_gen = pd.concat([ps4, xone], ignore_index=True)
new_gen = new_gen.join(score_lookup, on=key(new_gen))

main_other = main[~main["Platform"].isin(["PS4", "XOne"])]
df = pd.concat([main_other[COLS], new_gen[COLS]], ignore_index=True)

df["Name"] = df["Name"].str.strip()
df["Publisher"] = df["Publisher"].fillna("Unknown").str.strip()
df.loc[df["Publisher"].isin(["N/A", ""]), "Publisher"] = "Unknown"
df["Developer"] = df["Developer"].fillna("Unknown")
df["Rating"] = df["Rating"].fillna("Not Rated")

df = (df.sort_values("Global_Sales", ascending=False)
        .drop_duplicates(["Name", "Platform"], keep="first")
        .sort_index())

region_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
df["Global_Sales"] = df[region_cols].sum(axis=1).round(2)

df["Year"] = df["Year"].astype("Int64")
for c in ["Critic_Count", "User_Count"]:
    df[c] = df[c].astype("Int64")

family = {"PS": "PlayStation", "PS2": "PlayStation", "PS3": "PlayStation", "PS4": "PlayStation",
          "PSP": "PlayStation", "PSV": "PlayStation",
          "XB": "Xbox", "X360": "Xbox", "XOne": "Xbox",
          "Wii": "Nintendo", "WiiU": "Nintendo", "NES": "Nintendo", "SNES": "Nintendo", "N64": "Nintendo",
          "GC": "Nintendo", "GB": "Nintendo", "GBA": "Nintendo", "DS": "Nintendo", "3DS": "Nintendo",
          "PC": "PC"}
df["Platform_Family"] = df["Platform"].map(family).fillna("Other")
df["Decade"] = (df["Year"] // 10 * 10).astype("Int64").astype(str) + "s"
df.loc[df["Year"].isna(), "Decade"] = "Unknown"
df["Score_Gap"] = (df["Critic_Score"] / 10 - df["User_Score"]).round(2)

df = df.reset_index(drop=True)
print("Final shape:", df.shape)
print("Remaining missing:\n", df.isna().sum()[df.isna().sum() > 0].to_string())

df.to_csv(f"{OUT_DIR}/Cleaned_Games.csv", index=False, encoding="utf-8-sig")

region_long = df.melt(id_vars=["Name", "Platform", "Year", "Genre", "Publisher"],
                      value_vars=region_cols, var_name="Region", value_name="Sales")
region_long["Region"] = region_long["Region"].map(
    {"NA_Sales": "North America", "EU_Sales": "Europe", "JP_Sales": "Japan", "Other_Sales": "Rest of World"})
region_long.to_csv(f"{OUT_DIR}/Sales_by_Region.csv", index=False, encoding="utf-8-sig")

total_games = df["Name"].nunique()
total_sales = df["Global_Sales"].sum()
print(f"Total unique games: {total_games:,} | Total records: {len(df):,} | Total sales: {total_sales:,.1f}M")

genre_count = df["Genre"].value_counts()
genre_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
platform_sales = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False)
publisher_sales = df[df["Publisher"] != "Unknown"].groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False)
top_games = df.groupby("Name")["Global_Sales"].sum().sort_values(ascending=False)
year_sales = df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum()
region_sales = df[region_cols].sum()
region_sales.index = ["North America", "Europe", "Japan", "Rest of World"]
avg_sales_genre = df.groupby("Genre")["Global_Sales"].mean().sort_values(ascending=False)

print("\nTop genre by count:", genre_count.index[0], "| by sales:", genre_sales.index[0])
print("Top platform:", platform_sales.index[0])
print("Top publisher:", publisher_sales.index[0])
print("\nTop 10 games:\n", top_games.head(10).round(2).to_string())
print("\nRegion share %:\n", (region_sales / region_sales.sum() * 100).round(1).to_string())
print("\nPeak year:", year_sales.idxmax(), round(year_sales.max(), 1))

scored = df.dropna(subset=["Critic_Score", "User_Score"])
corr = scored[["Critic_Score", "User_Score", "Global_Sales"]].corr()
print("\nCorrelation (rows with scores =", len(scored), "):\n", corr.round(3).to_string())

pg = df.pivot_table(index="Platform", columns="Genre", values="Global_Sales", aggfunc="sum", fill_value=0)

scored = scored.assign(Score_Bucket=pd.cut(scored["Critic_Score"], [0, 50, 60, 70, 80, 90, 100],
                                           labels=["<50", "50-59", "60-69", "70-79", "80-89", "90+"]))
bucket = scored.groupby("Score_Bucket", observed=True)["Global_Sales"].mean()
print("\nAvg sales by critic-score bucket:\n", bucket.round(2).to_string())

def save(name):
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/charts/{name}.png", dpi=150)
    plt.show()


genre_count.sort_values().plot.barh(color="#4C78A8")
plt.title("Number of Games by Genre"); plt.xlabel("Games"); save("01_genre_count")

genre_sales.sort_values().plot.barh(color="#F58518")
plt.title("Total Global Sales by Genre (M units)"); plt.xlabel("Sales (M)"); save("02_genre_sales")

platform_sales.head(10).sort_values().plot.barh(color="#54A24B")
plt.title("Top 10 Platforms by Global Sales (M units)"); plt.xlabel("Sales (M)"); save("03_platform_sales")

publisher_sales.head(10).sort_values().plot.barh(color="#E45756")
plt.title("Top 10 Publishers by Global Sales (M units)"); plt.xlabel("Sales (M)"); save("04_publisher_sales")

top_games.head(10).sort_values().plot.barh(color="#B279A2")
plt.title("Top 10 Best-Selling Games (M units)"); plt.xlabel("Sales (M)"); save("05_top_games")

year_sales.plot(marker="o", color="#4C78A8")
plt.title("Global Sales Trend by Year (M units)"); plt.xlabel("Year"); plt.ylabel("Sales (M)"); save("06_sales_trend")

plt.figure(figsize=(7, 7))
plt.pie(region_sales, labels=region_sales.index, autopct="%1.1f%%", startangle=90,
        wedgeprops=dict(width=0.4))
plt.title("Sales Share by Region"); save("07_region_donut")

plt.scatter(scored["Critic_Score"], scored["Global_Sales"], alpha=.3, s=12)
plt.yscale("log"); plt.xlabel("Critic Score"); plt.ylabel("Global Sales (M, log)")
plt.title(f"Critic Score vs Sales (r = {corr.loc['Critic_Score', 'Global_Sales']:.2f})"); save("08_score_vs_sales")

plt.scatter(scored["User_Score"], scored["Global_Sales"], alpha=.3, s=12, color="#F58518")
plt.yscale("log"); plt.xlabel("User Score"); plt.ylabel("Global Sales (M, log)")
plt.title(f"User Score vs Sales (r = {corr.loc['User_Score', 'Global_Sales']:.2f})"); save("09_user_vs_sales")

bucket.plot.bar(color="#54A24B", rot=0)
plt.title("Average Sales per Game by Critic Score Bucket"); plt.ylabel("Avg Sales (M)"); save("10_score_bucket")

top_pl = platform_sales.head(10).index
plt.figure(figsize=(12, 6))
plt.imshow(pg.loc[top_pl], aspect="auto", cmap="YlOrRd")
plt.xticks(range(pg.shape[1]), pg.columns, rotation=45, ha="right")
plt.yticks(range(len(top_pl)), top_pl)
plt.colorbar(label="Sales (M)"); plt.title("Platform x Genre Sales (M units)"); plt.grid(False); save("11_platform_genre_heatmap")

top5 = genre_sales.head(5).index
gy = (df.dropna(subset=["Year"]).query("Genre in @top5")
        .pivot_table(index="Year", columns="Genre", values="Global_Sales", aggfunc="sum").fillna(0))
gy.plot(figsize=(11, 6)); plt.title("Sales Trend of Top 5 Genres"); plt.ylabel("Sales (M)"); save("12_genre_trend")

print("\nSaved:", f"{OUT_DIR}/Cleaned_Games.csv", f"{OUT_DIR}/Sales_by_Region.csv", f"{OUT_DIR}/charts/*.png")