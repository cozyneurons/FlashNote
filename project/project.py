import csv
import os
from datetime import datetime, timedelta
import random

CSV_FILE = 'flashcards.csv'

def add_flashcard(question, answer, subject):
    today = datetime.today().date().isoformat()
    card = [question, answer, subject, today, today, "1"]

    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["question", "answer", "subject", "last_reviewed", "next_due", "difficulty"])
        writer.writerow(card)
    return card

def get_due_flashcards(subject):
    due_cards = []
    today = datetime.today().date()

    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["subject"].lower() == subject.lower():
                next_due = datetime.strptime(row["next_due"], "%Y-%m-%d").date()
                if next_due <= today:
                    due_cards.append(row)
    return due_cards

def update_flashcard(card, correct):
    updated_rows = []
    today = datetime.today().date()

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["question"] == card["question"] and row["answer"] == card["answer"]:
                row["last_reviewed"] = today.isoformat()
                if correct:
                    difficulty = min(int(row["difficulty"]) + 1, 5)
                    interval = [1, 2, 4, 7, 14][difficulty - 1]
                else:
                    difficulty = 1
                    interval = 1
                row["difficulty"] = str(difficulty)
                row["next_due"] = (today + timedelta(days=interval)).isoformat()
            updated_rows.append(row)

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)

def view_all_flashcards():
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def main():
    while True:
        print("\n📚 Flash Note ")
        print("1. Add Flashcard")
        print("2. Review Flashcards by Subject")
        print("3. View All Flashcards")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            q = input("Enter question: ")
            a = input("Enter answer: ")
            s = input("Enter subject: ")
            add_flashcard(q, a, s)
            print("✅ Flashcard added.")
        elif choice == '2':

            cards = view_all_flashcards()
            subjects = sorted(set(card['subject'] for card in cards))
            if not subjects:
                print("❌ No subjects found. Add flashcards first.")
                continue

            print("\n📘 Subjects:")
            for idx, sub in enumerate(subjects, 1):
                print(f"{idx}. {sub}")

            try:
                selected = int(input("Choose a subject by number: "))
                subject = subjects[selected - 1]
            except (ValueError, IndexError):
                print("❌ Invalid selection.")
                continue

            due_cards = get_due_flashcards(subject)
            if not due_cards:
                print(f"🎉 No cards due today for [{subject}].")
                continue

            random.shuffle(due_cards)
            score = 0
            for i, card in enumerate(due_cards, 1):
                print(f"\nQ{i}: {card['question']}")
                input("Press Enter to show answer...")
                print(f"🧠 A: {card['answer']}")
                got_it = input("Did you get it right? (y/n): ").strip().lower() == 'y'
                update_flashcard(card, got_it)
                if got_it:
                    score += 1
            percent = (score / len(due_cards)) * 100
            print(f"\n🎯 Review complete: {score}/{len(due_cards)} correct ({percent:.1f}%).")

            if percent == 100:
                print("🏆 Perfect! You're unstoppable!")
            elif percent >= 80:
                print("🔥 Great job! You're mastering this subject.")
            elif percent >= 60:
                print("💪 Keep it up! You're getting there.")
            elif percent >= 40:
                print("📘 You're learning! A little more practice will help.")
            else:
                print("🌱 Every expert was once a beginner — don't give up!")
        elif choice == '3':
            cards = view_all_flashcards()
            for idx, card in enumerate(cards, 1):
                print(f"{idx}. [{card['subject']}] Q: {card['question']} | A: {card['answer']} | Due: {card['next_due']} | Diff: {card['difficulty']}")
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
