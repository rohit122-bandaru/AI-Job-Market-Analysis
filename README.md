# AI and the Future of Employment: Analyzing the Impact of Artificial Intelligence on the Job Market

## Project Overview

This project analyzes patterns in the job market related to Artificial
Intelligence (AI). The analysis focuses on how AI adoption is
represented across industries and how it is associated with automation
risk, salary, required skills, remote-work characteristics, and
projected job growth.

The project follows this analytical flow:

**AI Adoption → Automation Risk → Salary & Job Characteristics →
Required Skills → Future Job Growth**

The project is developed as an **Exploratory Data Analysis (EDA)**
project using Python. It focuses on descriptive and comparative analysis
rather than building a complex machine-learning prediction system.

> **Important:** The dataset is observational. The findings describe
> patterns and associations within the supplied records and should not
> be interpreted as proof of cause-and-effect relationships.

------------------------------------------------------------------------

## Dataset

**Dataset file:** `ai_job_market_insights.csv`

The dataset is included in this project repository. It contains
job-market records with information about:

-   Job Title
-   Industry
-   Company Size
-   Location
-   AI Adoption Level
-   Automation Risk
-   Required Skills
-   Salary (USD)
-   Remote-Friendly Status
-   Job Growth Projection

### Dataset Link

[Open the project dataset](ai_job_market_insights.csv)

------------------------------------------------------------------------

## Project Description

The objective of this project is to understand how different job-market
characteristics are distributed in a dataset containing AI-related
employment information.

The analysis covers:

1.  Job distribution across industries
2.  Average salary by industry
3.  Distribution of AI adoption levels
4.  Salary comparison across AI adoption levels
5.  Distribution of automation risk
6.  Automation-risk composition by industry
7.  Distribution of job-growth projections
8.  Job-growth composition across AI adoption levels
9.  Most frequently required skills
10. Salary distribution for remote-friendly and non-remote jobs

The analysis also performs additional comparisons involving job titles,
automation risk, required skills, remote work, and job-growth
projections.

------------------------------------------------------------------------

## Technologies Used

  Technology / Library   Purpose
  ---------------------- -----------------------------------------------
  Python                 Main programming and analysis language
  pandas                 Data loading, cleaning, grouping and analysis
  Matplotlib             Creating and exporting charts
  Seaborn                Statistical visualization and styling
  Streamlit              Interactive dashboard presentation
  Plotly                 Interactive dashboard charts
  CSV                    Source dataset format

------------------------------------------------------------------------

## Project Files

``` text
AI-Job-Market-Analysis/
│
├── ai_job_market_analysis.py
├── ai_job_market_insights.csv
├── app.py
├── requirements.txt
├── README.md
│
├── 01_jobs_by_industry.png
├── 02_avg_salary_by_industry.png
├── 03_ai_adoption_distribution.png
├── 04_ai_adoption_vs_salary.png
├── 05_automation_risk_distribution.png
├── 06_automation_risk_by_industry.png
├── 07_job_growth_distribution.png
├── 08_ai_adoption_vs_job_growth.png
├── 09_top_10_skills.png
└── 10_remote_vs_nonremote_salary.png
```

The `.venv` virtual-environment folder should **not** be uploaded to
GitHub.

------------------------------------------------------------------------

## Data Processing and Methodology

The project uses the following workflow:

### 1. Data Loading

The CSV dataset is loaded into a pandas DataFrame and checked for
loading errors and missing expected columns.

### 2. Data Understanding

The dataset dimensions, column names, data types, missing values,
duplicate records, unique categorical values, and numerical statistics
are examined.

### 3. Data Cleaning

The project:

-   Removes unnecessary leading and trailing whitespace.
-   Converts `Salary_USD` into numeric format.
-   Removes records with missing critical values.
-   Removes invalid non-positive salary values.
-   Removes duplicate records.
-   Resets the DataFrame index.

### 4. Exploratory Data Analysis

Frequency distributions, group-wise averages, and cross-tabulations are
used to identify patterns in the dataset.

### 5. AI Impact Analysis

AI adoption is compared with:

-   Salary
-   Automation risk
-   Job-growth projection

### 6. Skills Analysis

The frequency of required skills is calculated and the top 10 recorded
skills are visualized.

### 7. Visualization

Ten charts are generated to communicate the major findings clearly.

------------------------------------------------------------------------

## Key Analysis Areas

### Industry Analysis

The project compares the number of recorded jobs and average salary
across industries.

### AI Adoption Analysis

Jobs are grouped into **Low, Medium, and High** AI adoption categories
to examine their distribution and associated salary patterns.

### Automation Risk Analysis

The project examines **Low, Medium, and High** automation-risk
categories and compares their composition across industries.

### Job Growth Analysis

Job-growth projections are grouped into **Decline, Stable, and Growth**
and compared across AI adoption levels.

### Skills Analysis

The project identifies the most frequently recorded required skills,
including technical, analytical, business, and communication-related
skills.

### Remote Work Analysis

A boxplot is used to compare salary distributions between
remote-friendly and non-remote jobs, including their spread and
potential outliers.

------------------------------------------------------------------------

## How to Run the Project

### Step 1: Install Python

Install Python 3.x on your system.

### Step 2: Clone or Download the Repository

Place all project files in the same project folder.

### Step 3: Create a Virtual Environment (Recommended)

``` bash
python -m venv .venv
```

Activate it on Linux/macOS:

``` bash
source .venv/bin/activate
```

On Windows:

``` bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies

``` bash
pip install -r requirements.txt
```

### Step 5: Run the Python Analysis

``` bash
python ai_job_market_analysis.py
```

This generates the analysis output and the ten PNG visualizations.

### Step 6: Run the Interactive Dashboard

If `app.py` is included in the repository:

``` bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, normally:

``` text
http://localhost:8501
```

> Run the Streamlit dashboard with `streamlit run app.py`, not
> `python app.py`.

------------------------------------------------------------------------

## Key Outputs

The project produces ten visualizations:

1.  **Number of Jobs by Industry**
2.  **Average Salary by Industry**
3.  **Distribution of AI Adoption Levels**
4.  **Average Salary by AI Adoption Level**
5.  **Distribution of Automation Risk**
6.  **Automation Risk Composition by Industry**
7.  **Distribution of Job Growth Projections**
8.  **Job Growth Composition by AI Adoption Level**
9.  **Top 10 Most Frequently Required Skills**
10. **Salary Comparison: Remote-Friendly vs Non-Remote Jobs**

These visualizations support the interpretation of industry structure,
AI adoption, automation exposure, salary patterns, skill demand, remote
work, and projected job growth.

------------------------------------------------------------------------

## Key Findings

The analysis indicates that:

-   Jobs are represented across multiple industries, enabling
    cross-industry comparison.
-   Average salary differs across industries in the supplied dataset.
-   Low, Medium, and High AI adoption categories are all represented.
-   Salary levels vary across AI adoption categories.
-   Automation risk is distributed across Low, Medium, and High
    categories.
-   Automation-risk composition differs between industries.
-   Decline, Stable, and Growth job projections are all represented.
-   Job-growth composition varies across AI adoption categories.
-   Python is prominent among the frequently recorded required skills.
-   The dataset contains a mixture of technical, analytical, business,
    design, and communication skills.
-   Remote-friendly and non-remote jobs show different salary
    distributions with visible variation and outliers.

These findings describe the supplied dataset and should not be treated
as universal labor-market conclusions.

------------------------------------------------------------------------

## Learning Outcomes

Through this project, I learned how to:

-   Load and validate a CSV dataset using pandas.
-   Clean and prepare data for analysis.
-   Handle missing and invalid values.
-   Remove duplicate records.
-   Use `groupby()`, `value_counts()`, and `crosstab()`.
-   Calculate descriptive statistics.
-   Select suitable visualizations for different analytical questions.
-   Interpret categorical and numerical variables.
-   Compare distributions using boxplots.
-   Present analytical findings in a structured project report.
-   Understand the difference between association and causation.
-   Organize a Python data-analysis project into reusable sections.

------------------------------------------------------------------------

## Challenges Faced

Some of the challenges during the project included:

-   Understanding and validating the dataset structure.
-   Handling missing or invalid data values.
-   Selecting appropriate charts for different types of analysis.
-   Comparing categorical variables using cross-tabulations.
-   Presenting multiple findings without making the report unnecessarily
    complex.
-   Interpreting AI-related patterns without making unsupported causal
    claims.
-   Organizing the analysis, visualizations, report, requirements, and
    dashboard into a submission-ready project.

------------------------------------------------------------------------

## Limitations

This project has several limitations:

-   The dataset is observational.
-   The analysis does not prove causal relationships.
-   The dataset represents a limited set of job records.
-   Job-growth categories are projections contained in the dataset and
    are not independently verified forecasts.
-   Salary values are recorded in USD and may not represent every
    geographic labor market.
-   The project does not attempt to predict actual future employment
    numbers.

------------------------------------------------------------------------

## Future Scope

The project can be extended by:

-   Adding a larger and more recent job-posting dataset.
-   Including historical job-posting dates for time-series analysis.
-   Adding education and experience-level variables.
-   Comparing multiple geographic markets.
-   Tracking changes in skill demand over time.
-   Adding statistical significance and association testing.
-   Improving the Streamlit dashboard with additional filters and
    interactive charts.
-   Building machine-learning models when a clearly defined prediction
    task and suitable dataset are available.

------------------------------------------------------------------------

## Internship Context

**Program:** IBM SkillsBuild Data Analytics with AI Internship 2026\
**Conducted by:** BharatCares in association with AICTE\
**Project Type:** Data Analytics / Exploratory Data Analysis\
**Student:** Abhishek Negi

------------------------------------------------------------------------

## Conclusion

This project demonstrates a complete Python-based exploratory data
analytics workflow for examining AI-related job-market patterns. It
combines data validation, cleaning, descriptive analysis,
cross-tabulation, visualization, interpretation, and documentation.

The project provides a structured view of how AI adoption, automation
risk, salary, required skills, remote work, and job-growth projections
appear together in the supplied dataset.

The results are intended to support analytical understanding of the
dataset rather than provide guaranteed predictions about the future of
employment.
