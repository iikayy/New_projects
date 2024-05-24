from flask import Flask, render_template, redirect, url_for, flash, abort, current_app
from flask_bootstrap import Bootstrap5
from forms import RegisterForm, LoginForm, UploadPictureForm, UpdateProfileForm, ChangePasswordForm
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
from datetime import date
from imagekitio import ImageKit
from werkzeug.utils import secure_filename


IMAGEKIT_PRIVATE_KEY = os.environ.get('IMAGEKIT_PRIVATE_KEY')
AVIEN_PASSWORD = os.environ.get('AVIEN_PASSWORD')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/pics'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Initialize imageKit SDK
imagekit = ImageKit(
    private_key=IMAGEKIT_PRIVATE_KEY,
    public_key='public_fOFPZvhBmREFPjnl1Zka4VsdjAo=',
    url_endpoint='https://ik.imagekit.io/pwroigzp3'
)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['ADMIN_IDS'] = [1]  # IDs of admin users
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pics.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    posts = relationship("GramPics", back_populates="author")
    profile_pic_url: Mapped[str] = mapped_column(String(300))  # Store ImageKit profile picture URL
    # comments = relationship("Comment", back_populates="comment_author")


class GramPics(db.Model):
    __tablename__ = "gram_pics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # comments = relationship("Comment", back_populates="pics_author")


# class Comment(db.Model):
#     __tablename__ = "comments"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     text: Mapped[str] = mapped_column(Text, nullable=False)
#     author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
#     comment_author = relationship("User", back_populates="comments")
#     pics_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("gram_pics.id"))
#     pics_author = relationship("GramPics", back_populates="comments")


with app.app_context():
    db.create_all()

# Create an admin and author-only decorator
def admin_and_author_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        post_id = kwargs.get('pic_id')  # Get the pic ID from the URL parameters
        if post_id:
            pic = GramPics.query.get(post_id)  # Get the pic using the ID
            if not pic:
                abort(404)  # Pic not found
            if current_user.id != pic.author_id and current_user.id not in current_app.config['ADMIN_IDS']:
                return redirect(url_for('get_all_pics'))  # Redirect unauthorized users
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
def get_all_pics():
    pics = db.session.execute(db.select(GramPics)).scalars().all()
    return render_template("index.html", all_pics=pics)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_all_pics"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_pics', current_user=current_user.name))

    return render_template("login.html", form=form)


@app.route("/new-pics", methods=["GET", "POST"])
def add_new_pics():
    form = UploadPictureForm()
    if form.validate_on_submit():
        # Upload profile picture to ImageKit
        filename = secure_filename(form.pics.data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.pics.data.save(filepath)
        uploaded_file = imagekit.upload(
            file=open(filepath, 'rb'),
            file_name=filename,
        )
        new_pics = GramPics(
            title=form.title.data,
            img_url=uploaded_file.url,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_pics)
        db.session.commit()
        os.remove(filepath)
        return redirect(url_for("get_all_pics"))
    return render_template("post_pics.html", form=form)


@app.route("/profile/<int:user_id>", methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    profile = db.get_or_404(User, user_id)
    form = UpdateProfileForm(
        name=profile.name,
        email=profile.email,
        # profile_pic=profile.profile_pic_url
    )
    if form.validate_on_submit():
        # Update user information
        profile.name = form.name.data
        profile.email = form.email.data
        db.session.commit()

        if form.profile_pic.data:
            # Upload profile picture to ImageKit
            filename = secure_filename(form.profile_pic.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.profile_pic.data.save(filepath)
            uploaded_file = imagekit.upload(
                file=open(filepath, 'rb'),
                file_name=filename,
            )
            profile.profile_pic_url = uploaded_file.url
            db.session.commit()
            # Optionally, delete the local file after upload
            os.remove(filepath)
            # return 'Profile updated successfully'
        return redirect(url_for('get_all_pics', user_id=current_user.id))
    return render_template('profile.html', form=form)


@app.route("/delete/<int:pic_id>")
@admin_and_author_only
def delete_pic(pic_id):
    pic_to_delete = db.get_or_404(GramPics, pic_id)
    db.session.delete(pic_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_pics'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_pics'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)