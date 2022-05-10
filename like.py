from flask import request, Blueprint
from pymongo import MongoClient
from flask import jsonify, request, redirect, url_for
import jwt

SECRET_KEY = "team"

like_api = Blueprint('like_api', __name__)

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map

# 좋아요 누르면 포스트 아이디로 좋아요 저장
@like_api.route('/like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        postid_receive = request.form['postid_give']
        action_receive = request.form['action_give']

        doc = {
            "postid": postid_receive,
            "username": user_info['id'],
        }

        total_like = db.post.find_one({'postid': postid_receive})['like']

        if action_receive == "like":
            db.like.insert_one(doc)
            db.post.update_one({'_id': postid_receive}, {'$set': {'like': total_like + 1}})
        else:
            db.like.delete_one(doc)
            db.post.update_one({'_id': postid_receive}, {'$set': {'like': total_like - 1}})

        count = db.like.count_documents({"postid": postid_receive})
        return jsonify({"result": "success", "msg": "updated", "count": count})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))



