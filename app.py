import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Credit Card Delinquency Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #f7f9fc; }
  .hero {
    background: linear-gradient(135deg, #1a3a5c 0%, #2d6a9f 100%);
    padding: 3rem 2.5rem 2.5rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 2rem;
  }
  .hero h1 { font-size: 2.4rem; font-weight: 800; margin: 0 0 .4rem; }
  .hero p  { font-size: 1.05rem; opacity: .88; margin: 0; }
  .hero .badges { margin-top: 1.2rem; display: flex; gap: .6rem; flex-wrap: wrap; }
  .badge {
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.35);
    border-radius: 20px;
    padding: .28rem .85rem;
    font-size: .82rem;
    font-weight: 600;
    letter-spacing: .03em;
  }
  .section-title {
    font-size: 1.35rem; font-weight: 700;
    color: #1a3a5c; border-left: 4px solid #2d6a9f;
    padding-left: .7rem; margin: 1.6rem 0 1rem;
  }
  .card {
    background: white; border-radius: 12px;
    padding: 1.2rem 1.4rem; box-shadow: 0 2px 8px rgba(0,0,0,.07);
    margin-bottom: 1rem;
  }
  .best-badge {
    background: #e8f5e9; color: #2e7d32;
    font-size: .75rem; font-weight: 700;
    padding: .2rem .6rem; border-radius: 10px;
    margin-left: .5rem; vertical-align: middle;
  }
  .tab-content { padding-top: .5rem; }
  div[data-testid="metric-container"] {
    background: white; border-radius: 10px;
    padding: .8rem 1rem; box-shadow: 0 2px 6px rgba(0,0,0,.06);
  }
  img { border-radius: 8px; }
  .footer {
    text-align: center; color: #999; font-size: .82rem;
    margin-top: 3rem; padding-top: 1.5rem;
    border-top: 1px solid #e0e0e0;
  }
  .improvement-tag {
    display: inline-block;
    background: #e3f2fd; color: #1565c0;
    font-size: .78rem; font-weight: 600;
    padding: .2rem .65rem; border-radius: 8px;
    margin: .15rem;
  }
</style>
""", unsafe_allow_html=True)

ASSETS = Path("assets")
PDF_PATH = Path("ML_Credit_Card_Clients_Delinquency_Prediction_Report.pdf")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>💳 Credit Card Delinquency Prediction</h1>
  <p>Predicting whether a client will default on their credit card payment next month
     using four machine learning models built from scratch.</p>
  <div class="badges">
    <span class="badge">CS 7300 · Machine Learning</span>
    <span class="badge">Northeastern University</span>
    <span class="badge">30,000 Records · UCI Dataset</span>
    <span class="badge">Binary Classification</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Overview", "📊 EDA", "🤖 Models & Results", "🚀 Improvements", "📄 Report"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 · OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="section-title">Problem Statement</div>', unsafe_allow_html=True)
        st.markdown("""
Financial institutions need reliable methods to predict client delinquency on credit
card payments. Accurate predictions can **reduce financial risk**, refine lending strategies,
and enhance customer service.

This project builds and evaluates **four ML models from scratch** (no sklearn for training)
to predict whether a client will default on their payment next month — a binary classification
problem (1 = default, 0 = no default).
        """)

        st.markdown('<div class="section-title">Dataset</div>', unsafe_allow_html=True)
        df_desc = pd.DataFrame({
            "Property": ["Source", "Records", "Features", "Target", "Missing Values", "Time Period"],
            "Detail": [
                "UCI Machine Learning Repository",
                "30,000 credit card clients",
                "24 (demographics, payment history, bill statements)",
                "Default payment next month (0 / 1)",
                "None",
                "April – September 2005 (Taiwan)"
            ]
        })
        st.dataframe(df_desc, hide_index=True, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Key Highlights</div>', unsafe_allow_html=True)
        st.metric("Best Model Accuracy", "75.1%", "Neural Network MLP")
        st.metric("Best F1-Score", "73.7%", "Neural Network MLP")
        st.metric("Best AUC", "~0.82", "Neural Network MLP")
        st.metric("Dataset Size (after SMOTE)", "46,728", "+13,364 synthetic samples")

        st.markdown('<div class="section-title">Pipeline</div>', unsafe_allow_html=True)
        for step in [
            "1. Data Cleaning & Type Fixing",
            "2. Feature Engineering (Total_due)",
            "3. One-Hot Encoding + Standardization",
            "4. SMOTE Class Balancing",
            "5. 75/25 Train-Test Split",
            "6. Model Training & Evaluation",
        ]:
            st.markdown(f"- {step}")

    st.markdown('<div class="section-title">Feature Overview</div>', unsafe_allow_html=True)
    feat_cols = st.columns(3)
    groups = [
        ("Demographics", ["SEX", "EDUCATION", "MARRIAGE", "AGE"]),
        ("Credit & Payment History", ["LIMIT_BAL", "PAY_0 → PAY_6 (repayment status)"]),
        ("Financial Statements", ["BILL_AMT1–6 (bill amounts)", "PAY_AMT1–6 (payments made)", "Total_due (engineered)"]),
    ]
    for col, (title, feats) in zip(feat_cols, groups):
        with col:
            st.markdown(f'<div class="card"><strong>{title}</strong><ul>' +
                        "".join(f"<li>{f}</li>" for f in feats) +
                        "</ul></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 · EDA
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Class Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/01_default_distribution.png"), caption="Default Payment Distribution", use_container_width=True)
    c2.image(str(ASSETS / "eda/02_credit_limit_age.png"),     caption="Credit Limit & Age Density by Default Status", use_container_width=True)

    st.markdown("""
> **Key insight:** The dataset is heavily imbalanced — ~78% non-defaulters vs ~22% defaulters.
  Clients with lower credit limits are significantly more likely to default.
  SMOTE was applied to balance the classes before training.
""")

    st.markdown('<div class="section-title">Demographic Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.image(str(ASSETS / "eda/03_default_by_gender.png"),    caption="Default by Gender",         use_container_width=True)
    c2.image(str(ASSETS / "eda/04_default_by_education.png"), caption="Default by Education Level", use_container_width=True)
    c3.image(str(ASSETS / "eda/05_default_by_marriage.png"),  caption="Default by Marital Status",  use_container_width=True)

    st.markdown('<div class="section-title">Payment Behaviour Over Time</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/06_repayment_status.png"),       caption="Repayment Status (6 months)", use_container_width=True)
    c2.image(str(ASSETS / "eda/11_repay_status_default.png"),   caption="Repayment Status vs Default",  use_container_width=True)

    st.markdown('<div class="section-title">Financial Statement Distributions</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/07_bill_amounts.png"),   caption="Bill Amount Distributions (April–September)", use_container_width=True)
    c2.image(str(ASSETS / "eda/08_payment_amounts.png"), caption="Payment Amount Distributions",                use_container_width=True)

    st.markdown('<div class="section-title">Outlier Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "eda/09_age_boxplot.png"),         caption="Age vs Default Status",           use_container_width=True)
    c2.image(str(ASSETS / "eda/10_demographics_limit.png"),  caption="Demographics vs Credit Limit",    use_container_width=True)

    st.markdown('<div class="section-title">Correlation Analysis</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "eda/12_correlation_heatmap.png"), caption="Full Feature Correlation Heatmap", use_container_width=True)
    st.image(str(ASSETS / "eda/13_correlation_target.png"),  caption="Feature Correlation with Target Variable", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 · MODELS & RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Model Architectures</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    for col, name, desc in zip(
        [m1, m2, m3, m4],
        ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network"],
        [
            "Gradient descent from scratch. α=0.001, max 5000 iterations, L2 regularization (λ=0.01).",
            "Perceptron-style weight updates from scratch. α=0.001, 700 iterations.",
            "Laplace smoothing on priors, Gaussian per feature. Built from scratch with scipy.",
            "TensorFlow/Keras. Dense(64,ReLU) → Dropout(0.3) → Dense(32,ReLU) → Dropout(0.2) → Sigmoid. EarlyStopping.",
        ]
    ):
        col.markdown(f'<div class="card"><strong>{name}</strong><br/><small style="color:#555">{desc}</small></div>',
                     unsafe_allow_html=True)

    st.markdown('<div class="section-title">Performance Metrics</div>', unsafe_allow_html=True)

    metrics_df = pd.DataFrame({
        "Model":        ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network ⭐"],
        "Accuracy (%)": [62.16, 72.12, 62.55, 75.07],
        "Precision (%)": [62.16, 77.81, 60.11, 77.37],
        "Recall (%)":   [60.89, 61.36, 73.10, 70.41],
        "F1-Score (%)": [61.52, 68.61, 65.97, 73.72],
        "Specificity (%)": [63.42, 82.74, 52.14, 79.68],
    })

    def highlight_best(s):
        is_max = s == s.max()
        return ['background-color: #e8f5e9; font-weight: bold; color: #2e7d32'
                if v else '' for v in is_max]

    styled = (metrics_df.style
              .apply(highlight_best, subset=["Accuracy (%)","Precision (%)","Recall (%)","F1-Score (%)","Specificity (%)"])
              .format({"Accuracy (%)": "{:.2f}", "Precision (%)": "{:.2f}",
                       "Recall (%)": "{:.2f}", "F1-Score (%)": "{:.2f}", "Specificity (%)": "{:.2f}"}))
    st.dataframe(styled, hide_index=True, use_container_width=True)

    st.markdown('<div class="section-title">Bias–Variance Trade-off</div>', unsafe_allow_html=True)
    bv_df = pd.DataFrame({
        "Model":          ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network ⭐"],
        "Bias":           [0.379, 1.305, 0.376, 0.167],
        "Variance":       [0.250, 0.945, 0.239, 0.070],
        "Noise":          [0.378, 1.271, 0.375, 0.167],
        "Expected Loss":  [1.007, 3.522, 0.990, 0.405],
    })
    styled_bv = (bv_df.style
                 .apply(highlight_best, subset=["Bias","Variance","Noise","Expected Loss"])
                 .format({"Bias":"{:.3f}","Variance":"{:.3f}","Noise":"{:.3f}","Expected Loss":"{:.3f}"}))
    st.dataframe(styled_bv, hide_index=True, use_container_width=True)
    st.caption("⭐ Green = lowest (best) value in each column")

    st.markdown('<div class="section-title">Computational Cost</div>', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    time_df = pd.DataFrame({
        "Model": ["Logistic Regression", "Hard-Margin SVM", "Gaussian Naive Bayes", "Neural Network"],
        "Time (s)": [3.21, 35.50, 128.45, 5.41],
        "Space (MiB)": [537.73, 544.94, 548.78, 830.81],
    })
    tc1.dataframe(time_df, hide_index=True, use_container_width=True)
    tc2.markdown("""
**Key takeaways:**
- 🏆 **Neural Network** — best accuracy AND fast (5.4s)
- ⚠️ **GNB** is the slowest by far (128s) due to row-by-row probability computation
- ⚠️ **SVM** uses 2× more memory than LR/GNB at 830 MiB
- ✅ **LR** is the lightest and fastest from-scratch model
""")

    st.markdown('<div class="section-title">ROC-AUC Curves</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "results/03_roc_curves.png"), caption="ROC Curves — All Models", use_container_width=True)

    st.markdown('<div class="section-title">Confusion Matrices</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "results/04_confusion_matrices.png"), caption="Confusion Matrices — All Models", use_container_width=True)

    st.markdown('<div class="section-title">Train vs Test Accuracy</div>', unsafe_allow_html=True)
    st.image(str(ASSETS / "results/05_train_test_accuracy.png"), caption="Train vs Test Accuracy", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 · IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Improvements Applied</div>', unsafe_allow_html=True)

    improvements = [
        ("SMOTE Class Balancing",
         "Replaced basic oversampling with SMOTE (Synthetic Minority Over-sampling Technique), which generates synthetic interpolated samples rather than duplicating existing ones. Dataset grew from ~13K to 46,728 balanced samples.",
         "Data Quality"),
        ("L2 Regularization — Logistic Regression",
         "Added L2 (Ridge) regularization term (λ=0.01) to the gradient descent update to penalize large weights and reduce overfitting. Also added predict_proba() for probability-based evaluation.",
         "Model Quality"),
        ("Deeper Neural Network + Dropout",
         "Expanded from Dense(32)→Sigmoid to Dense(64,ReLU)→Dropout(0.3)→Dense(32,ReLU)→Dropout(0.2)→Sigmoid. Added EarlyStopping (patience=5) to prevent overfitting.",
         "Model Quality"),
        ("ROC-AUC Curves",
         "Added ROC curves and AUC scores for all 4 models — the standard metric for credit risk classification tasks. Allows comparison beyond simple accuracy.",
         "Evaluation"),
        ("Confusion Matrix Heatmaps",
         "Visual 2×2 heatmaps of TP/TN/FP/FN for all models side-by-side, making misclassification patterns immediately visible.",
         "Evaluation"),
        ("K-Fold Cross-Validation (k=5)",
         "5-fold CV on the Logistic Regression model to validate performance stability. Results: Mean Accuracy 58.75% ± 4.89%, Mean F1 60.00% ± 2.88%.",
         "Evaluation"),
        ("Train vs Test Accuracy Comparison",
         "Side-by-side bar chart comparing training and test accuracy for all models, making overfitting/underfitting patterns immediately visible.",
         "Evaluation"),
        ("LR Cost Curve",
         "Plotted the cost function over gradient descent iterations to visually confirm convergence behaviour.",
         "Diagnostics"),
    ]

    for title, desc, tag in improvements:
        st.markdown(
            f'<div class="card">'
            f'<span class="improvement-tag">{tag}</span>'
            f'<strong style="font-size:1rem"> {title}</strong>'
            f'<p style="margin:.5rem 0 0; color:#555; font-size:.9rem">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Training Diagnostics</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.image(str(ASSETS / "results/01_nn_training_history.png"), caption="Neural Network — Accuracy & Loss over Epochs", use_container_width=True)
    c2.image(str(ASSETS / "results/02_lr_cost_curve.png"),       caption="Logistic Regression — Cost over Iterations",    use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 · REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Project Report</div>', unsafe_allow_html=True)
    st.markdown("""
The full PDF report contains all results, plots, and metric tables from the latest notebook run.
    """)

    if PDF_PATH.exists():
        with open(PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="⬇️  Download Full PDF Report",
            data=pdf_bytes,
            file_name="Credit_Card_Delinquency_Prediction_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.warning("PDF report not found. Run the notebook to regenerate it.")

    st.markdown('<div class="section-title">Project Links</div>', unsafe_allow_html=True)
    st.markdown("""
| Resource | Link |
|----------|------|
| Dataset | [UCI ML Repository — Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) |
| Notebook | `ML_Credit_Card_Clients_Delinquency_Prediction.ipynb` |
""")

    st.markdown('<div class="section-title">Tech Stack</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, tech in zip(cols, ["Python 3.11", "NumPy · Pandas", "TensorFlow / Keras", "Streamlit"]):
        col.markdown(f'<div class="card" style="text-align:center"><strong>{tech}</strong></div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Amitoj Singh Kohli · CS 7300 Machine Learning · Northeastern University · 2026
</div>
""", unsafe_allow_html=True)
