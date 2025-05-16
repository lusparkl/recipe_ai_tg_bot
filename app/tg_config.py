from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

main_menu = InlineKeyboardBuilder()
recipe_from_name = types.InlineKeyboardButton(text = "🔍 Find", callback_data = "recipe_from_name")
recipe_from_ingridients = types.InlineKeyboardButton(text = "🍎 Create", callback_data = "recipe_from_ingridients")
saved = types.InlineKeyboardButton(text = "📚 My Saved Recipes", callback_data = "saved") 
main_menu.row(recipe_from_name, recipe_from_ingridients)
main_menu.row(saved)

back_menu = InlineKeyboardBuilder()
back_btn = types.InlineKeyboardButton(text="Back", callback_data="back")
back_menu.row(back_btn)

recipe_menu=InlineKeyboardBuilder()
save_btn=types.InlineKeyboardButton(text="Save", callback_data="save")
recipe_menu.row(back_btn, save_btn)

empty_button = types.InlineKeyboardButton(text="\u2800", callback_data="empty")
next_button = types.InlineKeyboardButton(text="Next", callback_data="next")
previous_button = types.InlineKeyboardButton(text="Previous", callback_data="previous")

saved_menu_first=InlineKeyboardBuilder()
saved_menu_first.row(empty_button, back_btn, next_button)
saved_menu_mid=InlineKeyboardBuilder()
saved_menu_mid.row(previous_button, back_btn, next_button)
saved_menu_last=InlineKeyboardBuilder()
saved_menu_last.row(previous_button, back_btn, empty_button)

main_menu_text="""🍳 Welcome to RecipeBot! 🍳

Your personal cooking assistant is here to inspire your next delicious meal!

What would you like to do today?

🔍 Find Recipe by Dish - Know exactly what you want to cook? Let me find the perfect recipe!

🍎 Create from Ingredients - Have random ingredients in your kitchen? Let's create something amazing!

📚 My Recipe Collection - Browse your saved culinary masterpieces"""

dish_from_name_text="""🔍 Find Recipe by Dish Name 🔍

Please enter the name of a dish you'd like to make.
For example: "Chicken Parmesan", "Vegetable Curry", or "Chocolate Chip Cookies"

Type the dish name below and I'll provide a complete recipe!"""

dish_from_ingridients_text="""🍎 Recipe from Ingredients 🍎

What ingredients do you have available? 

List them separated by commas (e.g., chicken, rice, tomatoes, garlic)

I'll create a delicious recipe using what you have on hand!"""

