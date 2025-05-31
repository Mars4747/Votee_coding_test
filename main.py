import requests
import random
import urllib3


# Remember to uncomment the following two lines when you first run
# import nltk
# nltk.download('words')

# from nltk.corpus import words

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('wordle_answers.txt', 'r') as f:
    word_list = [line.strip() for line in f if len(line.strip()) == 5]

correct_pos = [None] * 5
present_pos = {}
absent_pos = {}
tried = set()

def filter(word_list):
    filtered = []
    for word in word_list:
        if word in tried:
            continue
        if any(c and word[i] != c for i, c in enumerate(correct_pos)):
            continue

        # present
        ok = True
        for letter, pos_set in present_pos.items():
            if letter not in word:
                ok = False
                break
            for pos in pos_set:
                if word[pos] == letter:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue

        # absent
        ok = True
        for letter, pos_set in absent_pos.items():
            in_present = letter in present_pos
            in_correct = letter in correct_pos
            if (not in_present and not in_correct) and set(pos_set) == {0, 1, 2, 3, 4}:
                if letter in word:
                    ok = False
                    break
            else:
                for pos in pos_set:
                    if word[pos] == letter:
                        ok = False
                        break
                if not ok:
                    break
        if not ok:
            continue

        filtered.append(word)
    return filtered

def guess_word(word):
    url = "https://wordle.votee.dev:8000/random"
    params = {
        "guess": word,
        "size": 5
    }
    response = requests.get(url, params=params, verify=False)

    if response.status_code != 200:
        print(f"Request failed: {response.status_code}")
        return None
    
    result = response.json()
    print(f"\nGuess: {word}")
    for letter in result:
        print(f"  {letter['guess']} ➜ {letter['result']}")

    # Update strategy
    current_present = set()
    current_correct = set()

    for i, letter in enumerate(result):
        g = letter["guess"]
        r = letter["result"]

        if r  == "correct":
            correct_pos[i] = g
            current_correct.add(g)
        elif r == "present":
            current_present.add(g)
            if g not in present_pos:
                present_pos[g] = set()
            present_pos[g].add(i)
            current_present.add(g)

    for i, letter in enumerate(result):
        g = letter["guess"]
        r = letter["result"]
        if r == "absent":
            if g not in current_correct and g not in current_present:
                if g not in absent_pos:
                    absent_pos[g] = set()
                absent_pos[g].add(i)
    
    return all(letter["result"] == "correct" for letter in result)


def score(word):
    return len(set(word))

def main():
    MAX_ATTEMPTS = 20
    print("Start...")
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        candidates = filter(word_list)
        print(f"Remaining candidate: {len(candidates)}")
        if not candidates:
            print("There is no available candidates.")
            break

        print(f"\n Attempt {attempts + 1}")
        candidates = sorted(candidates, key = score, reverse = True)
        word = candidates[0]
        tried.add(word)
        attempts += 1

        if guess_word(word):
            print(f"Congrats! You are right and you used {attempts} times.")
            return
        print("present_pos:", present_pos)
        print("absent_pos:", absent_pos)
        print("correct_pos:", correct_pos)

    print("\n Failed to guess within the limit.")

if __name__ == "__main__":
    main()
