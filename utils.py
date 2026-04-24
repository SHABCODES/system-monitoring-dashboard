def check_thresholds(cpu, memory, disk):
    alerts = []

    if cpu > 85:
        alerts.append("High CPU Usage")
    if memory > 85:
        alerts.append("High Memory Usage")
    if disk > 90:
        alerts.append("High Disk Usage")

    return alerts