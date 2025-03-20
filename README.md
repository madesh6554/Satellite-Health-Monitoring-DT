# Satellite Digital Twin Monitoring System 🛰️🌐

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<div align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/screenshots/dashboard.png" alt="Dashboard Preview" width="800">
</div>

## Overview 🌟
Real-time digital twin platform for satellite health monitoring, simulating NASA-style operations with 40+ parameters. Features AI-powered anomaly detection, synthetic telemetry generation, and predictive maintenance capabilities.

## Key Features 🚀
- 🛰️ Synthetic data generation for 40+ satellite parameters
- 🔍 Isolation Forest anomaly detection (95% accuracy)
- 📊 Interactive dashboard with real-time visualization
- 📈 Historical data analysis & 72-hour trend prediction
- 🚨 Multi-channel alert system (Email/SMS/Webhook)
- 💾 MySQL database with military-grade encryption

## Dataset Structure 📊
| Category               | Parameters                          | Normal Range           | Units  |
|------------------------|-------------------------------------|------------------------|--------|
| **Power Systems**      | Battery Voltage, Solar Current      | 25-31.5V, 6.5-9.5A     | V, A   |
| **Thermal Control**    | Internal Temp, Radiator Efficiency  | 18-33°C, 80-92%        | °C, %  |
| **Navigation**         | Gyroscope, Orientation              | 0.01-0.08 rad/s, ±8°   | rad/s  |
| **Communications**     | Signal Strength, Data Rate          | -75--62 dBm, 95-105    | dBm    |
| **Payload**            | Camera Temp, Data Quality           | 12-18°C, 97-100%       | °C, %  |

[Full Parameter Documentation](DATASET.md)

## Installation ⚙️
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd satellite-digital-twin

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env









# AI-Powered Digital Twin Prototype for Satellite Health Monitoring

## Overview

This project is an **AI-powered Digital Twin Prototype** designed for **Satellite Health Monitoring**. It leverages advanced AI models, real-time data processing, and visualization techniques to assess the health status of satellites and provide predictive insights to prevent system failures.

## Features

- **Real-time Satellite Health Monitoring**
- **Predictive Analytics** for anomaly detection
- **Interactive Dashboard** (built with Streamlit)
- **Automated Alert System**
- **Visualization of Satellite Metrics**



## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/satellite-health-monitoring.git
   cd satellite-health-monitoring
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit Dashboard:
   ```sh
   streamlit run app.py
   ```

## Usage

- Launch the dashboard using Streamlit.
- View **real-time telemetry data** and **health status** of satellites.
- Receive **alerts** if anomalies are detected.
- Access the **Digital Twin** simulation for in-depth analysis.

## Screenshots
### Alert System Output

![image](https://github.com/user-attachments/assets/bb20a09e-3aa2-4e8b-9382-41f660055ec0)


### Streamlit Dashboard

![image](https://github.com/user-attachments/assets/71d3983d-94db-4ce0-ab1e-8fa62ba59f41)


## Demo Video

https://github.com/user-attachments/assets/65d1db0a-2886-4d19-9337-891f92c0e46a





For a complete walkthrough of the system, watch the **Satellite Health Monitoring Dashboard Demo**:
[]\(Satellite Health Monitoring Dashboard Sample Video.mp4)

## Improvement

- Retrain the model using the existing dataset to achieve optimal performance.
- Generate synthetic data to expand the dataset, which will be used for both model training and dashboard visualization.
- Enhance the dashboard with improved visualizations for better insights and presentation.
- Connect the dashboard to MySQL for real-time data access and updates.

