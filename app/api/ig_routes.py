from . import api
from ..models import Post

@api.route("/posts")
def getPostsAPI():
    posts = Post.query.all()
    return{
        'status': 'ok',
        'results': len(posts),
        'posts': [p.to_dict() for p in posts]

    }