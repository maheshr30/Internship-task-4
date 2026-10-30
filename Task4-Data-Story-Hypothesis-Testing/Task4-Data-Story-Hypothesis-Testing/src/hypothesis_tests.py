"""
Task 4 - Statistical Validation (hypothesis testing)
ApexPlanet Data Analytics Internship

Tests the key findings from Tasks 2 and 3 so that business conclusions rest on
evidence, not on eyeballing charts. Six tests are run and p-values are adjusted
for multiple testing (Holm method).

Run from the repository root:
    python src/hypothesis_tests.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
FIG, REP = ROOT / "figures", ROOT / "reports"
FIG.mkdir(exist_ok=True)
REP.mkdir(exist_ok=True)
ALPHA = 0.05
sns.set_theme(style="whitegrid", font_scale=0.95)

df = pd.read_csv(ROOT / "data" / "cleaned_sales_dataset.csv", parse_dates=["Order_Date"])
df["Half"] = np.where(df["Order_Date"] >= "2025-07-01", "H2", "H1")
results = []


def welch(a, b):
    """Welch t-test, 95% CI for mean(a) - mean(b), Cohen's d, Mann-Whitney p."""
    t, p = stats.ttest_ind(a, b, equal_var=False)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = np.sqrt(va + vb)
    dof = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    diff = a.mean() - b.mean()
    half = stats.t.ppf(0.975, dof) * se
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    mw_p = stats.mannwhitneyu(a, b, alternative="two-sided").pvalue
    return diff, diff - half, diff + half, diff / pooled, p, mw_p


# ---- T1: did the product mix change between H1 and H2? (chi-square, 6 x 2 table)
ct = pd.crosstab(df["Product"], df["Half"])
chi2, p1, dof1, _ = stats.chi2_contingency(ct)
cramers_v = np.sqrt(chi2 / ct.values.sum())
results.append(dict(id="T1", hypothesis="Product mix of orders changed between H1 and H2 2025",
                    test="Chi-square test of independence (product x half)", statistic=f"chi2={chi2:.2f}, df={dof1}",
                    effect=f"Cramer's V={cramers_v:.3f}", ci="", p=p1))

# ---- T2: Mobile share of orders fell from H1 to H2 (two-proportion z-test)
n1, n2 = (df["Half"] == "H1").sum(), (df["Half"] == "H2").sum()
x1 = ((df["Half"] == "H1") & (df["Product"] == "Mobile")).sum()
x2 = ((df["Half"] == "H2") & (df["Product"] == "Mobile")).sum()
p_h1, p_h2 = x1 / n1, x2 / n2
pool = (x1 + x2) / (n1 + n2)
z = (p_h1 - p_h2) / np.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
p2 = 2 * (1 - stats.norm.cdf(abs(z)))
se = np.sqrt(p_h1 * (1 - p_h1) / n1 + p_h2 * (1 - p_h2) / n2)
d = p_h1 - p_h2
results.append(dict(id="T2", hypothesis="Mobile's share of orders fell from H1 to H2",
                    test="Two-proportion z-test", statistic=f"z={z:.2f}",
                    effect=f"{p_h1:.1%} -> {p_h2:.1%} ({x1} -> {x2} orders)",
                    ci=f"drop of {d * 100:.1f} pts (95% CI {100 * (d - 1.96 * se):.1f} to {100 * (d + 1.96 * se):.1f})", p=p2))

# ---- T3-T5: order value comparisons (Welch t-test; Mann-Whitney as a robustness check)
groups = [
    ("T3", "Q3 orders are smaller than orders in other quarters",
     df.loc[df["Order_Quarter"] == "Q3", "Total_Sales"], df.loc[df["Order_Quarter"] != "Q3", "Total_Sales"], "Q3", "other quarters"),
    ("T4", "Weekend orders differ in value from weekday orders",
     df.loc[df["Is_Weekend"], "Total_Sales"], df.loc[~df["Is_Weekend"], "Total_Sales"], "weekend", "weekday"),
    ("T5", "Male and female order values differ",
     df.loc[df["Gender"] == "Male", "Total_Sales"], df.loc[df["Gender"] == "Female", "Total_Sales"], "male", "female"),
]
means = {}
for tid, hyp, a, b, la, lb in groups:
    diff, lo, hi, dcoh, p, mw = welch(a, b)
    means[tid] = (la, lb, a, b)
    results.append(dict(id=tid, hypothesis=hyp, test="Welch two-sample t-test",
                        statistic=f"mean {la} {a.mean():,.0f} vs {lb} {b.mean():,.0f}",
                        effect=f"Cohen's d={dcoh:.2f}; Mann-Whitney p={mw:.3f}",
                        ci=f"difference {diff:,.0f} (95% CI {lo:,.0f} to {hi:,.0f})", p=p))

# ---- T6: age is related to order value (Pearson)
r, p6 = stats.pearsonr(df["Age"], df["Total_Sales"])
rho, _ = stats.spearmanr(df["Age"], df["Total_Sales"])
results.append(dict(id="T6", hypothesis="Customer age is related to order value",
                    test="Pearson correlation", statistic=f"r={r:.3f}", effect=f"Spearman rho={rho:.3f}", ci="", p=p6))

# ---- Holm adjustment across the six tests
res = pd.DataFrame(results)
order = res["p"].argsort().values
m = len(res)
adj = np.empty(m)
running = 0.0
for rank, i in enumerate(order):
    running = max(running, (m - rank) * res.loc[i, "p"])
    adj[i] = min(running, 1.0)
res["p_adjusted_holm"] = adj
res["significant_at_5pct"] = res["p_adjusted_holm"] < ALPHA
res["p_raw"] = res["p"].round(4)
res["p_adjusted_holm"] = res["p_adjusted_holm"].round(4)
res = res.drop(columns="p")
res.to_csv(REP / "hypothesis_test_results.csv", index=False)
print(res.to_string(index=False))

# ---- Figures
share = pd.crosstab(df["Product"], df["Half"], normalize="columns") * 100
share = share.loc[share["H2"].sort_values().index]
fig, ax = plt.subplots(figsize=(7.5, 4))
y = np.arange(len(share))
ax.barh(y - 0.2, share["H1"], 0.4, label="H1 (Jan-Jun)", color="#9db8d3")
ax.barh(y + 0.2, share["H2"], 0.4, label="H2 (Jul-Jan 1)", color="#0f4c5c")
ax.set_yticks(y); ax.set_yticklabels(share.index); ax.set_xlabel("% of orders in the half-year")
ax.set_title("Share of orders by product: Mobile drops most"); ax.legend()
plt.tight_layout(); plt.savefig(FIG / "fig01_product_share_h1_h2.png", dpi=140); plt.close()

fig, ax = plt.subplots(figsize=(7.5, 3.8))
labels, ms, errs = [], [], []
for tid in ["T3", "T4", "T5"]:
    la, lb, a, b = means[tid]
    for lab, s in [(la, a), (lb, b)]:
        labels.append(lab); ms.append(s.mean() / 1e3); errs.append(1.96 * s.std(ddof=1) / np.sqrt(len(s)) / 1e3)
cols = ["#0f4c5c", "#9db8d3"] * 3
ax.bar(range(6), ms, yerr=errs, color=cols, capsize=4)
ax.set_xticks(range(6)); ax.set_xticklabels(labels, rotation=20)
ax.set_ylabel("Average order value (K)"); ax.set_title("Average order value with 95% confidence intervals")
plt.tight_layout(); plt.savefig(FIG / "fig02_aov_confidence_intervals.png", dpi=140); plt.close()
print("Done.")
