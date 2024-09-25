from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'  # Replace with your desired database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255))  # Store tags as a comma-separated string

    def __repr__(self):
        return f"<Post {self.id}>"

@app.route('/')
def index():
    posts = Post.query.all()
    tags = set()
    for post in posts:
        tags.update(post.tags.split(','))
    return render_template('index.html', posts=posts, tags=tags)

@app.route('/filter', methods=['POST'])
def filter_posts():
    tag = request.form.get('tag')
    posts = Post.query.filter(Post.tags.contains(tag)).all()
    tags = set()
    for post in posts:
        tags.update(post.tags.split(','))
    return render_template('index.html', posts=posts, tags=tags)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)