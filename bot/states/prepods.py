from aiogram.fsm.state import State, StatesGroup


class TeacherState(StatesGroup):
    name = State()