
import random
from datetime import datetime
import ast
import operator


# -------------------- CHAT HISTORY --------------------

def save_history(sender, message):
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"{sender}: {message}\n")


# -------------------- BOT REPLY --------------------

def bot_reply(message):
    print("Bot:", message)
    save_history("Bot", message)


# -------------------- CALCULATOR --------------------

def safe_calculate(expression):

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow
    }

    if len(expression) > 100:
        raise ValueError("Expression too long")

    tree = ast.parse(expression, mode="eval")

    def solve(node):

        if isinstance(node, ast.Expression):
            return solve(node.body)

        elif isinstance(node, ast.Constant) and type(node.value) in (int, float):

            if abs(node.value) > 1e100:
                raise ValueError("Number too large")

            return node.value

        elif isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:

            left = solve(node.left)
            right = solve(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")

            result = allowed_operators[type(node.op)](left, right)

            if abs(result) > 1e100:
                raise ValueError("Result too large")

            return result

        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):

            value = solve(node.operand)

            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Invalid expression")

    return solve(tree)


# -------------------- RESPONSE GENERATOR --------------------

def get_response(user_input, user_name):

    if user_input.startswith("my name is "):

        name = user_input[11:].strip().title()

        if name:
            return f"Nice to meet you, {name}! 😊", name

        return "I didn't catch your name.", user_name

    elif user_input in ["what is my name", "do you know my name"]:

        if user_name:
            return f"Your name is {user_name}! 😊", user_name

        return "You haven't told me your name yet.", user_name

    elif any(word in user_input.split() for word in ["hello", "hi", "hey", "hii", "hiii"]):

        if user_name:
            responses = [
                f"Hi {user_name}! How can I help you? 😊",
                f"Hello {user_name}! Nice to see you!",
                f"Hey {user_name}! What can I do for you?",
                f"Hi there, {user_name}! 😊"
            ]

        else:
            responses = [
                "Hi! How can I help you?",
                "Hello! Nice to meet you!",
                "Hey! What can I do for you?",
                "Hi there! 😊"
            ]

        return random.choice(responses), user_name

    elif any(phrase in user_input for phrase in [
        "how are you",
        "how are you doing",
        "are you doing okay",
        "how are you today"
    ]):

        responses = [
            "I'm doing great! Thanks for asking. 😊",
            "I'm fine! How about you?",
            "All good here! What about you?"
        ]

        return random.choice(responses), user_name

    elif user_input == "what is your name":

        return "I'm CodeBot!", user_name

    elif user_input == "help":

        return "You can say hello, ask how I am, ask my name, or say bye.", user_name

    elif user_input in ["thanks", "thank you"]:

        return "You're welcome!", user_name

    elif user_input in ["good morning", "morning"]:

        return "Good morning! 🌞 Have a great day!", user_name

    elif user_input in ["good night", "night"]:

        return "Good night! 🌙 Sleep well!", user_name

    elif any(phrase in user_input for phrase in [
        "what can you do",
        "your features",
        "what are your abilities",
        "how can you help me"
    ]):

        return """
Here are some things I can do!

1. Chat with you
2. Remember your name
3. Tell you the date and time
4. Tell jokes
5. Answer basic questions
6. Perform simple calculations
""", user_name

    elif user_input in ["who created you", "who made you"]:

        return "I was created by Vanshika as part of The Vanshika Python project!", user_name

    elif user_input in ["tell me a joke", "joke"]:

        return "Why do programmers prefer dark mode?\nBecause light attracts bugs! 😂", user_name

    elif user_input in ["time", "what time is it", "current time"]:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}", user_name

    elif user_input in ["date", "today's date", "what is today's date"]:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}", user_name

    elif user_input.startswith("calculate "):

        expression = user_input[10:]

        try:
            result = safe_calculate(expression)

            return f"The answer is {result}", user_name

        except (ValueError, SyntaxError, TypeError, ZeroDivisionError, OverflowError, RecursionError):
            return "Please enter a valid arithmetic expression.", user_name

    else:

        return "Sorry, I don't understand that.", user_name


# -------------------- MAIN CHATBOT --------------------

def chatbot():

    print("================================")
    print("       🤖 THE VANSHiKA")
    print("================================")
    print("Type 'bye' to exit.\n")

    user_name = None

    while True:

        original_input = input("You: ").strip()

        if not original_input:
            continue

        user_input = original_input.lower().strip(" ?!.")

        save_history("You", original_input)

        if user_input in ["bye", "exit"]:

            bot_reply("Goodbye! Have a great day!")
            break

        response, user_name = get_response(user_input, user_name)

        bot_reply(response)


# -------------------- RUN PROJECT --------------------

if __name__ == "__main__":
    chatbot()
