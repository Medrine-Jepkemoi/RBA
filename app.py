from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask_login import LoginManager, login_manager, login_user
from flask_security import Security, SQLAlchemySessionUserDatastore



app = Flask(__name__)

# if database not present already
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///rolebasedaccess.db"
# needed for session cookies
app.config['SECRET_KEY'] = 'MY_SECRET'
# hashes the password and then stores in the database
app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
# allows new registrations to application
app.config['SECURITY_REGISTERABLE'] = True
# to send automatic registration email to user
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

db = SQLAlchemy
db.init_app(app)

app.app_context().push()


# create table in database for assigning roles
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))   
 
# create table in database for storing users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    # backreferences the user_id from roles_users table
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
 
# create table in database for storing roles
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
     

# load users, roles for a session
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

# creates all database tables
@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(port=5555)
