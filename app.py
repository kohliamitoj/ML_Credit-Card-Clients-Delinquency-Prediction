import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Credit Card Delinquency Prediction",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    background: #f8fafc;
    color: #1e293b;
}

/* hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Header ── */
.page-header {
    background: #0f172a;
    color: #f1f5f9;
    padding: 2.8rem 3rem 2.4rem;
    margin: -1rem -1rem 2rem;
}
.page-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0 0 .5rem;
    color: #f8fafc;
}
.page-header p {
    font-size: .95rem;
    color: #94a3b8;
    margin: 0 0 1.2rem;
    max-width: 640px;
    line-height: 1.6;
}
.tag-row { display: flex; gap: .5rem; flex-wrap: wrap; }
.tag {
    font-size: .73rem;
    font-weight: 500;
    letter-spacing: .04em;
    text-transform: uppercase;
    color: #cbd5e1;
    border: 1px solid #334155;
    padding: .2rem .65rem;
    border-radius: 3px;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
    font-family: 'Inter', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: .5rem 1.1rem !important;
    border-radius: 0 !important;
    letter-spacing: .01em;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0f172a !important;
    border-bottom: 2px solid #2563eb !important;
    font-weight: 600 !important;
}
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #e2e8f0;
    gap: 0;
}

/* ── Section heading ── */
.sh {
    font-size: 1rem;
    font-weight: 600;
    color: #0f172a;
    letter-spacing: -.01em;
    margin: 2rem 0 .75rem;
    padding-bottom: .4rem;
    border-bottom: 1px solid #e2e8f0;
}

/* ── Stat grid ── */
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin-bottom: 1rem; }
.stat-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 1rem 1.1rem;
}
.stat-label { font-size: .72rem; font-weight: 600; text-transform: uppercase;
              letter-spacing: .05em; color: #64748b; margin-bottom: .25rem; }
.stat-value { font-size: 1.45rem; font-weight: 700; color: #0f172a; letter-spacing: -.02em; }
.stat-sub   { font-size: .75rem; color: #64748b; margin-top: .1rem; }

/* ── Cards ── */
.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 1rem 1.1rem;
    margin-bottom: .6rem;
}
.card-title { font-size: .88rem; font-weight: 600; color: #0f172a; margin-bottom: .25rem; }
.card-body  { font-size: .82rem; color: #475569; line-height: 1.55; }
.pill {
    display: inline-block;
    font-size: .68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .05em;
    padding: .15rem .55rem;
    border-radius: 3px;
    margin-bottom: .4rem;
}
.pill-blue   { background: #dbeafe; color: #1d4ed8; }
.pill-green  { background: #dcfce7; color: #15803d; }
.pill-amber  { background: #fef3c7; color: #b45309; }
.pill-slate  { background: #f1f5f9; color: #475569; }

/* ── Insight box ── */
.insight {
    background: #f8fafc;
    border-left: 3px solid #2563eb;
    padding: .7rem 1rem;
    border-radius: 0 4px 4px 0;
    font-size: .85rem;
    color: #334155;
    margin: .75rem 0 1.25rem;
    line-height: 1.55;
}

/* ── Images ── */
img { border-radius: 4px !important; }

/* ── Tables ── */
[data-testid="stDataFrame"] { border: 1px solid #e2e8f0 !important; border-radius: 6px; }

/* ── Pipeline list ── */
.pipe-step {
    display: flex; align-items: flex-start; gap: .65rem;
    font-size: .85rem; color: #334155;
    padding: .45rem 0;
    border-bottom: 1px solid #f1f5f9;
}
.pipe-num {
    flex-shrink: 0;
    width: 1.4rem; height: 1.4rem;
    background: #0f172a; color: white;
    border-radius: 50%;
    font-size: .68rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin-top: .05rem;
}

/* ── Key takeaways list ── */
.kt li { font-size: .85rem; color: #334155; padding: .2rem 0; }

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #e2e8f0;
    font-size: .78rem;
    color: #94a3b8;
    text-align: center;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: #0f172a !important;
    color: white !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    padding: .6rem 1.4rem !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

ASSETS = Path("assets")
PDF_PATH = Path("Report.pdf")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h1>Credit Card Clients — Delinquency Prediction</h1>
  <p>Binary classification of credit card payment default using four machine learning
     models implemented from scratch on 30,000 client records.</p>
  <div class="tag-row">
    <span class="tag">CS 7300 · Machine Learning</span>
    <span class="tag">Northeastern University</span>
    <span class="tag">UCI Dataset</span>
    <span class="tag">Binary Classification</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "EDA", "Models & Results", "Improvements", "Report"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="sh">Problem Statement</div>', unsafe_allow_html=True)
        st.markdown("""
Financial institutions need reliable methods to predict credit card payment defaults.
Accurate predictions reduce financial risk, inform lending strategies, and improve
customer outcomes.

This project builds and evaluates **four ML models from scratch** — without sklearn for
training — to predict whether a client will default on their next monthly payment.
        """)

        st.markdown('<div class="sh">Dataset</div>', unsafe_allow_html=True)
        df_desc = pd.DataFrame({
            "Property": ["Source", "Records", "Features", "Target", "Missing Values", "Time Period"],
            "Detail": [
                "UCI Machine Learning Repository",
                "30,000 credit card clients",
                "24 (demographics, payment history, bill statements)",
                "Default payment next month (0 = no, 1 = yes)",
                "None",
                "April – September 2005, Taiwan"
            ]
        })
        st.dataframe(df_desc, hide_index=True, use_container_width=True)

        st.markdown('<div class="sh">Feature Groups</div>', unsafe_allow_html=True)
        feat_cols = st.columns(3)
        groups = [
            ("Demographics", "pill-slate", ["SEX", "EDUCATION", "MARRIAGE", "AGE"]),
            ("Credit & Repayment", "pill-blue", ["LIMIT_BAL", "PAY_0 – PAY_6"]),
            ("Financial Statements", "pill-green", ["BILL_AMT1–6", "PAY_AMT1–6", "Total_due (engineered)"]),
        ]
        for col, (title, pill, feats) in zip(feat_cols, groups):
            with col:
                items = "".join(f"<li style='font-size:.82rem;color:#475569;padding:.1rem 0'>{f}</li>" for f in feats)
                st.markdown(
                    f'<div class="card"><div class="card-title">{title}</div><ul style="margin:.3rem 0 0;padding-left:1.1rem">{items}</ul></div>',
                    unsafe_allow_html=True
                )

    with col2:
        st.markdown('<div class="sh">Key Results</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="stat-grid">
  <div class="stat-box">
    <div class="stat-label">Best Accuracy</div>
    <div class="stat-value">75.1%</div>
    <div class="stat-sub">Neural Network</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Best F1-Score</div>
    <div class="stat-value">73.7%</div>
    <div class="stat-sub">Neural Network</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Best AUC</div>
    <div class="stat-value">~0.82</div>
    <div class="stat-sub">Neural Network</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">After SMOTE</div>
    <div class="stat-value">46,728</div>
    <div class="stat-sub">balanced samples</div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="sh">Pipeline</div>', unsafe_allow_html=True)
        steps = [
            "Data cleaning & type fixing",
            "Feature engineering (Total_due)",
            "One-hot encoding + standardization",
            "SMOTE class balancing",
            "75 / 25 train-test split",
            "Model training & evaluation",
        ]
        for i, s in enumerate(steps, 1):
            st.markdown(
                f'<div class="pipe-step"><div class="pipe-num">{i}</div><span>{s}</span></div>',
                unsafe_allow_html=True
            )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — EDA
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sh">Class Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/01_default_distribution.png"), caption="Default payment distribution", use_container_width=True)
    c2.image(str(ASSETS / "eda/02_credit_limit_age.png"),     caption="Credit limit & age density by default status", use_container_width=True)
    st.markdown('<div class="insight">The dataset is heavily imbalanced — 78% non-defaulters vs 22% defaulters. Clients with lower credit limits default at a significantly higher rate. SMOTE was applied before training to balance the classes.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sh">Demographics</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.image(str(ASSETS / "eda/03_default_by_gender.png"),    caption="Default by gender",          use_container_width=True)
    c2.image(str(ASSETS / "eda/04_default_by_education.png"), caption="Default by education level", use_container_width=True)
    c3.image(str(ASSETS / "eda/05_default_by_marriage.png"),  caption="Default by marital status",  use_container_width=True)

    st.markdown('<div class="sh">Payment Behaviour Over Time</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/06_repayment_status.png"),     caption="Repayment status (6 months)", use_container_width=True)
    c2.image(str(ASSETS / "eda/11_repay_status_default.png"), caption="Repayment status vs default",  use_container_width=True)

    st.markdown('<div class="sh">Financial Distributions</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/07_bill_amounts.png"),    caption="Bill amounts — April to September", use_container_width=True)
    c2.image(str(ASSETS / "eda/08_payment_amounts.png"), caption="Payment amounts",                   use_container_width=True)

    st.markdown('<div class="sh">Outlier Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/09_age_boxplot.png"),        caption="Age by default status",      use_container_width=True)
    c2.image(str(ASSETS / "eda/10_demographics_limit.png"), caption="Demographics vs credit limit", use_container_width=True)

    st.markdown('<div class="sh">Correlation Analysis</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "eda/12_correlation_heatmap.png"), caption="Feature correlation heatmap", use_container_width=True)
    st.image(str(ASSETS / "eda/13_correlation_target.png"),  caption="Feature correlation with target variable", use_container_width=True)
    st.markdown('<div class="insight">Repayment status columns (PAY_0 – PAY_6) show the strongest positive correlation with default. Bill amounts are highly inter-correlated but weakly correlated with the target.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MODELS & RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sh">Model Descriptions</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    models_info = [
        ("Logistic Regression", "pill-slate",
         "Gradient descent from scratch. α=0.001, 5000 iterations, L2 regularization (λ=0.01)."),
        ("Hard-Margin SVM", "pill-blue",
         "Perceptron-style weight updates from scratch. α=0.001, 700 iterations."),
        ("Gaussian Naive Bayes", "pill-amber",
         "Gaussian likelihoods per feature per class. Laplace smoothing. Built from scratch."),
        ("Neural Network", "pill-green",
         "Dense(64,ReLU) → Dropout(0.3) → Dense(32,ReLU) → Dropout(0.2) → Sigmoid. EarlyStopping."),
    ]
    for col, (name, pill, desc) in zip([m1, m2, m3, m4], models_info):
        col.markdown(
            f'<div class="card"><span class="pill {pill}">{name}</span>'
            f'<div class="card-body">{desc}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sh">Performance Metrics</div>', unsafe_allow_html=True)
    metrics_df = pd.DataFrame({
        "Model":           ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network"],
        "Accuracy (%)":    [62.16, 72.12, 62.55, 75.07],
        "Precision (%)":   [62.16, 77.81, 60.11, 77.37],
        "Recall (%)":      [60.89, 61.36, 73.10, 70.41],
        "F1-Score (%)":    [61.52, 68.61, 65.97, 73.72],
        "Specificity (%)": [63.42, 82.74, 52.14, 79.68],
    })

    def highlight_best(s):
        is_max = s == s.max()
        return ['background-color: #dcfce7; color: #15803d; font-weight: 600'
                if v else '' for v in is_max]

    styled = (metrics_df.style
              .apply(highlight_best, subset=["Accuracy (%)","Precision (%)","Recall (%)","F1-Score (%)","Specificity (%)"])
              .format({c: "{:.2f}" for c in ["Accuracy (%)","Precision (%)","Recall (%)","F1-Score (%)","Specificity (%)"]}))
    st.dataframe(styled, hide_index=True, use_container_width=True)
    st.caption("Green = highest value in each column.")

    st.markdown('<div class="sh">Bias–Variance Decomposition</div>', unsafe_allow_html=True)
    bv_df = pd.DataFrame({
        "Model":         ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network"],
        "Bias":          [0.379, 1.305, 0.376, 0.167],
        "Variance":      [0.250, 0.945, 0.239, 0.070],
        "Noise":         [0.378, 1.271, 0.375, 0.167],
        "Expected Loss": [1.007, 3.522, 0.990, 0.405],
    })

    def highlight_min(s):
        is_min = s == s.min()
        return ['background-color: #dcfce7; color: #15803d; font-weight: 600'
                if v else '' for v in is_min]

    styled_bv = (bv_df.style
                 .apply(highlight_min, subset=["Bias","Variance","Noise","Expected Loss"])
                 .format({c: "{:.3f}" for c in ["Bias","Variance","Noise","Expected Loss"]}))
    st.dataframe(styled_bv, hide_index=True, use_container_width=True)
    st.caption("Green = lowest (best) value in each column.")

    st.markdown('<div class="sh">Computational Cost</div>', unsafe_allow_html=True)
    tc1, tc2 = st.columns([2, 1])
    time_df = pd.DataFrame({
        "Model":        ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network"],
        "Train Time (s)":  [3.21, 35.50, 128.45, 5.41],
        "Peak Mem (MiB)":  [537.73, 544.94, 548.78, 830.81],
    })
    tc1.dataframe(time_df, hide_index=True, use_container_width=True)
    with tc2:
        st.markdown("""
<ul class="kt">
  <li>Neural Network — best accuracy and fast (5.4 s)</li>
  <li>GNB slowest (128 s) due to row-by-row inference</li>
  <li>LR lightest and fastest from-scratch model</li>
</ul>
""", unsafe_allow_html=True)

    st.markdown('<div class="sh">ROC-AUC Curves</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "results/03_roc_curves.png"), caption="ROC curves — all models", use_container_width=True)

    st.markdown('<div class="sh">Confusion Matrices</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "results/04_confusion_matrices.png"), caption="Confusion matrices — all models", use_container_width=True)

    st.markdown('<div class="sh">Train vs Test Accuracy</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "results/05_train_test_accuracy.png"), caption="Train vs test accuracy", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sh">Improvements Applied</div>', unsafe_allow_html=True)

    improvements = [
        ("SMOTE Class Balancing", "pill-blue", "Data",
         "Replaced basic oversampling with SMOTE, which generates synthetic interpolated minority samples. Dataset grew from ~13K to 46,728 balanced records."),
        ("L2 Regularization", "pill-slate", "Model",
         "Added L2 ridge penalty (λ=0.01) to the logistic regression gradient update to reduce overfitting. Also added predict_proba() for probability-based evaluation."),
        ("Deeper Neural Network + Dropout", "pill-green", "Model",
         "Expanded to Dense(64,ReLU) → Dropout(0.3) → Dense(32,ReLU) → Dropout(0.2) → Sigmoid. Added EarlyStopping (patience=5)."),
        ("ROC-AUC Evaluation", "pill-amber", "Evaluation",
         "ROC curves and AUC scores computed for all four models — the standard metric for credit risk tasks."),
        ("Confusion Matrix Heatmaps", "pill-amber", "Evaluation",
         "Side-by-side 2x2 heatmaps showing TP/TN/FP/FN for all models to surface misclassification patterns."),
        ("K-Fold Cross-Validation (k=5)", "pill-amber", "Evaluation",
         "5-fold CV on logistic regression: Mean Accuracy 58.75% ± 4.89%, Mean F1 60.00% ± 2.88%."),
        ("Train vs Test Accuracy Chart", "pill-slate", "Diagnostics",
         "Bar chart comparing train and test accuracy for all models to make overfitting/underfitting immediately visible."),
        ("LR Cost Curve", "pill-slate", "Diagnostics",
         "Cost function plotted over gradient descent iterations to verify convergence."),
    ]

    for title, pill, tag, desc in improvements:
        st.markdown(
            f'<div class="card">'
            f'<span class="pill {pill}">{tag}</span>'
            f'<div class="card-title" style="display:inline;margin-left:.5rem">{title}</div>'
            f'<div class="card-body" style="margin-top:.35rem">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sh">Training Diagnostics</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "results/01_nn_training_history.png"), caption="Neural network — accuracy & loss over epochs", use_container_width=True)
    c2.image(str(ASSETS / "results/02_lr_cost_curve.png"),       caption="Logistic regression — cost over iterations",   use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sh">Project Report</div>', unsafe_allow_html=True)
    st.markdown("Full report with all plots, metric tables, and methodology from the latest notebook run.")

    if PDF_PATH.exists():
        with open(PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="Download Report (PDF)",
            data=pdf_bytes,
            file_name="Credit_Card_Delinquency_Prediction_Report.pdf",
            mime="application/pdf",
        )
    else:
        st.warning("Report PDF not found.")

    st.markdown('<div class="sh">Resources</div>', unsafe_allow_html=True)
    st.markdown("""
| | |
|---|---|
| Dataset | [UCI ML Repository — Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) |
| Notebook | `ML_Credit_Card_Clients_Delinquency_Prediction.ipynb` |
""")

    st.markdown('<div class="sh">Tech Stack</div>', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    for col, tech in zip([t1, t2, t3, t4], ["Python 3.11", "NumPy / Pandas", "TensorFlow · Keras", "Streamlit"]):
        col.markdown(f'<div class="card" style="text-align:center;padding:.9rem"><div class="card-title">{tech}</div></div>', unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Amitoj Singh Kohli &nbsp;·&nbsp; CS 7300 Machine Learning &nbsp;·&nbsp; Northeastern University &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)
