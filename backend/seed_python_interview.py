from app.database import SessionLocal
from app.models.topic import Topic
from app.models.question import Question
from app.enums.question_difficulty import QuestionDifficulty


TOPIC_NAME = "Python"


QUESTIONS = [
    # =========================================================
    # EASY — 10 QUESTIONS
    # =========================================================

    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is Python, and what are its key features?"
        ),
        "expected_answer": (
            "Python is a high-level, interpreted, general-purpose "
            "programming language. Key features include dynamic typing, "
            "being interpreted rather than compiled ahead of time, support "
            "for procedural, object-oriented, and functional programming, "
            "automatic memory management through garbage collection, and "
            "a large standard library."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is the difference between a list and a tuple?"
        ),
        "expected_answer": (
            "A list is mutable and is defined using square brackets. "
            "A tuple is immutable and is defined using parentheses. "
            "Tuples are generally faster and use less memory, and a tuple "
            "can be used as a dictionary key if all its elements are "
            "hashable, whereas a list cannot."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What are Python's built-in data types?"
        ),
        "expected_answer": (
            "Python's built-in data types include numeric types such as "
            "int, float, and complex; sequence types such as str, list, "
            "tuple, and range; mapping type dict; set types set and "
            "frozenset; boolean bool; and NoneType."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is the difference between == and is?"
        ),
        "expected_answer": (
            "The == operator checks value equality, meaning whether two "
            "objects contain the same data. The is operator checks identity "
            "equality, meaning whether two references point to the same "
            "object in memory."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is indentation and why does Python rely on it?"
        ),
        "expected_answer": (
            "Python uses whitespace indentation instead of braces to define "
            "code blocks such as loops, functions, and conditionals. "
            "Indentation is part of Python's syntax and enforces readable "
            "and consistently formatted code."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is a variable in Python, and how is it different "
            "from variables in statically typed languages?"
        ),
        "expected_answer": (
            "A Python variable is a name bound to an object and does not "
            "have a fixed type declared upfront. The type belongs to the "
            "object rather than the variable name, so the same variable "
            "can be rebound to objects of different types."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What are mutable and immutable objects? Give examples."
        ),
        "expected_answer": (
            "Mutable objects can be changed after creation, such as lists, "
            "dictionaries, and sets. Immutable objects cannot be changed "
            "after creation, such as integers, floats, strings, tuples, "
            "and frozensets. Modifying an immutable object creates a new "
            "object."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is the difference between str and repr?"
        ),
        "expected_answer": (
            "str() returns a human-readable informal string representation "
            "intended mainly for end users. repr() returns an unambiguous "
            "formal representation intended mainly for developers and "
            "debugging, ideally one that can recreate the object."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What are Python namespaces?"
        ),
        "expected_answer": (
            "A namespace is a mapping from names to objects used to avoid "
            "naming conflicts. Python has built-in, global, and local "
            "namespaces, organized through the LEGB lookup rule: Local, "
            "Enclosing, Global, and Built-in."
        ),
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": (
            "What is PEP 8?"
        ),
        "expected_answer": (
            "PEP 8 is Python's official style guide. It covers naming "
            "conventions, indentation, line length, formatting, and other "
            "coding practices that help keep Python code consistent and "
            "readable."
        ),
    },


    # =========================================================
    # MEDIUM — 14 QUESTIONS
    # =========================================================

    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is the difference between deep copy and shallow copy?"
        ),
        "expected_answer": (
            "A shallow copy creates a new outer object but keeps references "
            "to the same nested objects as the original. A deep copy "
            "recursively copies nested objects, making the copied structure "
            "independent of the original. Python provides copy.copy() for "
            "shallow copying and copy.deepcopy() for deep copying."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What are *args and **kwargs?"
        ),
        "expected_answer": (
            "*args collects extra positional arguments into a tuple, while "
            "**kwargs collects extra keyword arguments into a dictionary. "
            "They allow functions to accept a variable number of arguments."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is a decorator in Python?"
        ),
        "expected_answer": (
            "A decorator is a function that takes another function or class "
            "as input and extends or modifies its behavior without permanently "
            "changing its source code. Decorators are commonly applied using "
            "the @decorator_name syntax and rely on Python functions being "
            "first-class objects."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is the difference between a generator and a normal function?"
        ),
        "expected_answer": (
            "A normal function uses return to produce a value and then exits. "
            "A generator function uses yield to produce values lazily, "
            "pausing its execution state between calls. It returns a "
            "generator object that can be iterated without storing the entire "
            "sequence in memory."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is the difference between an iterator and an iterable?"
        ),
        "expected_answer": (
            "An iterable is an object capable of returning its members one "
            "at a time and typically implements __iter__. An iterator is an "
            "object with a __next__ method that produces the next value and "
            "raises StopIteration when exhausted. An iterator can be obtained "
            "from an iterable using iter()."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is list comprehension, and why is it preferred over loops?"
        ),
        "expected_answer": (
            "List comprehension is concise syntax for creating lists using "
            "an expression, an iterable, and optionally a condition. It is "
            "generally faster than an equivalent simple for loop and is more "
            "readable for straightforward transformations and filtering."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is the Global Interpreter Lock (GIL)?"
        ),
        "expected_answer": (
            "The GIL is a mutex in CPython that allows only one thread to "
            "execute Python bytecode at a time. It simplifies memory "
            "management but limits true parallelism for CPU-bound "
            "multithreaded programs. Multiprocessing is generally better "
            "for CPU-bound work, while threading can still help with "
            "I/O-bound work."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is the difference between @staticmethod, "
            "@classmethod, and an instance method?"
        ),
        "expected_answer": (
            "An instance method takes self and operates on a particular "
            "object instance. A class method takes cls and operates on the "
            "class itself, allowing access to class state. A static method "
            "takes neither self nor cls and behaves like a regular function "
            "logically grouped inside the class namespace."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is exception handling, and how is it done in Python?"
        ),
        "expected_answer": (
            "Exception handling manages runtime errors using try and except "
            "blocks. Python also provides else, which runs when no exception "
            "occurs, and finally, which runs regardless of whether an "
            "exception occurs and is commonly used for cleanup. Custom "
            "exceptions can be created by subclassing Exception."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is a context manager, and what does the with statement do?"
        ),
        "expected_answer": (
            "A context manager manages the setup and teardown of resources "
            "such as files and locks. It commonly implements __enter__ and "
            "__exit__. The with statement automatically calls the cleanup "
            "logic even when an exception occurs."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is the difference between __init__ and __new__?"
        ),
        "expected_answer": (
            "__new__ is called first and is responsible for creating and "
            "returning a new instance. __init__ is called afterward to "
            "initialize the already-created instance. Overriding __new__ "
            "is relatively uncommon and is mainly useful for immutable "
            "types or patterns such as singletons."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What is monkey patching?"
        ),
        "expected_answer": (
            "Monkey patching is dynamically modifying or extending a class "
            "or module at runtime, such as replacing a method without "
            "changing the original source code. It can be powerful but may "
            "make software harder to understand, debug, and maintain."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "Explain Python's memory management model."
        ),
        "expected_answer": (
            "Python manages memory using a private heap where objects are "
            "allocated. Reference counting is the primary mechanism for "
            "tracking object lifetimes, and objects are normally deallocated "
            "when their reference count reaches zero. A cyclic garbage "
            "collector supplements reference counting by detecting and "
            "cleaning reference cycles."
        ),
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": (
            "What are Python's magic or dunder methods? Give examples."
        ),
        "expected_answer": (
            "Magic or dunder methods are special methods surrounded by "
            "double underscores that allow objects to integrate with "
            "Python's built-in syntax and operations. Examples include "
            "__init__, __str__, __repr__, __len__, __eq__, and __add__."
        ),
    },


    # =========================================================
    # HARD — 11 QUESTIONS
    # =========================================================

    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What is the difference between multithreading, "
            "multiprocessing, and asyncio in Python?"
        ),
        "expected_answer": (
            "Multithreading uses multiple threads sharing memory and is "
            "effective for I/O-bound work but is limited by the GIL for "
            "CPU-bound Python bytecode. Multiprocessing uses separate "
            "processes with separate interpreters and memory spaces, "
            "bypassing the GIL and making it suitable for CPU-bound "
            "parallelism, but with higher memory and communication costs. "
            "asyncio provides single-threaded cooperative concurrency using "
            "an event loop and async/await, making it efficient for high "
            "volumes of I/O-bound work when the code supports non-blocking "
            "operations."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "Explain the Method Resolution Order (MRO) and how Python "
            "resolves multiple inheritance."
        ),
        "expected_answer": (
            "MRO defines the order in which Python searches base classes "
            "when looking for methods or attributes. Python uses the C3 "
            "linearization algorithm to create a consistent and monotonic "
            "order even with complex multiple inheritance and diamond "
            "structures. The MRO can be inspected using ClassName.__mro__ "
            "or ClassName.mro()."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What are metaclasses in Python?"
        ),
        "expected_answer": (
            "A metaclass is the class of a class. It defines how classes "
            "themselves are constructed, just as normal classes define how "
            "their instances are constructed. By default, Python classes "
            "are instances of type. Custom metaclasses can control class "
            "creation, enforce rules, or implement patterns such as "
            "automatic registration."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What are descriptors, and how do property, staticmethod, "
            "and classmethod relate to them?"
        ),
        "expected_answer": (
            "A descriptor is an object implementing one or more of "
            "__get__, __set__, or __delete__, allowing it to customize "
            "attribute access. property, staticmethod, and classmethod "
            "use the descriptor protocol internally. Descriptors are used "
            "for attribute access, validation, computed properties, and "
            "other low-level behavior."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What is the difference between is, ==, and hash() in the "
            "context of custom objects, and how do __eq__ and __hash__ interact?"
        ),
        "expected_answer": (
            "is compares object identity, while == performs value "
            "comparison and can call a custom __eq__ implementation. "
            "Objects used as dictionary keys or set elements must be "
            "hashable. If two objects are considered equal by __eq__, "
            "they must have the same hash value. If __eq__ is overridden "
            "without a consistent __hash__, Python normally makes the "
            "object unhashable by setting __hash__ to None."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "Explain closures in Python and how they relate to Python's "
            "scoping rules."
        ),
        "expected_answer": (
            "A closure occurs when a nested function captures and remembers "
            "variables from an enclosing function's scope even after the "
            "outer function has finished executing. This works because "
            "Python functions retain references to their enclosing lexical "
            "scope. Closures are commonly used in decorators and factory "
            "functions and are related to Python's LEGB scoping rules."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What is the difference between copy.deepcopy, pickling, "
            "and __reduce__ for object serialization?"
        ),
        "expected_answer": (
            "deepcopy recursively duplicates an object in memory using "
            "the copy module and can use __deepcopy__ when defined. "
            "Pickling serializes an object into a byte stream for storage "
            "or transfer and can reconstruct it later. deepcopy and "
            "pickle can rely on __reduce__ or __reduce_ex__, as well as "
            "__getstate__ and __setstate__, to determine how custom "
            "objects should be reconstructed."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "How does Python's garbage collector handle reference cycles, "
            "and what role do __del__ and weak references play?"
        ),
        "expected_answer": (
            "Reference counting alone cannot free objects involved in "
            "reference cycles because their reference counts never reach "
            "zero. Python's cyclic garbage collector periodically detects "
            "and collects unreachable cycles. __del__ methods historically "
            "complicated cycle collection, while weakref provides references "
            "that do not increase reference counts and can help prevent "
            "unwanted object retention."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What is the difference between __slots__ and a regular class, "
            "and what are the trade-offs?"
        ),
        "expected_answer": (
            "Regular Python instances normally store attributes in a "
            "per-instance __dict__, allowing dynamic attribute addition "
            "but using more memory. __slots__ restricts instances to a "
            "fixed set of attributes and can reduce memory usage and "
            "improve attribute access performance. The trade-offs include "
            "losing dynamic attribute assignment and additional complexity "
            "with multiple inheritance."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "Explain how Python coroutines and the asyncio event loop "
            "actually work under the hood."
        ),
        "expected_answer": (
            "A coroutine created with async def can suspend at await points "
            "and return control to the event loop. The event loop maintains "
            "tasks and callbacks and repeatedly resumes ready tasks based "
            "on I/O readiness notifications from the operating system. "
            "This allows many concurrent I/O-bound operations to run on a "
            "single thread without traditional thread-based preemption."
        ),
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": (
            "What is duck typing, and how does it relate to Python's "
            "dynamic type system?"
        ),
        "expected_answer": (
            "Duck typing means an object's suitability for an operation "
            "depends on whether it provides the required methods or "
            "attributes rather than on its explicit class or inheritance "
            "hierarchy. This reflects Python's dynamic typing philosophy. "
            "For example, any object implementing the required iteration "
            "protocol can be used in a for loop regardless of its class."
        ),
    },
]


def seed_python_questions() -> None:
    db = SessionLocal()

    try:
        topic = (
            db.query(Topic)
            .filter(Topic.name == TOPIC_NAME)
            .first()
        )

        if not topic:
            topic = Topic(
                name=TOPIC_NAME,
                description=(
                    "Python programming language interview "
                    "questions covering fundamentals, "
                    "intermediate concepts, and advanced topics."
                ),
                is_active=True,
            )

            db.add(topic)
            db.commit()
            db.refresh(topic)

            print(
                f"Created topic: {topic.name} "
                f"(ID: {topic.id})"
            )

        else:
            print(
                f"Using existing topic: {topic.name} "
                f"(ID: {topic.id})"
            )

        existing_count = (
            db.query(Question)
            .filter(Question.topic_id == topic.id)
            .count()
        )

        if existing_count > 0:
            print(
                f"Python topic already contains "
                f"{existing_count} question(s)."
            )
            print(
                "No questions were inserted to avoid duplicates."
            )
            return

        questions = [
            Question(
                topic_id=topic.id,
                difficulty=item["difficulty"],
                question_text=item["question_text"],
                expected_answer=item["expected_answer"],
            )
            for item in QUESTIONS
        ]

        db.add_all(questions)
        db.commit()

        print()
        print("=" * 60)
        print("PYTHON INTERVIEW QUESTION BANK CREATED")
        print("=" * 60)
        print(f"Topic ID       : {topic.id}")
        print(f"Topic          : {topic.name}")
        print(f"Total questions: {len(questions)}")
        print(
            "Easy           : "
            f"{sum(1 for q in questions if q.difficulty == QuestionDifficulty.EASY)}"
        )
        print(
            "Medium         : "
            f"{sum(1 for q in questions if q.difficulty == QuestionDifficulty.MEDIUM)}"
        )
        print(
            "Hard           : "
            f"{sum(1 for q in questions if q.difficulty == QuestionDifficulty.HARD)}"
        )
        print("=" * 60)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_python_questions()