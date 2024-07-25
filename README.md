# skyrim_quiz
This is education project of creatin' bot for telegram with help of aiogram.

Press button, or write /whiterun to start quiz.

This is a Python script that implements a quiz bot using the aiogram library, which is a Python wrapper for the Telegram Bot API. Here's a breakdown of the code:

Importing Libraries

The script starts by importing various libraries:

nest_asyncio: a library that allows running asynchronous code in a synchronous environment.
asyncio: a built-in Python library for writing single-threaded concurrent code.
logging: a built-in Python library for logging events.
aiosqlite: a library that provides an asynchronous interface to SQLite databases.
aiogram: the main library for building Telegram bots.
quiz_data and db_commands: custom modules that contain quiz data and database commands, respectively.
Setting up the Bot

The script sets up a Telegram bot using the aiogram library:

API_TOKEN: a variable that stores the bot's API token.
bot: an instance of the Bot class, which represents the Telegram bot.
dp: an instance of the Dispatcher class, which is responsible for handling incoming messages and callbacks.
Defining Keyboard Builders

The script defines two keyboard builders:

generate_options_keyboard: a function that generates an inline keyboard with answer options for a quiz question.
ReplyKeyboardBuilder: a class that builds a reply keyboard with a single button to start the quiz.
Defining Callback Handlers

The script defines two callback handlers:

right_answer: a function that handles callbacks when a user answers a question correctly.
wrong_answer: a function that handles callbacks when a user answers a question incorrectly.
Both handlers update the quiz state, display a message to the user, and proceed to the next question or end the quiz if necessary.

Defining Message Handlers

The script defines three message handlers:

cmd_start: a function that handles the /start command and displays a welcome message with a button to start the quiz.
cmd_quiz: a function that handles the /whiterun command or the "Начать игру" button and starts a new quiz.
new_quiz: a function that starts a new quiz by updating the quiz state and displaying the first question.
Defining Database Functions

The script defines several database functions:

update_quiz_index: a function that updates the quiz state in the database.
get_quiz_index: a function that retrieves the current quiz index from the database.
save_results: a function that saves the quiz results to the database.
Main Function

The script defines a main function that:

Creates the database tables using the create_table function from the db_commands module.
Starts the bot using the start_polling method of the Dispatcher class.
Running the Bot

Finally, the script runs the bot using the asyncio.run function, which executes the main function asynchronously.

Overall, this script implements a simple quiz bot that uses a SQLite database to store quiz state and results. The bot responds to user input, updates the quiz state, and displays messages and keyboards accordingly.
