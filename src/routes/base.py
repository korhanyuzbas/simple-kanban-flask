from routes.user import initialize_user_routes
from routes.board import initialize_board_routes
from routes.card import initialize_card_routes
from routes.comment import initialize_comment_routes


def initialize_routes(api):
    initialize_user_routes(api)
    initialize_board_routes(api)
    initialize_card_routes(api)
    initialize_comment_routes(api)
