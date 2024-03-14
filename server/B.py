import flask

app = flask.Flask(__name__)


@app.route("/ballot")
def new_ballot():
    # TODO: encripta
    return dict(ballots=[{"id": "0xCAF3", "Candidato A": 0, "Candidato B": 0, "Candidato C": 0, "Nulo": 0},
                         {"id": "0xCAF4", "Candidato A": 0, "Candidato B": 0, "Candidato C": 0, "Nulo": 0},
                         {"id": "0xCAF5", "Candidato A": 0, "Candidato B": 0, "Candidato C": 0, "Nulo": 0}])


@app.route("/vote", methods=["POST"])
def vote():
    vote = flask.request.get_json()

    for cell in vote:
        print(cell)

    return "OK"
