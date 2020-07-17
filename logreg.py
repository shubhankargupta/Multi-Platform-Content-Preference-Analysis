import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import seaborn as sns


sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
data = pd.read_csv('testing1.csv', header=0)
data = data.dropna()
print(data.shape)
print(list(data.columns))
#sns.countplot(x="FB_Followers",data=data, palette='hls')
#plt.show()
data.isnull().sum()
X = data.iloc[:,0:6]
y = data.iloc[:,6]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
#print y_train.shape
classifier = LogisticRegression(C=1e5)
classifier.fit(X_train, y_train)
coef = classifier.coef_[0]
print (coef)
y_pred = classifier.predict(X_test)
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(classifier.score(X_test, y_test)))
print(classification_report(y_test, y_pred))
