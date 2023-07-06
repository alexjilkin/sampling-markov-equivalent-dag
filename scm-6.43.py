import numpy as np
import statsmodels.api as sm
from scipy.stats import linregress
import matplotlib.pyplot as plt

# The lm() function creates a linear regression model in R. 
# This function takes an R formula Y ~ X where Y is the 
# outcome variable and X is the predictor variable.

# The ~ symbol defines the predictors and the target variable

# OLS - Ordinary Least Squares

np.random.seed(1)
n = 100
rnorm = np.random.normal(size=n)

C = rnorm
A = 0.8*np.random.normal(size=n)
K = A + 0.1*np.random.normal(size=n)
X = C - 2*A + 0.2*np.random.normal(size=n)
F = 3*X + 0.8*np.random.normal(size=n)
D = -2*X + 0.5*np.random.normal(size=n)
G = D + 0.5*np.random.normal(size=n)
Y = 2*K - D + 0.2*np.random.normal(size=n)
H = 0.5*Y + 0.1*np.random.normal(size=n)

# Linear regression
X1 = sm.add_constant(X)
model1 = sm.OLS(Y, X1)
results1 = model1.fit()
print(results1.params)

X2 = sm.add_constant(np.column_stack((X, K)))
model2 = sm.OLS(Y, X2)
results2 = model2.fit()
print(results2.params)

X3 = sm.add_constant(np.column_stack((X, F, C, K)))
model3 = sm.OLS(Y, X3)
results3 = model3.fit()
print(results3.params)


# Generate x values for plotting
x_vals = np.linspace(np.min(X), np.max(X), 100)

# Plot the functions
plt.scatter(X, Y, label='Data')
plt.plot(x_vals, results1.params[0] + results1.params[1] * x_vals, label='Y ~ X')
plt.plot(x_vals, results2.params[0] + results2.params[1] * x_vals + results2.params[2] * K, label='Y ~ X + K')
plt.plot(x_vals, results3.params[0] + results3.params[1] * x_vals + results3.params[2] * F + results3.params[3] * C + results3.params[4] * K, label='Y ~ X + F + C + K')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()