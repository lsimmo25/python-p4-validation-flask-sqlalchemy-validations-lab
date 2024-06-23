from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
import re

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        #Validate name is not empty
        if not name:
            raise ValueError("Author must have a name")
        
        #Validate name is unique
        existing_author = Author.query.filter(Author.name==name).first()
        if existing_author:
            raise ValueError("Name must be unique")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):

        #Validate author phone number is exactly 10 digits
        if not re.fullmatch(r'\d{10}', number):
            raise ValueError("Phone number must be exactly 10 digits.")
        return number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    #validate length of content
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 chars")
        return content
    
    @validates('summary')
    #validate summary
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary cannot be longer than 250 chars")
        return summary
    
    @validates('category')
    #validate category
    def validate_category(self, key, cat):
        if cat not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return cat
    
    @validates('title')
    #validates title
    def validate_title(self, key, title):
        click_bait = ["Won't Believe", "Secret", "Top", "Guess"]
        in_title = []

        for bait in click_bait:
            if bait in title:
                in_title.append(bait)
                
        if not in_title:
            raise ValueError("Title must have click bait")
        
        if not title:
            raise ValueError("Post must have a title")
        
        return title
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
