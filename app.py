from flask import Flask, render_template, request, jsonify, g, url_for, redirect, session
import openai
import pyttsx3
import speech_recognition as sr
import sqlite3
import webbrowser
import subprocess
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

# Set OpenAI API key
openai.api_key = "Your-API_Key-Here"

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Function to generate response using GPT-3
def generate_response(prompt):
    if "open" in prompt.lower():
        open_website(prompt)
        return "Opening website..."
    elif "time" in prompt.lower():
        current_time = datetime.now().strftime("%I:%M %p")  # Get current time in HH:MM AM/PM format
        return f"The current time is {current_time}."
    elif "date" in prompt.lower():
        current_date = datetime.now().strftime("%B %d, %Y")  # Get current date in Month Day, Year format
        return f"Today's date is {current_date}."
    else:
        # If the prompt doesn't match any predefined patterns, use GPT-3 to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()

def open_website(query):
    if "youtube" in query.lower():
        webbrowser.open("https://www.youtube.com")
        return "YouTube"
    elif "spotify" in query.lower():
        webbrowser.open("https://open.spotify.com")
        return "Spotify"
    elif "whatsapp" in query.lower():
        webbrowser.open("https://web.whatsapp.com")
        return "WhatsApp"
    elif "gmail" in query.lower():
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        return "GMail"
    elif "netflix" in query.lower():
        webbrowser.open("https://www.netflix.com")
        return "Netflix"
    elif "linkedin" in query.lower():
        webbrowser.open("https://in.linkedin.com")
        return "LinkedIn"
    elif "google" in query.lower():
        webbrowser.open("https://www.google.com")
        return "Google"
    elif "instagram" in query.lower():
        webbrowser.open("https://www.instagram.com")
        return "Instagram"
    elif "maps" in query.lower():
        webbrowser.open("https://www.google.com/maps")
        return "Maps"
    else:
        return None  # Return None if the website is not recognized

# Function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def handle_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Say your question...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        if query:
            if query.lower() == "history":
                # Retrieve past interactions from database
                past_interactions = get_past_interactions()

                if past_interactions:
                    interactions = "<br>".join([f"Question: {interaction[1]}<br>Answer: {interaction[2]}<br>--------------------<br>" for interaction in past_interactions])
                    return "Past Interactions:<br>" + interactions
                else:
                    return "No past interactions found."
            else:
                return query
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)
    except Exception as e:
        return "An error occurred: {}".format(e)

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create tables if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

# Create contacts table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone_number TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS interactions
             (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT)''')

conn.commit()

# Function to get the database connection
def get_db():
    if 'db' not in g:
        # Create a new database connection if it doesn't exist
        g.db = sqlite3.connect('users.db')
        g.db.row_factory = sqlite3.Row  # Enable row access by column name
    return g.db

# Function to get the database cursor
def get_cursor():
    db = get_db()
    if 'cursor' not in g:
        # Create a new cursor if it doesn't exist
        g.cursor = db.cursor()
    return g.cursor

def get_past_interactions():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM interactions")
    past_interactions = c.fetchall()

    interaction_strings = []
    for interaction in past_interactions:
        question = interaction[1]
        answer = interaction[2]
        interaction_strings.append(f"Question: {question}<br>Answer: {answer}<br>--------------------<br>")

    return "\n".join(interaction_strings)


# Function to authenticate user
def authenticate_user(username, password):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

# Function to register user
def register_user(username, password):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            return redirect(url_for('home'))  # Redirect to home page
        else:
            return render_template('login.html')
    return render_template('login.html')

# Route for home page after successful login
@app.route('/home')
def home():
    return render_template('home.html')

# Route for registration
@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('login'))  # Redirect to the home route (index.html)
    return render_template('registration.html')

conversation_history = []  # Initialize an empty list to store conversation history

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    print("User input:", user_input)  # Debug print

    if user_input.lower() == "voice":
        response = handle_voice_input()
        speak_text(response)
    elif user_input.lower() == "history":  # Check if user requests history
        # Retrieve past interactions from database
        past_interactions = get_past_interactions()
        if past_interactions:
            response = "Past Interactions:<br><br>" + past_interactions
        else:
            response = "No past interactions found."
    elif user_input.lower() == "time":  # Check if user requests the current time
        current_time = datetime.now().strftime("%I:%M %p")  # Get current time in HH:MM AM/PM format
        response = f"The current time is {current_time}."
    elif "open" in user_input.lower():  # Check if user requests to open a website
        website_name = open_website(user_input)
        if website_name:
            response = f"Opening {website_name}..."
        else:
            response = "Website not recognized."
    elif user_input.lower().startswith("add contact"):
        # Extract the name and phone number from the user input
        parts = user_input.split("add contact ")[1].split(",")
        if len(parts) == 2:
            name, phone_number = parts
            try:
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute("INSERT INTO contacts (name, phone_number) VALUES (?, ?)", (name.strip(), phone_number.strip()))
                conn.commit()
                response = 'Contact added successfully.'
            except Exception as e:
                response = f'Error adding contact: {str(e)}'
            finally:
                conn.close()
        else:
            response = 'Please provide both name and phone number for the contact.'
    elif user_input.lower().startswith("call "):
        contact_name = user_input.split("call ")[1]
        return jsonify({'response': f"make_call_{contact_name}"})
    else:
        # Get the last question from conversation history if it exists
        last_question = conversation_history[-1][0] if conversation_history else ""
        
        # Concatenate current question with last question for context
        prompt = f"User: {last_question}\n {user_input}"
        print("Prompt:", prompt)  # Debug print
        response = generate_response(prompt)
        
        # Update conversation history with current question and response
        conversation_history.append((user_input, response))
        print("Conversation history:", conversation_history)  # Debug print
        
        # Store the question and response in the database
        cursor = get_cursor()
        cursor.execute("INSERT INTO interactions (question, answer) VALUES (?, ?)", (user_input, response))
        get_db().commit()
        print("Stored in database")  # Debug print
        
    print("Response:", response)  # Debug print
    return jsonify({'response': response})


@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    if name and phone_number:
        try:
            conn = sqlite3.connect('users.db')  # Corrected database file name
            c = conn.cursor()
            c.execute("INSERT INTO contacts (name, phone_number) VALUES (?, ?)", (name, phone_number))
            conn.commit()
            return 'Contact added successfully.'
        except Exception as e:
            return str(e), 500  # Return the error message with status code 500
        finally:
            conn.close()  # Close the database connection
    else:
        return 'Name and phone number are required.', 400


@app.route('/make_call', methods=['POST'])
def make_call():
    contact_name = request.form['contact_name']
    
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT phone_number FROM contacts WHERE name = ?", (contact_name,))
        result = c.fetchone()
        
        if result:
            phone_number = result[0]
            subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{phone_number}'])
            return jsonify({'response': f'Calling {contact_name} at {phone_number}...'})
        else:
            return jsonify({'response': f'Contact {contact_name} not found'})
    except Exception as e:
        return jsonify({'response': f'An error occurred: {str(e)}'}), 500
    finally:
        conn.close()


@app.route('/send_message', methods=['POST'])
def send_message():
    contact_name = request.form['contact_name']
    message = request.form['message']
    
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT phone_number FROM contacts WHERE name = ?", (contact_name,))
        result = c.fetchone()
        
        if result:
            phone_number = result[0]
            subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO', '-d', f'sms:{phone_number}', '--es', 'sms_body', f'"{message}"'])
            return jsonify({'response': f'Message sent to {contact_name} at {phone_number}.'})
        else:
            return jsonify({'response': f'Contact {contact_name} not found.'})
    except Exception as e:
        return jsonify({'response': f'An error occurred: {str(e)}'}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)

