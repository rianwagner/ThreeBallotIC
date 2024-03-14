import flask

app = flask.Flask(__name__)

@app.route("/login")
def login():
    login = flask.request.get_json() # { "username": "Rian", "password": "senha" }

    # TODO: Autenticação
    authentication_failed = False

    if authentication_failed:
        return "Authentication Failed", 405

    # TODO: Salvar voto no BD.

    return "OK"
