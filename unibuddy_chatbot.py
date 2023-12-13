# questions for teacher: why the json file does not update completely immediately?

# This program is a CHAT BOT. It will ask some personal questions and display some
# personalized answers based on the user's characteristics. It will also
# provide responses to the user's doubts about the University and the courses.

# We created JSON files to store the responses for the personal questions, and for
# the user's doubts

# This CHAT BOT will try to guess the user's question based on the "chatbot_faq.json" file.
# This file contains a set of related words for each question; each related word has a weight.
# Based on the question entered by the user, it will analyse each word of the user's question and compair
# them with the related words of each question in "chatbot_faq.json" file. It will sum the weight
# of each word and decide which question in the file is more likely to be the one the user entered.
# If it guessed, the words entered by the user that matched the related words list will increase the weight
# and the new ones will be added; if not, it will decrease.


import json
from time import sleep


def char_remove(phrase):
    """
    This function will eliminate special characters from a string and spaces in head or tail.
        Parameters:
            phrase (string): any string.
        Returns:
            phrase (string): string without special characters.
    """

    char = "?/.,:;*$%#|!+[{(]})"
    for item in char:
        phrase = phrase.replace(item, "")
    return phrase.split()


def remove_s(list_strings):
    """
    This function will eliminate letter "S" from strings within a list, aiming convert plural in singular.
        Parameters:
            list_strings (list): list of strings.
        Returns:
            list_singular (list): list of singular strings.
    """

    list_singular = []
    for index in list_strings:
        list_singular.append(index.rstrip("s"))
    return list_singular


def exclude_stop_words(phrase, stop_words):
    """
    This function will eliminate some words from a phrase.
        Parameters:
            phrase (string): phrase in the format of a string.
            stop_words (list): list with words to be searched and deleted from the phrase.
        Returns:
            phrase (list): list of the words from the phrase without the stop_words.
    """

    phrase = char_remove(phrase)
    phrase = remove_s(phrase)
    for index in stop_words:
        if stop_words[index] in phrase:
            phrase.remove(stop_words[index])
    return phrase


# This is a set of files created in JSON that'll be used in this code

# Personalized wordings based on the user's age.
open_ages_wording = open("chatbot_ages_wordings.json", "r")
content_ages_wording = json.load(open_ages_wording)

# List of possible colours. It's used to check if the user entered a valid colour name.
open_colours_list = open("chatbot_colours_list.json", "r")
content_colours_list = json.load(open_colours_list)

# Personalized wordings based on the user's age.
open_colours_wording = open("chatbot_colours_wordings.json", "r")
content_colours_wording = json.load(open_colours_wording)

# List of words with few meaning. Words in the question entered by the user that match this list
# will be eliminated.
open_stop_words_list = open("chatbot_stop_words_list.json", "r")
content_stop_words_list = json.load(open_stop_words_list)

# Lis of questions, responses, related words and weights
open_faq = open("chatbot_faq.json", "r+")
content_faq = json.load(open_faq)


# Initial greetings.
print(f"""
{'*'*30} Welcome to the UniBuddy {'*'*30}
Hi! My name is UniBuddy and I am here to help you through your university journey.
I am going to ask you a few questions so I can get to know you a little better.
""")


# The user will input three personal data and based on them a wording will be displayed.

# The 1st personal data: name.
while True:
    name = input("What is your name? ").strip()
    if name.replace(" ", "").isalpha():
        print(f"Hi {name}, nice to meet you!\n")
        sleep(2)
        break
    else:
        print("Something confused me. Please try again with no special character.\n")
        sleep(1.5)

# The 2nd personal data: age. Based on the age, a wording coming from 'content_ages_wording' will be displayed.
while True:
    age = input("How old are you? ").replace(" ", "").strip()
    if age.isnumeric():
        age = int(age)

        # Look for the wording corresponding to the age.
        for index in content_ages_wording:
            min_age = content_ages_wording[index]["min_age"]
            max_age = content_ages_wording[index]["max_age"]
            wording = content_ages_wording[index]["wording"]
            if min_age <= age <= max_age:
                print(wording+"\n")
                sleep(3)
                break
        break
    else:
        print("I think this is not a valid number. Could please you try again?\n")
        sleep(1.5)

# The 3rd personal data: colour. Based on the colour, a wording coming from 'content_colours_wording' will be displayed.
while True:
    colour = input("What is your favourite colour? ").strip().lower()
    if colour.replace(" ", "").isalpha():

        # Look for the wording corresponding to the colour.
        colour_found = False
        for index_wor in content_colours_wording:
            if colour == content_colours_wording[index_wor]["colour"]:
                print(content_colours_wording[index_wor]["wording"]+"\n")
                sleep(5)
                colour_found = True
                break

        # Check if the entered colour is a valid one, base on the 'content_colours_list' variable.
        known_colour = False
        if not colour_found:
            for index_list in content_colours_list:
                if colour == content_colours_list[index_list]:
                    known_colour = True
                    break
            if known_colour:
                print(f"I guess you're the first person I know that likes {colour}. It's interesting\n")
                sleep(5)
                break
            else:
                print("I couldn't find this colour. Could try again, please!!!\n")
                sleep(1.5)
        else:
            break
    else:
        print("Something confused me. Please try again with no special character.\n")
        sleep(1.5)


# Final greetings
print(f"""
{80*'='}
I think those are all the questions I needed to ask...

Thank you for telling me more about yourself! It's so lovely to meet you {name}.
You can ask me whatever questions about:
    - fees
    - curriculum
    - accommodation
    - clubs
    - courses,
I'll do my best to answer them.
When you're done asking me questions, you can just say "Bye".
{80*'='}

""")
sleep(3)


# In this section it starts the questions and answers.
# The chatbot will try 2 times to understand the question. If unsuccessful, it'll provide a list of questions.
# It will try to figure out the question based on the comparison of the words within the question
# and the words in 'content_faq' variable, where there are a list of related words for each question.
# Whenever the user confirms the chatbot got it right, the words used by the user will be added into
# the lis of related words; if the words are already there, it will increase its weight.
# In the opposite situation, it will decrease the weight of the word.

count = 0
while True:
    if count <= 2:
        question = input("How can I help you? ").strip().lower()

        if question == "bye":
            print("It was nice to talk to you. See you soon!")
            break

        # If the entered question is numeric, too short or has only one word, user will have to enter again
        elif len(question) < 3 and question.count(" ") == 0 and question.isnumeric():
            print("I'm not sure if you've made your question. Could you try again, please?")

        else:
            # This function will eliminate especial characters (like "#$?!"), certain words with little
            # meaning (like "how", "of", "the") and the letter "S".
            question = exclude_stop_words(question, content_stop_words_list)
            print(question)

            # This will iterate in the content_faq to try to figure out what question has more related-word to the
            # words withing the question entered by the user. It will take in consideration the weight that each word
            # has for each question in content_faq. The decision will be stored in a dictionary.
            faq_choose = {"index": -1, "weight": 0}

            for ind_cont in content_faq:
                faq_choose_temp = {"index": -1, "weight": 0}

                for ind_rela, related_word in enumerate(content_faq[ind_cont]["related_words"]):

                    if related_word in question:
                        faq_choose_temp["index"] = ind_cont
                        faq_choose_temp["weight"] += content_faq[ind_cont]["related_words_weight"][ind_rela]

                if faq_choose_temp["weight"] > faq_choose["weight"]:
                    faq_choose["index"] = faq_choose_temp["index"]
                    faq_choose["weight"] = faq_choose_temp["weight"]

                # Reset of the temporary dictionary
                faq_choose_temp["index"] = -1
                faq_choose_temp["weight"] = 0

            # If no word within user's question is found, they'll be asked to make another question.
            if faq_choose["index"] == -1:
                print("Sorry, I couldn't understand. Let's try again.")
                count += 1

            # If any word within user's question is found, they'll be asked to confirm if the guess is correct.
            else:
                possible_question = content_faq[faq_choose["index"]]["question"]
                possible_response = content_faq[faq_choose["index"]]["response"]
                confirmation = input(f"Would you like to know {possible_question}? ").lower()
                confirmation = char_remove(confirmation)

                test_confirmation = False
                for index in confirmation:
                    if index in "yesyeptruetruthokokaysurecorrectright":
                        test_confirmation = True

                # If the guess is correct, the response is displayed and the words within user's question
                # will be stored in JSON file or increased its weight.
                if test_confirmation:
                    print(possible_response)
                    count = 0
                    print(question)
                    for user_word in question:
                        if user_word in content_faq[faq_choose["index"]]["related_words"]:
                            for ind_rela, related_word in enumerate(content_faq[faq_choose["index"]]["related_words"]):
                                if user_word == related_word:
                                    content_faq[faq_choose["index"]]["related_words_weight"][ind_rela] += 1
                                    open_faq.seek(0)
                                    json.dump(content_faq, open_faq, indent=4)
                        else:
                            content_faq[faq_choose["index"]]["related_words"].append(user_word)
                            content_faq[faq_choose["index"]]["related_words_weight"].append(1)
                            open_faq.seek(0)
                            json.dump(content_faq, open_faq, indent=4)

                # If the guess is not correct, the user will be asked to make another question and the words
                # within user's question will be decreased its weight.
                else:
                    print("Sorry, I couldn't understand. Let's try again.")
                    count += 1

                    for ind_rela, related_word in enumerate(content_faq[faq_choose["index"]]["related_words"]):

                        for user_word in question:
                            if user_word == related_word and user_word not in content_faq[faq_choose["index"]]["key_words"]:
                                content_faq[faq_choose["index"]]["related_words_weight"][ind_rela] -= 1
                                open_faq.seek(0)
                                json.dump(content_faq, open_faq, indent=4)

    # If the user tried 2 times and the robot didn't guess the question, they'll be displayed options
    else:
        print("""

I'm going to provide you a list o question I'm able to answer:

1. Where is the fees office?
2. Who can help me with my curriculum form?
3. Where can I find out more about student accommodation?
4. What clubs does the University offer?
5. Which courses should I take?

""")
        option = input("Please select the option you need help with: ")
        if option == "bye":
            print("It was nice to talk to you. See you soon!")
            break
        elif not option.isnumeric():
            print("Please, type a number corresponding to the question.")
        elif not int(option) in [1, 2, 3, 4, 5]:
            print("Please, type a number corresponding to the question.")
        else:
            option = int(option) - 1
            print(content_faq[str(option)]["response"])
            print("")
            count = 0
