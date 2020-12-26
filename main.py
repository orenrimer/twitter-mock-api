from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class TweetsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Integer, nullable=False)
    retweets = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Tweet(content = {self.content}, comments = {self.comments}, retweets = {self.retweets}, likes = {self.likes})"


def args_parser(required=True):
    put_args = reqparse.RequestParser()
    put_args.add_argument('content', type=str, help="tweet content", required=required)
    put_args.add_argument('comments', type=int, help="number of comments", required=required)
    put_args.add_argument('retweets', type=int, help="number of retweets", required=required)
    put_args.add_argument('likes', type=str, help="number of likes", required=required)
    return put_args

resource_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'comments':fields.Integer,
    'retweets': fields.Integer,
    'likes': fields.Integer
}


class Tweet(Resource):
    @marshal_with(resource_fields)
    def get(self, tweet_id):
        tweet = TweetsModel.query.filter_by(id=tweet_id).first()
        if not tweet:
            abort(404, massage="cannot find tweet, tweet id not in database.")
        return tweet

    @marshal_with(resource_fields)
    def put(self, tweet_id):
        args = args_parser(required=True).parse_args()
        if TweetsModel.query.filter_by(id=tweet_id).first():
            abort(409, massage="tweet id already exists in database.")
        tweet = TweetsModel(id=tweet_id, content=args['content'], comments=args['comments'], retweets=args['retweets'], likes=args['likes'])
        db.session.add(tweet)
        db.session.commit()
        return tweet, 201

    @marshal_with(resource_fields)
    def patch(self, tweet_id):
        args = args_parser(required=False).parse_args()
        tweet = TweetsModel.query.filter_by(id=tweet_id).first()
        if not tweet:
            abort(404, massage="tweet doesn't exists")
        if args['content']:
            tweet.content = args['content']
        elif args['comments']:
            tweet.comments = args['comments']
        elif args['retweets']:
            tweet.retweets = args['retweets']
        elif args['likes']:
            tweet.likes = args['likes']
        db.session.commit()
        return tweet, 200

    def delete(self, tweet_id):
        tweet = TweetsModel.query.filter_by(id=tweet_id).first()
        if not tweet:
            abort(404, massage="tweet doesn't exists")
        db.session.delete(tweet)
        db.session.commit()
        return "", 204


api.add_resource(Tweet, "/tweet/<int:tweet_id>")

if __name__ == '__main__':
    # clear_data(db.session)
    app.run(debug=True)