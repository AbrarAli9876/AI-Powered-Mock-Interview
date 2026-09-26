from __future__ import annotations

from app.database import SessionLocal
from app.enums.coding_language import CodingLanguage
from app.enums.question_difficulty import QuestionDifficulty
from app.models.coding_question import CodingQuestion
from app.models.coding_test_case import CodingTestCase


# =========================================================
# CONFIGURATION
# =========================================================

PYTHON_TOPIC_ID = 1

LANGUAGE = CodingLanguage.PYTHON

DIFFICULTY = QuestionDifficulty.EASY


# =========================================================
# CODING QUESTION DATA
# =========================================================

CODING_QUESTIONS = [
    {
        "title": "Reverse a String",
        "problem_statement": (
            "Write a Python program to reverse a given string. "
            "The program should read one string from the input "
            "and print the string in reverse order."
        ),
        "input_format": (
            "The first line contains a single string. "
            "The string may contain letters, digits, spaces, "
            "or other characters."
        ),
        "output_format": (
            "Print the given string in reverse order."
        ),
        "constraints": (
            "1 <= length of string <= 1000"
        ),
        "examples": (
            "Input: hello\n"
            "Output: olleh"
        ),
        "starter_code": (
            "text = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Think about how you can access characters "
            "from the end of a string to the beginning."
        ),
        "hint_2": (
            "Python provides a simple sequence operation "
            "that can reverse a string."
        ),
        "test_cases": [
            ("hello", "olleh"),
            ("Python", "nohtyP"),
            ("a", "a"),
        ],
    },
    {
        "title": "Check if a String is a Palindrome",
        "problem_statement": (
            "Write a Python program to determine whether a "
            "given string is a palindrome. A palindrome reads "
            "the same from left to right and right to left."
        ),
        "input_format": (
            "The first line contains a single string."
        ),
        "output_format": (
            "Print 'Palindrome' if the string is a palindrome; "
            "otherwise print 'Not Palindrome'."
        ),
        "constraints": (
            "1 <= length of string <= 1000"
        ),
        "examples": (
            "Input: madam\n"
            "Output: Palindrome"
        ),
        "starter_code": (
            "text = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Compare the original string with the string "
            "formed by reading it backwards."
        ),
        "hint_2": (
            "A palindrome should have identical characters "
            "at corresponding positions from both ends."
        ),
        "test_cases": [
            ("madam", "Palindrome"),
            ("hello", "Not Palindrome"),
            ("level", "Palindrome"),
        ],
    },
    {
        "title": "Find the Missing Number in an Array",
        "problem_statement": (
            "You are given n distinct integers from the range "
            "1 to n+1 with exactly one number missing. Find "
            "and print the missing number."
        ),
        "input_format": (
            "The first line contains n, the number of elements. "
            "The second line contains n distinct integers."
        ),
        "output_format": (
            "Print the missing number."
        ),
        "constraints": (
            "1 <= n <= 10000\n"
            "The numbers are distinct and belong to the range 1 to n+1."
        ),
        "examples": (
            "Input: 5\n"
            "1 2 3 5 6\n"
            "Output: 4"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "The complete range has a predictable sum."
        ),
        "hint_2": (
            "Compare the expected sum of all numbers with "
            "the sum of the given numbers."
        ),
        "test_cases": [
            ("5\n1 2 3 5 6", "4"),
            ("4\n1 2 3 5", "4"),
            ("1\n2", "1"),
        ],
    },
    {
        "title": "Count Frequency of Each Character",
        "problem_statement": (
            "Write a Python program that counts how many times "
            "each character appears in a given string. Print "
            "each character and its frequency in the order in "
            "which each character first appears."
        ),
        "input_format": (
            "The first line contains a string."
        ),
        "output_format": (
            "Print each character followed by its frequency, "
            "one character per line, using the format "
            "character frequency."
        ),
        "constraints": (
            "1 <= length of string <= 1000"
        ),
        "examples": (
            "Input: banana\n"
            "Output:\n"
            "b 1\n"
            "a 3\n"
            "n 2"
        ),
        "starter_code": (
            "text = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "A dictionary can store a character as a key "
            "and its count as the value."
        ),
        "hint_2": (
            "Process each character one at a time and update "
            "its count."
        ),
        "test_cases": [
            ("banana", "b 1\na 3\nn 2"),
            ("hello", "h 1\ne 1\nl 2\no 1"),
            ("aabbc", "a 2\nb 2\nc 1"),
        ],
    },
    {
        "title": "Two Sum",
        "problem_statement": (
            "Given an array of integers and a target value, "
            "find two different elements whose values add up "
            "to the target. Print their zero-based indices."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers. The third line contains the target."
        ),
        "output_format": (
            "Print the two zero-based indices separated by a space. "
            "The pair should be printed in increasing index order."
        ),
        "constraints": (
            "2 <= n <= 10000\n"
            "A valid pair is guaranteed to exist."
        ),
        "examples": (
            "Input: 4\n"
            "2 7 11 15\n"
            "9\n"
            "Output: 0 1"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "target = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "For every number, think about the other number "
            "you need to reach the target."
        ),
        "hint_2": (
            "A dictionary can remember numbers you have already seen "
            "and their indices."
        ),
        "test_cases": [
            ("4\n2 7 11 15\n9", "0 1"),
            ("3\n3 2 4\n6", "1 2"),
            ("4\n3 3 5 7\n6", "0 1"),
        ],
    },
    {
        "title": "Move All Zeroes to the End",
        "problem_statement": (
            "Given an array of integers, move all zero values "
            "to the end of the array while keeping the relative "
            "order of all non-zero elements unchanged."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the modified array."
        ),
        "constraints": (
            "1 <= n <= 10000"
        ),
        "examples": (
            "Input: 5\n"
            "0 1 0 3 12\n"
            "Output: 1 3 12 0 0"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Separate the non-zero values from the zero values."
        ),
        "hint_2": (
            "The final array should contain all non-zero values "
            "first, followed by the required number of zeroes."
        ),
        "test_cases": [
            ("5\n0 1 0 3 12", "1 3 12 0 0"),
            ("4\n1 2 3 4", "1 2 3 4"),
            ("5\n0 0 1 0 2", "1 2 0 0 0"),
        ],
    },
    {
        "title": "Check if Two Strings are Anagrams",
        "problem_statement": (
            "Write a Python program to determine whether two "
            "given strings are anagrams. Two strings are anagrams "
            "if they contain the same characters with the same "
            "frequencies."
        ),
        "input_format": (
            "The first line contains the first string. "
            "The second line contains the second string."
        ),
        "output_format": (
            "Print 'Anagram' if the strings are anagrams; "
            "otherwise print 'Not Anagram'."
        ),
        "constraints": (
            "1 <= length of each string <= 1000"
        ),
        "examples": (
            "Input: listen\n"
            "silent\n"
            "Output: Anagram"
        ),
        "starter_code": (
            "first = input()\n"
            "second = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Anagrams have the same character counts."
        ),
        "hint_2": (
            "You can compare the characters after arranging "
            "both strings in the same order."
        ),
        "test_cases": [
            ("listen\nsilent", "Anagram"),
            ("hello\nworld", "Not Anagram"),
            ("triangle\nintegral", "Anagram"),
        ],
    },
    {
        "title": "Check for Balanced Parentheses",
        "problem_statement": (
            "Given a string containing parentheses '(', ')', "
            "brackets '[', ']', and braces '{', determine whether "
            "the brackets are properly balanced and correctly nested."
        ),
        "input_format": (
            "The first line contains a string containing brackets."
        ),
        "output_format": (
            "Print 'Balanced' if all brackets are correctly matched; "
            "otherwise print 'Not Balanced'."
        ),
        "constraints": (
            "1 <= length of string <= 1000"
        ),
        "examples": (
            "Input: ({[]})\n"
            "Output: Balanced"
        ),
        "starter_code": (
            "text = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "A stack is useful because the most recently opened "
            "bracket must be closed first."
        ),
        "hint_2": (
            "When you see a closing bracket, compare it with "
            "the most recent opening bracket."
        ),
        "test_cases": [
            ("({[]})", "Balanced"),
            ("([)]", "Not Balanced"),
            ("((()))", "Balanced"),
        ],
    },
    {
        "title": "Maximum Subarray Sum",
        "problem_statement": (
            "Given an array of integers, find the contiguous "
            "subarray with the largest possible sum and print "
            "that maximum sum."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the maximum subarray sum."
        ),
        "constraints": (
            "1 <= n <= 10000\n"
            "-10000 <= array element <= 10000"
        ),
        "examples": (
            "Input: 9\n"
            "-2 1 -3 4 -1 2 1 -5 4\n"
            "Output: 6"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "At each position, decide whether it is better to "
            "extend the previous subarray or start a new one."
        ),
        "hint_2": (
            "Keep track of both the best sum ending at the current "
            "position and the best sum seen overall."
        ),
        "test_cases": [
            ("9\n-2 1 -3 4 -1 2 1 -5 4", "6"),
            ("5\n1 2 3 4 5", "15"),
            ("4\n-5 -2 -8 -1", "-1"),
        ],
    },
    {
        "title": "Flatten a Nested List",
        "problem_statement": (
            "Given a nested list containing integers and other "
            "nested lists, flatten it into a single list while "
            "preserving the original left-to-right order."
        ),
        "input_format": (
            "The first line contains a valid Python-style nested "
            "list representation, such as [1, [2, [3, 4]], 5]."
        ),
        "output_format": (
            "Print the flattened list in Python list format."
        ),
        "constraints": (
            "The nesting depth is at most 20.\n"
            "The list contains at least one integer."
        ),
        "examples": (
            "Input: [1, [2, [3, 4]], 5]\n"
            "Output: [1, 2, 3, 4, 5]"
        ),
        "starter_code": (
            "import ast\n"
            "\n"
            "data = ast.literal_eval(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "A recursive function can process an integer directly "
            "and recursively process a nested list."
        ),
        "hint_2": (
            "Keep one result list and add elements to it in their "
            "original order."
        ),
        "test_cases": [
            ("[1, [2, [3, 4]], 5]", "[1, 2, 3, 4, 5]"),
            ("[[1, 2], [3, 4]]", "[1, 2, 3, 4]"),
            ("[1, [2], [[3]]]", "[1, 2, 3]"),
        ],
    },
    {
        "title": "First Non-Repeating Character",
        "problem_statement": (
            "Given a string, find the first character that occurs "
            "exactly once in the string."
        ),
        "input_format": (
            "The first line contains a string."
        ),
        "output_format": (
            "Print the first non-repeating character. If every "
            "character repeats, print '-1'."
        ),
        "constraints": (
            "1 <= length of string <= 1000"
        ),
        "examples": (
            "Input: swiss\n"
            "Output: w"
        ),
        "starter_code": (
            "text = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "First determine how many times every character occurs."
        ),
        "hint_2": (
            "After building the frequency table, scan the original "
            "string from left to right."
        ),
        "test_cases": [
            ("swiss", "w"),
            ("aabbc", "c"),
            ("aabb", "-1"),
        ],
    },
    {
        "title": "Rotate an Array by K Positions",
        "problem_statement": (
            "Given an array and an integer k, rotate the array "
            "to the right by k positions."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers. The third line contains k."
        ),
        "output_format": (
            "Print the rotated array."
        ),
        "constraints": (
            "1 <= n <= 10000\n"
            "0 <= k <= 100000"
        ),
        "examples": (
            "Input: 5\n"
            "1 2 3 4 5\n"
            "2\n"
            "Output: 4 5 1 2 3"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "k = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "If k is larger than the array length, reduce it using "
            "the array length."
        ),
        "hint_2": (
            "Think about splitting the array into two parts and "
            "changing their order."
        ),
        "test_cases": [
            ("5\n1 2 3 4 5\n2", "4 5 1 2 3"),
            ("4\n1 2 3 4\n1", "4 1 2 3"),
            ("3\n1 2 3\n3", "1 2 3"),
        ],
    },
    {
        "title": "Find Duplicates in an Array",
        "problem_statement": (
            "Given an array of integers, find all values that "
            "appear more than once. Print each duplicate only once "
            "in the order in which it is first detected."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the duplicate values separated by spaces. "
            "If there are no duplicates, print '-1'."
        ),
        "constraints": (
            "1 <= n <= 10000"
        ),
        "examples": (
            "Input: 6\n"
            "1 2 3 2 4 1\n"
            "Output: 2 1"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Use a set to remember values that have already appeared."
        ),
        "hint_2": (
            "A value becomes a duplicate when you encounter it "
            "again after it has already been seen."
        ),
        "test_cases": [
            ("6\n1 2 3 2 4 1", "2 1"),
            ("5\n1 2 3 4 5", "-1"),
            ("6\n4 4 5 6 5 4", "4 5"),
        ],
    },
    {
        "title": "Merge Two Sorted Arrays",
        "problem_statement": (
            "Given two arrays sorted in ascending order, merge "
            "them into one sorted array."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n sorted integers. The third line contains m. The "
            "fourth line contains m sorted integers."
        ),
        "output_format": (
            "Print the merged sorted array."
        ),
        "constraints": (
            "1 <= n, m <= 10000"
        ),
        "examples": (
            "Input: 3\n"
            "1 3 5\n"
            "3\n"
            "2 4 6\n"
            "Output: 1 2 3 4 5 6"
        ),
        "starter_code": (
            "n = int(input())\n"
            "first = list(map(int, input().split()))\n"
            "m = int(input())\n"
            "second = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Both arrays are already sorted, so you do not need "
            "to sort them again."
        ),
        "hint_2": (
            "Use two positions, one for each array, and repeatedly "
            "take the smaller current value."
        ),
        "test_cases": [
            ("3\n1 3 5\n3\n2 4 6", "1 2 3 4 5 6"),
            ("2\n1 2\n3\n1 3 4", "1 1 2 3 4"),
            ("1\n5\n3\n1 2 3", "1 2 3 5"),
        ],
    },
    {
        "title": "Find the Second Largest Element",
        "problem_statement": (
            "Given an array of integers, find the second largest "
            "distinct value in the array."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the second largest distinct element."
        ),
        "constraints": (
            "2 <= n <= 10000\n"
            "At least two distinct values are present."
        ),
        "examples": (
            "Input: 5\n"
            "10 5 8 12 3\n"
            "Output: 10"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "You can keep track of the largest and second-largest "
            "distinct values while scanning the array."
        ),
        "hint_2": (
            "When a new maximum is found, the previous maximum "
            "may become the second largest."
        ),
        "test_cases": [
            ("5\n10 5 8 12 3", "10"),
            ("5\n1 5 3 4 2", "4"),
            ("6\n10 10 8 7 9 9", "9"),
        ],
    },
    {
        "title": "Find the Intersection of Two Arrays",
        "problem_statement": (
            "Given two arrays of integers, find the values that "
            "appear in both arrays. Print each common value only "
            "once in ascending order."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "the first array. The third line contains m. The fourth "
            "line contains the second array."
        ),
        "output_format": (
            "Print the common values in ascending order. If there "
            "are no common values, print '-1'."
        ),
        "constraints": (
            "1 <= n, m <= 10000"
        ),
        "examples": (
            "Input: 4\n"
            "1 2 2 3\n"
            "3\n"
            "2 3 4\n"
            "Output: 2 3"
        ),
        "starter_code": (
            "n = int(input())\n"
            "first = list(map(int, input().split()))\n"
            "m = int(input())\n"
            "second = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "A set can efficiently represent the distinct values "
            "of an array."
        ),
        "hint_2": (
            "The intersection contains values present in both sets."
        ),
        "test_cases": [
            ("4\n1 2 2 3\n3\n2 3 4", "2 3"),
            ("3\n1 2 3\n3\n4 5 6", "-1"),
            ("5\n5 1 2 2 3\n4\n2 3 3 4", "2 3"),
        ],
    },
    {
        "title": "Check if a Number is a Power of Two",
        "problem_statement": (
            "Given a positive integer n, determine whether it "
            "is a power of two."
        ),
        "input_format": (
            "The first line contains a positive integer n."
        ),
        "output_format": (
            "Print 'Yes' if n is a power of two; otherwise print 'No'."
        ),
        "constraints": (
            "1 <= n <= 10^9"
        ),
        "examples": (
            "Input: 16\n"
            "Output: Yes"
        ),
        "starter_code": (
            "n = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Powers of two have a special binary representation."
        ),
        "hint_2": (
            "You can repeatedly divide by two or use a bitwise "
            "property to test the number."
        ),
        "test_cases": [
            ("16", "Yes"),
            ("18", "No"),
            ("1", "Yes"),
        ],
    },
    {
        "title": "Implement a FIFO Queue Using Two Stacks",
        "problem_statement": (
            "Implement a basic FIFO queue using two stacks. "
            "The input contains a sequence of queue operations. "
            "Support ENQUEUE x and DEQUEUE operations. Print the "
            "value removed by every DEQUEUE operation."
        ),
        "input_format": (
            "The first line contains q, the number of operations. "
            "Each following line contains either 'ENQUEUE x' or "
            "'DEQUEUE'. A DEQUEUE operation is only performed when "
            "the queue is non-empty."
        ),
        "output_format": (
            "For every DEQUEUE operation, print the removed value "
            "on a separate line."
        ),
        "constraints": (
            "1 <= q <= 10000"
        ),
        "examples": (
            "Input: 5\n"
            "ENQUEUE 10\n"
            "ENQUEUE 20\n"
            "DEQUEUE\n"
            "ENQUEUE 30\n"
            "DEQUEUE\n"
            "Output:\n"
            "10\n"
            "20"
        ),
        "starter_code": (
            "q = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Use one stack for incoming elements and another "
            "stack for outgoing elements."
        ),
        "hint_2": (
            "When the output stack is empty, transfer elements "
            "from the input stack to reverse their order."
        ),
        "test_cases": [
            (
                "5\nENQUEUE 10\nENQUEUE 20\nDEQUEUE\nENQUEUE 30\nDEQUEUE",
                "10\n20",
            ),
            (
                "6\nENQUEUE 1\nENQUEUE 2\nENQUEUE 3\nDEQUEUE\nDEQUEUE\nDEQUEUE",
                "1\n2\n3",
            ),
            (
                "7\nENQUEUE 5\nDEQUEUE\nENQUEUE 7\nENQUEUE 8\nDEQUEUE\nDEQUEUE\nENQUEUE 9",
                "5\n7\n8",
            ),
        ],
    },
    {
        "title": "Find Maximum and Minimum in One Pass",
        "problem_statement": (
            "Given an array of integers, find both the maximum "
            "and minimum values using a single pass through the array."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the minimum value followed by the maximum value."
        ),
        "constraints": (
            "1 <= n <= 10000"
        ),
        "examples": (
            "Input: 5\n"
            "4 1 8 2 6\n"
            "Output: 1 8"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Initialize both values using the first element."
        ),
        "hint_2": (
            "During the same loop, compare each value with both "
            "the current minimum and maximum."
        ),
        "test_cases": [
            ("5\n4 1 8 2 6", "1 8"),
            ("4\n-5 -2 -10 -1", "-10 -1"),
            ("3\n7 7 7", "7 7"),
        ],
    },
    {
        "title": "Check if a String is a Valid Shuffle",
        "problem_statement": (
            "Given three strings A, B, and C, determine whether "
            "C is a valid shuffle of A and B. C is a valid shuffle "
            "if it contains all characters from A and B while "
            "preserving the relative order of characters from each "
            "source string."
        ),
        "input_format": (
            "The first line contains string A. The second line "
            "contains string B. The third line contains string C."
        ),
        "output_format": (
            "Print 'Valid' if C is a valid shuffle of A and B; "
            "otherwise print 'Invalid'."
        ),
        "constraints": (
            "1 <= length of A, B <= 1000\n"
            "length of C = length of A + length of B"
        ),
        "examples": (
            "Input: ab\n"
            "cd\n"
            "acbd\n"
            "Output: Valid"
        ),
        "starter_code": (
            "a = input()\n"
            "b = input()\n"
            "c = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "At every position in C, the character must come from "
            "the next unused character of either A or B."
        ),
        "hint_2": (
            "Think of the problem as moving through A and B while "
            "matching characters in C."
        ),
        "test_cases": [
            ("ab\ncd\nacbd", "Valid"),
            ("ab\ncd\nabcd", "Valid"),
            ("ab\ncd\nadbc", "Invalid"),
        ],
    },
    {
        "title": "Implement Binary Search",
        "problem_statement": (
            "Given a sorted array of integers and a target value, "
            "find the zero-based index of the target using binary "
            "search. If the target is not present, print -1."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n sorted integers. The third line contains the target."
        ),
        "output_format": (
            "Print the zero-based index of the target, or -1 if "
            "the target does not exist."
        ),
        "constraints": (
            "1 <= n <= 10000\n"
            "The array is sorted in ascending order."
        ),
        "examples": (
            "Input: 5\n"
            "1 3 5 7 9\n"
            "7\n"
            "Output: 3"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "target = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Use the middle element to determine which half "
            "of the array can contain the target."
        ),
        "hint_2": (
            "Keep left and right boundaries and repeatedly reduce "
            "the search range."
        ),
        "test_cases": [
            ("5\n1 3 5 7 9\n7", "3"),
            ("6\n2 4 6 8 10 12\n2", "0"),
            ("5\n1 3 5 7 9\n4", "-1"),
        ],
    },
    {
        "title": "Find All Pairs with a Given Sum",
        "problem_statement": (
            "Given an array of integers and a target value, find "
            "all unique pairs of values whose sum equals the target. "
            "Print each pair in ascending order."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers. The third line contains the target."
        ),
        "output_format": (
            "Print each pair on a separate line in the format "
            "smaller_value larger_value. If no pair exists, print -1."
        ),
        "constraints": (
            "2 <= n <= 10000"
        ),
        "examples": (
            "Input: 6\n"
            "1 5 7 -1 5 3\n"
            "6\n"
            "Output:\n"
            "1 5\n"
            "-1 7"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "target = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "For each number, calculate the value needed to "
            "reach the target."
        ),
        "hint_2": (
            "Use a set to avoid printing the same value pair "
            "more than once."
        ),
        "test_cases": [
            (
                "6\n1 5 7 -1 5 3\n6",
                "-1 7\n1 5",
            ),
            (
                "5\n2 4 3 5 1\n6",
                "1 5\n2 4",
            ),
            (
                "4\n1 2 3 4\n20",
                "-1",
            ),
        ],
    },
    {
        "title": "Longest Common Prefix",
        "problem_statement": (
            "Given a list of strings, find the longest prefix "
            "shared by all strings."
        ),
        "input_format": (
            "The first line contains n. The following n lines "
            "each contain one string."
        ),
        "output_format": (
            "Print the longest common prefix. If no common prefix "
            "exists, print '-1'."
        ),
        "constraints": (
            "1 <= n <= 1000\n"
            "1 <= length of each string <= 1000"
        ),
        "examples": (
            "Input: 3\n"
            "flower\n"
            "flow\n"
            "flight\n"
            "Output: fl"
        ),
        "starter_code": (
            "n = int(input())\n"
            "words = [input() for _ in range(n)]\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Start with the first string as a possible prefix."
        ),
        "hint_2": (
            "Compare the prefix with each remaining string and "
            "shorten it whenever necessary."
        ),
        "test_cases": [
            ("3\nflower\nflow\nflight", "fl"),
            ("3\ndog\ndoor\ndoll", "do"),
            ("3\ncat\ndog\nfish", "-1"),
        ],
    },
    {
        "title": "Remove Duplicates from a Sorted Array",
        "problem_statement": (
            "Given a sorted array of integers, remove duplicate "
            "values so that each value appears only once. Print "
            "the resulting array."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers sorted in non-decreasing order."
        ),
        "output_format": (
            "Print the array after removing duplicate values."
        ),
        "constraints": (
            "1 <= n <= 10000"
        ),
        "examples": (
            "Input: 7\n"
            "1 1 2 2 3 4 4\n"
            "Output: 1 2 3 4"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Because the array is sorted, equal values will appear "
            "next to each other."
        ),
        "hint_2": (
            "Keep a result list and add a value only when it differs "
            "from the previously added value."
        ),
        "test_cases": [
            ("7\n1 1 2 2 3 4 4", "1 2 3 4"),
            ("5\n1 2 3 4 5", "1 2 3 4 5"),
            ("6\n2 2 2 3 3 4", "2 3 4"),
        ],
    },
    {
        "title": "Check if Two Strings are One Edit Distance Apart",
        "problem_statement": (
            "Given two strings, determine whether they are exactly "
            "one edit apart. A single edit can be an insertion, "
            "deletion, or replacement of one character."
        ),
        "input_format": (
            "The first line contains the first string. "
            "The second line contains the second string."
        ),
        "output_format": (
            "Print 'Yes' if the strings are exactly one edit apart; "
            "otherwise print 'No'."
        ),
        "constraints": (
            "0 <= length of each string <= 1000"
        ),
        "examples": (
            "Input: pale\n"
            "ple\n"
            "Output: Yes"
        ),
        "starter_code": (
            "first = input()\n"
            "second = input()\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "First compare the lengths of the two strings."
        ),
        "hint_2": (
            "After locating the first mismatch, consider whether "
            "one insertion, deletion, or replacement can make them equal."
        ),
        "test_cases": [
            ("pale\nple", "Yes"),
            ("pale\nbale", "Yes"),
            ("pale\nbake", "No"),
        ],
    },
    {
        "title": "Find the Missing and Duplicate Numbers",
        "problem_statement": (
            "An array contains numbers from 1 to n, but one number "
            "appears twice and another number is missing. Find both "
            "the duplicate and missing numbers."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the duplicate number followed by the missing number."
        ),
        "constraints": (
            "2 <= n <= 10000"
        ),
        "examples": (
            "Input: 5\n"
            "1 2 2 4 5\n"
            "Output: 2 3"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Count how many times each number from 1 to n occurs."
        ),
        "hint_2": (
            "The number with count two is the duplicate, while "
            "the number with count zero is missing."
        ),
        "test_cases": [
            ("5\n1 2 2 4 5", "2 3"),
            ("4\n1 1 3 4", "1 2"),
            ("6\n1 2 3 5 6 6", "6 4"),
        ],
    },
    {
        "title": "Count Lines and Words in Text",
        "problem_statement": (
            "Given a block of text through standard input, count "
            "the number of lines and the number of words. The first "
            "line of the input contains the number of text lines, "
            "followed by those lines."
        ),
        "input_format": (
            "The first line contains n, the number of text lines. "
            "The next n lines contain the text."
        ),
        "output_format": (
            "Print the number of lines followed by the number of "
            "words in the format: Lines: X and Words: Y"
        ),
        "constraints": (
            "1 <= n <= 10000\n"
            "Words are separated by whitespace."
        ),
        "examples": (
            "Input: 2\n"
            "Hello world\n"
            "Python is easy\n"
            "Output: Lines: 2 and Words: 5"
        ),
        "starter_code": (
            "n = int(input())\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Read exactly n lines after reading the number of lines."
        ),
        "hint_2": (
            "The split() method can divide each line into words."
        ),
        "test_cases": [
            (
                "2\nHello world\nPython is easy",
                "Lines: 2 and Words: 5",
            ),
            (
                "3\nOne two\nThree\nFour five six",
                "Lines: 3 and Words: 6",
            ),
            (
                "1\nHello",
                "Lines: 1 and Words: 1",
            ),
        ],
    },
    {
        "title": "Find the Most Frequent Element",
        "problem_statement": (
            "Given a list of integers, find the element that occurs "
            "most frequently. If multiple elements have the same "
            "highest frequency, return the one that appears first "
            "in the array."
        ),
        "input_format": (
            "The first line contains n. The second line contains "
            "n integers."
        ),
        "output_format": (
            "Print the most frequent element."
        ),
        "constraints": (
            "1 <= n <= 10000"
        ),
        "examples": (
            "Input: 7\n"
            "1 3 2 3 4 3 2\n"
            "Output: 3"
        ),
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "\n"
            "# Write your solution here\n"
        ),
        "hint_1": (
            "Use a dictionary to count the frequency of every element."
        ),
        "hint_2": (
            "After finding the highest frequency, scan the original "
            "array to resolve ties by first occurrence."
        ),
        "test_cases": [
            ("7\n1 3 2 3 4 3 2", "3"),
            ("5\n5 5 1 2 2", "5"),
            ("6\n1 2 3 2 3 1", "1"),
        ],
    },
]


# =========================================================
# VALIDATION
# =========================================================

def validate_question_data() -> None:
    """
    Validate the seed data before inserting anything
    into the database.
    """

    if len(CODING_QUESTIONS) != 28:
        raise ValueError(
            f"Expected exactly 28 coding questions, "
            f"found {len(CODING_QUESTIONS)}."
        )

    for index, question in enumerate(
        CODING_QUESTIONS,
        start=1,
    ):
        required_fields = [
            "title",
            "problem_statement",
            "input_format",
            "output_format",
            "constraints",
            "examples",
            "starter_code",
            "hint_1",
            "hint_2",
            "test_cases",
        ]

        for field in required_fields:
            if not question.get(field):
                raise ValueError(
                    f"Question {index} "
                    f"('{question.get('title', 'Unknown')}') "
                    f"is missing '{field}'."
                )

        test_cases = question["test_cases"]

        if len(test_cases) != 3:
            raise ValueError(
                f"Question {index} "
                f"('{question['title']}') must have exactly "
                f"3 test cases, found {len(test_cases)}."
            )

        for test_case_index, test_case in enumerate(
            test_cases,
            start=1,
        ):
            if (
                not isinstance(test_case, tuple)
                or len(test_case) != 2
            ):
                raise ValueError(
                    f"Question {index}, test case "
                    f"{test_case_index} is invalid."
                )

            input_data, expected_output = test_case

            if not isinstance(input_data, str):
                raise ValueError(
                    f"Question {index}, test case "
                    f"{test_case_index} input must be a string."
                )

            if not isinstance(expected_output, str):
                raise ValueError(
                    f"Question {index}, test case "
                    f"{test_case_index} expected output "
                    f"must be a string."
                )


# =========================================================
# SEED FUNCTION
# =========================================================

def seed_coding_questions() -> None:
    """
    Insert the complete Easy Python coding question bank.

    Each question contains:
    - Complete problem information
    - Two hints
    - Exactly three visible test cases
    """

    validate_question_data()

    db = SessionLocal()

    try:
        # -----------------------------------------------------
        # CHECK FOR EXISTING QUESTIONS
        # -----------------------------------------------------

        existing_count = (
            db.query(CodingQuestion)
            .filter(
                CodingQuestion.topic_id == PYTHON_TOPIC_ID,
                CodingQuestion.language == LANGUAGE,
                CodingQuestion.difficulty == DIFFICULTY,
            )
            .count()
        )

        if existing_count > 0:
            raise RuntimeError(
                "Python Easy coding questions already exist "
                f"({existing_count} found). "
                "Delete the existing coding questions before "
                "running this seeder."
            )

        # -----------------------------------------------------
        # CREATE QUESTIONS
        # -----------------------------------------------------

        questions_to_create = []

        for question_data in CODING_QUESTIONS:

            question = CodingQuestion(
                topic_id=PYTHON_TOPIC_ID,
                language=LANGUAGE,
                difficulty=DIFFICULTY,
                title=question_data["title"],
                problem_statement=(
                    question_data["problem_statement"]
                ),
                input_format=(
                    question_data["input_format"]
                ),
                output_format=(
                    question_data["output_format"]
                ),
                constraints=(
                    question_data["constraints"]
                ),
                examples=question_data["examples"],
                starter_code=(
                    question_data["starter_code"]
                ),
                hint_1=question_data["hint_1"],
                hint_2=question_data["hint_2"],
            )

            questions_to_create.append(
                question
            )

        # -----------------------------------------------------
        # INSERT QUESTIONS
        # -----------------------------------------------------

        db.add_all(questions_to_create)

        db.flush()

        # -----------------------------------------------------
        # CREATE THREE TEST CASES PER QUESTION
        # -----------------------------------------------------

        test_cases_to_create = []

        for question_index, (
            question,
            question_data,
        ) in enumerate(
            zip(
                questions_to_create,
                CODING_QUESTIONS,
            ),
            start=1,
        ):

            for execution_order, (
                input_data,
                expected_output,
            ) in enumerate(
                question_data["test_cases"],
                start=1,
            ):

                test_case = CodingTestCase(
                    coding_question_id=question.id,
                    input_data=input_data,
                    expected_output=expected_output,
                    is_hidden=False,
                    execution_order=execution_order,
                )

                test_cases_to_create.append(
                    test_case
                )

        # -----------------------------------------------------
        # INSERT TEST CASES
        # -----------------------------------------------------

        db.add_all(test_cases_to_create)

        db.commit()

        # -----------------------------------------------------
        # SUCCESS MESSAGE
        # -----------------------------------------------------

        print()
        print("=" * 60)
        print("CODING QUESTION SEEDING COMPLETED")
        print("=" * 60)
        print(
            f"Questions inserted : "
            f"{len(questions_to_create)}"
        )
        print(
            f"Test cases inserted: "
            f"{len(test_cases_to_create)}"
        )
        print(
            f"Language           : "
            f"{LANGUAGE.value}"
        )
        print(
            f"Difficulty         : "
            f"{DIFFICULTY.value}"
        )
        print(
            f"Topic ID           : "
            f"{PYTHON_TOPIC_ID}"
        )
        print("=" * 60)
        print()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    seed_coding_questions()