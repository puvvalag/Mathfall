
# AI generated code

import os
import time
import random
import msvcrt
from colorama import init, Fore, Style

# Initialize colorama for colored text in the console
init()

# Game settings
SCREEN_HEIGHT = 20  # Number of rows in the console "screen"
DANGER_LINE = int(SCREEN_HEIGHT * 0.9)  # 90% of the screen height
FALL_SPEED = 0.5  # Time (in seconds) between each fall step
STARTING_LIVES = 3  # Number of lives the player starts with
POINTS_PER_CORRECT = 10  # Points awarded for a correct answer
POINTS_PER_WRONG = -5  # Points deducted for a wrong answer or miss

def clear_screen():
    """Clear the console screen."""
    os.system("cls")

def generate_expression():
    """Generate a random math expression and its correct answer."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(["+", "-"])
    
    if operator == "+":
        answer = num1 + num2
    else:
        # Ensure subtraction doesn't result in a negative number
        num1, num2 = max(num1, num2), min(num1, num2)
        answer = num1 - num2
    
    return f"{num1}{operator}{num2}=", answer

def display_welcome_screen():
    """Display the welcome screen with instructions."""
    clear_screen()
    print(Fore.CYAN + "=" * 20)
    print(Fore.YELLOW + " Welcome to Math Fall! 🎉")
    print(Fore.CYAN + "=" * 20)
    print(Fore.WHITE + "Solve the math problems before they reach the red line!")
    print("Type the answer and press Enter.")
    print("You have 3 lives. Don’t let the problems fall too far!")
    print(Fore.YELLOW + "Let’s get started! 😊")
    print(Fore.CYAN + "=" * 20)
    print(Fore.WHITE + "Press any key to start...")
    msvcrt.getch()  # Wait for a key press

def display_game_over_screen(score):
    """Display the game over screen with the final score."""
    clear_screen()
    print(Fore.CYAN + "=" * 20)
    print(Fore.RED + "Game Over! 😊")
    print(Fore.YELLOW + f"Your Score: {score}")
    print(Fore.GREEN + "You’re a Math Superstar! 🌟")
    print(Fore.CYAN + "=" * 20)
    print(Fore.WHITE + "Press any key to exit...")
    msvcrt.getch()

def display_feedback(correct):
    """Display feedback based on whether the answer was correct."""
    clear_screen()
    if correct:
        print(Fore.GREEN + "Awesome! You got it! 🎈")
        print(Fore.YELLOW + "  * * *  ")  # Simple ASCII "firework"
        print(Fore.YELLOW + "  * * *  ")
    else:
        print(Fore.RED + "Oops! Try again! 😊")
    time.sleep(1)

def main():
    """Main game loop."""
    score = 0
    lives = STARTING_LIVES
    display_welcome_screen()

    while lives > 0:
        # Generate a new expression
        expression, correct_answer = generate_expression()
        position = 0  # Start at the top of the screen
        user_answer = ""  # Store the user's typed answer (corrected from user-answer)
        answered = False

        # Falling loop for the current expression
        while position < DANGER_LINE and lives > 0:
            clear_screen()
            
            # Print empty lines before the expression
            for _ in range(position):
                print()
            
            # Print the expression in a bright color
            print(Fore.YELLOW + expression)
            
            # Print empty lines after the expression
            for _ in range(SCREEN_HEIGHT - position - 2):
                print()
            
            # Print the danger line in red
            print(Fore.RED + "-" * 10 + Style.RESET_ALL)
            
            # Print score and lives
            print(Fore.CYAN + f"Score: {score}  Lives: {lives}" + Style.RESET_ALL)
            
            # Print the answer prompt
            print(Fore.WHITE + "Answer: " + user_answer, end="", flush=True)

            # Check for user input (non-blocking)
            if msvcrt.kbhit():
                char = msvcrt.getch().decode("utf-8")
                if char == "\r":  # Enter key
                    try:
                        if int(user_answer) == correct_answer:
                            score += POINTS_PER_CORRECT
                            display_feedback(True)
                        else:
                            score = max(0, score + POINTS_PER_WRONG)  # Don't let score go below 0
                            lives -= 1
                            display_feedback(False)
                        answered = True
                        break
                    except ValueError:
                        score = max(0, score + POINTS_PER_WRONG)
                        lives -= 1
                        display_feedback(False)
                        answered = True
                        break
                elif char.isdigit() or char == "-":  # Allow negative numbers
                    user_answer += char
                    print(user_answer, end="", flush=True)

            position += 1
            time.sleep(FALL_SPEED)

        # If the expression reaches the danger line without an answer
        if position >= DANGER_LINE and not answered:
            lives -= 1
            score = max(0, score + POINTS_PER_WRONG)
            clear_screen()
            print(Fore.RED + "Too slow! You lost a life! 😊")
            time.sleep(1)

    # Game over
    display_game_over_screen(score)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        clear_screen()
        print(Fore.RED + "Game exited. Thanks for playing! 😊")