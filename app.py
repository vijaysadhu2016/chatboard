from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import base64
from PIL import Image
import io
import gevent.monkey
gevent.monkey.patch_all()

app = Flask(__name__)

# Get environment variables with fallbacks
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chat.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

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
            'timestamp': self.timestamp.strftime('%d %b %y, %I:%M %p')
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
        username = request.form.get('username')
        password = request.form.get('password')
        
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
    if 'username' not in session:
        return
    
    current_time = datetime.now()
    message = {
        'username': session['username'],
        'content': data.get('content', ''),
        'type': data.get('type', 'text'),
        'timestamp': current_time.strftime('%d %b %y, %I:%M %p')
    }
    
    if message['type'] == 'image':
        try:
            image_data = message['content'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Generate unique filename
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session['username']}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save image
            image.save(filepath)
            message['content'] = f"/uploads/{filename}"
        except Exception as e:
            print(f"Error processing image: {e}")
            return
    
    # Store message in database
    try:
        db_message = Message(
            username=message['username'],
            content=message['content'],
            message_type=message['type'],
            timestamp=current_time
        )
        db.session.add(db_message)
        db.session.commit()
        
        # Add message ID to the response
        message['id'] = db_message.id
        
        emit('new_message', message, broadcast=True)
    except Exception as e:
        print(f"Error saving message: {e}")
        db.session.rollback()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False) 