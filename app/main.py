from flask import Flask, jsonify, request
from cal import getEventsOfToday
from mathdata import Exercises
import random

app = Flask(__name__)
app.exercises = None

@app.route("/getEventsOfToday", methods=["POST"])
def get_events():
    if request.form.get("pwd") == "RPiPico":
        return jsonify(getEventsOfToday())
    else:
        return jsonify({"error": "access denied"})

@app.route("/getRandomExercise/<string:topic>")
def get_random_exercise(topic: str):
    data = app.exercises.get_exercises(topic, not_done=True)
    if not data:
        return jsonify({})
    e = random.choice(data)
    app.exercises.mark_as_done(e["id"])
    return jsonify(e)

def main():
    app.exercises = Exercises()
    app.run(host="0.0.0.0", port=10505)


if __name__ == "__main__":
    main()