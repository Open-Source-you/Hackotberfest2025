# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Load the dataset
iris = load_iris()
X = iris.data
y = iris.target

# Create a DataFrame with the input features and target variable
df = pd.DataFrame(X, columns=iris.feature_names)
df["species"] = y

# Split dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df[iris.feature_names], df["species"], test_size=0.3, random_state=42
)

# Create and train the model
classifier = DecisionTreeClassifier(random_state=42)
classifier.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = classifier.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Visualize the decision tree
plt.figure(figsize=(10, 10))
tree.plot_tree(
    classifier,
    filled=True,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
)
plt.show()
