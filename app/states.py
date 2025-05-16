from aiogram.fsm.state import State, StatesGroup

class Req(StatesGroup):
    by_name=State()
    by_ingridients=State()
    currently_requesting=State()
    message_to_delete=State()

class Pag(StatesGroup):
    current_page=State()
    recipes=State()