from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column (db.Integer, db.ForeignKey ('restaurant.id'), nullable=False)
    photos = db.relationship ('Photo', backref='belong_post', lazy='dynamic')
    advertisement_id = db.Column (db.Integer, db.ForeignKey ('advertisement.id'))
    number_of_like = db.Column (db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Photo(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    photo_link = db.Column(db.String(4000), nullable=False)
    number_of_like = db.Column(db.Integer)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Advertisement(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    advertisement_link = db.Column (db.String (4000),nullable=False,unique=True)
    posts = db.relationship('Post', backref = 'advertisment', lazy ='dynamic')

restaurantfood = db.Table('restaurantfood',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
)

restaurantfeature = db.Table('restaurantfeature',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id')),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'))
)


class Restaurant(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    posts = db.relationship('Post', backref='About_restaurant', lazy='dynamic')
    location_id = db.Column (db.Integer, db.ForeignKey ('location.id'),nullable=False)
    cusine_id = db.Column (db.Integer, db.ForeignKey ('cusine.id'))
    foodlist= db.relationship('Food', secondary= restaurantfood, backref=db.backref('Restaurants', lazy='dynamic'))
    rating = db.Column(db.Integer)
    intro = db.Column(db.String(500), nullable=False)
    contact_methods = db.relationship('Contact', backref = 'restaurant', lazy ='dynamic')
    spending_per_head = db.Column (db.Integer)
    open_hour = db.Column (db.Integer)
    closing_hour = db.Column (db.Integer)
    working_day = db.Column (db.String(100))
    features = db.relationship('Feature', secondary= restaurantfeature, backref=db.backref('Restaurants', lazy='dynamic'))


class Location(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    location_google_link = db.Column(db.String(4000))
    country_id = (db.Integer, db.ForeignKey('country.id'))

class Country(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String(100), index=True,nullable=False, unique=True)

class Cusine(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(140),nullable=False, unique=True)
    restaurants = db.relationship('Restaurant', backref = 'cusine', lazy ='dynamic')

class Food(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(140),nullable=False, unique=True)

class Contact(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    telephone = db.Column (db.Integer, unique=True)
    email = db.Column(db.String(200), unique=True)
    restaurant_id = db.Column (db.Integer, db.ForeignKey ('restaurant.id'),nullable=False)


class Feature(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False, unique=True)



class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(150), nullable=False)
    menu_category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False)
    menu_category = db.relationship("MenuCategory")

class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
