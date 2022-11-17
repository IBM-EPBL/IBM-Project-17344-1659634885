from connect import app, db
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/", methods=["GET", "POST"])
def index():

    RegistrationForm = registrationForm()
    LoginForm = loginForm()

    if RegistrationForm.validate_on_submit():
        user = Users.query.filter_by(email=RegistrationForm.email2.data).first()

        if user is not None:
            flash("Email Id already registered!")

        else:

            passw = generate_password_hash(RegistrationForm.password2.data)

            user = Users(
                email=RegistrationForm.email2.data,
                name=RegistrationForm.username2.data,
                pasword_hash=passw,
            )

            db.session.add(user)
            db.session.commit()
            flash("Thanks for registeration! Login to continue")
            return redirect(url_for("index"))

    if LoginForm.validate_on_submit():
        user = Users.query.filter_by(email=LoginForm.email1.data).first()

        if user is not None and user.check_password(LoginForm.password1.data):

            login_user(user)
            # flash('Log in Success')

            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("dashboard")

            return redirect(next)

        elif user is None:
            flash("Email Id not registered!")

        else:
            flash("Wrong Password!")

    return render_template("index.html", logForm=LoginForm, signForm=RegistrationForm)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int("3000"), debug=True)
