# Blog-with-Django

## Project setup

### 1. Clone the repo
   
  ```terminal

    https://github.com/GeorgiDN/Blog-with-Django.git

  ```

### 2. Open the project


### 3. Install dependencies
 
   ```terminal
   
     pip install -r requirements.txt
  
   ```

### 4. Change DB settings in settings.py

  ```py
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "your_db_name",
            "USER": "your_username",
            "PASSWORD": "your_pass",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
  ```

### 5. Run the migrations

  ```terminal

    python manage.py migrate

  ```

### 6. Run the project

  ```terminal

    python manage.py runserver

  ```

Description
A blogging platform that allows users to create, read, update, and delete posts. 
Users can interact with posts through likes and comments, and personalize their experience with profile pictures. 
The application also includes features such as password reset via email, sending messages, adding friends

## Features
### Posts
- Create new blog posts.
- Edit or update their existing posts.
- Delete posts they own.
- View all posts in a structured feed.

### Comments:
- Add, edit, delete and like comments on any post.
- Comments are tied to user accounts.

### Likes:
- Like or unlike posts and comments.
- View the total number of likes on a post or and comment and users who liked.

### User Profiles
- Profile pictures for users.
- View user-specific content.

### Authentication
- User registration and login.
- Password reset functionality with email.

### Friends
- Users can send friend request
- Accept or reject friend request
- Accept or reject friend request
- Friend's list

### Messages
- Users can send messages each other
- Upload file, edit and remove message 
