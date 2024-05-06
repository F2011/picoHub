import json
import os
from copy import deepcopy

class Exercises:
    def __init__(self) -> None:
        self.data = {}
        self.not_done_data = {}
        self.read_math_data()
    
    def mark_as_done(self, id: str) -> bool:
        topic = id.split("@")[0]
        for ex in self.not_done_data[topic]:
            if ex["id"] == id:
                self.not_done_data[topic].remove(ex)
        for ex in self.data[topic]:
            if ex["id"] == id:
                ex["done"] = True
                return True
        return False
    
    def read_math_data(self):
        absolute_root = "data/math/"
        for root, dirs, files in os.walk(absolute_root):
            for dir in dirs:
                self.data[dir] = []

            relative_root = root.removeprefix(absolute_root)
            print("Loading " + root + "...")
            for filename in files:
                with open(os.path.join(root, filename)) as j:
                    id = relative_root + "@" + filename.removesuffix(".json")
                    exercise = json.load(j)
                    exercise["id"] = id
                    exercise["done"] = False
                    self.data[relative_root].append(exercise)
        self.not_done_data = deepcopy(self.data)
    
    def get_exercises(self, topic: str, not_done=False) -> list:
        if not_done:
            return deepcopy(self.not_done_data[topic])
        else:
            return deepcopy(self.data[topic])

if __name__ == "__main__":
    exercises = Exercises()
    for e in exercises.get_exercises("counting_and_probability")[0:5]:
        print(e)
    exercises.mark_as_done("counting_and_probability@816")
    for e in exercises.get_exercises("counting_and_probability")[0:5]:
        print(e)