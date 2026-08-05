<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">EMPLOYEE'S DATA ANALYSIS</h2>
</div>
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">IMPORTING VARIOUS MODULES</h2>
</div>
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">LOADING DATASET</h2>
</div>
#### If The dataset contain 'NaN', 'N/A', 'NA', 'n/a', 'n.a.', 'N#A', 'n#a', '?' values .We need to replace with Null.
## Summary Statistics of numeric variables:
## Missing Value
### Duplicate Value
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">EXPLORATOTY DATA ANALYSIS</h2>
</div>
## Univariate Analysis
## Multivariate Analysis
## Outlier Treatment
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">LABEL ENCODING</h2>
</div>
### Segregate Categorical and Numerical Columns
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">DATA SCALING</h2>
</div>
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">TRAIN & TEST SPLIT</h2>
</div>
<div style="text-align: center; background-color: #8ABEB9; padding: 10px;">
    <h2 style="font-weight: bold;">MODEL BUILDING</h2>
</div>
#### Summarize the performance of each regression model based on the provided metrics:

#### Linear Regression:

Both training and testing RMSE are around 0.55, indicating moderate predictive performance.
MAE is relatively low, suggesting that predictions are close to the actual values on average.
However, the R2 score is close to zero, indicating poor fit to the data.

#### Lasso Regression:

Similar performance to Linear Regression with slightly lower RMSE and MAE.
The R2 score remains close to zero, indicating weak explanatory power.

#### Ridge Regression:

Performance metrics are nearly identical to Linear Regression, suggesting similar predictive power.
The R2 score is still close to zero, indicating poor model fit.

#### k-Neighbors Regression:

Higher RMSE and MAE compared to Linear Regression models, indicating poorer predictive performance.
The negative R2 score for the testing set suggests that the model performs worse than a horizontal line.

#### Decision Tree Regression:

Perfect performance on the training set (RMSE and MAE are zero) suggests overfitting.
However, on the testing set, RMSE and MAE are high, and the negative R2 score indicates poor generalization.

#### Random Forest Regression:

Lower RMSE and MAE compared to other models, suggesting better predictive performance.
A relatively high R2 score on the testing set indicates decent explanatory power.

#### AdaBoost Regression:

Higher RMSE and MAE compared to Random Forest Regression.
The negative R2 score for the testing set suggests a poor fit to the data.

#### XGBRegressor:

The lowest RMSE and MAE among all models, indicating superior predictive performance.

However, the negative R2 score for the testing set suggests limited explanatory power.

In summary, among the models evaluated, the Random Forest Regression and XGBRegressor demonstrate better predictive performance, with lower RMSE and MAE. However, their R2 scores indicate limited explanatory power.
## OTHER MODEL
#### Summary of the performance of each classifier:

#### Logistic Regression:

Training dataset accuracy: 78.51%
Testing dataset accuracy: 79.78%
Logistic Regression achieves moderate accuracy on both the training and testing datasets.

#### Random Forest Classifier:

Training dataset accuracy: 100%
Testing dataset accuracy: 82.67%
The Random Forest Classifier achieves perfect accuracy on the training dataset, indicating potential overfitting. However, it still performs well on the testing dataset, indicating good generalization.

#### Decision Tree Classifier:

Training dataset accuracy: 100%
Testing dataset accuracy: 82.44%
Similar to Random Forest, the Decision Tree Classifier achieves perfect accuracy on the training dataset, suggesting overfitting. However, it also demonstrates good performance on the testing dataset.

#### Support Vector Machine (SVM):

Training dataset accuracy: 78.51%
Testing dataset accuracy: 79.78%
SVM achieves accuracy similar to Logistic Regression on both training and testing datasets.

#### In summary, all models perform reasonably well on the testing dataset, with accuracies ranging from around 79% to 83%. However, there are indications of overfitting in the Decision Tree and Random Forest models, as they achieve perfect accuracy on the training dataset but slightly lower accuracy on the testing dataset. Logistic Regression and SVM demonstrate more consistent performance across both training and testing datasets. 
## HyperParameter Training
