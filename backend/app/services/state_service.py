from collections import deque


MAX_HISTORY = 100


class StateService:
    def __init__(self):
        self.current_state = None
        self.history = deque(maxlen=MAX_HISTORY)

    def update(self, state):
        self.current_state = state
        self.history.append(state)

    def get_current_state(self):
        return self.current_state

    def get_history(self):
        return list(self.history)

    def reset(self):
        self.current_state = None
        self.history.clear()


state_service = StateService()