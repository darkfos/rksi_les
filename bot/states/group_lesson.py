from aiogram.fsm.state import State, StatesGroup


class GroupState(StatesGroup):
    """
        Состояние - получения названия группы для поиска
        расписания пар
    """

    name_group = State()