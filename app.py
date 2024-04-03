from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import pickle

app = Flask(__name__)
app.secret_key = '53a4737f02e21ed27eb0d0fa5ecc2669'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if User.query.filter_by(username=username).first():
                error = 'Username already exists!'
                return render_template('register.html', error=error)
            else:
                new_user = User(username=username, password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))

    return render_template('register.html')
     

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template("login.html")
    

@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect(url_for('login'))
    return 'Logged in as {}'.format(session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/aboutus')
def aboutUs():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route("/home")
def home():
    AnimalName=sorted(d['AnimalName'].unique())
    symptoms1=sorted(d['symptoms1'].unique())
    symptoms2=sorted(d['symptoms2'].unique())
    symptoms3=sorted(d['symptoms3'].unique())
    symptoms4=sorted(d['symptoms4'].unique())
    symptoms5=sorted(d['symptoms5'].unique())
    AnimalName.insert(0, 'Select animal')
    symptoms1.insert(0, 'Select symptom1')
    symptoms2.insert(0, 'Select symptom2')
    symptoms3.insert(0, 'Select symptom3')
    symptoms4.insert(0, 'Select symptom4')
    symptoms5.insert(0, 'Select symptom5')
    return render_template("home.html", AnimalName=AnimalName, symptoms1=symptoms1,
                           symptoms2=symptoms2, symptoms3=symptoms3, symptoms4=symptoms4,
                           symptoms5=symptoms5)
    

d = pd.read_csv('Animal_Disease_dataset.csv')
model = pickle.load(open("random1.pkl", "rb"))

@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction_text = ""  # Initialize prediction text
    
    if request.method == "POST":
        # Columns Reading
        AnimalName = request.form.get("AnimalName")
        symptoms1 = request.form.get("symptoms1")
        symptoms2 = request.form.get("symptoms2")
        symptoms3 = request.form.get("symptoms3")
        symptoms4 = request.form.get("symptoms4")
        symptoms5 = request.form.get("symptoms5")

        # Make prediction
        prediction = model.predict(pd.DataFrame([[AnimalName, symptoms1, symptoms2, symptoms3, symptoms4, symptoms5]],
                                                columns=['AnimalName', 'symptoms1', 'symptoms2', 'symptoms3',
                                                         'symptoms4', 'symptoms5']))
        prediction_text = "The Animal is suffering from {} Disease".format(prediction[0])  
        
        return render_template("predict1.html", prediction_text=prediction_text)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
