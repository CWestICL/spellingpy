import requests
import random

vowels = "aeiou"
consonants = "bcdfghjklmnpqrstvwxyz"

def get_char(category):
    return random.choice(category)

def get_letters():
    letters = ""
    for x in range(5):
        char = get_char(vowels)
        letters += char
    for x in range(6):
        char = get_char(consonants)
        letters += char
    for x in range(5):
        category = random.choice([vowels,consonants])
        char = get_char(category)
        letters += char
    shuffled = ''.join(random.sample(letters,len(letters)))
    #print(letters)
    #print(shuffled)
    return shuffled

def print_grid(letters):
    for x in range(4):
        line = ""
        for y in range(4):
            line += "[ " + letters[0].upper() + " ] "
            letters = letters[1:]
        print(line)

def make_guess(letters):
    answer_input = input("Longest word:")
    validate_check = validate(answer_input,letters)
    if not validate_check:
        print("Invalid answer!")
        make_guess(letters)
    else:
        print("Checking dictionary...")
        app_id = '6ce7ceb9'
        app_key = 'bac47f553632715817395f753efc74d2'
        language = 'en-gb'
        word_id = answer_input
        url = 'https://od-api.oxforddictionaries.com/api/v2/lemmas/'  + language + '/'  + word_id.lower()
        r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
        print(r.status_code)
        status = str(r.status_code)
        if status == "404":
            print("Word is not in the dictionary!")
            make_guess(letters)
        elif status == "200":
            print("You guessed " + word_id.lower().capitalize() + " for a score of " + str(len(word_id)) + "!")
        else:
            print("code {}\n".format(r.status_code))
            print("Error connecting to server! Try again?")
            make_guess(letters)

def validate(guess,letters):
    for gchar in guess:
        if gchar in letters:
            letters.replace(gchar,"",1)
        else:
            return False
    return True

def main():
    letters = get_letters()
    print_grid(letters)
    make_guess(letters)

main()