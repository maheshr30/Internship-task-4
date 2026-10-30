# Data Story: What Really Drives Our Revenue

**Task 4 - Data Storytelling | ApexPlanet Data Analytics Internship | Author: Mahesh R**
Audience: sales and marketing leadership. Slides: `../deck/Final_Presentation.pptx`.

## 1. Objective
Understand what drives revenue in 1,000 retail orders (139.4 M, 1 Jan 2025 to 1 Jan 2026) and decide where to focus promotions.

## 2. The analysis in three steps

**Step 1: The business is steady and led by large baskets (Tasks 1-2).**
Revenue runs at about 12 M a month. Order value depends equally on unit price (r = 0.69) and quantity (r = 0.65). The top 10% of orders bring in 27.6% of revenue.

**Step 2: Revenue comes from a type of order, not a type of person (Task 3).**
Orders with 6+ units at 25,000+ per unit ("Big spenders") are 24.7% of orders and **53.2% of revenue**. Small, low-priced orders ("Light buyers") are 25.1% of orders and **7.0%**. These segments look the same by age, gender, city and category (all p > 0.05).

**Step 3: We tested the "interesting" findings (Task 4).**
Charts hinted that Mobile was declining, that Q3 was weak, and that gender or weekday mattered. After statistical testing:

| Finding | Evidence | Confidence |
|---|---|---|
| Revenue concentrated in large orders | Descriptive, robust | **Established** |
| Age, gender, weekday do not explain order value | p = 0.28 to 0.97; effects tiny | **Established** (within data limits) |
| Mobile's share of orders fell (21.2% to 15.6%) | raw p = 0.021, adjusted p = 0.124 | **Suggestive, monitor** |
| Weak Q3 order values | p = 0.079 | **Not established** |

## 3. Conclusions
- Revenue is a **basket-size** story: quantity and price, not customer demographics or timing.
- Demographic targeting has no support in this data.
- Mobile deserves attention but not alarm.

## 4. Call to action
1. **Trigger promotions on basket contents:** multi-unit bundles on premium items to protect Big spenders (53% of revenue); multi-buy and trade-up offers to move Light buyers up.
2. **Drop age and gender targeting** for now; there is no evidence it would pay off.
3. **Monitor Mobile** and re-run the same test on the next two quarters of data, with the decision rule agreed in advance.
4. **Fix the data foundations:** unique order IDs, reliable customer IDs and product-specific pricing, so retention and lifetime-value analysis become possible.
