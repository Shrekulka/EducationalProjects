# bot_guess_the_number/handlers/client.py
import traceback

from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import ATTEMPTS, POSITIVE_RESPONSE, NEGATIVE_RESPONSE
from create_bot import bot
from data_base.sqlite_db import get_user_game_data, update_user_game_data
from models.user_game_data import UserGameData
from utils.client_utils import get_random_number


# @dp.message(CommandStart()) или @dp.message(Command(commands=["start"]))
async def process_start_command(message: Message) -> None:
    """
        Handles the /start command, sends a welcome message to the user with their name and suggests starting the
        "Guess the number" game. Removes the /start command from the chat.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None

        Exceptions:
            If an error occurs while sending the message, returns information about the error.
    """
    try:
        # Получаем данные игры пользователя по его идентификатору
        user_id = message.from_user.id
        user_data = await get_user_game_data(user_id)

        # Если игра для данного пользователя уже идет, то отправляем сообщение о том, что игра уже начата
        if user_data.is_playing:
            await message.answer("You are already playing a game.")
            return

        # Создаем новые данные игры для данного пользователя и обновляем их
        new_user_data = UserGameData(user_id=user_id)
        await update_user_game_data(new_user_data)

        # Отправка приветственного сообщения с именем пользователя и предложение начать игру
        await bot.send_message(message.from_user.id,
                               f"Hello, {message.from_user.first_name}! 👋\n\nLet's play 'Guess the number'?"
                               f"\n\nTo get the rules and a list of available commands, send /help 🎮")
        # Удаление команды /start из чата
        await message.delete()
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# @dp.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    """
        Handles the /help command, sends the game rules and a list of available commands to the user.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)
    # Отправляем сообщение с правилами игры и списком команд
    await message.answer(f"Game rules:\n\nI choose a number between 1 and 100, and you need to guess it"
                         f"\nYou have {user_data.remaining_attempts} attempts\n\nAvailable commands:\n/help - game "
                         f"rules and command list\n/cancel - exit the game\n/stat - view statistics\n\nLet's play? 🎲")


# @dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message) -> None:
    """
        Handles the /stat command, sends the user their game statistics.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)

    # Если у пользователя нет данных об игре, отправляем сообщение о том, что у него нет статистики
    if user_data is None:
        await message.answer("You don't have any game statistics yet. 📊")
        return
    # Отправляем сообщение со статистикой игры пользователя
    await message.answer(f"🎮 Total games played: {user_data.total_games}\n🏆 Games won: {user_data.games_won}")


# @dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message) -> None:
    """
        Handles the /cancel command, allowing the user to exit the current game.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)
    # Если пользователь играет, устанавливаем флаг is_playing в False и обновляем данные пользователя
    if user_data.is_playing:
        user_data.is_playing = False
        await update_user_game_data(user_data)
        # Отправляем сообщение о том, что пользователь вышел из игры
        await message.answer("You have exited the game. If you want to play again, let me know. 😔")
    # Если пользователь не играет, отправляем сообщение о том, что мы не играем с ним, но можем поиграть один раз
    else:
        await message.answer("We're not playing with you anyway. Maybe let's play once? 😉")


# @dp.message(F.text.lower().in_(POSITIVE_RESPONSE))
async def process_positive_answer(message: Message) -> None:
    """
        Handles the positive response from the user to start the game.

        Arguments:
            message (Message): The message object containing information about the user who sent the response.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)
    # Если пользователь не играет, устанавливаем флаг is_playing в True, выбираем случайное число, устанавливаем
    # количество оставшихся попыток и обновляем данные пользователя
    if not user_data.is_playing:
        user_data.is_playing = True
        user_data.target_number = get_random_number()
        user_data.remaining_attempts = ATTEMPTS
        await update_user_game_data(user_data)
        # Отправляем сообщение о начале игры
        await message.answer("Hooray! 🎉\n\nI've chosen a number between 1 and 100, try to guess it!")
    # Если пользователь уже играет, отправляем сообщение о том, что мы можем реагировать только на числа от 1 до 100
    # и команды /cancel и /stat во время игры
    else:
        await message.answer("I can only react to numbers from 1 to 100 and the commands "
                             "/cancel and /stat while we're playing the game. 🎲")


# @dp.message(F.text.lower().in_(NEGATIVE_RESPONSE))
async def process_negative_answer(message: Message) -> None:
    """
        Handles the negative response from the user to start the game.

        Arguments:
            message (Message): The message object containing information about the user who sent the response.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)
    # Если пользователь не играет, отправляем сообщение о том, что это жаль, и предлагаем сыграть снова
    if not user_data.is_playing:
        await message.answer("That\'s too bad. 😔\n\nIf you want to play again, just let me know.")
    # Если пользователь уже играет, отправляем сообщение о том, что мы сейчас играем, и просим отправлять числа 1-100
    else:
        await message.answer("We are currently playing a game. Please send numbers from 1 to 100. 🎲")


# @dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message) -> None:
    """
        Handles the user's response containing numbers within the 'Guess the number' game.

        Arguments:
            message (Message): The message object containing information about the user and the textual content
            of the response.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)
    # Если пользователь играет
    if user_data.is_playing:

        # Если осталась 1 попытка
        if user_data.remaining_attempts == 1:
            # Помечаем, что пользователь больше не играет
            user_data.is_playing = False
            # Увеличиваем общее количество сыгранных игр
            user_data.total_games += 1
            # Обновляем данные игры пользователя
            await update_user_game_data(user_data)
            # Отправляем сообщение о том, что пользователь проиграл и предлагаем сыграть ещё раз
            await message.answer(f"Unfortunately, you have no more attempts left. You lost. 😔\n\nMy number "
                                 f"was {user_data.target_number}\n\nLet\'s play again? 🎮")

        # Если введенное пользователем число равно загаданному числу
        elif int(message.text) == user_data.target_number:
            # Помечаем, что пользователь больше не играет
            user_data.is_playing = False
            # Увеличиваем общее количество сыгранных игр
            user_data.total_games += 1
            # Увеличиваем количество выигранных игр
            user_data.games_won += 1
            # Обновляем данные игры пользователя
            await update_user_game_data(user_data)
            # Отправляем сообщение о том, что пользователь угадал число и предлагаем сыграть ещё раз
            await message.answer("Hooray!!! You guessed the number! 🎉\n\nMaybe let\'s play again? 🎮")

        # Если введенное пользователем число больше загаданного числа
        elif int(message.text) > user_data.target_number:
            # Уменьшаем количество оставшихся попыток
            user_data.remaining_attempts -= 1
            # Обновляем данные игры пользователя
            await update_user_game_data(user_data)
            # Отправляем сообщение о том, что число меньше введенного и указываем количество оставшихся попыток
            await message.answer(f"My number is lower. 🔽\nYou have {user_data.remaining_attempts} attempts left.")

        # Если введенное пользователем число меньше загаданного числа
        elif int(message.text) < user_data.target_number:
            # Уменьшаем количество оставшихся попыток
            user_data.remaining_attempts -= 1
            # Обновляем данные игры пользователя
            await update_user_game_data(user_data)
            # Отправляем сообщение о том, что число больше введенного и указываем количество оставшихся попыток
            await message.answer(f"My number is higher. 🔼\nYou have {user_data.remaining_attempts} attempts left.")

    # Если пользователь ещё не начал игру, отправляем сообщение с предложением начать игру
    else:
        await message.answer("We are not playing yet. Do you want to play? 🎲")


# @dp.message()
async def process_other_answers(message: Message) -> None:
    """
        Handles user responses that are not numbers within the 'Guess the number' game.

        Arguments:
            message (Message): The message object containing information about the user and the textual content
            of the response.

        Returns:
            None
    """
    # Получаем данные игры пользователя по его идентификатору
    user_data = await get_user_game_data(message.from_user.id)
    # Если пользователь уже играет, отправляем сообщение о том, что игра уже идёт
    if user_data.is_playing:
        await message.answer("We are currently playing a game. Please send numbers from 1 to 100. 🎯")
    # Если пользователь не играет, отправляем сообщение с предложением начать игру
    else:
        await message.answer("I'm a pretty limited bot, let's just play a game, shall we? 😅")


def register_handlers_client(dp: Dispatcher) -> None:
    """
        Register all handlers for the client part of the bot.

        Args:
            dp: The Dispatcher instance.
    """
    # Регистрируем хэндлеры команд
    dp.message.register(process_start_command, CommandStart())  # Обработка команды /start
    dp.message.register(process_stat_command, Command(commands='stat'))  # Обработка команды /stat
    dp.message.register(process_help_command, Command(commands='help'))  # Обработка команды /help
    dp.message.register(process_cancel_command, Command(commands='cancel'))  # Обработка команды /cancel

    # Регистрируем хэндлеры ответов пользователя

    # Обработка положительных ответов пользователя
    dp.message.register(process_positive_answer, lambda m: m.text.lower() in POSITIVE_RESPONSE)
    # Обработка отрицательных ответов пользователя
    dp.message.register(process_negative_answer, lambda m: m.text.lower() in NEGATIVE_RESPONSE)
    # Обработка числовых ответов пользователя
    dp.message.register(process_numbers_answer, lambda m: m.text.isdigit() and 1 <= int(m.text) <= 100)
    # Обработка прочих ответов пользователя
    dp.message.register(process_other_answers)
