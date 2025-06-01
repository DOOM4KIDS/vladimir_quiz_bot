import logging
from telegram import *
from telegram.ext import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

START, Q1, Q2, Q3, Q4, Q5, END = range(7)

QUIZ = {
    "q1": {
        "text": "1. Кто крестил Русь?\n1) Пётр Великий\n2) Иван Грозный\n3) Князь Владимир Святославович",
        "correct": "3",
        "explanation": "✅ Верно!"
    },
    "q2": {
        "text": "2. Как был представлен образ Князя Владимира в советский период?\n1) Строго положительным\n2) Неоднозначным, признавалась его роль в объединении государства\n3) Строго негативным",
        "correct": "2",
        "explanation": "✅ Верно!"
    },
    "q3": {
        "text": "3. В каком году вышел мультфильм 'Князь Владимир'?\n1) 2004\n2) 2005\n3) 2006",
        "correct": "3",
        "explanation": "✅ Верно!"
    },
    "q4": {
        "text": "4. На какой московской площади расположен памятник Владимиру Великому?\n1) Боровицкая\n2) Манежная\n3) Рижская",
        "correct": "1",
        "explanation": "✅ Верно!"
    },
    "q5": {
        "text": "5. Кто сыграл главную роль в кинофильме 'Викинг' 2016 года?\n1) Александр Петров\n2) Данила Козловский\n3) Алексей Серебряков",
        "correct": "2",
        "explanation": "✅ Верно!"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал квиз.")
    
    reply_keyboard = [["Начать квиз"]]
    
    await update.message.reply_text(
        f"Приветствую! Это квиз об образе князя Владимира в русской культурной памяти.\n"
        "Вас ждёт 5 вопросов с вариантами ответов.\n\n"
        "Нажмите 'Начать квиз', когда будете готовы!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return START

async def question_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["score"] = 0
    await update.message.reply_text(
        QUIZ["q1"]["text"],
        reply_markup=ReplyKeyboardMarkup(
            [["1", "2", "3"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return Q1

async def question_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    
    if user_answer == QUIZ["q1"]["correct"]:
        context.user_data["score"] += 1
        await update.message.reply_text(QUIZ["q1"]["explanation"])
    else:
        await update.message.reply_text("❌ Неверно. Правильный ответ: 3) Князь Владимир Святославович")
    
    await update.message.reply_text(
        QUIZ["q2"]["text"],
        reply_markup=ReplyKeyboardMarkup(
            [["1", "2", "3"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return Q2

async def question_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    
    if user_answer == QUIZ["q2"]["correct"]:
        context.user_data["score"] += 1
        await update.message.reply_text(QUIZ["q2"]["explanation"])
    else:
        await update.message.reply_text("❌ Неверно. Правильный ответ: 2) Неоднозначным")
    
    await update.message.reply_text(
        QUIZ["q3"]["text"],
        reply_markup=ReplyKeyboardMarkup(
            [["1", "2", "3"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return Q3

async def question_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    
    if user_answer == QUIZ["q3"]["correct"]:
        context.user_data["score"] += 1
        await update.message.reply_text(QUIZ["q3"]["explanation"])
    else:
        await update.message.reply_text("❌ Неверно. Правильный ответ: 3) 2006")
    
    await update.message.reply_text(
        QUIZ["q4"]["text"],
        reply_markup=ReplyKeyboardMarkup(
            [["1", "2", "3"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return Q4

async def question_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    
    if user_answer == QUIZ["q4"]["correct"]:
        context.user_data["score"] += 1
        await update.message.reply_text(QUIZ["q4"]["explanation"])
    else:
        await update.message.reply_text("❌ Неверно. Правильный ответ: 1) Боровицкая")
    
    await update.message.reply_text(
        QUIZ["q5"]["text"],
        reply_markup=ReplyKeyboardMarkup(
            [["1", "2", "3"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return Q5

async def end_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    
    if user_answer == QUIZ["q5"]["correct"]:
        context.user_data["score"] += 1
        await update.message.reply_text(QUIZ["q5"]["explanation"])
    else:
        await update.message.reply_text("❌ Неверно. Правильный ответ: 2) Данила Козловский")
    
    score = context.user_data.get("score", 0)
    percentage = int(score / len(QUIZ) * 100)
    
    if percentage == 100:
        reaction = " "
    elif percentage >= 70:
        reaction = " "
    elif percentage >= 40:
        reaction = " "
    else:
        reaction = " "
    
    await update.message.reply_text(
        f"📊 <b>Твой результат:</b> {score} из {len(QUIZ)} ({percentage}%)\n"
        f"{reaction}\n\n"
        "Чтобы пройти квиз ещё раз, нажми /start",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} отменил квиз.")
    await update.message.reply_text(
        "Квиз прерван. Нажми /start, чтобы начать заново.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7629024665:AAF1w5BC_fEcbX8A7QEFZPUIJ3WZvqduBI8").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(filters.Regex("^Начать квиз$"), question_1)],
            Q1: [MessageHandler(filters.Regex("^[123]$"), question_2)],
            Q2: [MessageHandler(filters.Regex("^[123]$"), question_3)],
            Q3: [MessageHandler(filters.Regex("^[123]$"), question_4)],
            Q4: [MessageHandler(filters.Regex("^[123]$"), question_5)],
            Q5: [MessageHandler(filters.Regex("^[123]$"), end_quiz)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
