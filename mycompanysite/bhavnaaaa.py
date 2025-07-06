###########################################
#     Future Science Hub - Flask Site     #
#     Created by Harpal Makwana           #
#     Language: Python (Flask)            #
###########################################

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this

# ================== Mail Configuration ==================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'      # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password_here'     # Use app password if Gmail

mail = Mail(app)

# ================== Project Data ==================
projects_data = [
    {"title": "Smart Dustbin", "desc": "Ultrasonic-based automatic dustbin", "mrp": "₹799", "image": "smartdustbin.jpg", "category": "arduino"},
    {"title": "Voice-Controlled Car", "desc": "Bluetooth + Voice activated robot", "mrp": "₹1,299", "image": "voicecar.jpg", "category": "arduino"},
    {"title": "Obstacle Avoiding Robot", "desc": "IR + Ultrasonic navigation", "mrp": "₹999", "image": "obsticlerobot.jpg", "category": "arduino"},
    {"title": "Weather Monitor", "desc": "DHT11-based live temperature", "mrp": "₹599", "image": "weather.jpg", "category": "iot"},
    {"title": "Soil Moisture Planting", "desc": "Automatic watering system", "mrp": "₹799", "image": "soilplant.jpg", "category": "iot"},
    {"title": "Solar Tracker", "desc": "Dual axis servo controlled", "mrp": "₹1,499", "image": "solar.jpg", "category": "3dprint"},
    {"title": "3D Printed Robot", "desc": "Custom design with servo arm", "mrp": "₹1,899", "image": "robot3d.jpg", "category": "3dprint"},
    {"title": "Bluetooth Door Lock", "desc": "Security with mobile control", "mrp": "₹1,299", "image": "doorlock.jpg", "category": "arduino"}
]

# ================== Routes ==================

@app.route('/')
def home():
    return render_template('index.html', products=projects_data[:6])

@app.route('/projects')
def projects():
    return render_template('projects.html', products=projects_data)

@app.route('/projects/<category>')
def projects_by_category(category):
    filtered = [p for p in projects_data if p["category"] == category]
    return render_template('projects.html', products=filtered, category=category)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    image_folder = 'static/images/gallery'
    images = os.listdir(image_folder) if os.path.exists(image_folder) else []
    return render_template('gallery.html', images=images)

@app.route('/3dprint')
def three_d_print():
    filtered = [p for p in projects_data if p["category"] == "3dprint"]
    return render_template('projects.html', products=filtered, category="3D Print")

@app.route('/diagram')
def diagram():
    return render_template('diagram.html')

@app.route('/team')
def team():
    team_members = [
        {
            "name": "Harpal Makwana",
            "role": "Founder & Developer",
            "image": "/static/images/harpal.jpg",
            "social": {
                "linkedin": "https://linkedin.com/in/harpal",
                "instagram": "https://instagram.com/future_science_hub",
                "youtube": "https://youtube.com/@FutureScienceHub"
            }
        },
        {
            "name": "Payal Makwana",
            "role": "Content Creator",
            "image": "/static/images/payal.jpg",
            "social": {
                "instagram": "https://instagram.com/future_science_hub"
            }
        },
        {
            "name": "FutureBot 2025",
            "role": "AI Project Assistant",
            "image": "/static/images/futurebot.jpg"
        }
    ]
    return render_template('team.html', team=team_members)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(f"Message from {name}",
                      sender=email,
                      recipients=['your_email@gmail.com'])  # Replace with your receiving email
        msg.body = message

        try:
            mail.send(msg)
            flash('✅ Message sent successfully!')
        except Exception as e:
            print("Email error:", e)
            flash('❌ Message failed to send. Please check mail settings.')

        return redirect(url_for('contact'))

    return render_template('contact.html')

# ================== Run App ==================
if __name__ == '__main__':
    app.run(debug=True)
