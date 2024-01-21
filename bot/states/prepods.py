from aiogram.fsm.state import State, StatesGroup


class TeacherState(StatesGroup):
    """
        Состояние - получения инициалов преподавателя
        для поиска расписания пар
    """

    name = State()