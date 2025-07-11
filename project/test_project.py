import os
import csv
import pytest
from datetime import datetime, timedelta
from project import add_flashcard, view_all_flashcards, get_due_flashcards

TEST_CSV = 'test_flashcards.csv'

import project
project.CSV_FILE = TEST_CSV

@pytest.fixture(autouse=True)
def run_around_tests():
    if os.path.exists(TEST_CSV):
        os.remove(TEST_CSV)
    yield
    if os.path.exists(TEST_CSV):
        os.remove(TEST_CSV)

def test_add_flashcard():
    card = add_flashcard("How is your mood?", "Mast", "Feelings")
    assert card[0] == "How is your mood?"
    assert card[1] == "Mast"
    assert card[2] == "Feelings"

    with open(TEST_CSV, newline='') as f:
        rows = list(csv.reader(f))
        assert len(rows) == 2

def test_view_all_flashcards():
    add_flashcard("Powerhouse of the cell?", "Mitochondria", "Sci")
    cards = view_all_flashcards()
    assert len(cards) == 1
    assert cards[0]["answer"] == "Mitochondria"
    assert cards[0]["subject"] == "Sci"

def test_get_due_flashcards():
    today = datetime.today().date().isoformat()
    past = (datetime.today().date() - timedelta(days=2)).isoformat()

    with open(TEST_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer", "subject", "last_reviewed", "next_due", "difficulty"])
        writer.writerow(["Q1", "A1", "science", today, past, "1"])
        writer.writerow(["Q2", "A2", "science", today, "2999-12-31", "1"])
        writer.writerow(["Q3", "A3", "math", today, past, "1"])

    due = get_due_flashcards("science")
    assert len(due) == 1
    assert due[0]["question"] == "Q1"

def test_subject_field_in_flashcard():
    card = add_flashcard("What is Array", "Nice Data Structure", "CS")
    cards = view_all_flashcards()
    assert cards[0]["subject"] == "CS"
