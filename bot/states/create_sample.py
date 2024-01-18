from aiogram.fsm.state import StatesGroup, State
from aiogram import types

class SampleData(StatesGroup):
    name: str = State()
    name_group: str = State()