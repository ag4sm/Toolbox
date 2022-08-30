from tkinter import CASCADE
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, UserMixin, login
from datetime import datetime as dt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    # Should return a unique identifying string
    def __repr__(self):
        return f'<user: {self.email} | {self.id}>'

    # Human readable version of repr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # hashes password for security
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares original password to hashed password
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    def user_from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        
    # save user to database
    def save(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader 
def load_user(id):
    return User.query.get(int(id))

# one to one relationship just gets a db.ForeignKey pointing back to the table it links to
# db.relationship is used for the one to many references
class Toolbox(db.Model):
    toolbox_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    tools = db.relationship('Tool', backref='toolbox', lazy=True, cascade = 'all, delete, delete-orphan')

    def __repr__(self):
        return f'<Toolbox: {self.toolbox_id} | {self.tool_id}>'

    def __str__(self):
        return f'<Toolbox: {self.tools}>'

    # save to database
    def save(self):
        db.session.add(self)
        db.session.commit()

class Tool(db.Model):
    tool_id = db.Column(db.Integer, primary_key=True)
    toolboxid = db.Column(db.Integer, db.ForeignKey('toolbox.toolbox_id'))
    tool_name = db.Column(db.String(20), index=True, unique=False)
    tool_brand = db.Column(db.String(20), index=True, unique=False)
    quantity = db.Column(db.Integer)
    toolboxes = db.relationship('Toolbox', backref='tool', lazy=True, cascade = 'all, delete, delete-orphan')

    def __repr__(self):
        return f'<Tool:  {self.tool_brand} | {self.tool_name}>'

    def __str__(self):
        return f'<Tool:  {self.tool_brand} | {self.tool_name}>'

    def tool_from_dict(self, data):
        self.tool_name = data['tool_name']
        self.tool_brand = data['tool_brand']
        self.quantity = data['quantity']
        
    # save user to database
    def save(self):
        db.session.add(self)
        db.session.commit()
