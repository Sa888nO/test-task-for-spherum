import imp
from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import * 

Base.metadata.create_all(bind=engine)



# api /users
@app.route('/users', methods=['GET'])
def get_users_list():
    users = User.query.all()
    serialized = []
    for user in users: 
        serialized.append({
            'id': user.id,
            'name': user.name,
            'password': user.password
        })
    return jsonify(serialized)

@app.route('/users', methods=['POST'])
def update_users_list():
    new_one = User(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'name': new_one.name,
        'password': new_one.password  
    }
    return jsonify(serialized)

# api /posts
@app.route('/posts', methods=['GET'])
def get_posts_list():
    posts = Post.query.all()
    serialized = []
    for post in posts: 
        serialized.append({
            'id': post.id,
            'user_id': post.user_id,
            'title': post.title,
            'text': post.text
        })
    return jsonify(serialized)

@app.route('/posts', methods=['POST'])
def update_postrs_list():
    new_one = Post(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'user_id': new_one.user_id,
        'title': new_one.title,
        'text': new_one.text
    }
    return jsonify(serialized)

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    item = Post.query.filter(Post.id == post_id).first()
    params = request.json
    if not item:
        return {'massage': 'No posts with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
    'id': item.id,
    'user_id': item.user_id,
    'title': item.title,
    'text': item.text
    }
    return jsonify(serialized)

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    item = Post.query.filter(Post.id == post_id).first()
    if not item:
        return {'massage': 'No posts with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()