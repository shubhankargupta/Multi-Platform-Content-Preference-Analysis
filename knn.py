import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
 


# loading training data
df = pd.read_csv('testing.csv',header=0)
df.head()


# create design matrix X and target vector y
X = np.array(df.ix[:, 0:6]) 	# end index is exclusive
y = np.array(df.ix[:,6]) 	# another way of indexing a pandas df

# split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)




# creating odd list of K for KNN
myList = list(range(1,10))

# subsetting just the odd ones
neighbors = filter(lambda x: x % 2 != 0, myList)

# empty list that will hold cv scores
cv_scores = []

# perform 10-fold cross validation
for k in neighbors:
    knn = KNeighborsClassifier(n_neighbors=k)
    #cv = KFold(X.shape[0], 10, shuffle=True, random_state=42)
    scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
    cv_scores.append(scores.mean())


# changing to misclassification error
MSE = [1 - x for x in cv_scores]

# determining best k
optimal_k = neighbors[MSE.index(min(MSE))]
print "The optimal number of neighbors is %d" % optimal_k

# plot misclassification error vs k
plt.plot(neighbors, MSE)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.show()



# instantiate learning model (k = 3)
knn = KNeighborsClassifier(n_neighbors=optimal_k)

# fitting the model
knn.fit(X_train, y_train)

# predict the response
pred = knn.predict(X_test)

confusion_matrix = confusion_matrix(y_test, pred)
print(confusion_matrix)

print(classification_report(y_test, pred))

# evaluate accuracy
print accuracy_score(y_test, pred)


