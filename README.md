ABSTRACT

This project's main aim is to predict credit card delinquency for the upcoming month, and it uses a dataset from the UCI Machine Learning Repository. The dataset has 30,000 instances, 24 features, and one target variable, including credit limit, demographic details, payment history, and bill statements. 

I have prepared the dataset for model training by meticulously processing the data and engineering features. The preprocessing included handling irregularities in categorical variables, and also, introduced a derived feature called 'Total_due.' 

I developed four machine learning algorithms, which are Logistic Regression using Gradient Descent, Hard-Margin SVM, Gaussian Naive Bayes, and a Neural Network implemented via TensorFlow and Keras. Also, evaluated each model based on precision, recall, accuracy, and other relevant metrics. 

The focus was to assess predictive power and computational efficiency. The models' performances provided insights that could aid financial institutions in mitigating risks and making decisions related to credit lending.

INTRODUCTION

Business Problem Definition: 
Financial institutions continuously seek reliable methods to predict client delinquency on credit card payments. Accurate predictions can significantly reduce financial risk, refine lending strategies, and enhance customer service. 

The ability to predict client credit card payment delinquencies is a key challenge in the constantly changing world of financial institutions. Precise forecasts not only reduce financial hazards but also enable organizations to improve lending practices and customer support. This research aims to estimate customer defaults in the following month by using previous data to build predictive models from scratch in response to this problem. To minimize potential financial losses, the initiative seeks to facilitate preventive steps by identifying the underlying traits and patterns of clients who are at risk of default. 

The project takes a careful approach to model building and explores machine learning algorithms that are created independently of pre-built libraries. The aim of binary classification is to determine if a client will default or not. This project focuses on developing predictive models from scratch that predict client defaults in the subsequent month based on historical data. 

Problem Setting: 
The problem at hand is a binary classification task where the outcome variable (Y) indicates whether a client will default (1) or not (0) in the next month. The challenge lies in utilizing historical payment data, billing statements, and client information to build a robust predictive model without reliance on pre-built libraries for model development.

DATA DESCRIPTION

Data Source:
Dataset Link: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients

The dataset is sourced from the UCI Machine Learning Repository and contains 30,000 records and 25 features. It comprises various features such as credit limit, gender, education, marital status, age, past payment history, bill statements, and previous payment amounts. 

This diverse dataset will be leveraged to understand the relationship between client attributes and default behavior. Given the absence of missing values, the dataset offers a suitable foundation for analysis. 

Data Dictionary:
Given below is the data dictionary of the dataset: -

	Default Payment Next Month (Yes = 1, No = 0)

	Sex (1 = male; 2 = female)

	Education (1 = graduate school; 2 = university; 3 = high school; 4 = others)

	Marriage (1 = married; 2 = single; 3 = others)

	Age (years)

	Pay_0; . . . ; Pay_6 (-2 = No credit consumed; -1 = pay duly; 1 = payment delay for one month; 2 = payment delay for two months; . . .; 8 = payment delay for eight months)

	Bill_Amt1; . . . ;Bill_Amt6 (in NT dollar) (Amount of bill in September 2005; . . . ; Amount of bill in April 2005)

	Pay_Amt1; . . .; Pay_Amt6 (in NT dollar) (Amount paid in September 2005; . . . ; Amount paid in April 2005)


METHODS: MODEL DEVELOPMENT

Dataset Splitting into Training and Test Sets:
Before training our machine learning models, I meticulously partitioned the balanced dataset into two sets - a training set and a test set. This crucial step was taken to enable me to evaluate the performance of the model against unseen data confidently. I adopted a 75-25 data split, where adequate data was used for learning patterns (X_train and y_train), while a significant portion was kept aside for testing predictions (X_test and y_test). The random_state parameter ensured that the split was deterministic, essential for the reproducibility of model performance evaluation.

Model Development:
In my methodological approach, I meticulously crafted and rigorously evaluated four distinct machine learning algorithms to construct a robust predictive framework. My methodology was grounded in the principles of algorithmic development from the ground up, with the notable exception of the neural network model, where I utilized the advanced capabilities of TensorFlow and Keras. Below is a detailed account of the models I developed:

1.	Logistic Regression Model Using Gradient Descent (Base Model): My initial model was a logistic regression classifier implemented to benchmark subsequent models. The simplicity of logistic regression, paired with the robustness of gradient descent for optimization, provided a solid foundation for the binary classification task. The development of this model involved iteratively adjusting the weights to minimize the cost function evaluating the gradients of the cost with respect to the model parameters.

2.	Hard-Margin SVM: Recognizing the prowess of SVMs in handling high-dimensional data, I developed a Hard-Margin SVM model designed to find the optimal separating hyperplane for the data. This model is especially adept at classifying data with a clear margin of separation, and my implementation focused on maximizing this margin to achieve the best possible classification boundary.

3.	Gaussian Naive Bayes: I integrated the Gaussian Naive Bayes algorithm, which is predicated on the assumption of independence between predictors and the normal distribution of features. This model is known for its computational efficiency and suitability for datasets with many categorical features.

4.	Neural Networks (Multi-Layer Perceptron Classifier): To explore the complex nonlinear relationships within the data, I employed a Multi-Layer Perceptron Classifier. This neural network was constructed using TensorFlow and Keras, enabling me to define a sophisticated architecture with multiple layers and activation functions. The model was designed to discern intricate patterns that simpler models might overlook.

Each model was diligently tuned and calibrated to align with the specific characteristics of the dataset. The hyperparameters for each model were fine-tuned to optimize performance, and feature scaling was employed to ensure that each input contributed equitably to the learning process. I also engaged in performance tuning, a critical step to ensure that the model generalizes well to new data while avoiding overfitting.

Subsequent sections will delve into the detailed implementation, optimization strategies employed, and the comparative analysis of the model performances. This comprehensive evaluation will underscore the strengths and limitations of each algorithm within the context of the dataset.

