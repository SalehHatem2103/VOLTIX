# 🚢 Titanic Passengers Dashboard

An interactive dashboard built with **Plotly Dash** to explore survival patterns among Titanic passengers, backed by a fully cleaned dataset and a documented data-cleaning pipeline.

---

## 📁 Project Contents

| File | Description |
|---|---|
| `File_3.csv` | Raw Titanic passenger dataset |
| `clean_titanic_data.ipynb` | Jupyter notebook with the full data-cleaning pipeline |
| `File_3_cleaned.csv` | Cleaned dataset (output of the notebook) |
| `titanic_dashboard.py` | Dash application (KPIs, charts, filters) |

---

## 🧹 Data Cleaning

The raw dataset (418 rows) had several quality issues that were addressed before analysis:

- **Corrupted quotes in `Name`** — some names contained leftover/malformed quote characters (e.g. `Miriam"")"""`) from the original file; these were stripped and whitespace normalized.
- **Missing `Age`** (86 rows) — imputed using the median age grouped by extracted `Title` and `Pclass`, rather than a single overall median.
- **Missing `Fare`** (1 row) — imputed using the median fare for the passenger's `Pclass`.
- **Missing `Cabin`** (327 rows, ~78%) — rather than dropping the column:
  - Added a `Deck` feature (first letter of the cabin code, or `Unknown`)
  - Added a `HasCabin` binary flag
  - Filled remaining blanks with `"Unknown"`
- **Feature engineering**:
  - `Title` — extracted from `Name` (Mr, Mrs, Miss, Master, Rare)
  - `FamilySize` — `SibSp + Parch + 1`
- **Type fixes** — enforced correct integer/float types across numeric columns.
- **Duplicates** — verified no duplicate `PassengerId` values.

Result: **418 rows × 16 columns, 0 missing values.**

---

## 📊 Key Insights

- **Overall survival rate:** 36.4%
- **By class:** 1st class passengers survived at a notably higher rate (46.7%) than 2nd (32.3%) and 3rd class (33.0%) — consistent with the "women and children first, higher classes closer to lifeboats" narrative around the disaster.
- **By port of embarkation:** Passengers who boarded at Queenstown had the highest survival rate (52.2%), followed by Cherbourg (39.2%) and Southampton (32.6%).
- **Fare vs. class:** Average fare scales sharply with class — 1st class ($94.28) vs. 2nd ($22.20) vs. 3rd ($12.44) — reinforcing fare as a strong proxy for socio-economic status.
- **Cabin availability:** Passengers with a recorded cabin number had a higher survival rate (48.4%) than those without (33.0%), likely correlating with class and deck location.
- **Family size:** Passengers traveling with a small family (2–4 members) tended to survive at higher rates than those traveling completely alone or in very large groups.
- **Titles:** The majority of passengers held the title "Mr" (240), followed by "Miss" (79) and "Mrs" (72), with a small number of "Master" (21) and rarer titles (6).

> **Note on the `Survived` column:** This dataset is the Kaggle Titanic *test* split, which does not include verified ground-truth outcomes. The `Survived` values here reflect a baseline assumption (female = survived, male = did not), not confirmed historical outcomes. The sex-based split above should be read as a property of this specific file, not as a general finding — the other patterns (class, fare, family size, cabin) are independent of that assumption and still hold analytical value.

---

## 📈 Dashboard Overview

Built with **Dash** + **Plotly Express**, running locally on `127.0.0.1:8050`.

**Filters (sidebar):**
- Passenger Class
- Port of Embarkation

**KPIs:**
- Total Passengers
- Survival Rate
- Average Age
- Average Fare

**Charts:**
- Survival Count by Passenger Class
- Survival Rate by Sex
- Age Distribution
- Fare vs. Age by Survival

All KPIs and charts update live based on the selected filters.

---

## 🛠️ Tech Stack

- Python 3
- pandas
- Plotly Express
- Dash

---

## ▶️ How to Run

1. Install dependencies:
   ```bash
   pip install dash pandas plotly
   ```
2. Make sure `File_3_cleaned.csv` is in the same folder as `titanic_dashboard.py`.
3. Run the app:
   ```bash
   python titanic_dashboard.py
   ```
4. Open your browser at `http://127.0.0.1:8050`.

---

## 📌 Notes

- To regenerate `File_3_cleaned.csv` from scratch, run all cells in `clean_titanic_data.ipynb` (update the input file path in the first cell if needed).
- Dataset source: [Kaggle — Titanic: Machine Learning from Disaster](https://www.kaggle.com/c/titanic).
