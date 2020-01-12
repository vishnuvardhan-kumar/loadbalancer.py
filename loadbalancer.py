import flask, requests, itertools
app, self_host, self_port, nodes = flask.Flask(__name__), "0.0.0.0", 5000, itertools.cycle(['Put your urls here'])
@app.errorhandler(404)
def route_page(err):
    curr_node = next(nodes)
    return getattr(requests, flask.request.method.lower())(f"{curr_node}{flask.request.path}").text
if __name__ == "__main__": app.run(host=self_host, port=self_port)