# -*- coding: utf-8 -*-
import telebot
from telebot import types
import os
from flask import Flask, request
import threading

# Минимальный веб-сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "pong", 200

def run_web():
    app.run(host='0.0.0.0', port=5000)

# Запускаем веб-сервер в фоне
web_thread = threading.Thread(target=run_web, daemon=True)
web_thread.start()

# Ваш бот
bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("Происхождение", callback_data="history")
    btn2 = types.InlineKeyboardButton("Виды", callback_data="types")
    btn3 = types.InlineKeyboardButton("Их мотивы и цели", callback_data="motives")
    btn4 = types.InlineKeyboardButton("Произведения", callback_data="works")
    btn5 = types.InlineKeyboardButton("Что это вообще такое?", callback_data="what_is")
    btn6 = types.InlineKeyboardButton("Автор заикался", callback_data="avtor_is")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.send_message(
        message.chat.id, 
        "Добро пожаловать в микро-справочник по тентаклям\n\nВыбери, что тебя интересует:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "history":
        text = """
Слово «тентакли» появилось на свет в результате чудовищной ошибки неизвестного естествоиспытателя, который в условиях, приближённых к существующей реальности жителей японских прибрежных посёлков (а именно — вдоволь напившись сакэ) попытался пересчитать щупальца у Хозяина Моря. Щупалец оказалось неровным счётом пять («пентакль»). 
Утром естествоиспытатель с больной головой пересчитал щупальца — на сей раз он сосчитал верно, и их оказалось восемь. Не долго думая, от слова «пентакль» была взята первая буква и принята за цифру 5.
П = 5
Р = 6
С = 7
Т = 8
Так появилось слово «тентакль».
По альтернативной версии, тот самый естествоиспытатель был родом из Англии и насчитал десять щупалец (англ. ten — «десять»).
Другая версия гласит, что саке было выпито достаточно, дабы в глазах свершилось раздвоение, и щупалец оказалось ровным счётом десять (англ. ten — «десять»).
Некто Децл однажды предположил, что дреды — это «такие» тентакли, что, безусловно, является ересью. Вскоре он исчез, зохаванный Ктулху, а его место занимает бракованный ОБЧР.
Также, по непроверенным данным, война в Камбодже была начата именно тентаклями, а не морскими котами, как многие думают."""
        show_back_button(call, text)
        
    elif call.data == "types":
        show_types_menu(call.message)
        
    elif call.data == "types_origin":
        show_origin_menu(call.message)
        
    elif call.data == "types_function":
        show_function_menu(call.message)
        
    elif call.data == "origin_biological":
        text = """
 **Биологические тентакли**

Тентакли естественного происхождения у морских существ:
Осьминоги - 8 гибких щупалец
Кальмары - 8 рук + 2 ловчих щупальца
Медузы - тонкие стрекательные щупальца
Актинии - ловчие щупальца с ядом

Характеристики: гибкость, регенерация, тактильная чувствительность.
        """
        show_back_to_origin(call, text)
        
    elif call.data == "origin_alien":
        text = """
 **Инопланетные тентакли**

Внеземные существа с тентаклями:
Космические монстры - огромные щупальца
Инопланетные расы - разумные существа
Гибриды - смесь органики и технологии

Особенности: необычные цвета, свечение, особые способности.
        """
        show_back_to_origin(call, text)
        
    elif call.data == "origin_mythical":
        text = """
 **Мифические тентакли**

Божества и монстры из мифологии:
Кракены - гигантские морские чудовища
Ктулху - космическое божество
Гидры - многоголовые чудовища
Древние боги - в стиле Лавкрафта

Особенности: огромные размеры, магические способности.
        """
        show_back_to_origin(call, text)
        
    elif call.data == "origin_mechanical":
        text = """
 **Механические тентакли**

Искусственно созданные тентакли:
Роботы-осьминоги - для исследований
Кибернетические протезы
Боевые машины с щупальцами
Медицинские роботы

Преимущества: прочность, программируемость, специализация.
        """
        show_back_to_origin(call, text)
        
    elif call.data == "function_combat":
        text = """
**Боевые тентакли**

Используются для атаки и защиты:
Ударные щупальца - мощные удары
Хватательные - захват противника
Ядовитые - инъекция токсинов
Режущие - острые как лезвия

Применение: ближний бой, обездвиживание, устрашение.
        """
        show_back_to_function(call, text)
        
    elif call.data == "function_manipulation":
        text = """
**Манипуляционные тентакли**

Для тонких операций и работы:
Точные манипуляции - как пальцы
Подъем грузов - мощные захваты
Исследовательские - сенсоры и камеры
Строительные - монтаж конструкций

Применение: наука, медицина, промышленность.
        """
        show_back_to_function(call, text)
        
    elif call.data == "function_romantic":
        text = """
**Романтические/ эротические тентакли**

В культурном и художественном контексте:
Нежные прикосновения
Объятия и защита
Символика многогранности
Художественный троп в аниме
Спаривание (нет блин спаринг)
Оплодотворение

Особенности: эстетика, символика, эмоциональность, НУ И КОНЕЧНО ЖЕЛАНИЕ ВЫЕКАТЬ ТЕБЯЯ.
        """
        show_back_to_function(call, text)
        
    elif call.data == "function_defensive":
        text = """
**Защитные тентакли**

Для обороны и выживания:
Шипастые щупальца - физическая защита
Камуфляжные - маскировка
Дымовые - создание завесы
Регенерирующие - быстрое восстановление

Применение: самозащита, укрытие, бегство.
        """
        show_back_to_function(call, text)
        
    elif call.data == "motives":
        text = """
**Мотивы и цели тентаклей:**

Да хз, автор устал уже писать, главное, они  хотят весело провести с тобой время...ну может быть весело будет только им, но это не важно.
Но зато известны мотивы автора: сделать из подручных средств такое щупальце и посадить на него кого-то
        """
        show_back_button(call, text)
        
    elif call.data == "works":
        text = """
Первыми произведениями считаются:
Гравюра Кацусики Хокусая «Сон жены рыбака» (1814)
Нэцкэ с подобным сюжетом (XVII век). 

Литература:
"Зов Ктулху" Г.Ф. Лавкрафт
"Война миров" Герберт Уэллс

Аниме и манга:
Стальной алхимик
One Piece
Токийский гуль (ХАХА ЧЁ СЕРЬЁЗНО)
        """
        show_back_button(call, text)
        
    elif call.data == "what_is":
        text = """
Тентакль (от лат. tentaculum — «щупальце»)

Тентакли (также щупальца, лат. tentacula) — щупальцеподобные образования некоторых живых организмов. В советской науке термин подвергался критике, как следование зарубежной терминологии, наравне с терминами педункль (лат. pedunculus) вместо «стебельки»[1]. После окончательного выделения протист в отдельную парафилетическую группу термин «тентакль» иногда используется для обозначения функциональных аналогов щупалец у протист, в отличие от собственно «щупальца» у животных[2].

Тентакли — фаллический символ в манге и аниме жанра хентай, обычно изображаемый в виде многочисленных щупалец осьминогов.

Тентакл — вымышленное существо из компьютерной игры Half-Life.
        """
        show_back_button(call, text)

    elif call.data == "avtor_is":
        text = """
ААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА.
        """
        show_back_button(call, text)
    
    elif call.data == "back":
        show_main_menu(call.message)
        
    elif call.data == "back_to_types":
        show_types_menu(call.message)
        
    elif call.data == "back_to_origin":
        show_origin_menu(call.message)
        
    elif call.data == "back_to_function":
        show_function_menu(call.message)
    
    bot.answer_callback_query(call.id)

def show_main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("Происхождение", callback_data="history")
    btn2 = types.InlineKeyboardButton("Их виды", callback_data="types")
    btn3 = types.InlineKeyboardButton("Мотивы и цели", callback_data="motives")
    btn4 = types.InlineKeyboardButton("Произведения", callback_data="works")
    btn5 = types.InlineKeyboardButton("Что это вообще такое?", callback_data="what_is")
    btn6 = types.InlineKeyboardButton("Автор заикался", callback_data="avtor_is")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Добро пожаловать в микро-справочник по тентаклям\n\nВыбери, что тебя интересует:",
        reply_markup=markup
    )

def show_types_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("По происхождению", callback_data="types_origin")
    btn2 = types.InlineKeyboardButton("По функциям", callback_data="types_function")
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back")
    
    markup.add(btn1, btn2, btn_back)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="**Виды тентаклей**\n\nВыберите классификацию:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_origin_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("Биологические", callback_data="origin_biological")
    btn2 = types.InlineKeyboardButton("Инопланетные", callback_data="origin_alien")
    btn3 = types.InlineKeyboardButton("Мифические", callback_data="origin_mythical")
    btn4 = types.InlineKeyboardButton("Механические", callback_data="origin_mechanical")
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back_to_types")
    
    markup.add(btn1, btn2, btn3, btn4, btn_back)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="**Тентакли по происхождению**\n\nВыберите тип:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_function_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("Боевые", callback_data="function_combat")
    btn2 = types.InlineKeyboardButton("Манипуляционные", callback_data="function_manipulation")
    btn3 = types.InlineKeyboardButton("Романтические", callback_data="function_romantic")
    btn4 = types.InlineKeyboardButton("Защитные", callback_data="function_defensive")
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back_to_types")
    
    markup.add(btn1, btn2, btn3, btn4, btn_back)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="**Тентакли по функциям**\n\nВыберите назначение:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_back_button(call, text):
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back")
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=markup
    )

def show_back_to_origin(call, text):
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back_to_origin")
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=markup
    )

def show_back_to_function(call, text):
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back_to_function")
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=markup
    )

if __name__ == "__main__":
    try:
        print("Бот-справочник запущен...")
        print("Веб-сервер запущен на порту 5000")
        print("Бот работает в режиме polling")
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
