from avengers import app, db, Message, mail
from flask import render_template, request, redirect, url_for

# Import for Forms
from avengers.forms import UserInfoForm, PhoneNumber, LoginForm


# Import for Models
from avengers.models import User, check_password_hash

# Import for Flask Login - Login Required, login_user, current_user, logout_user
from flask_login import login_required, login_user, current_user,logout_user



# Home Route
@app.route('/')
def home():
    customer_name = "Jackie"
    return render_template("home.html", customer_name = customer_name)


# Register Route
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = UserInfoForm()
    if request.method == "POST" and form.validate():
        # Get Information
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n", username, password, email)
        # Create an instance of user
        user = User(username,email,password)
        # Open and insert into database
        db.session.add(user)
        # Save info into database
        db.session.commit()

        # Flask Email Sender
        msg = Message(f'Thanks for Signing Up! {email}', recipients = [email])
        msg.body = ("Congrats on Signing Up!  Looking forward to your post!")
        msg.html = ('<h1> Welcome to May_Blog!</h1>' '<p>This will be fun!</p>')
        
        mail.send(msg)


        
    return render_template('register.html', form = form)

# Register Phone Number Route
@app.route('/phone', methods = ["GET", "POST"])
def phone():
    phone_number = PhoneNumber()
    if request.method == "POST" and phone_number.validate():
        first_name = phone_number.first_name.data
        last_name = phone_number.last_name.data
        area_code = phone_number.area_code.data
        number = phone_number.number.data
        print("\n", first_name, last_name, number)
    return render_template('/phone.html', phone_number = phone_number)

# Login Form Route
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))