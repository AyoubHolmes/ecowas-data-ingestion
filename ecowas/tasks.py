from ecowas import get_model

class Tasks:
    def __init__(self, model):
        self.model = model

    

def init():
    model = get_model()
    model.create_db_if_not_exists()

