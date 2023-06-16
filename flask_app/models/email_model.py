from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Emails:

    DB = 'email_validation'
    tables = 'emails'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'SELECT * FROM {cls.tables};'
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        if results:
            for user in results:
                users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, id):
        query = f'SELECT * FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = f'INSERT INTO {cls.tables} (email) VALUES (%(email)s);'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'UPDATE {cls.tables} SET email = %(email)s WHERE id = %(id)s;'
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def validate_user(cls, email):
        query = f'SELECT * FROM {cls.tables} WHERE email = %(email)s;'
        results = connectToMySQL(cls.DB).query_db(query, email)
        if results:
            flash('Email already in database')
            return True
        email_name = email['email']
        flash(f'The email address you entered {email_name} is a VALID email address! Thank you!')
        return False
        
    
    @staticmethod
    def validate_email( email ):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash('Invalid email address!')
            is_valid = False
        return is_valid