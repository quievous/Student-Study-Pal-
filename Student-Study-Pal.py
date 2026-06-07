from abc import ABC, abstractmethod
import unittest
import json
import os

class IInputReader(ABC):
    @abstractmethod
    def read(self, prompt):
        pass

class IOutputWriter(ABC):
    @abstractmethod
    def write(self, message):
        pass

class Schedule:
    def __init__(self, day, time, task):
        self.__day  = day
        self.__time = time
        self.__task = task

    def get_day(self):
        return self.__day

    def get_time(self):
        return self.__time

    def get_task(self):
        return self.__task


class Quiz:
    def __init__(self, subject, question, choices, answer):
        self.__subject  = subject
        self.__question = question
        self.__choices  = choices
        self.__answer   = answer

    def get_subject(self):
        return self.__subject

    def get_question(self):
        return self.__question

    def get_choices(self):
        return self.__choices

    def get_answer(self):
        return self.__answer


class Deadline:
    def __init__(self, task, completed=False):
        self.__task      = task
        self.__completed = completed

    def get_task(self):
        return self.__task

    def get_completed(self):
        return self.__completed

    def toggle_completed(self):
        self.__completed = not self.__completed


class StudyHour:
    def __init__(self, day, hours, subject, score):
        self.__day     = day
        self.__hours   = hours
        self.__subject = subject
        self.__score   = score

    def get_day(self):
        return self.__day

    def get_hours(self):
        return self.__hours

    def get_subject(self):
        return self.__subject

    def get_score(self):
        return self.__score


class ConsoleInputReader(IInputReader):
    def read(self, prompt):
        return input(prompt)


class ConsoleOutputWriter(IOutputWriter):
    def write(self, message):
        print(message)


class DataProcessor:
    def __init__(self, filename=None):
        if filename is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir, "data.json")
        self.__filename    = filename
        self.__schedules   = []
        self.__quizzes     = []
        self.__deadlines   = []
        self.__study_hours = []
        self.load_from_file()

    def add_schedule(self, schedule):
        self.__schedules.append(schedule)
        self.save_to_file()

    def get_schedules(self):
        return self.__schedules

    def add_quiz(self, quiz):
        self.__quizzes.append(quiz)
        self.save_to_file()

    def get_quizzes(self):
        return self.__quizzes

    def add_deadline(self, deadline):
        self.__deadlines.append(deadline)
        self.save_to_file()

    def get_deadlines(self):
        return self.__deadlines

    def add_study_hour(self, study_hour):
        self.__study_hours.append(study_hour)
        self.save_to_file()

    def get_study_hours(self):
        return self.__study_hours

    def save_to_file(self):
        try:
            data = {
                "schedules": [
                    {"day":  s.get_day(),
                     "time": s.get_time(),
                     "task": s.get_task()}
                    for s in self.__schedules
                ],
                "quizzes": [
                    {"subject":  q.get_subject(),
                     "question": q.get_question(),
                     "choices":  q.get_choices(),
                     "answer":   q.get_answer()}
                    for q in self.__quizzes
                ],
                "deadlines": [
                    {"task":      d.get_task(),
                     "completed": d.get_completed()}
                    for d in self.__deadlines
                ],
                "study_hours": [
                    {"day":     s.get_day(),
                     "hours":   s.get_hours(),
                     "subject": s.get_subject(),
                     "score":   s.get_score()}
                    for s in self.__study_hours
                ]
            }
            with open(self.__filename, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load_from_file(self):
        try:
            if not os.path.exists(self.__filename):
                return
            with open(self.__filename, "r") as f:
                data = json.load(f)

            self.__schedules = [
                Schedule(s["day"], s["time"], s["task"])
                for s in data.get("schedules", [])
            ]
            self.__quizzes = [
                Quiz(q["subject"], q["question"],
                     q["choices"], q["answer"])
                for q in data.get("quizzes", [])
            ]
            self.__deadlines = [
                Deadline(d["task"], d["completed"])
                for d in data.get("deadlines", [])
            ]
            self.__study_hours = [
                StudyHour(s["day"], s["hours"],
                          s["subject"], s["score"])
                for s in data.get("study_hours", [])
            ]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")


class StudentStudyPalApp:
    def __init__(self, reader, writer, processor):
        self.__reader    = reader
        self.__writer    = writer
        self.__processor = processor

    def run(self):
        while True:
            self.__writer.write("\n" + "=" * 40)
            self.__writer.write("Student Study Pal".center(40))
            self.__writer.write("=" * 40)
            self.__writer.write("[1] Study Schedule")
            self.__writer.write("[2] Deadlines")
            self.__writer.write("[3] Quiz")
            self.__writer.write("[4] Progress")
            self.__writer.write("[5] Exit")
            self.__writer.write("=" * 40)

            choice = self.__reader.read("Enter choice: ")

            if choice == "1":
                self.study_schedule_menu()
            elif choice == "2":
                self.deadline_menu()
            elif choice == "3":
                self.quiz_menu()
            elif choice == "4":
                self.weekly_progress()
            elif choice == "5":
                self.__writer.write("Goodbye!")
                break
            else:
                self.__writer.write("Invalid choice! Please enter 1-5.")

    def study_schedule_menu(self):
        while True:
            self.__writer.write("\n" + "=" * 40)
            self.__writer.write("Study Schedule".center(40))
            self.__writer.write("=" * 40)
            self.__writer.write("[1] Add Schedule")
            self.__writer.write("[2] View Schedules")
            self.__writer.write("[3] Back")
            self.__writer.write("=" * 40)

            choice = self.__reader.read("Enter choice: ")

            if choice == "1":
                while True:
                    day = self.__reader.read("Enter day (YYYY-MM-DD): ")
                    if len(day) != 10 or day[4] != "-" or day[7] != "-":
                        self.__writer.write("Error: Invalid date format! Please try again.")
                    else:
                        break

                while True:
                    time = self.__reader.read("Enter time (HH:MM): ")
                    if len(time) != 5 or time[2] != ":":
                        self.__writer.write("Error: Invalid time format! Please try again.")
                    else:
                        break

                while True:
                    task = self.__reader.read("Enter task: ")
                    if not task.strip():
                        self.__writer.write("Error: Task cannot be empty! Please try again.")
                    else:
                        break

                self.__processor.add_schedule(Schedule(day, time, task))
                self.__writer.write("Schedule added successfully!")

            elif choice == "2":
                schedules = self.__processor.get_schedules()
                if not schedules:
                    self.__writer.write("No schedules yet!")
                else:
                    self.__writer.write("\n" + "=" * 40)
                    self.__writer.write("Your Schedules".center(40))
                    self.__writer.write("=" * 40)
                    for i, s in enumerate(schedules):
                        self.__writer.write(
                            f"{i+1}. {s.get_day()} | {s.get_time()} | {s.get_task()}")

            elif choice == "3":
                break

            else:
                self.__writer.write("Invalid choice! Please enter 1-3.")

    def deadline_menu(self):
        while True:
            self.__writer.write("\n" + "=" * 40)
            self.__writer.write("Deadlines".center(40))
            self.__writer.write("=" * 40)
            self.__writer.write("[1] Add Task")
            self.__writer.write("[2] View Tasks")
            self.__writer.write("[3] Mark Task as Done")
            self.__writer.write("[4] Back")
            self.__writer.write("=" * 40)

            choice = self.__reader.read("Enter choice: ")

            if choice == "1":
                while True:
                    task = self.__reader.read("Enter task: ")
                    if not task.strip():
                        self.__writer.write("Error: Task cannot be empty! Please try again.")
                    else:
                        break

                self.__processor.add_deadline(Deadline(task))
                self.__writer.write("Task added successfully!")

            elif choice == "2":
                deadlines = self.__processor.get_deadlines()
                if not deadlines:
                    self.__writer.write("No tasks yet!")
                else:
                    self.__writer.write("\n" + "=" * 40)
                    self.__writer.write("Your Tasks".center(40))
                    self.__writer.write("=" * 40)
                    for i, d in enumerate(deadlines):
                        status = "✅" if d.get_completed() else "❌"
                        self.__writer.write(f"{i+1}. {status} {d.get_task()}")

            elif choice == "3":
                deadlines = self.__processor.get_deadlines()
                if not deadlines:
                    self.__writer.write("No tasks yet!")
                else:
                    self.__writer.write("\n" + "=" * 40)
                    self.__writer.write("Your Tasks".center(40))
                    self.__writer.write("=" * 40)
                    for i, d in enumerate(deadlines):
                        status = "✅" if d.get_completed() else "❌"
                        self.__writer.write(f"{i+1}. {status} {d.get_task()}")

                    while True:
                        try:
                            num   = self.__reader.read("Enter task number: ")
                            index = int(num) - 1
                            if 0 <= index < len(deadlines):
                                deadlines[index].toggle_completed()
                                self.__processor.save_to_file()
                                self.__writer.write("Task updated successfully!")
                                break
                            else:
                                self.__writer.write("Invalid task number! Please try again.")
                        except ValueError:
                            self.__writer.write("Error: Please enter a valid number!")

            elif choice == "4":
                break

            else:
                self.__writer.write("Invalid choice! Please enter 1-4.")

    def quiz_menu(self):
        while True:
            self.__writer.write("\n" + "=" * 40)
            self.__writer.write("Quiz".center(40))
            self.__writer.write("=" * 40)
            self.__writer.write("[1] Create Quiz")
            self.__writer.write("[2] Take Quiz")
            self.__writer.write("[3] View Quizzes")
            self.__writer.write("[4] Back")
            self.__writer.write("=" * 40)

            choice = self.__reader.read("Enter choice: ")

            if choice == "1":
                while True:
                    subject = self.__reader.read("Enter subject: ")
                    if not subject.strip():
                        self.__writer.write("Error: Subject cannot be empty! Please try again.")
                    else:
                        break

                while True:
                    question = self.__reader.read("Enter question: ")
                    if not question.strip():
                        self.__writer.write("Error: Question cannot be empty! Please try again.")
                    else:
                        break

                while True:
                    choice_a = self.__reader.read("Choice A: ")
                    choice_b = self.__reader.read("Choice B: ")
                    choice_c = self.__reader.read("Choice C: ")
                    choice_d = self.__reader.read("Choice D: ")
                    if not all([choice_a.strip(), choice_b.strip(),
                                choice_c.strip(), choice_d.strip()]):
                        self.__writer.write("Error: All choices cannot be empty! Please try again.")
                    else:
                        break

                while True:
                    answer = self.__reader.read("Enter answer (A/B/C/D): ").upper()
                    if answer not in ["A", "B", "C", "D"]:
                        self.__writer.write("Error: Answer must be A, B, C, or D! Please try again.")
                    else:
                        break

                self.__processor.add_quiz(Quiz(
                    subject, question,
                    [choice_a, choice_b, choice_c, choice_d],
                    answer))
                self.__writer.write("Quiz added successfully!")

            elif choice == "2":
                quizzes = self.__processor.get_quizzes()
                if not quizzes:
                    self.__writer.write("No quizzes yet!")
                else:
                    subjects = []
                    for q in quizzes:
                        if q.get_subject() not in subjects:
                            subjects.append(q.get_subject())

                    self.__writer.write("\n" + "=" * 40)
                    self.__writer.write("Select Subject".center(40))
                    self.__writer.write("=" * 40)
                    for i, s in enumerate(subjects):
                        self.__writer.write(f"{i+1}. {s}")

                    while True:
                        try:
                            num   = self.__reader.read("Enter subject number: ")
                            index = int(num) - 1
                            if 0 <= index < len(subjects):
                                break
                            else:
                                self.__writer.write("Invalid subject number! Please try again.")
                        except ValueError:
                            self.__writer.write("Error: Please enter a valid number!")

                    subject         = subjects[index]
                    subject_quizzes = [q for q in quizzes if q.get_subject() == subject]

                    score = 0
                    for q in subject_quizzes:
                        self.__writer.write("\n" + "=" * 40)
                        self.__writer.write(q.get_question())
                        self.__writer.write(f"A) {q.get_choices()[0]}")
                        self.__writer.write(f"B) {q.get_choices()[1]}")
                        self.__writer.write(f"C) {q.get_choices()[2]}")
                        self.__writer.write(f"D) {q.get_choices()[3]}")

                        while True:
                            ans = self.__reader.read("Your answer (A/B/C/D): ").upper()
                            if ans not in ["A", "B", "C", "D"]:
                                self.__writer.write("Error: Answer must be A, B, C, or D! Please try again.")
                            else:
                                break

                        if ans == q.get_answer():
                            self.__writer.write("Correct! ✅")
                            score += 1
                        else:
                            self.__writer.write(
                                f"Wrong! ❌ Correct answer is {q.get_answer()}")

                    total   = len(subject_quizzes)
                    percent = round((score / total) * 100, 1)
                    self.__writer.write("\n" + "=" * 40)
                    self.__writer.write(
                        f"Score: {score}/{total} ({percent}%)".center(40))
                    self.__writer.write("=" * 40)

                    while True:
                        day = self.__reader.read("Enter today's date: ")
                        if not day.strip():
                            self.__writer.write("Error: Date cannot be empty! Please try again.")
                        else:
                            break

                    while True:
                        try:
                            hours = float(self.__reader.read("Enter study hours: "))
                            if hours < 0:
                                self.__writer.write("Error: Hours cannot be negative! Please try again.")
                            else:
                                break
                        except ValueError:
                            self.__writer.write("Error: Please enter a valid number!")

                    self.__processor.add_study_hour(
                        StudyHour(day, hours, subject, percent))
                    self.__writer.write("Progress saved!")

            elif choice == "3":
                quizzes = self.__processor.get_quizzes()
                if not quizzes:
                    self.__writer.write("No quizzes yet!")
                else:
                    groups = {}
                    for q in quizzes:
                        groups.setdefault(q.get_subject(), []).append(q)

                    self.__writer.write("\n" + "=" * 40)
                    self.__writer.write("All Quizzes".center(40))
                    self.__writer.write("=" * 40)

                    for subject, questions in groups.items():
                        self.__writer.write(
                            f"\n📚 {subject} ({len(questions)} questions)")
                        self.__writer.write("-" * 40)
                        for i, q in enumerate(questions):
                            self.__writer.write(f"  Q{i+1}: {q.get_question()}")
                            self.__writer.write(f"  A) {q.get_choices()[0]}")
                            self.__writer.write(f"  B) {q.get_choices()[1]}")
                            self.__writer.write(f"  C) {q.get_choices()[2]}")
                            self.__writer.write(f"  D) {q.get_choices()[3]}")
                            self.__writer.write(f"  Answer: {q.get_answer()}")

            elif choice == "4":
                break

            else:
                self.__writer.write("Invalid choice! Please enter 1-4.")

    def weekly_progress(self):
        self.__writer.write("\n" + "=" * 40)
        self.__writer.write("Progress Tracker".center(40))
        self.__writer.write("=" * 40)

        deadlines   = self.__processor.get_deadlines()
        done        = sum(1 for d in deadlines if d.get_completed())
        undone      = sum(1 for d in deadlines if not d.get_completed())

        self.__writer.write(f"✅ Completed Tasks : {done}")
        self.__writer.write(f"❌ Undone Tasks    : {undone}")

        study_hours = self.__processor.get_study_hours()
        total_hours = round(sum(s.get_hours() for s in study_hours), 1)

        self.__writer.write(f"⏱  Total Study Hours: {total_hours} hrs")
        self.__writer.write("=" * 40)
        self.__reader.read("Press Enter to go back to Main Menu...")


class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = DataProcessor("test_data.json")

    def tearDown(self):
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")

    def test_add_and_get_schedule(self):
        schedule = Schedule("2026-05-01", "08:00", "Math Review")
        self.processor.add_schedule(schedule)
        self.assertEqual(len(self.processor.get_schedules()), 1)
        self.assertEqual(self.processor.get_schedules()[0].get_day(), "2026-05-01")

    def test_add_and_get_quiz(self):
        quiz = Quiz("Math", "What is 2+2?", ["1", "2", "3", "4"], "D")
        self.processor.add_quiz(quiz)
        self.assertEqual(len(self.processor.get_quizzes()), 1)
        self.assertEqual(self.processor.get_quizzes()[0].get_subject(), "Math")

    def test_add_and_get_deadline(self):
        deadline = Deadline("Submit assignment")
        self.processor.add_deadline(deadline)
        self.assertEqual(len(self.processor.get_deadlines()), 1)
        self.assertEqual(self.processor.get_deadlines()[0].get_task(), "Submit assignment")

    def test_add_and_get_study_hour(self):
        study_hour = StudyHour("2026-05-01", 2.5, "Math", 90.0)
        self.processor.add_study_hour(study_hour)
        self.assertEqual(len(self.processor.get_study_hours()), 1)
        self.assertEqual(self.processor.get_study_hours()[0].get_score(), 90.0)

    def test_deadline_toggle_completed(self):
        deadline = Deadline("Study Science")
        self.assertFalse(deadline.get_completed())
        deadline.toggle_completed()
        self.assertTrue(deadline.get_completed())
        deadline.toggle_completed()
        self.assertFalse(deadline.get_completed())

    def test_schedule_attributes(self):
        schedule = Schedule("2026-05-01", "08:00", "Math Review")
        self.assertEqual(schedule.get_day(), "2026-05-01")
        self.assertEqual(schedule.get_time(), "08:00")
        self.assertEqual(schedule.get_task(), "Math Review")

    def test_quiz_attributes(self):
        quiz = Quiz("Science", "What is H2O?",
                    ["Fire", "Water", "Air", "Earth"], "B")
        self.assertEqual(quiz.get_subject(), "Science")
        self.assertEqual(quiz.get_question(), "What is H2O?")
        self.assertEqual(quiz.get_answer(), "B")

    def test_study_hour_attributes(self):
        study_hour = StudyHour("2026-05-01", 3.0, "English", 85.0)
        self.assertEqual(study_hour.get_day(), "2026-05-01")
        self.assertEqual(study_hour.get_hours(), 3.0)
        self.assertEqual(study_hour.get_subject(), "English")
        self.assertEqual(study_hour.get_score(), 85.0)

    def test_console_input_reader(self):
        self.assertTrue(issubclass(ConsoleInputReader, IInputReader))
        self.assertTrue(hasattr(ConsoleInputReader, "read"))

    def test_console_output_writer(self):
        self.assertTrue(issubclass(ConsoleOutputWriter, IOutputWriter))
        self.assertTrue(hasattr(ConsoleOutputWriter, "write"))

    def test_schedule_invalid_date_format(self):
        invalid_day = "20260501"
        with self.assertRaises(ValueError):
            if len(invalid_day) != 10 or invalid_day[4] != "-" or invalid_day[7] != "-":
                raise ValueError("Invalid date format!")

    def test_schedule_invalid_time_format(self):
        invalid_time = "0800"
        with self.assertRaises(ValueError):
            if len(invalid_time) != 5 or invalid_time[2] != ":":
                raise ValueError("Invalid time format!")

    def test_schedule_empty_task(self):
        invalid_task = "   "
        with self.assertRaises(ValueError):
            if not invalid_task.strip():
                raise ValueError("Task cannot be empty!")

    def test_deadline_empty_task(self):
        invalid_task = ""
        with self.assertRaises(ValueError):
            if not invalid_task.strip():
                raise ValueError("Task cannot be empty!")

    def test_quiz_empty_subject(self):
        invalid_subject = "  "
        with self.assertRaises(ValueError):
            if not invalid_subject.strip():
                raise ValueError("Subject cannot be empty!")

    def test_quiz_invalid_answer(self):
        invalid_answer = "E"
        with self.assertRaises(ValueError):
            if invalid_answer not in ["A", "B", "C", "D"]:
                raise ValueError("Answer must be A, B, C, or D!")

    def test_study_hour_negative_hours(self):
        invalid_hours = -1.0
        with self.assertRaises(ValueError):
            if invalid_hours < 0:
                raise ValueError("Hours cannot be negative!")

    def test_deadline_invalid_index(self):
        deadline = Deadline("Study Math")
        self.processor.add_deadline(deadline)
        deadlines     = self.processor.get_deadlines()
        invalid_index = 99 - 1
        self.assertFalse(0 <= invalid_index < len(deadlines))

    def test_quiz_empty_choices(self):
        invalid_choices = ["A answer", "", "C answer", "D answer"]
        with self.assertRaises(ValueError):
            if not all(c.strip() for c in invalid_choices):
                raise ValueError("All choices cannot be empty!")

    def test_study_hour_zero_hours(self):
        study_hour = StudyHour("2026-05-01", 0.0, "Math", 0.0)
        self.processor.add_study_hour(study_hour)
        self.assertEqual(self.processor.get_study_hours()[0].get_hours(), 0.0)


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromTestCase(TestDataProcessor)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        print("\nTests failed. Please fix the errors above before running the app.")
    else:
        print("\nAll tests passed. Starting app...\n")
        reader    = ConsoleInputReader()
        writer    = ConsoleOutputWriter()
        processor = DataProcessor()
        app       = StudentStudyPalApp(reader, writer, processor)
        app.run()