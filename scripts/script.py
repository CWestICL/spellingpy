from re import T
import requests
import random


def get_prompt():
    print("Waiting for response from server...")

    #"""
    response = requests.get("https://imdb-api.com/en/API/IMDbList/k_ix66kf8r/ls507259888")
    #1001 movies - ls052535080
    #Monster movies - ls507259888
    #print("Response got!")
    #print(response)

    if response.ok:
        print("200!")

    json = response.json()
    #print("-Json got-")
    #print(json)

    return random.choice(json["items"])["title"]
    #"""

    """
    response = requests.get("https://pokeapi.co/api/v2/pokemon")
    print("Response got!")
    #print(response)

    if not response.ok:
        return ""

    json = response.json()
    #print("-Json got-")
    #print(json)

    poke_num = random.randint(1,151)

    #print("https://pokeapi.co/api/v2/pokemon/{}".format(poke_num))
    print("Waiting for response from server...")
    response = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(poke_num))
    print("Response got!")
    #print(response)

    if not response.ok:
        return ""

    json = response.json()
    #print("-Json got-")
    #print(json)
    return json["forms"][0]["name"].capitalize()
    """

def play_hangman():
    prompt_title = get_prompt()
    if not prompt_title:
        print("Error connecting to API server!")
        return
    corr_letters = []
    wron_letters = []
    lives = 6
    hangman_turn(prompt_title,corr_letters,wron_letters,lives)

def hangman_turn(prompt_title,corr_letters,wron_letters,lives):
    letter_left = print_display(prompt_title,corr_letters)
    if letter_left == 0:
        print("You solved it with " + str(lives) + " lives remaining!")
        #print("The answer was:",prompt_title)
    else:
        print("Lives left: ",lives)
        #print("Letters left:",letter_left)
        guess = make_guess(corr_letters,wron_letters)
        if guess in prompt_title.lower():
            corr_letters.append(guess)
        else:
            wron_letters.append(guess)
            print("Sorry! There is no '" + guess + "'")
            lives -= 1
        if lives == 0:
            print("GAME OVER!")
            print("The answer was:",prompt_title)
        else:
            hangman_turn(prompt_title,corr_letters,wron_letters,lives)

def print_display(prompt_title,corr_letters):
    title = ""
    line = ""
    letter_left = 0
    for char in prompt_title:
        line += "-"
        if char.lower() in corr_letters:
            title += char
        elif not char.isalpha():
            title += char
        else:
            title += "?"
            letter_left += 1
    print(line + "\n" + title + "\n" + line)
    return letter_left

def make_guess(corr_letters,wron_letters):
    guess = input("Guess a letter:").lower()
    if len(guess) != 1:
        print("Invalid guess")
        return make_guess(corr_letters,wron_letters)
    elif not guess.isalpha():
        print("Invalid guess")
        return make_guess(corr_letters,wron_letters)
    elif guess in corr_letters or guess in wron_letters:
        print("Letter already guessed")
        return make_guess(corr_letters,wron_letters)
    else:
        return guess

def main():
    play_hangman()

main()