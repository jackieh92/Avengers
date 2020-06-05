from avengers import app, db, Message, mail
from flask import render_template, request, redirect, url_for

# Import for Forms
from avengers.forms import UserInfoForm, PhoneNumber, LoginForm


# Import for Models
from avengers.models import User, check_password_hash, Phone

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
        user_id = current_user.id
        print("\n", first_name, last_name, number)

        phone = Phone(first_name, last_name, area_code, number, user_id)
        db.session.add(phone)
        db.session.commit()
        return redirect(url_for('phone_display', phone_id = phone.id))
    return render_template('/phone.html', phone_number = phone_number)




# To see phone number displayed in ONE place
@app.route('/phone_display')
def phone_display():
    user = current_user
    form = Phone.query.filter_by(user_id=current_user.id).first()
    #form = Phone.query.get_or_404(phone_id)

    return render_template('phone_display.html', form = form)




@app.route('/phone/update/<int:phone_id>', methods = ['GET', 'POST'])
@login_required
def phone_update(phone_id):
    form = Phone.query.get_or_404(phone_id)
    update_phone = PhoneNumber()
    
    if request.method == 'POST' and update_phone.validate():
        first_name = update_phone.first_name.data
        last_name = update_phone.last_name.data
        area_code = update_phone.area_code.data
        number = update_phone.number.data
        print(first_name, last_name, area_code, number)

        # Update will be added to database here
        form.first_name = first_name
        form.last_name = last_name
        form.area_code = area_code
        form.number = number

        db.session.commit()
        return redirect(url_for('phone_update', phone_id = form.id))
    return render_template('phone_update.html', update_phone = update_phone)




@app.route('/phone/delete/<int:phone_id>', methods = ['POST'])
@login_required
def phone_delete(phone_id):
    post = Phone.query.get_or_404(phone_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))




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