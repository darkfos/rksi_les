from aiogram.fsm.state import StatesGroup, State


class SampleData(StatesGroup):
    """
        Состояние - регистрация шаблона
    """

    name: str = State()
    name_group: str = State()


class ChoicePeople(StatesGroup):

    choice_pers: str = State()
    name_pers: str = State()