# Run with: python accept-input-quiz.py
def ask_question(question, options):
    print(question)
    for i, option in enumerate(options, start=1):
        print(f"{i}) {option}")

    while True:
        answer = input("Enter the number of your choice: ")
        if answer.isdigit():
            answer = int(answer)
            if 1 <= answer <= len(options):
                return answer
        print("Invalid input. Please enter a valid number.")

def main():
    house_scores = {'Gryffindor': 0, 'Ravenclaw': 0, 'Hufflepuff': 0, 'Slytherin': 0}

    # Question 1
    answer = ask_question("Q1) Do you like Dawn or Dusk?", ["Dawn", "Dusk"])
    if answer == 1:
        house_scores['Gryffindor'] += 1
        house_scores['Ravenclaw'] += 1
    elif answer == 2:
        house_scores['Hufflepuff'] += 1
        house_scores['Slytherin'] += 1

    # Question 2
    answer = ask_question("Q2) When I'm dead, I want people to remember me as:", ["The Good", "The Great", "The Wise", "The Bold"])
    house_scores['Hufflepuff'] += 2 if answer == 1 else 0
    house_scores['Slytherin'] += 2 if answer == 2 else 0
    house_scores['Ravenclaw'] += 2 if answer == 3 else 0
    house_scores['Gryffindor'] += 2 if answer == 4 else 0

    # Question 3
    answer = ask_question("Q3) Which kind of instrument most pleases your ear?", ["The Violin", "The Trumpet", "The Piano", "The Drum"])
    house_scores['Slytherin'] += 4 if answer == 1 else 0
    house_scores['Hufflepuff'] += 4 if answer == 2 else 0
    house_scores['Ravenclaw'] += 4 if answer == 3 else 0
    house_scores['Gryffindor'] += 4 if answer == 4 else 0

    result = max(house_scores, key=house_scores.get)
    print(f"You're in {result}!")

if __name__ == "__main__":
    main()