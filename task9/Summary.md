# Task 9 – Customer Data Analysis: Summary of Key Findings

**Dataset:** 2,100 unique customers after cleaning (50 duplicate rows removed), purchases from Oct 2022 to Jul 2025.

## Data cleaning
- Standardized Gender labels (M/male/F/female → Male/Female); missing values filled from the customer's first name.
- Invalid ages (-1, 200) and missing ages replaced with values around the mean (~54), kept between 18 and 90. Age is therefore approximate, because most ages were imputed (the data is synthetic).
- Ratings outside the 1–5 scale (value 10) and invalid dates (32/13/2020) were set to empty; missing Category and Purchase Amount were left empty (not imputed). The Phone column was dropped (2 distinct values only).

## Key KPIs
| KPI | Value |
|---|---|
| Customers | 2,100 |
| Total revenue | $1,021,324 |
| Average purchase | $509.90 |
| Average rating | 3.03 / 5 |

## Findings
1. **Customers:** Males are 52.3% and females 47.7% of customers. Average purchase is similar (~$500 vs ~$520), so gender has little effect on spending. The 65+ group is the largest, but average purchase is flat across age groups (~$490–$526), so age does not drive spending.
2. **Categories:** Clothing leads in revenue ($163.9K, 21.7%) and has the highest average purchase ($537); Toys is lowest in revenue ($141.4K). The five categories are close (about 19%–22% of revenue each), so there is no dominant category.
3. **Ratings:** Ratings are spread almost evenly from 1 to 5 and only ~39% are 4–5 stars. The average is 3.03, which signals low overall satisfaction. Electronics is rated highest (3.11) and Books lowest (2.96).
4. **Trends over time:** Revenue grew from $342K (2023) to $364K (2024), about +6%. 2022 (Oct–Dec) and 2025 (Jan–Jul) are partial years. Average purchase value drifts down slowly from year to year ($531 → $495).
5. **Seasonality:** Revenue peaks in Nov–Dec and in May–June; September and August are the weakest months.

## Recommendations
- Run campaigns and stock up ahead of Nov–Dec and May–June; push promotions in Aug–Sep to lift the slow months.
- Investigate the low ratings (about 6 in 10 are 3 stars or below), starting with Books.
- Grow Clothing, the strongest category, and keep targeting all age groups and both genders equally.
