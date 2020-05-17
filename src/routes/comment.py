from controllers.comment import CommentApi, CommentsApi


def initialize_comment_routes(api):
    api.add_resource(CommentsApi, '/card/<pk>/comment')
    api.add_resource(CommentApi, '/comment/<pk>')
