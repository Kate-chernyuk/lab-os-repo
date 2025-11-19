#!/usr/bin/env python3
import os
import csv
import glob
from collections import defaultdict
import sys

def get_subjects(base_path):
    """Получить список предметов из базовой директории"""
    subjects = [d for d in os.listdir(base_path)
                if os.path.isdir(os.path.join(base_path, d))
                and not (d.startswith('.') or d == "students")]
    return subjects

def find_student_with_most_mistakes(group_number, base_path="."):
    """Анализ данных для конкретной группы - находим студента с наибольшим количеством неправильных ответов"""
    subjects = get_subjects(base_path)

    student_correct_answers = defaultdict(int)
    best_answer = defaultdict(int) #не имея точного числа вопросов, будем брать максимальное из предоставленных правильных

    for subject in subjects:
        test_path = os.path.join(base_path, subject, "tests", "TEST-*")
        test_files = glob.glob(test_path)

        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='UTF-8') as f:
                    reader = csv.reader(f, delimiter=';')

                    for row in reader:
                        if len(row) >= 5:
                            group, name, date, correct_answers, grade = row

                            if group.strip() == group_number.strip():
                                try:
                                    correct = int(correct_answers.strip())
                                    student_correct_answers[name] += correct
                                    best_answer[str(test_file)] = max(correct, best_answer[str(test_file)])
                                except ValueError:
                                    continue
            except Exception as e:
                print(f"Ошибка при чтении {test_file}: {e}")
                continue

    if student_correct_answers:
        # коварно исходим из той логики, что студент с наименьшим количеством правильных ответов = студент с наибольшим количеством неправильных
        min_student = min(student_correct_answers.items(), key=lambda x: x[1])
        possible_answers_count = sum(best_answer.values())
        print(f"1. СТУДЕНТ С НАИБОЛЬШИМ ЧИСЛОМ НЕПРАВИЛЬНЫХ ОТВЕТОВ:")
        print(f"   Студент: {min_student[0]}")
        print(f"   Количество неправильных ответов: {possible_answers_count - min_student[1]}")


def analyze_attendance(group_number, base_path="."):
    """Анализ посещаемости - найти занятия с минимальной и максимальной посещаемостью"""
    subjects = get_subjects(base_path)
    attendance_stats = defaultdict(int)

    for subject in subjects:
        attendance_path = os.path.join(base_path, subject, f"{group_number}-attendance")
        attendance_files = glob.glob(attendance_path)

        for attendance_file in attendance_files:
            try:
                with open(attendance_file, 'r', encoding='utf-8') as f:
                    total_attendance = 0

                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            name, attendance_str = parts[0], parts[1]
                            attendance_count = attendance_str.count('1')
                            total_attendance += attendance_count

                    attendance_stats[subject] += total_attendance
            except Exception as e:
                continue

    if attendance_stats:
        min_att = min(attendance_stats.items(), key=lambda x: x[1])
        max_att = max(attendance_stats.items(), key=lambda x: x[1])

        print(f"\n2. СТАТИСТИКА ПОСЕЩАЕМОСТИ:")
        print(f"   Занятие с минимальной посещаемостью: {min_att[0]}")
        print(f"   Количество посещений: {min_att[1]}")
        print(f"   Занятие с максимальной посещаемостью: {max_att[0]}")
        print(f"   Количество посещений: {max_att[1]}")



if __name__ == "__main__":
    if len(sys.argv) > 1:
        group_number = sys.argv[1]
        base_path = sys.argv[2] if len(sys.argv) > 2 else "."
    else:
        group_number = "A-09-22"
        base_path = "/os-labs/labs-2025/lab3/labfiles-25"

    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

    find_student_with_most_mistakes(group_number, base_path)
    analyze_attendance(group_number, base_path)
