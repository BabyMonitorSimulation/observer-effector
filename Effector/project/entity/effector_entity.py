import requests


class Effector:
    def __init__(self, steps_to_adapt, steps_for_behave_normal):
        self.steps_to_adapt = steps_to_adapt
        self.steps_for_behave_normal = steps_for_behave_normal

    def adapt(self, scenario):
        print('adapt: ', self.steps_to_adapt[scenario])
        for step in self.steps_to_adapt[scenario]:
            print("I'm adapting")
            print(f"STEP: {step}")
            requests.request(method=step["method"],
                             url=step["url"],
                             json=step["body"])

    def behave_normal(self, scenario):
        print('normal: ', self.steps_for_behave_normal[scenario])
        for step in self.steps_for_behave_normal[scenario]:
            print("I'm returning to normal")
            print(f"STEP: {step}")
            requests.request(method=step["method"],
                             url=step["url"],
                             json=step["body"])
