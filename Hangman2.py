# Hangman Game 
import string
import pandas as pd
import numpy as np

#Load words from file
def load_words(filename="words.txt"):
    print("Loading word list from file...")
    with open(filename, "r") as file:
        wordlist = file.read().split()
    return wordlist

#Helper functions
def is_word_guessed(secret_word, letters_guessed):
    """Check if player has guessed all letters."""
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    """Return the word with guessed letters and underscores for missing ones."""
    result = ""
    for letter in secret_word:
        if letter in letters_guessed:
            result += letter
        else:
            result += "_ "
    return result

def get_available_letters(letters_guessed):
    """Return letters that have not been guessed yet."""
    available = ""
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available += letter
    return available

# The main code
def hangman(secret_word):
    """Run one game of Hangman."""
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")

    guesses_remaining = 6
    letters_guessed = []
    total_attempts = 0
    wrong_guess = False

    # Keep looping until guesses run out or word is guessed
    while guesses_remaining > 0:
        print("-" * 25)
        print(f"You have {guesses_remaining} guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))

        guess = input("Please guess a letter: ").lower()
        total_attempts += 1

        # Validate input
        if not guess.isalpha() or len(guess) != 1:
            print("Please enter one alphabet letter only.")
            continue

        # Already guessed letter
        if guess in letters_guessed:
            print("You already guessed that letter.")
            continue

        # Add guess to list
        letters_guessed.append(guess)

        # Check guess result
        if guess in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
        else:
            print("Wrong guess:", get_guessed_word(secret_word, letters_guessed))
            guesses_remaining -= 1
            wrong_guess = True

        # Check win condition
        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            score = guesses_remaining * len(set(secret_word))
            print(f"Your score: {score}\n")
            return True, total_attempts, score, guesses_remaining

    # If loop ends, player lost
    print("You ran out of guesses. The word was:", secret_word)
    return False, total_attempts, 0, guesses_remaining

#choose difficulty
def choose_difficulty(words):
    level = input("Choose difficulty (easy / medium / hard): ").lower()
    if level == "easy":
        pool = [w for w in words if len(w) <= 5]
    elif level == "medium":
        pool = [w for w in words if 6 <= len(w) <= 8]
    else:
        pool = [w for w in words if len(w) > 8]
    return np.random.choice(pool)

# Run multiple games and analyze with Pandas
def play_hangman_games():
    words = load_words()
    if not words:
        return
    results = []
    # Play 3 games 
    for i in range(3):
        print(f"Starting Game {i+1}")
        secret_word = choose_difficulty(words)
        win, attempts, score, guesses_remaining = hangman(secret_word)
        results.append({
            "Game_No": i + 1,
            "Secret_Word": secret_word,
            "Win": win,
            "Attempts": attempts,
            "Score": score
        })
        #Bonus round
        if win and score >= 20:
            print("Bonus Round Unlocked!")
            bonus_word = np.random.choice([w for w in words if 6 <= len(w) <= 8])
            b_win, b_attempts, b_score, b_guesses = hangman(bonus_word)
            results.append({
                "Game_No": f"{i+1}-Bonus",
                "Secret_Word": bonus_word,
                "Win": b_win,
                "Attempts": b_attempts,
                "Score": b_score
            })
        #Boss stage
        if win and guesses_remaining == 6:
            print("Secret Boss Stage Unlocked!")
            boss_word = np.random.choice([w for w in words if len(w) > 8])
            boss_win, boss_attempts, boss_score, boss_guesses = hangman(boss_word)
            results.append({
                "Game_No": f"{i+1}-Boss",
                "Secret_Word": boss_word,
                "Win": boss_win,
                "Attempts": boss_attempts,
                "Score": boss_score
            })

    # Convert to DataFrame for easy viewing
    df = pd.DataFrame(results)
    print("Game Summary:")
    print(df)

    # Simple stats using NumPy
    avg_score = np.mean(df["Score"])
    win_rate = np.mean(df["Win"]) * 100

    print(f"\nAverage Score: {avg_score:.2f}")
    print(f"Win Rate: {win_rate:.1f}%")

#Run the program
if __name__ == "__main__":
    play_hangman_games()