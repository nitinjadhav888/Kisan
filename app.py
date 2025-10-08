# kisan_connect.py

from flask import Flask, render_template_string, request

# --- Application Setup ---
app = Flask(__name__)

# --- In-Memory Data ---
MANDI_PRICES = {
    'Pune, Maharashtra': {
        'Wheat': {'price': '₹2,500/quintal', 'date': '2025-09-19'},
        'Onion': {'price': '₹2,200/quintal', 'date': '2025-09-19'},
    },
    'Ludhiana, Punjab': {
        'Wheat': {'price': '₹2,650/quintal', 'date': '2025-09-19'},
        'Rice': {'price': '₹3,500/quintal', 'date': '2025-09-19'},
    },
    'Patna, Bihar': {
        'Rice': {'price': '₹3,200/quintal', 'date': '2025-09-19'},
        'Potato': {'price': '₹1,800/quintal', 'date': '2025-09-19'},
    },
}

WEATHER_FORECAST = {
    'Pune': 'Partly cloudy with a chance of rain. Max Temp: 28°C.',
    'Ludhiana': 'Clear skies. Max Temp: 32°C.',
    'Patna': 'High humidity with scattered thunderstorms. Max Temp: 30°C.',
}

BEST_PRACTICES = {
    'pest_control': "Regularly inspect crops for early signs of pests. Use neem-based pesticides as an organic alternative.",
    'soil_health': "Practice crop rotation to maintain soil fertility and prevent nutrient depletion.",
    'irrigation': "Use drip irrigation systems to save water and deliver it directly to the roots.",
}

# --- HTML Templates ---
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Kisan Connect</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8f0; color: #333; }
        .container { max-width: 900px; margin: auto; background-color: #fff; padding: 25px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h1, h2 { text-align: center; color: #006400; }
        .nav-links a { display: inline-block; padding: 10px 20px; margin: 10px; background-color: #3cb371; color: white; border-radius: 5px; text-decoration: none; }
        .nav-links { text-align: center; margin-bottom: 20px; }
        .section { margin-top: 30px; border-top: 2px solid #ddd; padding-top: 20px; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #e8f5e9; margin: 8px 0; padding: 12px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌾 Kisan Connect: Empowering Farmers</h1>
        <div class="nav-links">
            <a href="/mandi-prices">Mandi Prices</a>
            <a href="/weather">Weather Forecast</a>
            <a href="/best-practices">Best Practices</a>
        </div>
        <p style="text-align: center;">Your one-stop platform for agricultural information.</p>
    </div>
</body>
</html>
"""

MANDI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Mandi Prices</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8f0; }
        .container { max-width: 900px; margin: auto; background-color: #fff; padding: 25px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h1 { color: #006400; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #3cb371; color: white; }
        a { color: #3cb371; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 Mandi Prices</h1>
        <p>Real-time prices from key markets in India.</p>
        <table>
            <thead>
                <tr>
                    <th>Market</th>
                    <th>Crop</th>
                    <th>Price</th>
                    <th>Last Updated</th>
                </tr>
            </thead>
            <tbody>
                {{ table_rows | safe }}
            </tbody>
        </table>
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>
"""

WEATHER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Forecast</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8f0; }
        .container { max-width: 900px; margin: auto; background-color: #fff; padding: 25px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h1 { color: #006400; text-align: center; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #e8f5e9; padding: 15px; margin: 10px 0; border-radius: 5px; }
        a { color: #3cb371; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌧️ Weather Forecast</h1>
        <ul>
            {% for city, forecast in weather_data.items() %}
                <li><strong>{{ city }}:</strong> {{ forecast }}</li>
            {% endfor %}
        </ul>
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>
"""

PRACTICES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Best Practices</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8f0; }
        .container { max-width: 900px; margin: auto; background-color: #fff; padding: 25px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h1 { color: #006400; text-align: center; }
        div.practice { background-color: #e8f5e9; padding: 15px; margin: 10px 0; border-radius: 5px; }
        h3 { color: #006400; }
        a { color: #3cb371; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 Agricultural Best Practices</h1>
        {% for title, content in practices.items() %}
            <div class="practice">
                <h3>{{ title.replace('_', ' ').title() }}</h3>
                <p>{{ content }}</p>
            </div>
        {% endfor %}
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>
"""

# --- Routes (URL Endpoints) ---
@app.route('/')
def home():
    """Serves the home page."""
    return render_template_string(HOME_HTML)

@app.route('/mandi-prices')
def mandi_prices():
    """Generates the mandi prices page."""
    table_rows = ""
    for market, crops in MANDI_PRICES.items():
        for crop, data in crops.items():
            table_rows += f"<tr><td>{market}</td><td>{crop}</td><td>{data['price']}</td><td>{data['date']}</td></tr>"
    
    return render_template_string(MANDI_HTML, table_rows=table_rows)

@app.route('/weather')
def weather():
    """Generates the weather forecast page."""
    return render_template_string(WEATHER_HTML, weather_data=WEATHER_FORECAST)

@app.route('/best-practices')
def best_practices():
    """Generates the best practices page."""
    return render_template_string(PRACTICES_HTML, practices=BEST_PRACTICES)

# --- Main Entry Point ---
if __name__ == '__main__':
    app.run(debug=True)