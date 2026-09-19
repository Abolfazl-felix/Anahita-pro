from enum import Enum


class State(Enum):

    IDLE = 0

    ADD_NAME = 1

    ADD_DATE = 2

    ADD_CHANNEL = 3

    EDIT = 4