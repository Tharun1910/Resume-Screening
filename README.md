# 🩺 Skin Cancer Classification using ResNet50 & EfficientNetV2B0

An advanced deep-learning system for **multi-class skin lesion classification** using the HAM10000 dataset.  
The project uses **ResNet50** and **EfficientNetV2B0** for classification and **Grad-CAM** for visual interpretability.  
A fully interactive **Streamlit web application** enables image upload, prediction.

---

## 🌟 Key Features

### 🔹 ResNet50 & EfficientNetV2B0 — Classification Models
- Pretrained ImageNet models, fine-tuned on HAM10000.
- Achieved strong performance:  
  **ResNet50 → 85% validation accuracy**  
  **EfficientNetV2B0 → 82% validation accuracy**
- Predicts **7 dermatological lesion categories**.
- Generates Grad-CAM heatmaps highlighting important lesion regions.
- Produces predicted class, confidence score, and class-wise probability distribution.

### 🔹 Streamlit Web App
- Upload skin lesion images in real-time.
- Fast predictions on CPU/GPU.
- Simple and responsive UI.
- Grad-CAM visualization for model transparency.

---

## 🧠 Classes Predicted
- **Actinic Keratoses (AKIEC)**
- **Basal Cell Carcinoma (BCC)**
- **Benign Keratosis (BKL)**
- **Dermatofibroma (DF)**
- **Melanoma (MEL)**
- **Melanocytic Nevi (NV)**
- **Vascular Lesions (VASC)**

---

## 📊 Model Performance Summary

### **ResNet50**
- **Validation Accuracy:** **85%**
- **Training Behavior:**  
  • Smooth convergence with stable loss curves  
  • Improved performance after fine-tuning  
- **Interpretability:**  
  • Grad-CAM highlights lesion center and border irregularities  
  • Helps identify melanoma-specific patterns such as asymmetry and color variation

### **EfficientNetV2B0**
- **Validation Accuracy:** **82%**
- **Training Behavior:**  
  • Faster training due to lightweight architecture  
  • Stable learning with minimal overfitting  
- **Interpretability:**  
  • Grad-CAM shows high focus on pigment regions and lesion textures  
  • Model provides sharp and localized activation maps  

---

## 🔬 Results at a Glance

| Model               | Validation Accuracy | Strengths                             | Notes                      |
|---------------------|---------------------|----------------------------------------|----------------------------|
| **ResNet50**        | **85%**             | Strong generalization, stable tuning   | Best performing classifier |
| **EfficientNetV2B0**| **82%**             | Fast training, clean Grad-CAM maps     | Slightly lower accuracy    |
