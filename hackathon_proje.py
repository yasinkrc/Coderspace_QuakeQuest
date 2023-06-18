""" 
Created by Yasin Karaca on 16.06.2023 - 18.06.2023


"""
import numpy as np
import cv2
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import time
from PyQt5.QtGui import QFont

# Load pre-trained VGG16 model
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

# Function to preprocess an image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize image to match VGG16 input size
    img = np.array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

# List of image paths
image_paths = ["C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon7.jpg",
               "C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon1.jpg",
               "C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon2.jpg",
               "C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon3.jpg",
               "C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon4.jpg",
               "C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon5.jpg",
               "C:\\Users\\yasin\\OneDrive\\Masaüstü\\hackathon\\hackathon6.jpg"]

# Preprocess the images and extract feature vectors
feature_vectors = []
for image_path in image_paths:
    image = preprocess_image(image_path)
    feature_vector = model.predict(image).flatten()
    feature_vectors.append(feature_vector)

# Capture an image from the camera
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
cv2.imwrite('captured_image.jpg', frame)
camera.release()

# Preprocess the captured image
captured_image = preprocess_image('captured_image.jpg')
captured_feature_vector = model.predict(captured_image).flatten()

# Calculate cosine similarity with each image in the list
similarities = []
for feature_vector in feature_vectors:
    similarity = cosine_similarity([feature_vector], [captured_feature_vector])[0][0]
    similarities.append(similarity)
""" 

<!DOCTYPE html>
<html>
<head>
    <title>Kamera Açma</title>
</head>
<body>
    <h1>Kamera Açma</h1>
    <div>
        <video id="video" width="640" height="480"></video>
    </div>
    <button id="startButton">Kamerayı Aç</button>
    <button id="captureButton">Fotoğraf Çek</button>
    <canvas id="canvas" width="640" height="480"></canvas>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const startButton = document.getElementById('startButton');
        const captureButton = document.getElementById('captureButton');
        let stream, mediaRecorder;
"""

""" 
        // Kamerayı başlatma
        startButton.addEventListener('click', async () => {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                video.play();
            } catch (error) {
                console.error('Kamera başlatma hatası:', error);
            }
        });

        // Fotoğraf çekme
        captureButton.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Çekilen fotoğrafı göstermek için aşağıdaki satırı kullanabilirsiniz
            // const dataUrl = canvas.toDataURL();
            // window.open(dataUrl);
        });
    </script>
</body>
</html>

"""
# Print the similarities
for i, similarity in enumerate(similarities):
    print("Similarity with Image", i+1, ":", similarity)

# Find the index of the highest similarity
max_similarity_index = np.argmax(similarities)

# Get the highest similarity value
max_similarity = similarities[max_similarity_index]

# Check if similarity is greater than 60%
if max_similarity > 0.6:
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    label = QLabel("Tebrikler! Algoritmanız Harika bir sonuç verdi.")
    layout.addWidget(label)
    
    label.setFont(QFont("Arial", 16)) 
    window.setLayout(layout)
    window.show()
    app.exec_()
else:
    import selenium.webdriver as webdriver
    
    # Open YouTube link
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""Maalesef, sonuçlar beklediğiniz gibi olmadı.
    Bu durumda, kendinizi geliştirmeniz gerektiğini anlamak önemlidir.
    Başarı için sürekli öğrenmeye ve kendinizi yenilemeye
    açık olmalısınız. Başarısızlık, yeni fırsatlar 
    ve deneyimler için bir kapı açabilir. Diğer insanların da etkilenebileceğini 
    unutmamak önemlidir, çünkü etrafımızdaki 
    insanlarla etkileşimlerimiz ve eylemlerimiz 
    toplumun genel gelişimini etkileyebilir.
    Bu nedenle, hatalardan ders çıkararak ve kendinizi geliştirerek 
    hem kişisel başarıyı hem de etrafınızdaki insanları olumlu yönde 
    etkileme fırsatını yakalayabilirsiniz.""")
    layout.addWidget(label)
    label.setFont(QFont("Arial", 16)) 

    window.setLayout(layout)
    window.show()
    app.exec_()
    driver = webdriver.Chrome()
    driver.get("https://youtu.be/WgFUJ2KkvIM")
    time.sleep(1)
    driver.maximize_window()
    time.sleep(5)
    
    
    # Close the browser
    driver.quit()





