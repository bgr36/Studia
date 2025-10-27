from tensorflow.keras.datasets import mnist
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

img_train = train_images/255
img_test = test_images/255
img_train = img_train.reshape(60000,28*28)
img_test = img_test.reshape(10000,28*28)

clf = RandomForestClassifier(n_estimators=200, random_state=123)
clf.fit(img_train, train_labels)

pred = clf.predict(img_test)
accuracy = accuracy_score(test_labels, pred)
report = classification_report(test_labels, pred)

print(f"Dokładność: {accuracy:.4f}")
print("Raport:")
print(report)
