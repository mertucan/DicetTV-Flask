from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Blogs, Contacts, Products, Cart

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    blog_data = Blogs.query.all()
    return render_template('blog.html', blog_data=blog_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/more')
def more():
    return render_template('more.html')

def get_cart_data(username):
    return Cart.query.filter_by(username=username).all()

@app.route('/cart')
@login_required
def cart():
    cart_data = get_cart_data(current_user.username)
    return render_template('cart.html', cart_data=cart_data)

@app.route('/clear_cart')
@login_required
def clear_cart():
    try:
        # Giriş yapmış olan kullanıcının cart verilerini sil
        Cart.query.filter_by(username=current_user.username).delete()

        # Değişiklikleri kaydet
        db.session.commit()

        # Silme işlemi başarılı olduysa, kullanıcıyı cart sayfasına yönlendir
        return redirect(url_for('cart'))

    except Exception as e:
        # Hata durumunda geri dön
        print(f"Error: {str(e)}")
        db.session.rollback()

    finally:
        # Veritabanı bağlantısını kapat
        db.session.close()

@app.route('/products')
def products():
    product_data = Products.query.all()
    return render_template('products.html', product_data = product_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user_info={'email': current_user.email, 'username': current_user.username})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user() 
    return redirect(url_for('index'))
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)