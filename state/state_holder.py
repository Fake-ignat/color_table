# coding: utf-8
import json
from utils import load_data
from constants import ROOT_DIR


class State_Holder():
    filename = f'{ROOT_DIR}/state/app_state.json'

    def __init__(self):
        self.appState = load_data(self.filename)

    def get_state(self):
        return self.appState

    def update_state(self, data):
        self.appState = {**self.appState, **data}

    def save_state(self):
        with open(self.filename, 'w') as f:
            json.dump(self.appState, f,  ensure_ascii=False)


state_holder = State_Holder()
data = {
    "Казахстан": {
        "Валакхия": {
            "isChosen": True
        }}}
state_holder.update_state(data)
state_holder.save_state()
