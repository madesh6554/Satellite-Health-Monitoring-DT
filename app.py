import mysql.connector
import pandas as pd
import joblib
import streamlit as st
import numpy as np
import time
import smtplib
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest
import joblib
load_dotenv()
DIGITAL_TWIN_VERSION = "4.0"
SYSTEM_ID = "SAT-2025-DT-001"
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "table": os.getenv("DB_TABLE")
}

ALERT_CONFIG = {
    "sender": os.getenv("EMAIL_SENDER"),
    "receiver": os.getenv("EMAIL_RECEIVER"),
    "password": os.getenv("EMAIL_PASSWORD")
}


class DatabaseManager:
    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class DataGenerator:
    def __init__(self):
        self.last_timestamp = datetime.now() - timedelta(minutes=1)
        self.param_config = {
            "timestamp": None,
            
            # Power Systems
            "battery_voltage": (25.0, 31.5, 28.0, 1.0),
            "battery_current": (3.5, 6.5, 5.0, 0.5),  
            "state_of_charge": (65, 98, 80, 2),  
            "solar_panel_voltage": (92.0, 108.0, 100.0, 3.0),
            "solar_panel_current": (6.5, 9.5, 8.0, 0.4),  
            "solar_panel_efficiency": (18, 26, 22, 1.5),  
            "power_consumption": (130.0, 170.0, 150.0, 5.0),
            
            # Thermal Systems
            "internal_temp": (18.0, 33.0, 25.0, 2.0),
            "battery_temp": (26.0, 34.0, 30.0, 1.5),
            "solar_panel_temp": (32.0, 45.0, 40.0, 3.0),
            "radiator_temp": (16.0, 24.0, 20.0, 1.5),  
            "radiator_efficiency": (80, 92, 85, 2),  
            "thermal_gradient": (4, 6, 5, 0.5),
            
            # Navigation and Control
            "position": (350, 480, 400, 30),  
            "velocity": (7.5, 7.7, 7.6, 0.05),  
            "gyroscope": (0.01, 0.08, 0.05, 0.005),
            "magnetometer_rpm": (4850, 5150, 5000, 75),  
            "reaction_wheel_rpm": (2950, 3050, 3000, 25),
            
            # Communications
            "thruster_status": (0, 1, 0.98),  
            "signal_strength": (-75.0, -62.0, -70.0, 3.0),
            "data_rate": (95.0, 105.0, 100.0, 2.5),
            "packet_loss": (0.0, 3.0, 0.5, 0.2),
            
            # Payload and Sensors
            "payload_power": (47, 53, 50, 1.5),  
            "sensor_data_rate": (9.5, 10.5, 10.0, 0.3),  
            "camera_temp": (12.0, 18.0, 15.0, 1.5),
            "data_quality": (97, 100, 98.5, 0.5),
            
            # Error Handling and Latency
            "error_flags": (0, 1, 0.98),  
            "latency": (150, 250, 200, 25),  
            "bit_error_rate": (1e-7, 1e-5, 5e-6, 1e-6),
            
            # Anomaly and Fault Detection
            "sensor_discrepancies": (0, 1, 0.99),  
            "thruster_malfunctions": (0, 1, 0.995),  
            "thruster_efficiency": (92, 98, 95, 1.5),
            
            # Orientation and Throughput
            "orientation": (-8.0, 8.0, 0.0, 2.0),
            "throughput": (93.0, 98.0, 95.0, 1.5),
            
            # Anomaly Flags
            "power_anomalies": (0, 1, 0.97),  
            "thermal_anomalies": (0, 1, 0.97),  
            "aocs_faults": (0, 1, 0.98),  
            "payload_failures": (0, 1, 0.98)
        }

    def _generate_value(self, config):
        if len(config) == 4:
            min_val, max_val, mean, std = config
            return np.clip(random.gauss(mean, std), min_val, max_val)
        return 0 if random.random() < config[2] else 1

    def generate_data_point(self):
        self.last_timestamp += timedelta(minutes=1)
        data = {"timestamp": self.last_timestamp}
        for param, config in self.param_config.items():
            if param != "timestamp":
                data[param] = self._generate_value(config)
        if random.random() < 0.50:
            anomaly_type = random.choice(["power", "thermal", "aocs", "payload"])
            if anomaly_type == "power":
                data["battery_voltage"] *= 0.6
                data["power_anomalies"] = 1
            elif anomaly_type == "thermal":
                data["internal_temp"] += 20
                data["thermal_anomalies"] = 1
            elif anomaly_type == "aocs":
                data["gyroscope"] *= 10
                data["aocs_faults"] = 1
            else:
                data["payload_failures"] = 1
                data["data_quality"] = 0
        return data

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)  # Initialize Isolation Forest
        self.scaler = StandardScaler()
        self.features = [
            "battery_voltage", "battery_current", "state_of_charge",
            "solar_panel_voltage", "solar_panel_current", "solar_panel_efficiency",
            "power_consumption", "internal_temp", "battery_temp",
            "solar_panel_temp", "radiator_temp", "radiator_efficiency",
            "thermal_gradient", "position", "velocity", "gyroscope",
            "magnetometer_rpm", "reaction_wheel_rpm", "thruster_status",
            "signal_strength", "data_rate", "packet_loss", "payload_power",
            "sensor_data_rate", "camera_temp", "data_quality", "error_flags",
            "latency", "bit_error_rate", "sensor_discrepancies",
            "thruster_malfunctions", "thruster_efficiency", "orientation",
            "throughput", "power_anomalies", "thermal_anomalies",
            "aocs_faults", "payload_failures"
        ]
        self._train_model()

    def _train_model(self):
        # Generate some initial data to train the model
        generator = DataGenerator()
        data_points = [generator.generate_data_point() for _ in range(100)]
        df = pd.DataFrame(data_points)
        scaled_data = self.scaler.fit_transform(df[self.features])
        self.model.fit(scaled_data)

        # Save the trained model and scaler
        joblib.dump(self.model, "isolation_forest_model.pkl")
        joblib.dump(self.scaler, "scaler.pkl")

    def predict(self, data):
        df = pd.DataFrame([data])
        scaled_data = self.scaler.transform(df[self.features])
        return self.model.predict(scaled_data)[0] == -1

class AlertSystem:
    def send_alert(self, data):
        try:
            msg = MIMEMultipart()
            msg['From'] = ALERT_CONFIG["sender"]
            msg['To'] = ALERT_CONFIG["receiver"]
            msg['Subject'] = f"🚨 {SYSTEM_ID} Anomaly Alert - {data['timestamp']}"
            body = f"""
            CRITICAL ANOMALY DETECTED!
            System: {SYSTEM_ID}
            Timestamp: {data['timestamp']}
            Key Parameters:
            - Battery Voltage: {data['battery_voltage']:.2f} V
            - Internal Temperature: {data['internal_temp']:.1f}°C
            - Gyroscope: {data['gyroscope']:.4f} rad/s
            - Data Quality: {data['data_quality']:.1f}%"""
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(ALERT_CONFIG.get("sender"), ALERT_CONFIG.get("password"))
            server.sendmail(ALERT_CONFIG["sender"], ALERT_CONFIG["receiver"], msg.as_string())
            server.quit()
        except Exception as e:
            st.error(f"Alert failed: {str(e)}")

class SatelliteDashboard:
    def __init__(self, data_generator):
        self.generator = data_generator
        st.set_page_config(page_title=f"{SYSTEM_ID} Monitor", layout="wide")
        st.title(f"🌍 {SYSTEM_ID} Digital Twin Dashboard")
        self.status_container = st.empty()
        self.metrics_container = st.container()
        self.chart_container = st.empty()
        st.sidebar.button("🔄 Manual Refresh", key="refresh")
        if 'history' not in st.session_state:
            self._load_initial_data()

    def _load_initial_data(self):
        with DatabaseManager() as cursor:
            cursor.execute(f"SELECT * FROM {DB_CONFIG['table']} ORDER BY timestamp DESC LIMIT 10")
            st.session_state.history = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    def update_display(self, data, anomaly):
        self._update_status(data, anomaly)
        self._update_metrics(data)
        self._update_charts()

    def _update_status(self, data, anomaly):
        status_color = "#FF4B4B" if anomaly else "#0F9D58"
        self.status_container.markdown(f"""
            <div style="padding:20px; background:{status_color}10; border-radius:10px; margin-bottom:20px;
                        border-left:5px solid {status_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.1)">
                <h2 style="color:{status_color}; margin:0;">
                    {'🚨 CRITICAL ANOMALY DETECTED' if anomaly else '✅ SYSTEM NOMINAL'} 
                    <span style="float:right; font-size:0.8em; color:#666;">{DIGITAL_TWIN_VERSION}</span>
                </h2>
                <p style="margin:5px 0 0 0; color:#666;">
                    Last Update: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}
                </p>
            </div>""", unsafe_allow_html=True)

    def _update_metrics(self, data):
        with self.metrics_container:
            st.subheader("🔑 Key System Metrics")
            cols = st.columns(4)
            metrics = [
                ("⚡ Power Systems", ['battery_voltage', 'solar_panel_voltage', 'power_consumption']),
                ("🌡 Thermal Systems", ['internal_temp', 'battery_temp', 'solar_panel_temp']),
                ("🛰 AOCS", ['gyroscope', 'orientation', 'reaction_wheel_rpm']),
                ("📡 Communications", ['signal_strength', 'data_rate', 'packet_loss'])
            ]
            for col, (title, params) in zip(cols, metrics):
                with col:
                    st.markdown(self._build_metric_card(title, params, data), unsafe_allow_html=True)

    def _build_metric_card(self, title, params, data):
        html = f"""
        <div style="padding:15px; background:#FFFFFF; border-radius:10px; border:1px solid #EEE; 
                    margin-bottom:20px; box-shadow:0 2px 4px rgba(0,0,0,0.05)">
            <h4 style="margin:0 0 15px 0; color:#2C3E50;">{title}</h4>"""
        for param in params:
            value = data[param]
            config = self.generator.param_config[param]
            min_val, max_val = (config[0], config[1]) if len(config) == 4 else (None, None)
            unit = self._get_unit(param)
            
            # Format value safely
            try:
                formatted_value = f"{float(value):.2f}{unit}" if isinstance(value, (int, float)) else f"{value}{unit}"
            except:
                formatted_value = f"{value}{unit}"
            
            alert = "⚠️" if (min_val and max_val and not (min_val <= value <= max_val)) else ""
            
            html += f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#666; font-size:0.9em;">{param.replace('_', ' ').title()}</span>
                    <span style="color:#FF4B4B;">{alert}</span>
                </div>
                <div style="font-size:1.4em; color:#2C3E50;">
                    {formatted_value}
                </div>
                <div style="font-size:0.8em; color:#888;">
                    Range: {min_val:.1f}-{max_val:.1f}{unit}
                </div>
            </div>"""
        return html + "</div>"

    def _update_charts(self):
        with self.chart_container:
            st.subheader("📈 Real-Time Telemetry Trends (Last 10 Readings)")
            df = pd.DataFrame(st.session_state.history[-10:]).set_index('timestamp')
            fig = make_subplots(rows=2, cols=2, subplot_titles=(
                'Battery Voltage (V)', 'Internal Temperature (°C)', 
                'Gyroscope (rad/s)', 'Data Quality (%)'))
            fig.add_trace(go.Scatter(x=df.index, y=df.battery_voltage, name='Battery', line=dict(color='#4285F4')), 1, 1)
            fig.add_trace(go.Scatter(x=df.index, y=df.internal_temp, name='Temp', line=dict(color='#DB4437')), 1, 2)
            fig.add_trace(go.Scatter(x=df.index, y=df.gyroscope, name='Gyro', line=dict(color='#0F9D58')), 2, 1)
            fig.add_trace(go.Scatter(x=df.index, y=df.data_quality, name='Quality', line=dict(color='#F4B400')), 2, 2)
            fig.update_layout(height=600, showlegend=False, margin=dict(l=40, r=40, t=80, b=40),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    def _get_unit(self, param):
        units = {
            "voltage": "V", "current": "A", "temp": "°C", "efficiency": "%",
            "consumption": "W", "velocity": "km/s", "rpm": "RPM",
            "rate": "Mbps", "loss": "%", "error": "bps", "orientation": "°"
        }
        return next((v for k, v in units.items() if k in param.lower()), "")

def main():
    generator = DataGenerator()
    detector = AnomalyDetector()
    alert = AlertSystem()
    dashboard = SatelliteDashboard(generator)

    if 'last_update' not in st.session_state:
        st.session_state.update({
            'last_update': datetime.min,
            'history': [],
            'data': None,
            'anomaly': False
        })

    if (datetime.now() - st.session_state.last_update).total_seconds() >= 2:
        try:
            new_data = generator.generate_data_point()
            anomaly = detector.predict(new_data)
            
            # Add anomaly status to data
            new_data['anomaly'] = int(anomaly)

            with DatabaseManager() as cursor:
                # Insert with anomaly column
                columns = list(new_data.keys())
                values = list(new_data.values())
                cursor.execute(
                    f"INSERT INTO {DB_CONFIG['table']} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))})",
                    values
                )

            # Keep only last 10 entries
            st.session_state.history = [new_data] + st.session_state.history[:9]
            
            st.session_state.update({
                'last_update': datetime.now(),
                'data': new_data,
                'anomaly': anomaly
            })
            
            if anomaly:
                alert.send_alert(new_data)

        except Exception as e:
            st.error(f"System Error: {str(e)}")

    if st.session_state.data:
        dashboard.update_display(st.session_state.data, st.session_state.anomaly)

    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()