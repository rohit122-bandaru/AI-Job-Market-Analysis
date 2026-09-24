"""
==================================================================
AI & THE FUTURE OF EMPLOYMENT
Analyzing the Impact of Artificial Intelligence on the Job Market
==================================================================

Streamlit dashboard companion to ai_job_market_analysis.py.

Run with:
    streamlit run app.py

Expects ai_job_market_insights.csv in the same folder.
==================================================================
"""

import os
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI & The Future of Employment",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

EXPECTED_COLUMNS = [
    "Job_Title", "Industry", "Company_Size", "Location",
    "AI_Adoption_Level", "Automation_Risk", "Required_Skills",
    "Salary_USD", "Remote_Friendly", "Job_Growth_Projection",
]

ORDER_LOW_MED_HIGH = ["Low", "Medium", "High"]
ORDER_GROWTH = ["Decline", "Stable", "Growth"]

CHART_TEMPLATE = "plotly_white"
COLOR_SEQ = px.colors.sequential.Viridis
COLOR_SEQ_DISCRETE = px.colors.qualitative.Set2


# ------------------------------------------------------------------
# DATA LOADING (cached, with error handling)
# ------------------------------------------------------------------
@st.cache_data
def load_data(path: str):
    if not os.path.exists(path):
        return None, f"File not found: '{path}'. Make sure the CSV is in the same folder as app.py."

    try:
        data = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return None, f"The file '{path}' is empty."
    except Exception as e:
        return None, f"Could not read '{path}'. Details: {e}"

    if data.empty:
        return None, "The dataset contains no records."

    missing_cols = [c for c in EXPECTED_COLUMNS if c not in data.columns]
    if missing_cols:
        return None, f"The dataset is missing expected columns: {missing_cols}"

    # --- Cleaning (mirrors ai_job_market_analysis.py) ---
    text_cols = data.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        data[col] = data[col].astype(str).str.strip()

    data["Salary_USD"] = pd.to_numeric(data["Salary_USD"], errors="coerce")
    data = data.dropna(subset=EXPECTED_COLUMNS)
    data = data[data["Salary_USD"] > 0]
    data = data.drop_duplicates().reset_index(drop=True)

    if data.empty:
        return None, "No valid records remained after cleaning the dataset."

    return data, None


df_raw, load_error = load_data("ai_job_market_insights.csv")

if load_error:
    st.error(f"⚠️ {load_error}")
    st.stop()


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.title("🤖 AI & The Future of Employment")
st.subheader("Analyzing the Impact of Artificial Intelligence on the Job Market")
st.caption(
    "This dashboard explores an observational dataset. All findings describe "
    "**associations and patterns**, not proven cause-and-effect relationships."
)
st.divider()


# ------------------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------------------
st.sidebar.header("🔎 Filters")


def make_filter(label, series):
    options = ["All"] + sorted(series.dropna().unique().tolist())
    return st.sidebar.selectbox(label, options)


industry_f = make_filter("Industry", df_raw["Industry"])
job_title_f = make_filter("Job Title", df_raw["Job_Title"])
location_f = make_filter("Location", df_raw["Location"])
ai_level_f = st.sidebar.selectbox("AI Adoption Level", ["All"] + ORDER_LOW_MED_HIGH)
risk_f = st.sidebar.selectbox("Automation Risk", ["All"] + ORDER_LOW_MED_HIGH)
growth_f = st.sidebar.selectbox("Job Growth Projection", ["All"] + ORDER_GROWTH)
remote_f = st.sidebar.selectbox("Remote-Friendly", ["All", "Yes", "No"])

df = df_raw.copy()
if industry_f != "All":
    df = df[df["Industry"] == industry_f]
if job_title_f != "All":
    df = df[df["Job_Title"] == job_title_f]
if location_f != "All":
    df = df[df["Location"] == location_f]
if ai_level_f != "All":
    df = df[df["AI_Adoption_Level"] == ai_level_f]
if risk_f != "All":
    df = df[df["Automation_Risk"] == risk_f]
if growth_f != "All":
    df = df[df["Job_Growth_Projection"] == growth_f]
if remote_f != "All":
    df = df[df["Remote_Friendly"] == remote_f]

st.sidebar.markdown(f"**Records after filtering:** {df.shape[0]} / {df_raw.shape[0]}")

if df.empty:
    st.warning("No records match the selected filters. Please adjust your filters.")
    st.stop()


# ------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------
def order_index(series_or_df, order):
    """Reindex to a preferred category order, keeping only present categories."""
    present = [o for o in order if o in series_or_df.index]
    return series_or_df.reindex(present)


def safe_mode(series):
    m = series.mode()
    return m.iloc[0] if not m.empty else "N/A"


# ------------------------------------------------------------------
# TOP KPI CARDS
# ------------------------------------------------------------------
st.markdown("## 📊 Key Performance Indicators")

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Jobs", f"{df.shape[0]:,}")
k2.metric("Average Salary", f"${df['Salary_USD'].mean():,.0f}")
k3.metric("Median Salary", f"${df['Salary_USD'].median():,.0f}")
k4.metric("Remote-Friendly Jobs", f"{(df['Remote_Friendly'] == 'Yes').mean() * 100:.1f}%")
k5.metric("Most Common AI Adoption", safe_mode(df["AI_Adoption_Level"]))
k6.metric("Most Common Growth Outlook", safe_mode(df["Job_Growth_Projection"]))

st.divider()


# ------------------------------------------------------------------
# SECTION 1 — JOB MARKET OVERVIEW
# ------------------------------------------------------------------
st.markdown("## 1️⃣ Job Market Overview")

col1, col2 = st.columns(2)

with col1:
    jobs_by_industry = df["Industry"].value_counts().sort_values()
    fig1 = px.bar(
        jobs_by_industry, x=jobs_by_industry.values, y=jobs_by_industry.index,
        orientation="h", template=CHART_TEMPLATE, color=jobs_by_industry.values,
        color_continuous_scale=COLOR_SEQ,
        labels={"x": "Number of Jobs", "y": "Industry"},
        title="Jobs by Industry",
    )
    fig1.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True, key="chart_1")

with col2:
    salary_by_industry = df.groupby("Industry")["Salary_USD"].mean().sort_values()
    fig2 = px.bar(
        salary_by_industry, x=salary_by_industry.values, y=salary_by_industry.index,
        orientation="h", template=CHART_TEMPLATE, color=salary_by_industry.values,
        color_continuous_scale=COLOR_SEQ,
        labels={"x": "Average Salary (USD)", "y": "Industry"},
        title="Average Salary by Industry",
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True, key="chart_2")

growth_dist = order_index(df["Job_Growth_Projection"].value_counts(), ORDER_GROWTH)
fig3 = px.pie(
    values=growth_dist.values, names=growth_dist.index, hole=0.45,
    template=CHART_TEMPLATE, color_discrete_sequence=COLOR_SEQ_DISCRETE,
    title="Job Growth Projection Distribution",
)
st.plotly_chart(fig3, use_container_width=True, key="chart_3")

st.divider()


# ------------------------------------------------------------------
# SECTION 2 — AI IMPACT (CORE SECTION)
# ------------------------------------------------------------------
st.markdown("## 2️⃣ AI Impact Analysis")
st.info(
    "This is the core section of the study. It examines how AI adoption "
    "**shows a relationship with** salary, automation risk, and job growth. "
    "The dataset is observational, so these are patterns and associations, "
    "not confirmed causes."
)

c1, c2 = st.columns(2)

with c1:
    ai_dist = order_index(df["AI_Adoption_Level"].value_counts(), ORDER_LOW_MED_HIGH)
    fig4 = px.bar(
        ai_dist, x=ai_dist.index, y=ai_dist.values, template=CHART_TEMPLATE,
        color=ai_dist.index, color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"x": "AI Adoption Level", "y": "Number of Jobs"},
        title="AI Adoption Level Distribution",
    )
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True, key="chart_4")

with c2:
    salary_by_ai = order_index(df.groupby("AI_Adoption_Level")["Salary_USD"].mean(), ORDER_LOW_MED_HIGH)
    fig5 = px.bar(
        salary_by_ai, x=salary_by_ai.index, y=salary_by_ai.values, template=CHART_TEMPLATE,
        color=salary_by_ai.index, color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"x": "AI Adoption Level", "y": "Average Salary (USD)"},
        title="AI Adoption vs Average Salary",
    )
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True, key="chart_5")

c3, c4 = st.columns(2)

with c3:
    ai_risk = pd.crosstab(df["AI_Adoption_Level"], df["Automation_Risk"], normalize="index") * 100
    ai_risk = ai_risk.reindex(index=[o for o in ORDER_LOW_MED_HIGH if o in ai_risk.index],
                               columns=[o for o in ORDER_LOW_MED_HIGH if o in ai_risk.columns])
    fig6 = px.bar(
        ai_risk, barmode="stack", template=CHART_TEMPLATE,
        color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"value": "Percentage of Jobs (%)", "AI_Adoption_Level": "AI Adoption Level", "variable": "Automation Risk"},
        title="AI Adoption vs Automation Risk (% composition)",
    )
    st.plotly_chart(fig6, use_container_width=True, key="chart_6")

with c4:
    ai_growth = pd.crosstab(df["AI_Adoption_Level"], df["Job_Growth_Projection"], normalize="index") * 100
    ai_growth = ai_growth.reindex(index=[o for o in ORDER_LOW_MED_HIGH if o in ai_growth.index],
                                   columns=[o for o in ORDER_GROWTH if o in ai_growth.columns])
    fig7 = px.bar(
        ai_growth, barmode="stack", template=CHART_TEMPLATE,
        color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"value": "Percentage of Jobs (%)", "AI_Adoption_Level": "AI Adoption Level", "variable": "Job Growth"},
        title="AI Adoption vs Job Growth (% composition)",
    )
    st.plotly_chart(fig7, use_container_width=True, key="chart_7")

with st.expander("📖 Interpretation notes — AI Impact"):
    st.write(
        "- Compare the salary bars across Low / Medium / High AI adoption to see whether "
        "higher adoption **appears associated with** higher or lower pay in the filtered data.\n"
        "- The stacked charts show how the *mix* of automation risk and growth outlook "
        "**shifts** across AI adoption levels, rather than a single trend.\n"
        "- These patterns describe the dataset only and should not be read as proof that "
        "AI adoption causes changes in risk, salary, or growth."
    )

st.divider()


# ------------------------------------------------------------------
# SECTION 3 — AUTOMATION RISK
# ------------------------------------------------------------------
st.markdown("## 3️⃣ Automation Risk")

r1, r2 = st.columns(2)

with r1:
    risk_dist = order_index(df["Automation_Risk"].value_counts(), ORDER_LOW_MED_HIGH)
    fig8 = px.bar(
        risk_dist, x=risk_dist.index, y=risk_dist.values, template=CHART_TEMPLATE,
        color=risk_dist.index, color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"x": "Automation Risk", "y": "Number of Jobs"},
        title="Automation Risk Distribution",
    )
    fig8.update_layout(showlegend=False)
    st.plotly_chart(fig8, use_container_width=True, key="chart_8")

with r2:
    salary_by_risk = order_index(df.groupby("Automation_Risk")["Salary_USD"].mean(), ORDER_LOW_MED_HIGH)
    fig9 = px.bar(
        salary_by_risk, x=salary_by_risk.index, y=salary_by_risk.values, template=CHART_TEMPLATE,
        color=salary_by_risk.index, color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"x": "Automation Risk", "y": "Average Salary (USD)"},
        title="Average Salary by Automation Risk",
    )
    fig9.update_layout(showlegend=False)
    st.plotly_chart(fig9, use_container_width=True, key="chart_9")

risk_industry = pd.crosstab(df["Industry"], df["Automation_Risk"], normalize="index") * 100
risk_industry = risk_industry.reindex(columns=[o for o in ORDER_LOW_MED_HIGH if o in risk_industry.columns])
fig10 = px.bar(
    risk_industry, barmode="stack", template=CHART_TEMPLATE,
    color_discrete_sequence=COLOR_SEQ_DISCRETE,
    labels={"value": "Percentage of Jobs (%)", "Industry": "Industry", "variable": "Automation Risk"},
    title="Automation Risk Composition by Industry",
)
st.plotly_chart(fig10, use_container_width=True, key="chart_10")

risk_job_title = pd.crosstab(df["Job_Title"], df["Automation_Risk"], normalize="index") * 100
risk_job_title = risk_job_title.reindex(columns=[o for o in ORDER_LOW_MED_HIGH if o in risk_job_title.columns])
fig11 = px.bar(
    risk_job_title, barmode="stack", template=CHART_TEMPLATE,
    color_discrete_sequence=COLOR_SEQ_DISCRETE,
    labels={"value": "Percentage of Jobs (%)", "Job_Title": "Job Title", "variable": "Automation Risk"},
    title="Automation Risk Composition by Job Title",
)
st.plotly_chart(fig11, use_container_width=True, key="chart_11")

st.divider()


# ------------------------------------------------------------------
# SECTION 4 — SALARY ANALYSIS
# ------------------------------------------------------------------
st.markdown("## 4️⃣ Salary Analysis")

fig12 = px.histogram(
    df, x="Salary_USD", nbins=30, template=CHART_TEMPLATE,
    color_discrete_sequence=["#3B7DD8"],
    labels={"Salary_USD": "Salary (USD)"},
    title="Overall Salary Distribution",
)
st.plotly_chart(fig12, use_container_width=True, key="chart_12")

s1, s2 = st.columns(2)

with s1:
    salary_by_industry2 = df.groupby("Industry")["Salary_USD"].mean().sort_values()
    fig13 = px.bar(
        salary_by_industry2, x=salary_by_industry2.values, y=salary_by_industry2.index,
        orientation="h", template=CHART_TEMPLATE, color=salary_by_industry2.values,
        color_continuous_scale=COLOR_SEQ,
        labels={"x": "Average Salary (USD)", "y": "Industry"},
        title="Average Salary by Industry",
    )
    fig13.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig13, use_container_width=True, key="chart_13")

with s2:
    remote_salary = df.groupby("Remote_Friendly")["Salary_USD"].mean()
    fig14 = px.box(
        df, x="Remote_Friendly", y="Salary_USD", template=CHART_TEMPLATE,
        color="Remote_Friendly", color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"Remote_Friendly": "Remote-Friendly", "Salary_USD": "Salary (USD)"},
        title="Remote vs Non-Remote Salary Comparison",
    )
    fig14.update_layout(showlegend=False)
    st.plotly_chart(fig14, use_container_width=True, key="chart_14")

st.divider()


# ------------------------------------------------------------------
# SECTION 5 — SKILLS
# ------------------------------------------------------------------
st.markdown("## 5️⃣ Required Skills Analysis")

skill_counts = Counter(df["Required_Skills"])
top_skills = pd.Series(skill_counts).sort_values(ascending=False)
top_10_skills = top_skills.head(10).sort_values()

most_frequent_skill = top_skills.idxmax()
st.success(f"🏆 **Most Frequently Required Skill:** {most_frequent_skill}")

sk1, sk2 = st.columns(2)

with sk1:
    fig15 = px.bar(
        top_10_skills, x=top_10_skills.values, y=top_10_skills.index,
        orientation="h", template=CHART_TEMPLATE, color=top_10_skills.values,
        color_continuous_scale=COLOR_SEQ,
        labels={"x": "Number of Job Postings", "y": "Skill"},
        title="Top 10 Required Skills",
    )
    fig15.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig15, use_container_width=True, key="chart_15")

with sk2:
    salary_by_skill = df.groupby("Required_Skills")["Salary_USD"].mean().sort_values()
    fig16 = px.bar(
        salary_by_skill, x=salary_by_skill.values, y=salary_by_skill.index,
        orientation="h", template=CHART_TEMPLATE, color=salary_by_skill.values,
        color_continuous_scale=COLOR_SEQ,
        labels={"x": "Average Salary (USD)", "y": "Required Skill"},
        title="Average Salary by Required Skill",
    )
    fig16.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig16, use_container_width=True, key="chart_16")

with st.expander("📖 View Skills by Industry (table)"):
    skills_industry = pd.crosstab(df["Industry"], df["Required_Skills"])
    st.dataframe(skills_industry, use_container_width=True)

st.divider()


# ------------------------------------------------------------------
# SECTION 6 — FUTURE JOB GROWTH
# ------------------------------------------------------------------
st.markdown("## 6️⃣ Future Job Growth")

g1, g2 = st.columns(2)

with g1:
    growth_dist2 = order_index(df["Job_Growth_Projection"].value_counts(), ORDER_GROWTH)
    fig17 = px.bar(
        growth_dist2, x=growth_dist2.index, y=growth_dist2.values, template=CHART_TEMPLATE,
        color=growth_dist2.index, color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"x": "Job Growth Projection", "y": "Number of Jobs"},
        title="Growth / Stable / Decline Distribution",
    )
    fig17.update_layout(showlegend=False)
    st.plotly_chart(fig17, use_container_width=True, key="chart_17")

with g2:
    growth_industry = pd.crosstab(df["Industry"], df["Job_Growth_Projection"], normalize="index") * 100
    growth_industry = growth_industry.reindex(columns=[o for o in ORDER_GROWTH if o in growth_industry.columns])
    fig18 = px.bar(
        growth_industry, barmode="stack", template=CHART_TEMPLATE,
        color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"value": "Percentage of Jobs (%)", "Industry": "Industry", "variable": "Job Growth"},
        title="Job Growth by Industry",
    )
    st.plotly_chart(fig18, use_container_width=True, key="chart_18")

g3, g4 = st.columns(2)

with g3:
    growth_ai = pd.crosstab(df["AI_Adoption_Level"], df["Job_Growth_Projection"], normalize="index") * 100
    growth_ai = growth_ai.reindex(index=[o for o in ORDER_LOW_MED_HIGH if o in growth_ai.index],
                                   columns=[o for o in ORDER_GROWTH if o in growth_ai.columns])
    fig19 = px.bar(
        growth_ai, barmode="stack", template=CHART_TEMPLATE,
        color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"value": "Percentage of Jobs (%)", "AI_Adoption_Level": "AI Adoption Level", "variable": "Job Growth"},
        title="Job Growth by AI Adoption Level",
    )
    st.plotly_chart(fig19, use_container_width=True, key="chart_19")

with g4:
    growth_risk = pd.crosstab(df["Automation_Risk"], df["Job_Growth_Projection"], normalize="index") * 100
    growth_risk = growth_risk.reindex(index=[o for o in ORDER_LOW_MED_HIGH if o in growth_risk.index],
                                       columns=[o for o in ORDER_GROWTH if o in growth_risk.columns])
    fig20 = px.bar(
        growth_risk, barmode="stack", template=CHART_TEMPLATE,
        color_discrete_sequence=COLOR_SEQ_DISCRETE,
        labels={"value": "Percentage of Jobs (%)", "Automation_Risk": "Automation Risk", "variable": "Job Growth"},
        title="Job Growth by Automation Risk",
    )
    st.plotly_chart(fig20, use_container_width=True, key="chart_20")

st.divider()


# ------------------------------------------------------------------
# SECTION 7 — KEY INSIGHTS
# ------------------------------------------------------------------
st.markdown("## 7️⃣ Key Insights")
st.caption("All figures below are calculated dynamically from the currently filtered dataset.")

highest_paying_industry = df.groupby("Industry")["Salary_USD"].mean().idxmax()
industry_highest_ai = (
    pd.crosstab(df["Industry"], df["AI_Adoption_Level"], normalize="index")
    .get("High", pd.Series(dtype=float))
)
industry_highest_ai_val = industry_highest_ai.idxmax() if not industry_highest_ai.empty else "N/A"

industry_highest_risk = (
    pd.crosstab(df["Industry"], df["Automation_Risk"], normalize="index")
    .get("High", pd.Series(dtype=float))
)
industry_highest_risk_val = industry_highest_risk.idxmax() if not industry_highest_risk.empty else "N/A"

job_highest_risk = (
    pd.crosstab(df["Job_Title"], df["Automation_Risk"], normalize="index")
    .get("High", pd.Series(dtype=float))
)
job_highest_risk_val = job_highest_risk.idxmax() if not job_highest_risk.empty else "N/A"

job_highest_growth = (
    pd.crosstab(df["Job_Title"], df["Job_Growth_Projection"], normalize="index")
    .get("Growth", pd.Series(dtype=float))
)
job_highest_growth_val = job_highest_growth.idxmax() if not job_highest_growth.empty else "N/A"

insights = {
    "💰 Highest Paying Industry": highest_paying_industry,
    "🤖 Industry with Highest AI Adoption": industry_highest_ai_val,
    "⚠️ Industry with Highest Automation Risk": industry_highest_risk_val,
    "📈 Most Common Growth Projection": safe_mode(df["Job_Growth_Projection"]),
    "🛠️ Most Frequently Required Skill": most_frequent_skill,
    "🔺 Job Title with Highest Automation Risk": job_highest_risk_val,
    "🚀 Job Title with Strongest Growth Outlook": job_highest_growth_val,
}

i_cols = st.columns(2)
for idx, (label, value) in enumerate(insights.items()):
    with i_cols[idx % 2]:
        st.markdown(f"**{label}**")
        st.markdown(f"### {value}")
        st.write("")

with st.expander("📝 Read the full analytical summary"):
    st.write(
        f"""
Based on the currently filtered data ({df.shape[0]} records), the job market shows the
following patterns:

- AI adoption is most commonly at the **{safe_mode(df['AI_Adoption_Level'])}** level, and the
  **{industry_highest_ai_val}** industry shows the largest share of High AI adoption.
- Automation risk is most commonly **{safe_mode(df['Automation_Risk'])}**, with the
  **{industry_highest_risk_val}** industry and the **{job_highest_risk_val}** role showing the
  highest share of High automation risk.
- The average salary is **${df['Salary_USD'].mean():,.2f}**, with **{highest_paying_industry}**
  as the highest-paying industry in this view.
- The job growth outlook is most commonly **{safe_mode(df['Job_Growth_Projection'])}**, and the
  **{job_highest_growth_val}** role shows the strongest share of jobs projected to grow.
- The most frequently required skill is **{most_frequent_skill}**.
- **{(df['Remote_Friendly'] == 'Yes').mean() * 100:.1f}%** of jobs in this view are remote-friendly.

These are associations observed in the dataset and should not be interpreted as proof that AI
adoption directly causes changes in salary, automation risk, or job growth.
        """
    )

st.divider()
st.caption(
    "Dashboard built with Streamlit • Data: ai_job_market_insights.csv • "
    "Companion to ai_job_market_analysis.py"
)
