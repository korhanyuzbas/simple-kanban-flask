from controllers.board import BoardApi, BoardsApi


def initialize_board_routes(api):
    api.add_resource(BoardsApi, '/board')
    api.add_resource(BoardApi, '/board/<pk>')
