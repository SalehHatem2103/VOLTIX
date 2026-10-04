# Hospital Analytics Dashboard

Data cleaning, KPI modeling, and an interactive Power BI dashboard built on a 2023 hospital patient dataset (247 records after cleaning).

## Dataset

10 fields per patient: name, age, gender, diagnosis, attending doctor, admission date, discharge date, bill amount, insurance type, and risk level.

## Data Cleaning

The raw dataset (248 records) required the following fixes, performed in Power Query:

| Issue | Records affected | Fix |
|---|---|---|
| Exact duplicate row | 1 | Removed |
| Discharge date earlier than admission date (reversed entry) | 29 (11.7%) | Swapped admission/discharge dates |
| Gender inconsistent with patient's first name | ~50% of records | Corrected gender from first-name lookup (all first names in this dataset are unambiguous by convention) |
| Missing values | 0 | None found |
| Inconsistent category labels (diagnosis, insurance, risk level) | 0 | None found — categories were already standardized |

Final cleaned dataset: **247 patient records**, no missing values, no duplicates, no logical date errors.

## KPIs & Measures

| KPI | Value |
|---|---|
| Total Patients | 247 |
| Total Billing | $618,995 |
| Average Bill per Patient | $2,506 |
| Average Length of Stay | 6.26 days |
| Average Patient Age | 47.4 |
| Patients with No Insurance | 29.15% |
| High-Risk Patients | 36.03% |

## Dashboard

Single-page interactive Power BI dashboard, "Hospital Analytics Dashboard — 2023":

<img width="1206" height="678" alt="dashboard" src="https://github.com/user-attachments/assets/c8d0f9df-0f71-4e40-a2e0-50c6179abf40" />

**Slicers (left panel):**
- Gender
- Insurance Type
- Risk Level
- Diagnosis

**KPI cards (top row):**
- Total Billing — 619K
- Average Length of Stay — 6.26 days
- Total Patients — 247
- High-Risk Rate — 36.03%

**Charts:**
- **Patients by Diagnosis** (bar) — patient count per diagnosis, sorted descending from Influenza (40) down to Pneumonia (8)
- **Insurance Type Distribution** (donut) — Private / Government / No Insurance, with the No Insurance share (29.15%) highlighted
- **Risk Level Distribution** (donut) — High / Medium / Low, with the High-risk share (36.03%) highlighted
- **Monthly Admissions Trend** (line) — patient count by admission month, Jan–Dec, showing the May peak and August dip

Color scheme: light background with a blue/teal palette (matching the health-themed logo), teal used consistently as a highlight color for the category each chart is drawing attention to (No Insurance, High Risk).

## Key Insights

1. **Influenza is the most common diagnosis** (40 cases, 16% of admissions), followed by Fractures (37) and Chronic Allergy (34) — together nearly half of all admissions.
2. **Pneumonia is the rarest diagnosis but the costliest per case** — only 8 cases, yet the highest average bill (~$3,150), a low-volume/high-cost condition worth monitoring closely.
3. **Insurance type does not reduce cost** — government-insured patients actually carry the highest average bill (~$2,745), while privately-insured patients have the lowest (~$2,350). Billing appears driven more by case mix (diagnosis) than by coverage type.
4. **Clear seasonal pattern in admissions** — May was the busiest month (32 patients) and August the quietest (10), a roughly 3x swing that could inform staffing decisions.
5. **Uneven doctor workload** — Dr. Reem Abdullah handled 42 patients versus 24 for Dr. Sara Ibrahim, a 75% gap between the busiest and least busy doctor.
6. **Demographics don't explain cost or stay length** — age, length of stay, and bill amount are only weakly correlated with each other (all |r| < 0.2), suggesting diagnosis type is the primary cost driver, not patient age.
7. **Meaningful uninsured population** — 29% of patients (72 of 247) have no insurance, relevant for financial planning and outreach.

## Tools

- **Power Query (Excel)** — data cleaning
- **Power BI** — DAX measures and interactive dashboard
