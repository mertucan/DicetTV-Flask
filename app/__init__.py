from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from flask_login import current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
admin = Admin()
babel = Babel()
login_manager = LoginManager(app)
login_manager.init_app(app)
admin.init_app(app)
babel.init_app(app)

from app import views, models, db
from app.models import User, Contacts, Blogs, Products, Cart

"""admin.add_view(ModelView(User, db.session))"""
admin.add_view(ModelView(Contacts, db.session))
admin.add_view(ModelView(Blogs, db.session))
admin.add_view(ModelView(Products, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/contact', methods=['POST'])
def add_email_to_contacts():
    if request.method == 'POST':
        email = request.form['email']
        new_email = Contacts(email=email)
        try:
            db.session.add(new_email)
            db.session.commit()
            flash('Email added to the contacts successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding email to the contacts!', 'danger')
        finally:
            db.session.close()
            
    return redirect(url_for('index'))

@app.route('/products', methods=['POST'])
@login_required
def add_item_to_cart():
    if request.method == 'POST':
        username = current_user.username  # Giriş yapmış kullanıcının adını al

        name = request.form['name']

        # Ürünü Products tablosundan çek
        product = Products.query.filter_by(name=name).first()

        if product:
            # Eğer ürün bulunursa, Cart nesnesine ekleyerek kaydet
            price = product.price
            new_item = Cart(username=username, name=name, price=price)

            try:
                db.session.add(new_item)
                db.session.commit()
                flash('Item added to the carts successfully!', 'success')
            except:
                db.session.rollback()
                flash('Error adding item to the carts!', 'danger')
            finally:
                db.session.close()
        else:
            flash('Product not found!', 'danger')

    return redirect(url_for('products'))


