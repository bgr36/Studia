import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow import keras
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Input
from sklearn.metrics import classification_report



(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
img_train = train_images/255
img_test = test_images/255
lbl_train = to_categorical(train_labels, 10)
lbl_test = to_categorical(test_labels, 10)

img_train = img_train.reshape(60000,28*28)
img_test = img_test.reshape(10000,28*28)

folder_path = "MyDataSet"
PngFiles = os.listdir(os.path.join(folder_path))
my_images = []
my_labels = []

for file in PngFiles:
    path = os.path.join(folder_path, file)
    img = Image.open(path).convert('L')  
    img_array = 1 - (np.array(img) / 255.0)  
    my_images.append(img_array)
    label = int(file[0])
    my_labels.append(label)

my_images = np.array(my_images)
my_labels = np.array(my_labels)

my_labels = keras.utils.to_categorical(my_labels, 10)
my_images = my_images.reshape(len(my_images), 28*28)

#test img import
# x=7
# plt.imshow(my_images[x], cmap="grey")
# plt.show()
# print(my_labels[x])

# plt.imshow(img_train[x], cmap="grey")
# plt.show()
# print(lbl_train[x])

model = Sequential([
    Input(shape=(28*28,)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(img_train, lbl_train, epochs = 8, batch_size = 32)



eval = model.evaluate(img_test, lbl_test, verbose =2)
print("Zbiór testowy MNIST:")
print("loss      accuracy")
print(eval)

predictions = model.predict(img_test)
y_pred = np.argmax(predictions, axis=1)        
y_true = np.argmax(lbl_test, axis=1)

report = classification_report(y_true, y_pred,zero_division=0)
print("MNIST:")
print(report)



eval = model.evaluate(my_images, my_labels, verbose =2)
print("Mój zbiór testowy:")
print("loss      accuracy")
print(eval)

predictions_custom = model.predict(my_images)
y_pred_custom = np.argmax(predictions_custom, axis=1)
y_true_custom = np.argmax(my_labels, axis=1)

report_custom = classification_report(y_true_custom, y_pred_custom)
print("Mój zbiór danych:")
print(report_custom)