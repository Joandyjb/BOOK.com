from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        
        username_check = self.filter(username=form['username'])
        if username_check:
            errors['username'] = "Username already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )

    def editUser (self, form):
        user_errors = {}
        if len(form['first_name']) < 1:
            user_errors['first_name'] = 'First Name cannot be empty'
        if len(form['last_name']) < 1:
            user_errors['last_name'] = 'Last Name cannot be empty'
        if not EMAIL_REGEX.match(form['email']):
            user_errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=form['email'])
        if email_check:
            user_errors['email'] = "Email already in use"
        return user_errors

class User(models.Model):
    first_name = models.CharField(max_length=45, default="")
    last_name = models.CharField(max_length=45, default="")
    username = models.CharField(max_length=45, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=45, default="")
    author = models.CharField(max_length=45, default="")
    yearPublished = models.IntegerField()
    genre = models.CharField(max_length=45)
    Description = models.CharField (max_length= 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class orderManager(models.Manager):
    pass


class Order(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="ordered_by")
    book= models.ForeignKey(Book,on_delete=models.CASCADE,related_name="book_title")
    purchasedate= models.DateTimeField(auto_now=True)
    objects= orderManager()


# # #STUFF TO POPULATE DB WITH
# from BookApp.models import *
# book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone",author="J. K. Rowling",yearPublished=1997,genre="Novella")
# book2 = Book.objects.create(title="The Little Prince",author="Antoine de Saint-Exupéry",yearPublished=1943,genre="fantasy")
# book3 = Book.objects.create(title="Dream of the Red Chamber",author="Cao Xueqin",yearPublished=1701 ,genre="fantasy")
# book4 = Book.objects.create(title="The Hobbit",author="J. R. R. Tolkien",yearPublished=1937,genre="fantasy")

# book5 = Book.objects.create(title="To Kill a Mockingbird",author="Harper Lee",yearPublished=1960,genre="Southern Gothic, Bildungsroman")
# book6 = Book.objects.create(title="The Great Gatsby",author="F Scott Fitzgerald",yearPublished=1925,genre="Novel Fiction Tragedy")
# book7 = Book.objects.create(title="OCEAN PREY",author="John Sandford",yearPublished=2021 ,genre="Mystery, Thriller, Suspense, Crime Fiction")
# book8 = Book.objects.create(title="A Promised Land",author="Barack Obama",yearPublished=2020,genre="Biography, Autobiography")

# book9 = Book.objects.create(title="Rowley Jefferson's Awesome Friendly Adventure",author="Jeff Kinney",yearPublished=2020, genre="Fiction, Humou")
# book10 = Book.objects.create(title="Untamed",author="Glennon Doyle",yearPublished=2020 ,genre="MBiography, Autobiography")
# book11 = Book.objects.create(title="Modern Comfort Food",author="Ina Garten",yearPublished=2020 ,genre="Recipe, Cookbook")
# book12 = Book.objects.create(title="The Ballad Of Songbirds And Snakes", author="Suzanne Collins",yearPublished=2020,genre="Science Fiction, Thriller, Adventure")