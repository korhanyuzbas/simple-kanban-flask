from controllers.card import CardsApi, CardApi


def initialize_card_routes(api):
    api.add_resource(CardsApi, '/board/<pk>/card')
    api.add_resource(CardApi, '/card/<pk>')
