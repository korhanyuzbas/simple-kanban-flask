from controllers.auth import SignupApi, LoginApi, ChangePassword, UserApi

def initialize_user_routes(api):
    api.add_resource(SignupApi, '/register')
    api.add_resource(LoginApi, '/login')

    api.add_resource(UserApi, '/user/<pk>/profile')

    api.add_resource(ChangePassword, '/user/change_password')
