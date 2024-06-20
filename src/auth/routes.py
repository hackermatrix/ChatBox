from flask import Blueprint,request,render_template,url_for,flash,redirect
from flask_login import login_user,logout_user,login_required,current_user
from src import bcrypt,db
from src.auth.models import User
auth_bp = Blueprint("auth",__name__)

from .forms import RegisterForm,LoginForm



@auth_bp.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered","info")
        return redirect(url_for('core.home'))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged ")

        return redirect(url_for('core.home'))

    return render_template("auth/register.html",form=form)




@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already Logged in","Info")
        return redirect(url_for('core.home'))

    form = LoginForm(request.form)
    if  form.validate_on_submit(extra_validators=None):
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('core.home'))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("auth/login.html", form=form)
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User Logged Out!","Success")
    return redirect(url_for("auth.login"))