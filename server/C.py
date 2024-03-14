import flask, requests

app = flask.Flask(__name__)

@app.route("/vote")
def vote():
    # Pede as cedulas do B.
    r = requests.get("http://localhost:5001/ballot")

    print(r.json())

    return "<h1>INTERFACE</h1>"

@app.route("/send")
def send():
    # flask.request.json()
    # TODO: id encriptado

    ballots=[ { "id": "0xCAF3", "hash":"0xCAF6" },
              { "id": "0xCAF4", "hash":"0xCAF7" },
              { "id": "0xCAF5", "hash":"0xCAF8" }  ]

    r = requests.post("http://localhost:5001/vote", json=ballots)

    print(r.content)

    return "<h1>VOTO ENVIADO</h1>"