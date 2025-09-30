from flask import Flask, render_template_string, jsonify
import subprocess
import json

app = Flask(__name__)

# Google Material Design 3 HTML template
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PAI Infrastructure</title>
    
    <!-- Google Fonts - Roboto (Google's standard) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    
    <style>
        /* Google Material Design 3 Color System */
        :root {
            --google-blue: #1a73e8;
            --google-blue-hover: #1557b0;
            --google-blue-light: #e8f0fe;
            --google-green: #137333;
            --google-red: #d93025;
            --google-yellow: #f9ab00;
            --google-gray-50: #f8f9fa;
            --google-gray-100: #f1f3f4;
            --google-gray-200: #e8eaed;
            --google-gray-300: #dadce0;
            --google-gray-400: #bdc1c6;
            --google-gray-500: #9aa0a6;
            --google-gray-600: #5f6368;
            --google-gray-700: #3c4043;
            --google-gray-800: #202124;
            --google-gray-900: #1a1a1a;
            
            /* Material Design Elevation Shadows */
            --elevation-1: 0 1px 2px 0 rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
            --elevation-2: 0 1px 2px 0 rgba(60, 64, 67, 0.3), 0 2px 6px 2px rgba(60, 64, 67, 0.15);
            --elevation-3: 0 1px 3px 0 rgba(60, 64, 67, 0.3), 0 4px 8px 3px rgba(60, 64, 67, 0.15);
            --elevation-4: 0 2px 3px 0 rgba(60, 64, 67, 0.3), 0 6px 10px 4px rgba(60, 64, 67, 0.15);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--google-gray-50);
            color: var(--google-gray-800);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }
        
        /* Google-style header */
        .header {
            text-align: center;
            margin-bottom: 48px;
        }
        
        .header h1 {
            font-size: 48px;
            font-weight: 400;
            color: var(--google-gray-800);
            margin-bottom: 16px;
            letter-spacing: -0.5px;
        }
        
        .header .subtitle {
            font-size: 20px;
            color: var(--google-gray-600);
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* Material Design Cards */
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: var(--elevation-1);
            transition: all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);
            overflow: hidden;
        }
        
        .card:hover {
            box-shadow: var(--elevation-3);
            transform: translateY(-1px);
        }
        
        .card-content {
            padding: 24px;
        }
        
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .card-icon {
            margin-right: 12px;
            color: var(--google-blue);
            font-size: 24px;
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 500;
            color: var(--google-gray-800);
            flex: 1;
        }
        
        .card-description {
            color: var(--google-gray-600);
            font-size: 14px;
            line-height: 1.4;
        }
        
        /* Status indicators */
        .status-indicator {
            padding: 4px 8px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-active {
            background-color: #e8f5e8;
            color: var(--google-green);
        }
        
        .status-inactive {
            background-color: #fce8e6;
            color: var(--google-red);
        }
        
        .status-checking {
            background-color: #fff3cd;
            color: var(--google-yellow);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        /* Grid layouts */
        .grid {
            display: grid;
            gap: 24px;
        }
        
        .grid-cols-1 { grid-template-columns: 1fr; }
        .grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
        
        @media (max-width: 768px) {
            .grid-cols-2, .grid-cols-3, .grid-cols-4 { 
                grid-template-columns: 1fr; 
            }
            
            .header h1 { font-size: 36px; }
            .header .subtitle { font-size: 18px; }
            .container { padding: 16px; }
        }
        
        /* Sections */
        .section {
            margin-bottom: 48px;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 400;
            color: var(--google-gray-800);
            margin-bottom: 24px;
            display: flex;
            align-items: center;
        }
        
        .section-title .material-icons {
            margin-right: 12px;
            color: var(--google-blue);
        }
        
        /* Links */
        .service-link {
            display: block;
            text-decoration: none;
            color: inherit;
        }
        
        .service-link .card:hover {
            border-left: 4px solid var(--google-blue);
        }
        
        /* Google-style button */
        .google-btn {
            display: inline-flex;
            align-items: center;
            padding: 10px 24px;
            border-radius: 4px;
            border: 1px solid var(--google-gray-300);
            background: white;
            color: var(--google-gray-700);
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
        }
        
        .google-btn:hover {
            box-shadow: var(--elevation-1);
            border-color: var(--google-gray-400);
        }
        
        .google-btn-primary {
            background: var(--google-blue);
            color: white;
            border-color: var(--google-blue);
        }
        
        .google-btn-primary:hover {
            background: var(--google-blue-hover);
            border-color: var(--google-blue-hover);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 64px;
            padding-top: 32px;
            border-top: 1px solid var(--google-gray-200);
            color: var(--google-gray-500);
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>PAI Infrastructure</h1>
            <p class="subtitle">Your centralized portal for monitoring and managing your Personal AI Infrastructure</p>
        </header>

        <section class="section">
            <h2 class="section-title">
                <span class="material-icons">dashboard</span>
                System Status
            </h2>
            <div class="grid grid-cols-4">
                <div class="card">
                    <div class="card-content">
                        <div class="card-header">
                            <span class="material-icons card-icon">computer</span>
                            <span class="card-title">HP Server</span>
                            <span id="node-exporter-status" class="status-indicator status-checking">Checking</span>
                        </div>
                        <p class="card-description">System metrics and monitoring</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-content">
                        <div class="card-header">
                            <span class="material-icons card-icon">timeline</span>
                            <span class="card-title">Prometheus</span>
                            <span id="prometheus-status" class="status-indicator status-checking">Checking</span>
                        </div>
                        <p class="card-description">Metrics collection</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-content">
                        <div class="card-header">
                            <span class="material-icons card-icon">analytics</span>
                            <span class="card-title">Grafana</span>
                            <span id="grafana-status" class="status-indicator status-checking">Checking</span>
                        </div>
                        <p class="card-description">Visualization dashboards</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-content">
                        <div class="card-header">
                            <span class="material-icons card-icon">video_library</span>
                            <span class="card-title">YouTube System</span>
                            <span id="jimmy-youtube-status" class="status-indicator status-checking">Checking</span>
                        </div>
                        <p class="card-description">Media automation</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">
                <span class="material-icons">apps</span>
                Services & Dashboards
            </h2>
            <div class="grid grid-cols-3">
                <a href="http://192.168.1.34:3000" target="_blank" class="service-link">
                    <div class="card">
                        <div class="card-content">
                            <div class="card-header">
                                <span class="material-icons card-icon">bar_chart</span>
                                <span class="card-title">Grafana Dashboards</span>
                            </div>
                            <p class="card-description">Visualize all your PAI metrics and performance data</p>
                            <div style="margin-top: 12px;">
                                <span class="google-btn google-btn-primary">
                                    <span class="material-icons" style="font-size: 16px; margin-right: 8px;">open_in_new</span>
                                    Open Dashboard
                                </span>
                            </div>
                        </div>
                    </div>
                </a>
                
                <a href="http://192.168.1.34:9090" target="_blank" class="service-link">
                    <div class="card">
                        <div class="card-content">
                            <div class="card-header">
                                <span class="material-icons card-icon">monitor_heart</span>
                                <span class="card-title">Prometheus Metrics</span>
                            </div>
                            <p class="card-description">Raw metrics collection and alerting configuration</p>
                            <div style="margin-top: 12px;">
                                <span class="google-btn">
                                    <span class="material-icons" style="font-size: 16px; margin-right: 8px;">open_in_new</span>
                                    View Metrics
                                </span>
                            </div>
                        </div>
                    </div>
                </a>
                
                <a href="http://192.168.1.34:5001" target="_blank" class="service-link">
                    <div class="card">
                        <div class="card-content">
                            <div class="card-header">
                                <span class="material-icons card-icon">smart_display</span>
                                <span class="card-title">YouTube Automation</span>
                            </div>
                            <p class="card-description">Manage YouTube downloads and Plex integration</p>
                            <div style="margin-top: 12px;">
                                <span class="google-btn">
                                    <span class="material-icons" style="font-size: 16px; margin-right: 8px;">open_in_new</span>
                                    Manage Downloads
                                </span>
                            </div>
                        </div>
                    </div>
                </a>
                
                <a href="http://192.168.1.17:32400" target="_blank" class="service-link">
                    <div class="card">
                        <div class="card-content">
                            <div class="card-header">
                                <span class="material-icons card-icon">movie</span>
                                <span class="card-title">Plex Media Server</span>
                            </div>
                            <p class="card-description">Stream your media library anywhere</p>
                            <div style="margin-top: 12px;">
                                <span class="google-btn">
                                    <span class="material-icons" style="font-size: 16px; margin-right: 8px;">play_circle</span>
                                    Launch Plex
                                </span>
                            </div>
                        </div>
                    </div>
                </a>
                
                <a href="http://192.168.1.34:9100/metrics" target="_blank" class="service-link">
                    <div class="card">
                        <div class="card-content">
                            <div class="card-header">
                                <span class="material-icons card-icon">memory</span>
                                <span class="card-title">HP Server Metrics</span>
                            </div>
                            <p class="card-description">Direct system performance data from HP server</p>
                            <div style="margin-top: 12px;">
                                <span class="google-btn">
                                    <span class="material-icons" style="font-size: 16px; margin-right: 8px;">code</span>
                                    Raw Data
                                </span>
                            </div>
                        </div>
                    </div>
                </a>
                
                <a href="http://192.168.1.17:9100/metrics" target="_blank" class="service-link">
                    <div class="card">
                        <div class="card-content">
                            <div class="card-header">
                                <span class="material-icons card-icon">server</span>
                                <span class="card-title">Plex Server Metrics</span>
                            </div>
                            <p class="card-description">System performance data for media server</p>
                            <div style="margin-top: 12px;">
                                <span class="google-btn">
                                    <span class="material-icons" style="font-size: 16px; margin-right: 8px;">code</span>
                                    Raw Data
                                </span>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        </section>

        <footer class="footer">
            <p>PAI Infrastructure • Built with Google Material Design 3</p>
        </footer>
    </div>

    <script>
        function updateStatus(elementId, isActive) {
            const element = document.getElementById(elementId);
            if (isActive) {
                element.textContent = 'Active';
                element.className = 'status-indicator status-active';
            } else {
                element.textContent = 'Offline';
                element.className = 'status-indicator status-inactive';
            }
        }

        async function fetchStatus() {
            try {
                const response = await fetch('/api/status_all');
                const data = await response.json();
                updateStatus('node-exporter-status', data.node_exporter_hp);
                updateStatus('prometheus-status', data.prometheus);
                updateStatus('grafana-status', data.grafana);
                updateStatus('jimmy-youtube-status', data.jimmy_youtube);
            } catch (error) {
                console.error('Error fetching status:', error);
                // Set all to offline on error
                ['node-exporter-status', 'prometheus-status', 'grafana-status', 'jimmy-youtube-status'].forEach(id => {
                    updateStatus(id, false);
                });
            }
        }

        // Fetch status every 10 seconds
        setInterval(fetchStatus, 10000);
        
        // Initial fetch after 1 second
        setTimeout(fetchStatus, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/api/status_all')
def status_all():
    status = {
        "node_exporter_hp": False,
        "prometheus": False,
        "grafana": False,
        "jimmy_youtube": False,
    }
    
    # Check Node Exporter (HP)
    try:
        result = subprocess.run(['ssh', 'jbyrd@192.168.1.34', 'curl -s http://192.168.1.34:9100/metrics'], capture_output=True, text=True, timeout=5)
        if "node_cpu_seconds_total" in result.stdout:
            status["node_exporter_hp"] = True
    except Exception:
        pass

    # Check Prometheus
    try:
        result = subprocess.run(['ssh', 'jbyrd@192.168.1.34', 'curl -s http://192.168.1.34:9090/-/healthy'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "Prometheus is Healthy" in result.stdout:
            status["prometheus"] = True
    except Exception:
        pass

    # Check Grafana
    try:
        result = subprocess.run(['ssh', 'jbyrd@192.168.1.34', 'curl -s http://192.168.1.34:3000/api/health'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "database" in result.stdout:
            status["grafana"] = True
    except Exception:
        pass

    # Check Jimmy's YouTube
    try:
        result = subprocess.run(['ssh', 'jbyrd@192.168.1.34', 'curl -s http://192.168.1.34:5001/api/status'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "total_channels" in result.stdout:
            status["jimmy_youtube"] = True
    except Exception:
        pass

    return jsonify(status)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "pai-portal"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
