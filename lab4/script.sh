#!/bin/bash

set -e

GROUP_NUMBER="${1:-A-09-22}"
BASE_PATH="${2:-.}"

echo "1. ПОИСК СТУДЕНТА С НАИБОЛЬШИМ КОЛИЧЕСТВОМ НЕПРАВИЛЬНЫХ ОТВЕТОВ"

find "$BASE_PATH" -name "TEST-*" -type f | while read test_file; do
    awk -F';' -v group="$GROUP_NUMBER" '$1 == group {
        correct = $4
        if (correct > max_score) max_score = correct
        student_correct[$2] += correct
        attempts[$2]++
    }
    END {
        for (student in attempts)
            print student, max_score * attempts[student], student_correct[student]
        } ' "$test_file";
    done | awk '
        {
            max_possible[$1] += $2
            total_correct[$1] += $3
        }
        END {
             min_correct = -1
             worst_student_1 = ""
             worst_student_2 = ""
             max_wrongs = 0
             for (student in max_possible) {
                 if (min_correct == -1) min_correct = total_correct[student]
                 if (total_correct[student] < min_correct) {
                     min_correct = total_correct[student]
                     worst_student_1 = student
                 }
                 if (max_possible[student] - total_correct[student] > max_wrongs) {
                     max_wrongs = max_possible[student] - total_correct[student]
                     worst_student_2 = student
                 }
             }
             print "СТУДЕНТ С НАИМЕНЬШИМ КОЛИЧЕСТВОМ ПРАВИЛЬНЫХ ОТВЕТОВ:"
             print "   Студент: " worst_student_1
             print "   Количество неправильных ответов: "  max_possible[worst_student_1] - total_correct[worst_student_1]
             print "СТУДЕНТ С НАИБОЛЬШЕЙ РАЗНИЦЕЙ МЕЖДУ ОБЩИМ КОЛИЧЕСТВОМ ВОПРОСОВ, НА КОТОРЫЕ ОН ОТВЕТИЛ, И КОЛИЧЕСТВОМ ПРАВИЛЬНЫХ ОТВЕТОВ:"
             print "   Студент: " worst_student_2
             print "   Количество неправильных ответов: "  max_wrongs

echo "2. СТАТИСТИКА ПОСЕЩАЕМОСТИ:"

find "$BASE_PATH" -name "${GROUP_NUMBER}-attendance" -type f | while read att_file; do
    subject=$(basename $(dirname "$att_file"))
    awk -v subject="$subject" '
    {
        att_str = $NF
        for (i = 1; i <= length(att_str); i++) {
            attendance[i] += substr(att_str, i, 1)
        }
    }
    END {
        for (class in attendance) {
            print subject " " class, attendance[class]
        }
    }' "$att_file";
done | awk '
    {
         if (!min_att || $3 < min_att) {
             min_att = $3
             min_class = $1 ", " $2
         }
         if (!max_att || $3 > max_att) {
             max_att = $3
             max_class = $1 ", " $2
         }
    }
    END {
        print "   Занятие с минимальной посещаемостью: " min_class
        print "   Количество посещений: " min_att
        print "   Занятие с максимальной посещаемостью: " max_class
        print "   Количество посещений: " max_att
   }'
