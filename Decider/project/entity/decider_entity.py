import requests


class Decider:
    def __init__(self, steps_to_adapt, steps_for_behave_normal):
        self.steps_to_adapt = steps_to_adapt
        self.steps_for_behave_normal = steps_for_behave_normal

    def adapt(self):
        for step in self.steps_to_adapt:
            print("I'm adapting")
            print(f"STEP: {step}")
            requests.request(method=step["method"],
                             url=step["url"],
                             json=step["body"])

    def behave_normal(self):
        for step in self.steps_for_behave_normal:
            print("I'm returning to normal")
            print(f"STEP: {step}")
            requests.request(method=step["method"],
                             url=step["url"],
                             json=step["body"])
