# Predictive Maintenance Control Center

AI-powered real-time predictive maintenance monitoring system for machine health monitoring, failure-risk prediction, live sensor analytics, and simulation-based condition monitoring.

## 🎥 Project Demonstration

▶️ **[Watch the Project Demo Video](https://drive.google.com/file/d/1LG50fqEfeutasxDoBdCoIyFlXKGogyJ1/view?usp=sharing)**

The demonstration shows the complete system running in real time, including:

- Live machine sensor data
- Failure probability prediction
- Dynamic risk levels
- Warning and critical alerts
- Real-time sensor charts
- Prediction history
- Simulation START / STOP / RESET controls
- WebSocket-based live communication
- System online/offline status

---

## 📌 Project Overview

The **Predictive Maintenance Control Center** is a full-stack AI application designed to monitor machine operating conditions and predict potential machine failure risks in real time.

The system combines:

- Machine learning
- FastAPI backend
- React frontend
- WebSocket communication
- Real-time data simulation
- Risk evaluation
- Interactive charts
- Prediction history

The project uses the **AI4I 2020 Predictive Maintenance Dataset** to simulate machine sensor measurements and generate real-time failure predictions.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Monitor machine sensor parameters in real time.
2. Predict the probability of machine failure.
3. Classify machine condition into different risk levels.
4. Generate real-time maintenance alerts.
5. Visualize sensor behavior through live charts.
6. Maintain recent prediction history.
7. Provide simulation controls for testing.
8. Demonstrate real-time AI integration using WebSockets.
9. Build a production-style predictive maintenance dashboard.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │     AI4I 2020 Dataset   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Simulation Service     │
                    │                         │
                    │ Reads machine data      │
                    │ row by row              │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Prediction Service    │
                    │                         │
                    │ Random Forest Model     │
                    │ Failure Probability     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Risk Service       │
                    │                         │
                    │ Normal / Warning /      │
                    │ Critical                │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    WebSocket Manager    │
                    │                         │
                    │ Real-time broadcasting  │
                    └────────────┬────────────┘
                                 │
                         WebSocket /ws
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     React Dashboard     │
                    │                         │
                    │ Sensors                 │
                    │ Risk                    │
                    │ Alerts                  │
                    │ Charts                  │
                    │ History                 │
                    └─────────────────────────┘
