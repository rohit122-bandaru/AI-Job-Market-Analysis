"""
==================================================================
PROJECT TITLE:
AI and the Future of Employment: Analyzing the Impact of
Artificial Intelligence on the Job Market
==================================================================

PROJECT OBJECTIVE:
To study how Artificial Intelligence is influencing the job market
by analyzing AI adoption across industries, automation risk of
different job roles, salary patterns, in-demand skills, and future
job growth projections. The project follows the analytical flow:

    AI Adoption -> Automation Risk -> Salary & Job Characteristics
                -> Required Skills -> Future Job Growth

Note: This is an OBSERVATIONAL dataset. All findings describe
associations / patterns in the data, NOT proven cause-and-effect
relationships.

DATASET: ai_job_market_insights.csv

Submitted for: IBM SkillsBuild Data Analytics with AI Internship 2026
==================================================================
"""

# ==================================================================
# IMPORT LIBRARIES
# ==================================================================
import os
import sys
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Consistent, professional visualization style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelsize"] = 11

PRIMARY_PALETTE = "viridis"


def section(title):
    """Print a clear, consistent section header to the console."""
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)


# ==================================================================
# LOAD DATA
# ==================================================================
section("1. DATA LOADING")

file_path = "ai_job_market_insights.csv"

try:
    df = pd.read_csv(file_path)
    print(f"Dataset successfully loaded from '{file_path}'.")
except FileNotFoundError:
    print(f"ERROR: The file '{file_path}' was not found.")
    print("Please make sure the CSV file is in the same folder as this script.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    print(f"ERROR: The file '{file_path}' is empty.")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Could not load the dataset. Details: {e}")
    sys.exit(1)

if df.empty:
    print("ERROR: The dataset contains no records. Exiting.")
    sys.exit(1)

# Verify that all expected columns are present
expected_columns = [
    "Job_Title", "Industry", "Company_Size", "Location",
    "AI_Adoption_Level", "Automation_Risk", "Required_Skills",
    "Salary_USD", "Remote_Friendly", "Job_Growth_Projection"
]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"ERROR: The dataset is missing expected columns: {missing_columns}")
    sys.exit(1)

print("All expected columns are present.")


# ==================================================================
# DATA UNDERSTANDING
# ==================================================================
section("2. DATA UNDERSTANDING")

print(f"Dataset Dimensions      : {df.shape}")
print(f"Number of Records       : {df.shape[0]}")
print(f"Number of Columns       : {df.shape[1]}")
print(f"\nColumn Names:\n{list(df.columns)}")

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values per Column:")
print(df.isnull().sum())

print(f"\nDuplicate Records: {df.duplicated().sum()}")

print("\nBasic Statistical Summary (Numeric Columns):")
print(df.describe())

categorical_cols = ["Industry", "Company_Size", "AI_Adoption_Level",
                     "Automation_Risk", "Remote_Friendly",
                     "Job_Growth_Projection", "Job_Title"]

print("\nUnique Values in Key Categorical Columns:")
for col in categorical_cols:
    print(f"\n{col} ({df[col].nunique()} unique values):")
    print(sorted(df[col].dropna().unique()))


# ==================================================================
# DATA CLEANING
# ==================================================================
section("3. DATA CLEANING")

initial_rows = df.shape[0]

# Remove leading/trailing whitespace from text columns
text_columns = df.select_dtypes(include="object").columns
for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# Ensure Salary_USD is numeric; invalid entries become NaN
df["Salary_USD"] = pd.to_numeric(df["Salary_USD"], errors="coerce")

# Drop rows with missing values in critical columns
before_na_drop = df.shape[0]
df = df.dropna(subset=expected_columns)
print(f"Rows removed due to missing/invalid values: {before_na_drop - df.shape[0]}")

# Remove invalid (zero or negative) salaries, if any
before_salary_filter = df.shape[0]
df = df[df["Salary_USD"] > 0]
print(f"Rows removed due to invalid Salary_USD (<= 0): {before_salary_filter - df.shape[0]}")

# Remove duplicate rows
before_dedup = df.shape[0]
df = df.drop_duplicates()
print(f"Duplicate rows removed: {before_dedup - df.shape[0]}")

df = df.reset_index(drop=True)

print(f"\nTotal rows before cleaning : {initial_rows}")
print(f"Total rows after cleaning  : {df.shape[0]}")
print("Data cleaning complete. Dataset is ready for analysis.")


# ==================================================================
# EXPLORATORY DATA ANALYSIS
# ==================================================================
section("4. EXPLORATORY DATA ANALYSIS")

# ---- A. Industry ----
print("\n--- Jobs by Industry ---")
jobs_by_industry = df["Industry"].value_counts()
print(jobs_by_industry)

print("\n--- Average Salary by Industry ---")
salary_by_industry = df.groupby("Industry")["Salary_USD"].mean().sort_values(ascending=False)
print(salary_by_industry.round(2))

print("\n--- AI Adoption Level Counts by Industry ---")
ai_by_industry = pd.crosstab(df["Industry"], df["AI_Adoption_Level"])
print(ai_by_industry)

print("\n--- Automation Risk by Industry ---")
risk_by_industry = pd.crosstab(df["Industry"], df["Automation_Risk"])
print(risk_by_industry)

print("\n--- Job Growth Projection by Industry ---")
growth_by_industry = pd.crosstab(df["Industry"], df["Job_Growth_Projection"])
print(growth_by_industry)

# ---- B. Job Titles ----
print("\n--- Most Common Job Titles ---")
job_title_counts = df["Job_Title"].value_counts()
print(job_title_counts)

print("\n--- Average Salary by Job Title ---")
salary_by_title = df.groupby("Job_Title")["Salary_USD"].mean().sort_values(ascending=False)
print(salary_by_title.round(2))

print("\n--- Automation Risk by Job Title ---")
print(pd.crosstab(df["Job_Title"], df["Automation_Risk"]))

print("\n--- Job Growth Projection by Job Title ---")
print(pd.crosstab(df["Job_Title"], df["Job_Growth_Projection"]))

# ---- C. AI Adoption relationships ----
print("\n--- Average Salary by AI Adoption Level ---")
salary_by_ai = df.groupby("AI_Adoption_Level")["Salary_USD"].mean().round(2)
print(salary_by_ai)

print("\n--- Automation Risk Counts by AI Adoption Level ---")
print(pd.crosstab(df["AI_Adoption_Level"], df["Automation_Risk"]))

print("\n--- Job Growth Counts by AI Adoption Level ---")
print(pd.crosstab(df["AI_Adoption_Level"], df["Job_Growth_Projection"]))

# ---- D. Automation Risk ----
print("\n--- Automation Risk Distribution ---")
automation_risk_counts = df["Automation_Risk"].value_counts()
print(automation_risk_counts)

print("\n--- Job Growth vs Automation Risk ---")
print(pd.crosstab(df["Automation_Risk"], df["Job_Growth_Projection"]))

# ---- E. Salary ----
print("\n--- Overall Salary Statistics ---")
print(f"Average Salary : ${df['Salary_USD'].mean():,.2f}")
print(f"Median Salary  : ${df['Salary_USD'].median():,.2f}")
print(f"Minimum Salary : ${df['Salary_USD'].min():,.2f}")
print(f"Maximum Salary : ${df['Salary_USD'].max():,.2f}")

print("\n--- Average Salary by Automation Risk ---")
salary_by_risk = df.groupby("Automation_Risk")["Salary_USD"].mean().round(2)
print(salary_by_risk)

print("\n--- Average Salary by Remote-Friendly Status ---")
salary_by_remote = df.groupby("Remote_Friendly")["Salary_USD"].mean().round(2)
print(salary_by_remote)

# ---- F. Remote Work ----
print("\n--- Remote-Friendly Job Percentage ---")
remote_pct = (df["Remote_Friendly"].value_counts(normalize=True) * 100).round(2)
print(remote_pct)

print("\n--- Remote-Friendly Jobs by Industry ---")
print(pd.crosstab(df["Industry"], df["Remote_Friendly"]))

# ---- G. Job Growth ----
print("\n--- Job Growth Projection Distribution ---")
growth_counts = df["Job_Growth_Projection"].value_counts()
print(growth_counts)


# ==================================================================
# SKILLS ANALYSIS
# ==================================================================
section("5. REQUIRED SKILLS ANALYSIS")

# Each record lists one primary required skill for the role.
# We count frequency directly (no delimiter splitting needed,
# since the column does not contain multi-skill strings).
skill_counts = Counter(df["Required_Skills"])
top_skills = pd.Series(skill_counts).sort_values(ascending=False)

print("\n--- Frequency of Each Required Skill ---")
print(top_skills)

print("\n--- Top 10 Required Skills ---")
top_10_skills = top_skills.head(10)
print(top_10_skills)

print("\n--- Required Skills by Industry (counts) ---")
print(pd.crosstab(df["Industry"], df["Required_Skills"]))

print("\n--- Average Salary by Required Skill ---")
salary_by_skill = df.groupby("Required_Skills")["Salary_USD"].mean().sort_values(ascending=False).round(2)
print(salary_by_skill)

most_frequent_skill = top_skills.idxmax()
highest_paid_skill = salary_by_skill.idxmax()
print(f"\nMost frequently required skill : {most_frequent_skill}")
print(f"Highest average-paying skill    : {highest_paid_skill}")


# ==================================================================
# AI IMPACT ANALYSIS (CORE SECTION)
# ==================================================================
section("6. AI IMPACT ANALYSIS")

print("This section explores how AI adoption relates to automation")
print("risk, salary, and job growth. All results describe patterns")
print("in the data ('associations'), not proven causation.\n")

print("--- Average Salary Across AI Adoption Levels ---")
print(salary_by_ai)

print("\n--- Automation Risk Composition (%) by AI Adoption Level ---")
ai_risk_pct = pd.crosstab(df["AI_Adoption_Level"], df["Automation_Risk"], normalize="index") * 100
print(ai_risk_pct.round(2))

print("\n--- Job Growth Composition (%) by AI Adoption Level ---")
ai_growth_pct = pd.crosstab(df["AI_Adoption_Level"], df["Job_Growth_Projection"], normalize="index") * 100
print(ai_growth_pct.round(2))

print("\n--- Industry with Highest Share of 'High' AI Adoption ---")
high_ai_share = pd.crosstab(df["Industry"], df["AI_Adoption_Level"], normalize="index")["High"].sort_values(ascending=False) * 100
print(high_ai_share.round(2))
industry_highest_ai = high_ai_share.idxmax()

print("\n--- Job Title with Highest Share of 'High' Automation Risk ---")
high_risk_share = pd.crosstab(df["Job_Title"], df["Automation_Risk"], normalize="index")["High"].sort_values(ascending=False) * 100
print(high_risk_share.round(2))
job_highest_risk = high_risk_share.idxmax()

print("\n--- Job Title with Highest Share of 'Growth' Projection ---")
high_growth_share = pd.crosstab(df["Job_Title"], df["Job_Growth_Projection"], normalize="index")["Growth"].sort_values(ascending=False) * 100
print(high_growth_share.round(2))
job_highest_growth = high_growth_share.idxmax()


# ==================================================================
# VISUALIZATIONS
# ==================================================================
section("7. VISUALIZATIONS")
print("Generating charts... a window/plot will be produced for each visualization.")

# 1. Job distribution by industry
plt.figure()
jobs_by_industry.sort_values().plot(kind="barh", color=sns.color_palette(PRIMARY_PALETTE, len(jobs_by_industry)))
plt.title("Number of Jobs by Industry")
plt.xlabel("Number of Jobs")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig("01_jobs_by_industry.png", dpi=150)
plt.close()

# 2. Average salary by industry
plt.figure()
salary_by_industry.sort_values().plot(kind="barh", color=sns.color_palette(PRIMARY_PALETTE, len(salary_by_industry)))
plt.title("Average Salary by Industry")
plt.xlabel("Average Salary (USD)")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig("02_avg_salary_by_industry.png", dpi=150)
plt.close()

# 3. AI adoption level distribution
plt.figure()
df["AI_Adoption_Level"].value_counts().reindex(["Low", "Medium", "High"]).plot(
    kind="bar", color=sns.color_palette(PRIMARY_PALETTE, 3))
plt.title("Distribution of AI Adoption Levels")
plt.xlabel("AI Adoption Level")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("03_ai_adoption_distribution.png", dpi=150)
plt.close()

# 4. AI adoption vs average salary
plt.figure()
salary_by_ai.reindex(["Low", "Medium", "High"]).plot(
    kind="bar", color=sns.color_palette(PRIMARY_PALETTE, 3))
plt.title("Average Salary by AI Adoption Level")
plt.xlabel("AI Adoption Level")
plt.ylabel("Average Salary (USD)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("04_ai_adoption_vs_salary.png", dpi=150)
plt.close()

# 5. Automation risk distribution
plt.figure()
automation_risk_counts.reindex(["Low", "Medium", "High"]).plot(
    kind="bar", color=sns.color_palette("magma", 3))
plt.title("Distribution of Automation Risk")
plt.xlabel("Automation Risk")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("05_automation_risk_distribution.png", dpi=150)
plt.close()

# 6. Automation risk by industry (stacked)
plt.figure()
risk_pct_industry = pd.crosstab(df["Industry"], df["Automation_Risk"], normalize="index") * 100
risk_pct_industry = risk_pct_industry[["Low", "Medium", "High"]]
risk_pct_industry.plot(kind="bar", stacked=True, color=sns.color_palette("magma", 3))
plt.title("Automation Risk Composition by Industry")
plt.xlabel("Industry")
plt.ylabel("Percentage of Jobs (%)")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Automation Risk")
plt.tight_layout()
plt.savefig("06_automation_risk_by_industry.png", dpi=150)
plt.close()

# 7. Job growth projection distribution
plt.figure()
growth_counts.reindex(["Decline", "Stable", "Growth"]).plot(
    kind="bar", color=sns.color_palette("crest", 3))
plt.title("Distribution of Job Growth Projections")
plt.xlabel("Job Growth Projection")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("07_job_growth_distribution.png", dpi=150)
plt.close()

# 8. AI adoption vs job growth (stacked)
plt.figure()
growth_pct_ai = ai_growth_pct[["Decline", "Stable", "Growth"]].reindex(["Low", "Medium", "High"])
growth_pct_ai.plot(kind="bar", stacked=True, color=sns.color_palette("crest", 3))
plt.title("Job Growth Composition by AI Adoption Level")
plt.xlabel("AI Adoption Level")
plt.ylabel("Percentage of Jobs (%)")
plt.xticks(rotation=0)
plt.legend(title="Job Growth")
plt.tight_layout()
plt.savefig("08_ai_adoption_vs_job_growth.png", dpi=150)
plt.close()

# 9. Top 10 required skills
plt.figure()
top_10_skills.sort_values().plot(kind="barh", color=sns.color_palette(PRIMARY_PALETTE, len(top_10_skills)))
plt.title("Top 10 Most Frequently Required Skills")
plt.xlabel("Number of Job Postings")
plt.ylabel("Skill")
plt.tight_layout()
plt.savefig("09_top_10_skills.png", dpi=150)
plt.close()

# 10. Remote-friendly vs non-remote salary comparison
plt.figure()
sns.boxplot(data=df, x="Remote_Friendly", y="Salary_USD", palette=PRIMARY_PALETTE)
plt.title("Salary Comparison: Remote-Friendly vs Non-Remote Jobs")
plt.xlabel("Remote-Friendly")
plt.ylabel("Salary (USD)")
plt.tight_layout()
plt.savefig("10_remote_vs_nonremote_salary.png", dpi=150)
plt.close()

print("All 10 visualizations have been saved as PNG files in the current folder.")


# ==================================================================
# KEY INSIGHTS
# ==================================================================
section("KEY INSIGHTS")

average_salary = df["Salary_USD"].mean()
highest_paying_industry = salary_by_industry.idxmax()
most_common_ai_level = df["AI_Adoption_Level"].mode()[0]
industry_highest_ai_adoption = industry_highest_ai
most_common_automation_risk = df["Automation_Risk"].mode()[0]
industry_highest_automation_risk = pd.crosstab(
    df["Industry"], df["Automation_Risk"], normalize="index"
)["High"].idxmax()
most_common_growth_projection = df["Job_Growth_Projection"].mode()[0]
most_frequent_required_skill = most_frequent_skill
remote_friendly_percentage = (df["Remote_Friendly"] == "Yes").mean() * 100

print(f"Average Salary:\n${average_salary:,.2f}\n")
print(f"Highest Paying Industry:\n{highest_paying_industry}\n")
print(f"Most Common AI Adoption Level:\n{most_common_ai_level}\n")
print(f"Industry With Highest AI Adoption:\n{industry_highest_ai_adoption}\n")
print(f"Most Common Automation Risk:\n{most_common_automation_risk}\n")
print(f"Industry With Highest Automation Risk:\n{industry_highest_automation_risk}\n")
print(f"Most Common Job Growth Projection:\n{most_common_growth_projection}\n")
print(f"Most Frequently Required Skill:\n{most_frequent_required_skill}\n")
print(f"Remote-Friendly Jobs:\n{remote_friendly_percentage:.2f}%\n")
print(f"Job Title With Highest Automation Risk Share:\n{job_highest_risk}\n")
print(f"Job Title With Highest Growth Projection Share:\n{job_highest_growth}\n")


# ==================================================================
# FINAL CONCLUSION
# ==================================================================
section("FINAL AI JOB MARKET CONCLUSION")

conclusion = f"""
Based on the analysis of this dataset, the job market shows several
patterns associated with the growing presence of Artificial
Intelligence:

1. AI ADOPTION: AI adoption levels across recorded jobs are led by
   the '{most_common_ai_level}' category overall, and the
   '{industry_highest_ai_adoption}' industry shows the largest share
   of jobs with High AI adoption in this dataset.

2. AUTOMATION RISK: The most common automation risk level recorded
   is '{most_common_automation_risk}'. The '{industry_highest_automation_risk}'
   industry shows the highest share of High automation-risk roles,
   and the '{job_highest_risk}' role shows the highest share of
   High automation risk among job titles. Across AI adoption levels,
   automation risk composition differs (see the AI Impact Analysis
   section), suggesting automation risk is not evenly spread but
   appears to vary with how heavily AI has been adopted.

3. SALARY PATTERNS: The average salary across all recorded jobs is
   ${average_salary:,.2f}, with the '{highest_paying_industry}'
   industry showing the highest average salary. Salary also appears
   to vary across AI adoption levels and automation risk categories,
   indicating that pay is associated with multiple job
   characteristics rather than AI adoption alone.

4. FUTURE JOB GROWTH: The most common job growth projection in the
   dataset is '{most_common_growth_projection}', and the
   '{job_highest_growth}' role shows the strongest share of jobs
   projected to grow. Growth projections also differ across AI
   adoption levels, suggesting that higher AI adoption is not
   uniformly linked to either growth or decline in this dataset.

5. REQUIRED SKILLS: The most frequently required skill recorded is
   '{most_frequent_required_skill}'. Skill demand appears to differ
   across industries, indicating a shifting skill landscape as
   different sectors adopt AI at different rates.

6. REMOTE WORK: {remote_friendly_percentage:.2f}% of jobs in the
   dataset are remote-friendly. Salary levels between remote and
   non-remote roles also show a difference, which may reflect
   broader shifts in how work is structured.

OVERALL: The dataset suggests that AI adoption, automation risk,
salary, required skills, and job growth are interconnected in
varying ways across industries and roles. However, since this is
observational data, these findings represent associations and
patterns rather than confirmed cause-and-effect relationships.
Employees and organizations should use these patterns to inform
proactive upskilling (particularly in skills like
'{most_frequent_required_skill}') and workforce planning, rather
than treating them as guaranteed future outcomes.
"""

print(conclusion)

section("PROJECT COMPLETE")
print("Analysis finished successfully. All insights above are")
print("calculated directly from the provided dataset.")
