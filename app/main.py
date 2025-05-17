from aiogram import types, F, Router, Bot
from aiogram.filters import Command
import app.tg_config as cnfg
from app.db import Database
from aiogram.fsm.context import FSMContext
from app.requests import get_recipe_by_name, get_recipe_by_ingridients
from app.states import Req, Pag

rt = Router()

@rt.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    await message.answer_photo(caption=cnfg.main_menu_text, photo=types.FSInputFile("img/search_by_name.png"), reply_markup=cnfg.main_menu.as_markup(), parse_mode="Markdown")
    db = Database()
    if not db.is_user_exists(user_id=message.from_user.id):
        db.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username or "unknown"
        )
    db.close()

@rt.callback_query(F.data == "recipe_from_name")
async def by_name_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    message_to_delete = await callback.message.edit_caption(caption=cnfg.dish_from_name_text, reply_markup=cnfg.back_menu.as_markup(), parse_mode="Markdown")
    await state.set_state(Req.by_name)
    await state.update_data(message_to_delete=message_to_delete)

@rt.message(Req.by_name)
async def make_request_by_name(message: types.Message, state: FSMContext):
    await state.set_state(Req.currently_requesting)
    dish_name=message.text
    try: 
        responce = await get_recipe_by_name(dish_name=dish_name)
        await show_recipe(message=message, recipe=responce)
    except Exception as e:
        await message.answer(text="Something wrong here", reply_markup=cnfg.back_menu.as_markup(), parse_mode="Markdown")
    finally:
        message_to_delete = await state.get_value("message_to_delete")
        await message_to_delete.delete()
        await state.clear()

@rt.callback_query(F.data == "recipe_from_ingridients")
async def by_ingridients_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    message_to_delete = await callback.message.edit_caption(caption=cnfg.dish_from_ingridients_text, reply_markup=cnfg.back_menu.as_markup(), parse_mode="Markdown")
    await state.set_state(Req.by_ingridients)
    await state.update_data(message_to_delete=message_to_delete)

@rt.message(Req.by_ingridients)
async def make_request_by_ingridients(message: types.Message, state: FSMContext):
    await state.set_state(Req.currently_requesting)
    ingridients=message.text
    try: 
        responce = await get_recipe_by_ingridients(user_ingridients=ingridients)
        await show_recipe(message=message, recipe=responce)
    except Exception as e:
        await message.answer(text="Something wrong here", reply_markup=cnfg.back_menu.as_markup(), parse_mode="Markdown")
    finally:
        message_to_delete = await state.get_value("message_to_delete")
        await message_to_delete.delete()
        await state.clear()

async def show_recipe(*, message: types.Message, recipe: str):
    await message.answer(text=recipe, reply_markup=cnfg.recipe_menu.as_markup(), parse_mode="Markdown")
    
@rt.message(Req.currently_requesting)
async def currently_requesting_message(message: types.Message):
    await message.answer("Currently requesting your recipe, wait a sec")

@rt.callback_query(F.data == "saved")
async def show_saved_recipes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Pag)
    db = Database()
    current_page = 0
    recipes=db.get_user_recipes(user_id=callback.from_user.id)

    if not recipes:
        await callback.message.edit_caption(caption="You don't have any saved recipes yet!", reply_markup=cnfg.back_menu.as_markup())
        return
    
    await state.update_data(current_page=current_page, recipes=recipes)
    current_recipe=recipes[current_page]

    keyboard = cnfg.saved_menu_first if len(recipes) > 1 else cnfg.back_menu
    await callback.message.answer(
        text=current_recipe,
        reply_markup=keyboard.as_markup(),
        parse_mode="Markdown"
    )
    db.close()

@rt.callback_query(F.data.in_(["next", "previous"]))
async def paginate_recipes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get('page', 0)
    recipes = data.get('recipes', [])
    
    if callback.data == "next":
        page += 1
    else:
        page -= 1
        
    current_recipe = recipes[page]
    
    if page == 0:
        keyboard = cnfg.saved_menu_first
    elif page == len(recipes) - 1:
        keyboard = cnfg.saved_menu_last
    else:
        keyboard = cnfg.saved_menu_mid
        
    await callback.message.edit_text(
        text=current_recipe,
        reply_markup=keyboard.as_markup(),
        parse_mode="Markdown"
    )
    await state.update_data(page=page)

@rt.callback_query(F.data == "back")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer_photo(caption=cnfg.main_menu_text, photo=types.FSInputFile("img/search_by_name.png"), reply_markup=cnfg.main_menu.as_markup(), parse_mode="Markdown")
    await callback.message.delete()

@rt.callback_query(F.data == "save")
async def save_recipe(callback: types.CallbackQuery):
    await callback.answer()
    u_id=callback.from_user.id
    recipe=callback.message.text
    db=Database()
    response = db.add_recipe(user_id=u_id, recipe=recipe)
    await callback.answer("Saved!" if response else "Failed to save")