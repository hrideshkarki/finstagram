from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    post = db.relationship('Post', backref = 'author', lazy = True)
    liked_posts = db.relationship('Post', secondary='like', lazy = True)
    followed = db.relationship(
        'User',
        secondary=followers,
        lazy = 'dynamic',
        backref=db.backref('followers', lazy = 'dynamic'),
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id)
        )
    


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
        
    def follow(self, user):
        self.followed.append(user)
        db.session.commit()
    def unfollow(self, user):
        self.followed.remove(user)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    img_url = db.Column(db.String, nullable = False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    likers = db.relationship('User', secondary='like')
    likers_2 = db.relationship('User', secondary = 'like_2')

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def saveChangesToDB(self):
        db.session.commit()

likes = db.Table('like_2',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable = False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable = False))

class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
#     message = db.Column(db.String(300), nullable = False)






# Like.query.all() # we would never start from the Like Model class so having it inherit from db.Model is a bit unnecessary
# Comment.query.get()

# user = User.query.get(1) # returns to us the "Sho" user
# user.like.all() # returns to us all the things that User 1 has liked

# post = Post.query.get(1) # return to us a post object with ID 1
# post.likers.all() # return to us all the people that liked post 1
