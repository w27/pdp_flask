import flask
from flask.views import View
from flask_restful import Resource, Api

app = flask.Flask(__name__)


@app.route("/")
def test_get():
    g = 5
    return flask.render_template('index.html')


@app.route("/test_get/<string:h>")
def test_post(h):
    print(h)
    return flask.render_template('index.html')


@app.route('/foo', methods=['POST'])
def foo():
    # data = flask.request.get_json()
    return flask.jsonify(flask.request.get_json(force=True))
    # return flask.jsonify(data)


api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = flask.request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')


if __name__ == "__main__":
    app.run(debug=True)

