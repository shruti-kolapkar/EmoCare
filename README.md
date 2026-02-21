# 🧠 Emotion Aware Patient Monitoring System  
### IoT-Based Real-Time Stress & Anxiety Detection

---

## 📌 Introduction
The **Emotion Aware Patient Monitoring System** is an intelligent healthcare monitoring solution that combines **IoT sensors**, **ESP32**, **Machine Learning**, and a **Streamlit-based dashboard** to continuously monitor patient vital signs and emotional stress levels.

Unlike traditional systems that focus only on physical parameters, this system also considers the **emotional and mental state** of the patient, enabling early detection of stress and anxiety.

---

## ❗ Problem Statement
Conventional patient monitoring systems:
- Monitor only physical vitals
- Ignore emotional health
- Lack intelligent prediction and recommendations
- Do not support remote and continuous monitoring effectively

This project solves these problems by integrating **emotion-aware intelligence** with real-time IoT monitoring and alerts.

---

## 🎯 Objectives
- Collect real-time physiological data using IoT sensors  
- Detect stress and emotional states using ML and AI techniques  
- Visualize patient data through an interactive dashboard  
- Trigger alerts when abnormal conditions are detected  
- Enable future-ready healthcare with intelligent recommendations  

---

## 🧩 System Architecture
The system consists of the following layers:

1. **Sensor Layer**
   - ECG Sensor – heart activity
   - Piezo Sensor – respiration rate
   - max30102 Sensor – emotional and stress-related signals (real or simulated)
   - GSR
   - DS18B20
   - ESP32 camera
   - Rfid-rc255

2. **Controller Layer**
   - ESP32 reads sensor values
   - Sends processed data via WiFi

3. **Cloud Layer**
   - ThingSpeak stores and manages live sensor data

4. **Application Layer**
   - Streamlit dashboard displays real-time graphs and alerts

5. **Intelligence Layer**
   - Machine learning model predicts stress levels
   - Alert system notifies caregivers

---

## 🛠️ Technologies Used

### 💻 Software
- Python  
- Streamlit  
- MicroPython  
- Plotly  
- Scikit-learn  

### 🔧 Hardware
- ESP32  
- ECG Sensor  
- Piezo Sensor  
- EEG Sensor (optional / simulated)  

### ☁️ Cloud & Communication
- ThingSpeak  
- Email / SMS / WhatsApp APIs  

---

## Author
### Aarya Falle
