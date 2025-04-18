from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import base64
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database Models
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), nullable=False)  # 'text' or 'image'
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'content': self.content,
            'type': self.message_type,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

# Hardcoded user credentials
USERS = {
    'admin': 'password123',
    'user1': 'password123',
    'user2': 'password123'
}

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get all messages from database
    messages = Message.query.order_by(Message.timestamp).all()
    messages = [msg.to_dict() for msg in messages]
    
    return render_template('chat.html', username=session['username'], messages=messages)

@socketio.on('send_message')
def handle_message(data):
    message = {
        'username': session['username'],
        'content': data['content'],
        'type': data['type'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if data['type'] == 'image':
        # Handle image upload
        try:
            image_data = data['content'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save image to static folder
            if not os.path.exists('static/uploads'):
                os.makedirs('static/uploads')
            
            filename = f"static/uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session['username']}.png"
            image.save(filename)
            message['content'] = filename
        except Exception as e:
            print(f"Error processing image: {e}")
            return
    
    # Store message in database
    db_message = Message(
        username=message['username'],
        content=message['content'],
        message_type=message['type'],
        timestamp=datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(db_message)
    db.session.commit()
    
    # Add message ID to the response
    message['id'] = db_message.id
    
    emit('new_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True) 