graph TD
    A[Data Generator] --> B[(MySQL Database)]
    B --> C{Anomaly Detector}
    C -->|Normal| D[Real-time Dashboard]
    C -->|Anomaly| E[Alert System]
    D --> F[Historical Analysis]
    E --> G[Notification Channels]