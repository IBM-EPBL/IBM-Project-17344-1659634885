from connect import app, db
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import loginForm, registrationForm, transactionForm, profiles
from models import Users, Transactions
from werkzeug.security import generate_password_hash, check_password_hash
from flask_msearch import Search
from picture_handler import add_profile_pic
from graphs import ghaint_chart, baseGraph, baseGraph2, savingGraph, savingGraph2
from datetime import datetime
from values import totalBal, leftBal, totalSpent

today = datetime.today()
now = datetime.now()


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


@app.route("/instructions")
def instructions():
    return render_template("instructions.html")


# @app.route("/test")
# def test():
#     bar = testchart()
#     return render_template("test.html", plot=bar)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


search = Search()
search.init_app(app)


@app.route("/search")
def search():
    data = Transactions.query.msearch(request.args.get("query")).all()
    return render_template("passbook.html", trans_data=data)


@app.route("/<int:row_id>/delete", methods=["POST"])
@login_required
def delete(row_id):
    delete__row = Transactions.query.get_or_404(row_id)
    db.session.delete(delete__row)
    db.session.commit()
    flash("Transaction deleted!")

    return redirect(url_for("passbook"))


@app.route("/passbook", methods=["GET", "POST"])
@login_required
def passbook():
    uid = current_user.id
    trans_data = Transactions.query.filter_by(userId=uid).order_by(
        Transactions.date.desc()
    )
    return render_template("passbook.html", trans_data=trans_data)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = profiles()

    if form.validate_on_submit():
        print("in if")
        if form.image.data:
            # print("image added")
            username = current_user.id
            image_data = current_user.profile_image
            # print(image_data)
            current_user.profile_image = "default_profile.jpeg"
            db.session.commit()
            pic = add_profile_pic(form.image.data, username, image_data)
            current_user.profile_image = pic

        current_user.budget = form.budget.data
        current_user.income = form.income.data
        db.session.commit()
        flash("User Account Updated")
        return redirect(url_for("profile"))

    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.budget.data = current_user.budget
        form.income.data = current_user.income
        form.image.data = current_user.profile_image

    profile_image = url_for(
        "static", filename="profile_pics/" + current_user.profile_image
    )
    
    
    return render_template("profile.html", proForm=form, profile_image=profile_image)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int("3000"), debug=True)