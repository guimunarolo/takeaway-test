from .views import users_list


def init_routes(app):
    app.router.add_get("/users", users_list)
