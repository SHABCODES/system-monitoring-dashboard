from flask import Flask
import pandas as pd
import plotly.graph_objects as go
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    file_path = "data/system_data.csv"

    if not os.path.exists(file_path):
        return "No data yet..."

    try:
        df = pd.read_csv(file_path)

        if df.empty or len(df) < 10:
            return "Collecting data..."

        # Convert time
        df["time"] = pd.to_datetime(df["time"], unit='s')

        # Improve disk visibility
        df["disk"] = df["disk"] * 100

        # -------- ANOMALY DETECTION --------
        from sklearn.ensemble import IsolationForest
        model = IsolationForest(contamination=0.05, random_state=42)
        df["anomaly"] = model.fit_predict(df[["cpu", "memory", "disk"]])
        anomalies = df[df["anomaly"] == -1]

        # -------- GRAPH --------
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["time"], y=df["cpu"],
            mode='lines',
            name='CPU',
            line=dict(width=2),
            hovertemplate='CPU: %{y:.2f}%<br>Time: %{x}'
        ))

        fig.add_trace(go.Scatter(
            x=df["time"], y=df["memory"],
            mode='lines',
            name='Memory',
            line=dict(width=2),
            hovertemplate='Memory: %{y:.2f}%<br>Time: %{x}'
        ))

        fig.add_trace(go.Scatter(
            x=df["time"], y=df["disk"],
            mode='lines',
            name='Disk',
            line=dict(width=2),
            hovertemplate='Disk: %{y:.2f}%<br>Time: %{x}'
        ))

        # 🔴 Anomaly Points
        fig.add_trace(go.Scatter(
            x=anomalies["time"],
            y=anomalies["cpu"],
            mode='markers',
            name='Anomalies',
            marker=dict(color='red', size=8),
            hovertemplate='⚠ Anomaly<br>CPU: %{y:.2f}%'
        ))

        # -------- GRAPH LAYOUT --------
        fig.update_layout(
            template="plotly_dark",
            title="🚀 System Monitoring Dashboard",
            xaxis_title="Time",
            yaxis_title="Usage %",
            hovermode="x unified",
            xaxis=dict(rangeslider=dict(visible=True))  # 🔥 Slider added
        )

        # 🔴 Threshold Line
        fig.add_hline(
            y=80,
            line_dash="dash",
            line_color="red",
            annotation_text="High Usage Zone",
            annotation_position="top left"
        )

        # -------- SUMMARY --------
        latest = df.iloc[-1]

        # 🎨 Dynamic colors
        cpu_color = "red" if latest['cpu'] > 80 else "#1e293b"
        mem_color = "orange" if latest['memory'] > 85 else "#1e293b"
        disk_color = "#1e293b"

        # 🚦 Status logic
        status = "🟢 Normal"
        if latest["cpu"] > 85 or latest["memory"] > 90:
            status = "🔴 Critical"
        elif latest["cpu"] > 70:
            status = "🟠 Warning"

        # Recent anomalies
        recent_anomalies = anomalies.tail(20)

        # -------- HTML --------
        html = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="3">
            <style>
                body {{
                    background-color: #0f172a;
                    color: white;
                    font-family: Arial;
                    text-align: center;
                }}

                .card {{
                    display: inline-block;
                    padding: 15px;
                    margin: 10px;
                    border-radius: 12px;
                    width: 150px;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}

                .card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
                }}

                .title {{
                    font-size: 18px;
                }}

                .value {{
                    font-size: 24px;
                    font-weight: bold;
                }}

                h2 {{
                    margin-top: 10px;
                    font-size: 28px;
                }}
            </style>
        </head>

        <body>

        <h1>🚀 System Monitoring Dashboard</h1>
        <h2>{status}</h2>

        <div class="card" style="background:{cpu_color}">
            <div class="title">CPU</div>
            <div class="value">{latest['cpu']:.2f}%</div>
        </div>

        <div class="card" style="background:{mem_color}">
            <div class="title">Memory</div>
            <div class="value">{latest['memory']:.2f}%</div>
        </div>

        <div class="card" style="background:{disk_color}">
            <div class="title">Disk</div>
            <div class="value">{latest['disk']:.2f}%</div>
        </div>

        <div class="card" style="background:#1e293b">
            <div class="title">Recent Anomalies</div>
            <div class="value">{len(recent_anomalies)}</div>
        </div>

        {fig.to_html(full_html=False)}

        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=False)