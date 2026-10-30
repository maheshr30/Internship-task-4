# Task 4 - Data Storytelling & Statistical Validation

ApexPlanet Software Pvt. Ltd. | Data Analytics Internship | Author: Mahesh R

## Objective
Turn the analysis from Tasks 1-3 into a business story for leadership, and check the key findings with hypothesis tests.

## Deliverables
| Requirement | Where |
|---|---|
| Final presentation deck (7 slides, with speaker notes) | [`deck/Final_Presentation.pptx`](deck/Final_Presentation.pptx) |
| Data story (objective, analysis, conclusions, call to action) | [`reports/Data_Story.md`](reports/Data_Story.md) |
| Hypothesis testing summary | [`reports/Hypothesis_Testing_Summary.md`](reports/Hypothesis_Testing_Summary.md), [`reports/hypothesis_test_results.csv`](reports/hypothesis_test_results.csv) |
| Test code | [`src/hypothesis_tests.py`](src/hypothesis_tests.py) |

## Headline
Revenue is a **basket-size story**: 24.7% of orders (6+ units at 25,000+ per unit) bring in 53.2% of revenue, and age, gender, city and weekday do not explain order value.

## Statistical validation
Six tests (chi-square, two-proportion z-test, Welch t-tests, Pearson correlation) with Holm-adjusted p-values. The closest result is Mobile's order-share drop (21.2% to 15.6%; raw p = 0.021, adjusted p = 0.124), so it is treated as a watch item, not a proven decline. The write-up explains why and what data would settle it.

## How to run
```bash
pip install -r requirements.txt
python src/hypothesis_tests.py
```
