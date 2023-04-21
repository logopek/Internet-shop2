import datetime
import time

import sqlalchemy.orm
from werkzeug.utils import secure_filename
from flask import request, render_template, Flask, redirect
import flask_login
import flask
import flask_paginate
from data.forms.login_form import LoginForm
from data.forms.register_form import RegisterForm
from data.forms.admin_form import AdminForm
from data import db_session
from data.models.users import User
from data.forms.additemform import AddItemForm
from data.models.item import Item
from data.roles.roles import *
import methods
import api.users
import api.items
import api.images

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////data/db/database.db"
app.config["SECRET_KEY"] = "some_secret_key"
app.register_blueprint(api.users.blueprint_users)
app.register_blueprint(api.items.blueprint_items)
app.register_blueprint(api.images.blueprint_images)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def get_all_items(offset: int, db_sess: sqlalchemy.orm.Session, category: str = '', per_page: int = 10):
    if category:
        tmp = db_sess.query(Item).filter(Item.category.like(f"%{request.args.get('category').lower()}%")).all()
        return tmp[offset: int(offset) + int(per_page)]
    else:
        tmp = db_sess.query(Item).all()
        return tmp[offset: int(offset) + int(per_page)]

@flask_login.login_required
def bancheck():
    return False


def admincfg(current_user: flask_login.current_user, t_user: int, method: methods.BanUnban | methods.SetRole):
    match str(method):
        case "ban_unban":
            db_sess = db_session.create_session()
            t = db_sess.query(User).where(User.id == t_user).one()
            if t:
                if t.role <= current_user.role:
                    message = "User have more/some privileges"
                else:
                    t.ban = method.value
                    message = "Success"
                    db_sess.commit()
            else:
                message = "User not found!"
        case "set_role":
            db_sess = db_session.create_session()
            t = db_sess.query(User).where(User.id == t_user).one()
            if t:
                if t.role <= current_user.role:
                    message = "User have more/some privileges"
                else:
                    t.role = method.value
                    message = "Success"
                    db_sess.commit()
            else:
                message = "User not found!"
    return message


def count_user_cart(items):
    x = {}
    for i in items:
        if x.get(i.title, None):
            x[i.title] += 1
        else:
            x[i.title] = 1
    return x


@app.errorhandler(500)
def error500(error):
    return "Error 500"


@app.errorhandler(404)
def error404(error):
    return render_template("404.html")


@app.errorhandler(403)
def error403(error):
    return render_template("403.html")

@app.errorhandler(401)
def error401(error):
    return redirect('/login')

@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route("/logout")
def logout():
    
    flask_login.logout_user()
    return redirect("/")


@app.route("/admin_panel", methods=["GET", "POST"])
@flask_login.login_required
def admin():
    
    if flask_login.current_user.role < 1000:
        if request.method == "GET":
            return render_template("admin_panel.html", form=AdminForm())
        else:
            form = AdminForm()
            message = ""
            if form.validate_on_submit():
                t_id = form.user_id.data
                if t_id == flask_login.current_user.id:
                    return render_template("admin_panel.html", message="Cant ban/promote yourself", form=AdminForm())

                if form.select.data == "Ban":
                    message = admincfg(flask_login.current_user, t_id, method=methods.BanUnban(1))
                if form.select.data == "Unban":
                    message = admincfg(flask_login.current_user, t_id, method=methods.BanUnban(0))
                if form.select.data == "Make Admin" and flask_login.current_user.role < ROLE_MODERATOR:
                    message = admincfg(flask_login.current_user, t_id, method=methods.SetRole(0))
                if form.select.data == "Make Moderator" and flask_login.current_user.role < ROLE_MODERATOR:
                    message = admincfg(flask_login.current_user, t_id, method=methods.SetRole(1))
                return render_template("admin_panel.html", form=AdminForm(), message=message)
    return flask.abort(403)


@app.route("/", methods=["GET", "POST"])
def main():
    pp = 5
    content = {}
    page = request.args.get('page', 1, type=int)
    
    db_sess = db_session.create_session()
    alls = get_all_items(offset=(page - 1) * pp, per_page=pp, category=request.args.get('category', ''),
                         db_sess=db_sess)
    content['items'] = alls
    print(alls)
    if request.args.get('category'):
        total = len(
            list(db_sess.query(Item).filter(Item.category.like(f"%{request.args.get('category').lower()}%")).all()))
    else:
        total = len(list(db_sess.query(Item).all()))
    content['pagination'] = flask_paginate.Pagination(page=page, total=total, per_page=pp, page_parameter='page',
                                                      css_framework='bootstrap5')
    db_sess.close()
    return render_template("index.html", content=content)


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first() or db_sess.query(User).filter(User.email == form.email.data).first():
            print('user exists')
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            login=form.login.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            flask_login.login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        db_sess.close()
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/additem", methods=["GET", "POST"])
@flask_login.login_required
def additem():
    
    x = flask_login.current_user.role
    if request.method == "GET":
        if x < 1000:
            return render_template("additem.html", form=AddItemForm())
        else:
            flask.redirect("/")
    else:
        form = AddItemForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            filename = secure_filename(form.image.data.filename)
            form.image.data.save('static/images/' + filename)
            db_sess.add(Item(
                title=form.title.data,
                price=form.price.data,
                about=form.about.data,
                category=form.category.data.lower(),
                image_path='static/images/' + filename
            ))
            db_sess.commit()
            db_sess.close()
            return redirect("/")
    return redirect("/")


@app.route('/buy/<int:id>', methods=["GET", "POST"])
@flask_login.login_required
def buy_item(id):
    
    if request.method == "GET":
        db_sess = db_session.create_session()
        item = db_sess.query(Item).where(Item.id == id).one()
        return render_template("buy.html", item=item)
    else:
        db_sess = db_session.create_session()
        item = db_sess.query(Item).where(Item.id == id).one()
        user = db_sess.query(User).where(User.id == flask_login.current_user.id).one()
        if user.balance - item.price >= 0:
            user.balance -= item.price
            user.items += " " + str(item.id)
        else:
            return render_template("index.html", message="No money!")
        db_sess.commit()
        db_sess.close()
        return redirect("/")


@app.route("/cart")
@flask_login.login_required
def cart():
    
    user = flask_login.current_user
    db_sess = db_session.create_session()
    cart_user = []
    for i in user.items.split():
        cart_user.append(db_sess.query(Item).where(Item.id == int(i)).one())
    db_sess.close()
    user_items_count = count_user_cart(cart_user)
    result = []
    for i in cart_user:
        if i not in result:
            result.append(i)
    return render_template("cart.html", items=result, user_items=user_items_count)


if __name__ == "__main__":
    db_session.global_init("db.db")
    app.run("127.0.0.1", 5006)
