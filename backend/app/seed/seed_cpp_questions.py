from __future__ import annotations

from collections import Counter

from app.database import SessionLocal
from app.enums.question_difficulty import QuestionDifficulty
from app.models.question import Question
from app.models.topic import Topic


TOPIC_NAME = "C++"

# Extracted from "C++ Interview Questions with Answers (Top Companies).pdf".
# Company labels follow the PDF's reported/inferred attribution; they are not official company question banks.
QUESTIONS = [
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between C and C++?",
        "expected_answer": "C is procedural; C++ adds object-oriented programming (classes, inheritance, polymorphism), generic programming (templates), references, function and operator overloading, namespaces, exceptions and a large standard library (STL). C++ is mostly a superset of C but not fully: some valid C code is invalid C++ (for example implicit conversion from void* ). C++ also gives you RAII, which makes resource management much safer.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are the four pillars of OOP? How does C++ support each?",
        "expected_answer": "Encapsulation: bundling data and functions in a class and hiding details using private / protected . Abstraction: exposing a simple interface and hiding implementation (abstract classes, header versus source files). Inheritance: a derived class reuses and extends a base class (single, multiple, multilevel). Polymorphism: compile-time (function and operator overloading, templates) and run- time (virtual functions).",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between a class and a struct ?",
        "expected_answer": "The only language difference is the default access: members and inheritance are private in a class and public in a struct. By convention, structs hold plain data and classes model objects with invariants and behavior.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are the access specifiers in C++?",
        "expected_answer": "public members are accessible everywhere; protected members are accessible in the class, its derived classes and friends; private members only inside the class and its friends. The access specifier on a base class ( public , protected , private inheritance) controls how base members appear in the derived class. Public inheritance models an \"is- a\" relationship.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between a pointer and a reference?",
        "expected_answer": "A pointer holds an address, can be null, can be reassigned and supports pointer arithmetic. A reference is an alias for an existing object: it must be initialized, cannot be null (in valid code), cannot be reseated and has no arithmetic. Use references for required parameters and pointers when \"no object\" or reseating is meaningful. Smart pointers are preferred when ownership is involved.",
        "companies": [
            "Zoho",
            "Oracle",
            "Amazon",
            "Goldman Sachs",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are constructors and destructors? What types of constructors exist?",
        "expected_answer": "A constructor initializes an object when it is created; a destructor cleans up when it is destroyed (and is the home of RAII). Constructor types: default, parameterized, copy, move (C++11), delegating (C++11), and explicit constructors that prevent implicit conversions. Constructors have no return type, cannot be virtual, and destructors run in the reverse order of construction.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is a copy constructor? What is the difference between shallow and deep copy?",
        "expected_answer": "A copy constructor creates a new object from an existing one. It is invoked when initializing from another object, passing or returning by value (when not elided) and in some container operations. The compiler generated one does a shallow (member by member) copy, so two objects can share the same heap pointer and double free it. A deep copy duplicates the pointed-to data. If a class owns a resource, define the copy operations (or delete them) deliberately.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between function overloading and overriding? What about operator overloading?",
        "expected_answer": "Overloading: same function name with different parameter lists in the same scope; resolved at compile time. Overriding: a derived class redefines a virtual base function with the same signature; resolved at run time. Use override so the compiler checks it. Operator overloading: giving user types custom behavior for operators such as + , == or << . Operators like :: , . , .* and ?: cannot be overloaded.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is a virtual function? What is polymorphism?",
        "expected_answer": "A virtual function is chosen at run time based on the actual object type, not the pointer or reference type. This gives run-time polymorphism: code written against a base class works with any derived class. It only works through pointers or references (not by value, which causes slicing), and a class with virtual functions needs a virtual destructor if it is deleted through a base pointer.",
        "companies": [
            "Zoho",
            "Oracle",
            "Microsoft",
            "Amazon",
            "Flipkart"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What does the static keyword do in C++?",
        "expected_answer": "Static local variable: initialized once and keeps its value between calls. Static data member: one copy shared by all objects of the class. Static member function: belongs to the class, has no this , and cannot access non- static members directly. Static at namespace scope (file level): gives internal linkage, so the name is private to that file.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What does const mean and where can it be used?",
        "expected_answer": "const declares that something must not be modified: variables, pointers ( const int* is a pointer to const data, int* const is a const pointer), reference parameters, and member functions ( void f() const promises not to change the object). Const correctness catches bugs at compile time and lets you pass temporaries to const& parameters. constexpr goes further by allowing compile-time evaluation.",
        "companies": [
            "Zoho",
            "Oracle",
            "Amazon",
            "Microsoft",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between new / delete and malloc / free ?",
        "expected_answer": "new allocates memory and calls the constructor, returns a typed pointer and throws std::bad_alloc on failure; delete calls the destructor and frees memory. malloc / free only deal with raw bytes, return void* and return null on failure. Use new[] with delete[] for arrays, and never mix the two families. Modern code prefers make_unique / make_shared and containers over raw new .",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between stack and heap memory?",
        "expected_answer": "The stack holds local variables and function call frames; allocation is very fast and automatic (freed on scope exit), the size is limited and overflow happens with deep recursion or large locals. The heap (free store) holds dynamically allocated objects whose lifetime you control; it is slower, can fragment and needs explicit or smart-pointer management to avoid leaks. There are also static/global storage and the code segment.",
        "companies": [
            "Oracle",
            "Zoho",
            "Goldman Sachs",
            "Microsoft",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the this pointer?",
        "expected_answer": "this is an implicit pointer available in non-static member functions that points to the object the function was called on. It is used to disambiguate member names, to return *this for method chaining and to pass the current object to other functions. In a const member function its type is pointer to const.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is an inline function? How does it differ from a macro?",
        "expected_answer": "inline is a request that the compiler may replace a call with the function body (and, more importantly today, it permits the definition to appear in multiple translation units). A macro is textual substitution by the preprocessor: no type checking, no scope, evaluates arguments multiple times and is hard to debug. Prefer inline functions, constexpr and templates to macros.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are namespaces, and why avoid using namespace std in headers?",
        "expected_answer": "Namespaces group names to avoid collisions. A using namespace directive in a header leaks every name into all files that include it, which causes ambiguity and surprising overload resolution. Use qualified names ( std::vector ) or narrow using declarations inside function scope or .cpp files.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is a friend function or friend class?",
        "expected_answer": "A friend is granted access to a class's private and protected members without being a member. It is used for operators such as operator<< and for tightly coupled helper classes. Friendship is not inherited, not mutual and not transitive. Overuse weakens encapsulation.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between a declaration and a definition? What are header guards?",
        "expected_answer": "A declaration introduces a name and its type; a definition also allocates storage or supplies the body. A name may be declared many times but defined only once (the One Definition Rule). Header guards ( #ifndef / #define or #pragma once ) stop a header from being included more than once in a translation unit, which would cause redefinition errors.",
        "companies": [
            "Zoho",
            "Oracle",
            "Amazon",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are the storage classes in C++?",
        "expected_answer": "auto (automatic storage, and since C++11 it means type deduction instead), register (removed in C++17), static , extern (declares a variable defined in another translation unit), mutable (a member that may change even in a const object) and thread_local (one copy per thread). Storage duration can be automatic, static, dynamic or thread.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "How does exception handling work in C++?",
        "expected_answer": "Code that may fail is placed in a try block, errors are signalled with throw , and catch blocks handle them by type. When an exception is thrown, the stack is unwound: destructors of fully constructed local objects run, which is why RAII is exception safe. Catch by const reference, order catch blocks from specific to general, and never let exceptions escape a destructor. Some domains (embedded, games, low latency) disable exceptions entirely and use error codes.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Microsoft",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How do virtual functions work internally (vtable and vptr)?",
        "expected_answer": "For each class with virtual functions the compiler builds a vtable: a table of pointers to the class's virtual function implementations. Each object stores a hidden vptr pointing to its class's vtable (set during construction). A virtual call loads the vptr, indexes the table and jumps, so it costs one extra indirection and usually prevents inlining. Consequences: objects of polymorphic classes are larger by a pointer, and virtual calls inside constructors and destructors resolve to the class currently being built or destroyed, not to the derived override.",
        "companies": [
            "Microsoft",
            "Amazon",
            "Oracle",
            "Goldman Sachs",
            "Zoho"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are pure virtual functions and abstract classes? Why do base classes need virtual destructors?",
        "expected_answer": "A pure virtual function ( = 0 ) has no required implementation in the base class, which makes the class abstract: it cannot be instantiated and defines an interface (a pure virtual function may still have a body). If you delete a derived object through a base pointer and the base destructor is not virtual, the behavior is undefined: usually only the base destructor runs and the derived part leaks. Rule: a class meant to be a polymorphic base gets a public virtual destructor (or a protected non-virtual one if it is never deleted through the base).",
        "companies": [
            "Microsoft",
            "Oracle",
            "Amazon",
            "Zoho",
            "Flipkart"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are the Rule of Three, Rule of Five and Rule of Zero?",
        "expected_answer": "If a class needs a custom destructor, copy constructor or copy assignment operator (because it owns a resource), it almost certainly needs all three: the Rule of Three. With C++11 add the move constructor and move assignment: the Rule of Five. The Rule of Zero says to design classes so that none of these are needed, by holding resources in members that already manage themselves ( std::vector , std::string , smart pointers). Prefer the Rule of Zero.",
        "companies": [
            "Google",
            "Microsoft",
            "Goldman Sachs",
            "Amazon",
            "Oracle"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Explain unique_ptr , shared_ptr and weak_ptr .",
        "expected_answer": "unique_ptr : sole ownership, no copy, movable, zero overhead over a raw pointer. The default choice. shared_ptr : shared ownership using a reference count; the object is destroyed when the last owner goes away. The control block makes it heavier, and cycles leak. weak_ptr : a non-owning observer of a shared_ptr object; it breaks cycles and can be converted with lock() only if the object is still alive. Prefer make_unique / make_shared . auto_ptr was removed in C++17.",
        "companies": [
            "Microsoft",
            "Google",
            "Amazon",
            "Goldman Sachs",
            "Meta"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is RAII and why is it central to C++?",
        "expected_answer": "Resource Acquisition Is Initialization ties a resource's lifetime (memory, file, lock, socket, transaction) to an object's lifetime: acquire in the constructor and release in the destructor. Because destructors run on every exit path, including exceptions and early returns, resources are released automatically. Examples: smart pointers, std::lock_guard , std::fstream , containers. It replaces try/finally and manual cleanup.",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "Goldman Sachs",
            "Oracle"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are move semantics and rvalue references?",
        "expected_answer": "An rvalue reference ( T&& ) binds to temporaries. A move constructor/assignment steals the internals of an object that is about to die (pointer swap) instead of copying them, which makes returning and inserting large objects cheap. std::move does not move anything: it casts an object to an rvalue so a move operation can be selected. A moved- from object must stay valid but unspecified (safe to destroy or assign). Mark move operations noexcept so containers use them.",
        "companies": [
            "Google",
            "Meta",
            "Microsoft",
            "Goldman Sachs",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are templates? Explain specialization and common pitfalls.",
        "expected_answer": "Templates (function, class, variable, alias) provide compile-time generics: the compiler generates code for each distinct set of template arguments (instantiation). A full specialization gives a custom implementation for specific arguments; partial specialization (class templates only) does so for a family of arguments. Pitfalls: code bloat, long unreadable error messages (improved by C++20 concepts), definitions usually must live in headers, and a lot of work moves to compile time.",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "Goldman Sachs",
            "Oracle"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Compare the main STL containers and when to use each.",
        "expected_answer": "vector : contiguous, O(1) random access and amortized O(1) push back, cache friendly; the default choice. deque : fast insertion at both ends, not contiguous. list / forward_list : O(1) insertion given an iterator, but poor cache behavior and per-node overhead. map / set : ordered, balanced tree (usually red-black), O(log n). unordered_map / unordered_set : hash table, average O(1), no ordering, worst case O(n). array : fixed size on the stack. stack , queue , priority_queue are adaptors.",
        "companies": [
            "Amazon",
            "Goldman Sachs",
            "Flipkart",
            "Microsoft",
            "Zoho"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are iterators? When do iterators get invalidated?",
        "expected_answer": "Iterators generalize pointers so algorithms work on any container. Categories: input, output, forward, bidirectional, random access (and contiguous in C++20). Invalidation: inserting into a vector may reallocate and invalidate all iterators (otherwise those after the insertion point); erasing invalidates iterators at and after the erased element; list and map erase invalidates only the erased element; a rehash in unordered_map invalidates iterators (but not references to elements). Using an invalidated iterator is undefined behavior.",
        "companies": [
            "Amazon",
            "Microsoft",
            "Goldman Sachs",
            "Oracle"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are function objects (functors), lambdas and std::function ?",
        "expected_answer": "A functor is an object with operator() . A lambda (C++11) is a compiler generated unnamed functor that can capture variables by value or reference. std::function is a type-erased, copyable wrapper that can hold any callable with a given signature; it is flexible but can allocate and prevents some inlining, while a lambda used through a template parameter has no such overhead. Capturing by reference a local that outlives its scope causes dangling references.",
        "companies": [
            "Microsoft",
            "Amazon",
            "Google",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are the exception safety guarantees, and what does noexcept do?",
        "expected_answer": "No-throw: the operation never throws (destructors, swap, moves). Strong: if it throws, state is unchanged (commit or rollback). Basic: no leaks and invariants hold, but state may have changed. None: no guarantee. noexcept declares that a function does not throw (if it does, std::terminate is called) and lets the compiler optimize. Standard containers use move_if_noexcept , so a throwing move constructor forces copies on reallocation.",
        "companies": [
            "Google",
            "Microsoft",
            "Goldman Sachs",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Explain the four C++ casts and why to avoid C-style casts.",
        "expected_answer": "static_cast : well defined, compile-time checked conversions (numeric, up and down a hierarchy without checks). dynamic_cast : safe run-time downcast for polymorphic types (returns null for pointers or throws bad_cast for references); needs RTTI. const_cast : adds or removes const / volatile ; modifying a truly const object is undefined behavior. reinterpret_cast : reinterprets bits between unrelated types; highly unsafe. A C-style cast can silently pick any of these, so it hides mistakes and is hard to search for.",
        "companies": [
            "Microsoft",
            "Oracle",
            "Amazon",
            "Zoho",
            "Flipkart"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is object slicing?",
        "expected_answer": "When a derived object is copied into a base object (by value), the derived part is cut off and virtual behavior is lost, because only the base subobject is copied. It happens with pass by value, storing derived objects in a vector<Base> or assigning to a base variable. Avoid it by using pointers, references or smart pointers to the base, and by making polymorphic base classes non-copyable.",
        "companies": [
            "Microsoft",
            "Oracle",
            "Zoho",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is multiple inheritance? What is the diamond problem and virtual inheritance?",
        "expected_answer": "A class may derive from more than one base. In the diamond (B and C both derive from A, D derives from B and C), D contains two copies of A, causing ambiguity and duplicated state. Virtual inheritance ( class B : virtual public A ) makes the most derived class hold a single shared A subobject, at the cost of extra indirection and the rule that the most derived class constructs the virtual base. Many designs avoid it by using interfaces (pure abstract classes) for multiple inheritance.",
        "companies": [
            "Zoho",
            "Oracle",
            "Microsoft",
            "Flipkart",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is a constructor initializer list? Why does it matter and what is the initialization order?",
        "expected_answer": "The initializer list initializes members directly instead of default constructing then assigning. It is required for const members, reference members, members and bases without default constructors. Members are initialized in the order they are declared in the class, not the order in the list; relying on a different order is a classic bug. Base classes are initialized before members.",
        "companies": [
            "Zoho",
            "Oracle",
            "Microsoft",
            "Amazon",
            "Flipkart"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What do explicit , mutable and volatile mean?",
        "expected_answer": "explicit on a constructor or conversion operator forbids implicit conversions. mutable lets a member change inside a const member function (for example a cache or a mutex). volatile tells the compiler a value may change outside the program's control (hardware registers), so every access must really happen; it does not provide atomicity or inter- thread synchronization in C++ (use std::atomic ).",
        "companies": [
            "Zoho",
            "Oracle",
            "Goldman Sachs",
            "Microsoft"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Which C++11 features changed everyday code (auto, range-for, nullptr, enum class and others)?",
        "expected_answer": "auto and decltype (type deduction), range-based for , nullptr (a typed null that replaces NULL ), enum class (scoped, strongly typed enums), override and final , = default / = delete , initializer lists and uniform brace initialization, lambdas, move semantics, smart pointers, constexpr , variadic templates, static_assert , std::thread and the memory model. Later standards added structured bindings, optional , variant , string_view (C++17), concepts, ranges, coroutines and std::span (C++20).",
        "companies": [
            "Microsoft",
            "Google",
            "Amazon",
            "Goldman Sachs",
            "Flipkart"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are memory leaks, dangling pointers and wild pointers? How do you detect them?",
        "expected_answer": "A leak is allocated memory that is never freed (often on an exception path or forgotten delete ). A dangling pointer refers to memory that has been freed or gone out of scope. A wild pointer was never initialized. Prevention: RAII, smart pointers and containers, no raw owning pointers, initialize everything. Detection: AddressSanitizer, LeakSanitizer, Valgrind, static analyzers (clang-tidy), and debug heaps on Windows.",
        "companies": [
            "Oracle",
            "Goldman Sachs",
            "Amazon",
            "Microsoft",
            "Zoho"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are the basics of multithreading in C++11 ( thread , mutex , condition_variable )? What are data races and deadlocks?",
        "expected_answer": "std::thread runs a callable on a new thread and must be join ed or detach ed. std::mutex provides mutual exclusion and should be locked through RAII wrappers ( lock_guard , unique_lock , scoped_lock ). condition_variable lets threads wait for a condition (always check it in a loop or with a predicate because of spurious wakeups). A data race (unsynchronized concurrent access where one is a write) is undefined behavior; a deadlock is threads waiting on each other's locks, prevented by consistent lock ordering or scoped_lock .",
        "companies": [
            "Goldman Sachs",
            "Google",
            "Amazon",
            "Microsoft",
            "Meta"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are copy elision and return value optimization? How do you choose between pass by value, reference and pointer?",
        "expected_answer": "Copy elision lets the compiler construct a result directly in its final location, skipping copies and moves; in C++17 it is guaranteed when returning a prvalue (a temporary), and named return value optimization (NRVO) remains optional. So do not write return std::move(local) , which can prevent it. Parameter guidelines: cheap types (ints, small structs) by value; large read-only objects by const& ; objects you will copy anyway by value then move; output or optional objects by reference or pointer; ownership transfer by unique_ptr by value.",
        "companies": [
            "Google",
            "Microsoft",
            "Goldman Sachs",
            "Amazon",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How are objects laid out in memory? Explain alignment, padding, sizeof and the empty base optimization.",
        "expected_answer": "Non-static data members are stored in declaration order within an access level, and each type has an alignment requirement, so the compiler inserts padding (reordering members from largest to smallest can shrink a struct). A polymorphic object also carries a vptr (usually first). With multiple inheritance, an object holds several base subobjects, and pointer conversions to a base may adjust the address. An empty class still has sizeof of at least 1 so distinct objects have distinct addresses, but an empty base can occupy no space (empty base optimization, and [[no_unique_address]] in C++20 for members). Layout matters for cache behavior, serialization and interop with C.",
        "companies": [
            "Google",
            "Goldman Sachs",
            "Meta",
            "Microsoft",
            "Oracle"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain the C++ memory model, std::atomic and memory orders.",
        "expected_answer": "Since C++11 the language defines how threads see each other's writes. A data race on a non-atomic object is undefined behavior. std::atomic<T> gives atomic operations with a chosen memory_order : seq_cst (default, a single total order, easiest to reason about), acquire / release (a release store makes earlier writes visible to a thread whose acquire load reads that value, forming a synchronizes-with edge), and relaxed (atomicity only, no ordering, fine for counters). Compilers and CPUs reorder instructions, so correctness depends on happens-before relationships, not on timing. Start with seq_cst and relax only with proof and measurement.",
        "companies": [
            "Google",
            "Goldman Sachs",
            "Meta",
            "Amazon",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What are forwarding references and perfect forwarding? What is reference collapsing?",
        "expected_answer": "In a deduced context such as template<class T> void f(T&& x) , T&& is a forwarding (universal) reference: it binds to both lvalues and rvalues, and T is deduced as U& for lvalues and U for rvalues. Reference collapsing rules ( & & becomes & , & && becomes & , && & becomes & , && && becomes && ) make this work. std::forward<T>(x) then restores the original value category, so wrappers (such as make_unique , emplace_back ) pass arguments to constructors with no extra copies. Common mistake: using std::move on a forwarding reference, which steals from lvalues.",
        "companies": [
            "Google",
            "Meta",
            "Microsoft",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What is SFINAE? How do constexpr , if constexpr and C++20 concepts improve template programming?",
        "expected_answer": "SFINAE (substitution failure is not an error) removes a template from overload resolution when substituting its arguments produces an invalid type, which enabled techniques like enable_if and traits but produced unreadable code and errors. constexpr functions can be evaluated at compile time; if constexpr (C++17) discards branches at compile time, replacing many SFINAE tricks; concepts (C++20) state requirements on template parameters directly ( requires ), giving clearer constraints, overloads and error messages. consteval and constinit strengthen compile-time guarantees.",
        "companies": [
            "Google",
            "Meta",
            "Microsoft",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What are the pitfalls of move semantics?",
        "expected_answer": "A moved-from object is valid but unspecified; use only assignment, destruction or reset on it. A move constructor that is not noexcept is not used by vector growth (the strong guarantee requires copies), silently costing performance. Returning std::move(local) blocks copy elision and can be slower. Moving from const objects falls back to a copy. Declaring a destructor or copy operations suppresses the implicit move operations (the Rule of Five). Moving a std::string or vector is cheap, but moving a std::array of large objects still copies elements.",
        "companies": [
            "Google",
            "Meta",
            "Goldman Sachs",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What is undefined behavior? Give examples and explain why compilers exploit it.",
        "expected_answer": "Undefined behavior (UB) means the standard places no requirements on the program: it may crash, appear to work or be optimized into something surprising. Examples: signed integer overflow, out of bounds access, dereferencing null or dangling pointers, use after free, data races, modifying a const object, violating the strict aliasing rule, unsequenced modifications of one variable, and reading an uninitialized variable. Compilers assume UB never happens, which lets them remove checks and reorder code (for example deleting a null check that comes after a dereference). Defense: sanitizers (UBSan, ASan, TSan), warnings, static analysis, safe types and code review. This is different from unspecified behavior (valid choices, such as argument evaluation order) and implementation defined behavior (documented, such as the size of int ).",
        "companies": [
            "Google",
            "Meta",
            "Goldman Sachs",
            "Microsoft",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How does exception handling work internally? What are its costs and failure modes?",
        "expected_answer": "Mainstream compilers use the table-driven (zero-cost) model: no runtime cost when no exception is thrown (apart from larger binaries), while a throw is slow because the runtime looks up unwind tables and walks the stack, running destructors (stack unwinding). Failure modes: throwing from a destructor during unwinding calls std::terminate ; an exception escaping a noexcept function terminates; throwing from a constructor skips that object's destructor (but destroys already built members and bases); uncaught exceptions terminate. That is why low latency and embedded code often compiles with exceptions off and uses error codes, std::expected (C++23) or similar types.",
        "companies": [
            "Microsoft",
            "Google",
            "Goldman Sachs",
            "Oracle"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How does std::shared_ptr work internally? What is make_shared and enable_shared_from_this ?",
        "expected_answer": "A shared_ptr holds two pointers: one to the object and one to a control block containing the strong count, weak count, deleter and allocator. Count updates are atomic, so copying a shared_ptr is thread safe but the pointed-to object is not. make_shared allocates the object and control block in one allocation (faster, more cache friendly) but the memory is not freed until the last weak_ptr is gone. Creating two shared_ptr s from the same raw pointer gives two control blocks and a double delete. enable_shared_from_this lets an object safely obtain a shared_ptr to itself. Cycles of shared owners leak and are broken with weak_ptr .",
        "companies": [
            "Microsoft",
            "Google",
            "Amazon",
            "Goldman Sachs",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What are custom allocators, placement new and memory pools? When are they worth it?",
        "expected_answer": "Placement new constructs an object in memory you already own ( new (ptr) T ), and you must call the destructor manually. Allocators let containers obtain memory from a custom source; C++17 std::pmr (polymorphic memory resources) makes this easier. Memory pools and arenas hand out fixed size or bump pointer allocations, removing the per allocation locking and fragmentation of general purpose malloc , which is valuable in latency sensitive systems (trading, games, real time). Costs: complexity, lifetime bugs and the loss of tooling support unless planned carefully.",
        "companies": [
            "Goldman Sachs",
            "Google",
            "Meta",
            "Amazon",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain name lookup, argument-dependent lookup (ADL) and two-phase lookup in templates.",
        "expected_answer": "ADL (Koenig lookup): when calling an unqualified function, the compiler also searches the namespaces of the argument types, which is why operator<< and swap for user types are found without qualification (hence the \"using std::swap then call swap\" idiom). Overload resolution then picks the best viable candidate by conversion ranks, with non- template functions preferred over templates when equal. Two-phase lookup: in a template, non-dependent names are resolved at definition time, dependent names at instantiation time, which is why members of a dependent base class need this-> or a using declaration.",
        "companies": [
            "Google",
            "Microsoft",
            "Meta",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Compare virtual dispatch, CRTP and type erasure for polymorphism.",
        "expected_answer": "Virtual functions: open set of types at run time, one indirect call, objects hold a vptr, hard to inline. CRTP (static polymorphism): a base template parameterized by the derived class calls derived functions without virtual overhead; resolved at compile time, inlinable, but each instantiation is a distinct type and the set of types is closed at compile time. Type erasure ( std::function , std::any , custom): value semantics with a runtime interface, hiding the concrete type behind a small virtual interface or function pointers; flexible but may allocate. Compilers can also devirtualize calls when the dynamic type is known (final classes, LTO).",
        "companies": [
            "Google",
            "Goldman Sachs",
            "Meta",
            "Microsoft",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain the One Definition Rule, linkage, name mangling, extern \"C\" and the static initialization order fiasco.",
        "expected_answer": "The ODR says every entity may be defined only once in the program (templates, inline functions and classes may be defined in multiple translation units if the definitions are identical); violations are undefined and often unnoticed. Internal linkage (static, anonymous namespaces) keeps names private to a file; external linkage shares them. Name mangling encodes namespaces, types and overloads into symbol names, so C++ libraries are tied to compiler and ABI; extern \"C\" disables mangling for C interop. The static initialization order fiasco is the unspecified order of dynamic initialization of globals across translation units, causing use of an unconstructed object; fix with function local statics (initialized on first use, thread safe since C++11) or constinit .",
        "companies": [
            "Microsoft",
            "Google",
            "Oracle",
            "Goldman Sachs",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do CPU caches, false sharing and branch prediction affect C++ performance?",
        "expected_answer": "Memory access dominates performance in many programs. Contiguous containers ( vector ) beat pointer chasing structures ( list , map ) because of spatial locality and hardware prefetching. Data-oriented design (struct of arrays, small hot structures) improves cache use. False sharing occurs when threads write independent variables that share a cache line (typically 64 bytes), forcing the line to bounce between cores; fix with padding or alignment ( alignas , std::hardware_destructive_interference_size ). Branch mispredictions cost around a dozen cycles; predictable branches and branch free code help. Always profile (perf, VTune, flame graphs) before optimizing.",
        "companies": [
            "Goldman Sachs",
            "Google",
            "Meta",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What is lock-free programming? What is the ABA problem, and when should you prefer mutexes?",
        "expected_answer": "Lock-free algorithms use atomic operations (compare and swap) so that some thread always makes progress, avoiding blocking, priority inversion and deadlock; wait-free is the stronger guarantee that every thread finishes in bounded steps. Hard parts: memory ordering, safe memory reclamation (hazard pointers, epoch based schemes) and the ABA problem (a value changes A to B and back to A so a compare and swap wrongly succeeds; use tagged pointers or version counters). Lock-free code is complex, easy to get wrong and not always faster; use mutexes by default, and use lock-free queues or counters only where profiling shows contention matters. A spinlock suits very short critical sections on dedicated cores.",
        "companies": [
            "Goldman Sachs",
            "Google",
            "Meta",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What are C++20 coroutines, ranges and modules?",
        "expected_answer": "Coroutines are functions that can suspend and resume ( co_await , co_yield , co_return ); the compiler turns them into a state machine, usually heap allocated, and libraries supply the promise types. They simplify async I/O and generators. Ranges provide composable, lazy views and pipelines over sequences with constrained algorithms. Modules replace textual #include with compiled interfaces ( import ), improving build time and isolation, although tooling support is still maturing. C++23 adds std::expected , std::print , std::mdspan and more.",
        "companies": [
            "Google",
            "Microsoft",
            "Meta",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do std::async , future and promise work? How is a thread pool designed, and what does thread_local do?",
        "expected_answer": "std::promise is the writing end of a shared state and std::future the reading end; std::async runs a callable, possibly on a new thread (launch policy matters, and a discarded future of an async task blocks in its destructor). A thread pool keeps a fixed number of workers pulling tasks from a synchronized queue, avoiding thread creation cost and oversubscription; design questions include queue type, work stealing, shutdown, exception propagation and back pressure. thread_local gives each thread its own copy of a variable, useful for caches and per-thread state but with initialization and destruction costs.",
        "companies": [
            "Amazon",
            "Goldman Sachs",
            "Google",
            "Microsoft",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain value categories (lvalue, prvalue, xvalue) and guaranteed copy elision in C++17.",
        "expected_answer": "Every expression has a type and a value category. An lvalue has an identity (a name, can be addressed); a prvalue is a pure temporary value (a literal, a function returning by value); an xvalue (expiring value) has identity but may be moved from (the result of std::move ); glvalue = lvalue or xvalue; rvalue = prvalue or xvalue. In C++17 a prvalue no longer creates a temporary: it initializes its destination directly, so returning or passing a temporary involves no copy or move (even for types that are not movable).",
        "companies": [
            "Google",
            "Meta",
            "Goldman Sachs",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What is the PIMPL idiom? What are its pros and cons compared with abstract interfaces?",
        "expected_answer": "PIMPL (pointer to implementation) puts a class's private details in a separate class held through a pointer (usually unique_ptr ) so the header exposes only a stable interface. Pros: faster builds (fewer header dependencies), a stable ABI across versions and hidden implementation. Cons: an extra allocation and indirection per object, boilerplate (the destructor must be defined where the implementation type is complete) and harder const correctness. Alternative: abstract interface plus factory (adds virtual dispatch but allows multiple implementations).",
        "companies": [
            "Microsoft",
            "Oracle",
            "Google",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What is exception-safe class design? Explain the copy-and-swap idiom and the strong guarantee.",
        "expected_answer": "The goal is that operations leave objects valid even when something throws. Use RAII members so partial construction cleans itself up, perform fallible work first and commit changes with non-throwing operations. Copy-and-swap implements assignment by taking the argument by value (copying, which may throw, before any state changes) and then swapping with a noexcept swap , giving the strong guarantee and self-assignment safety for free. Trade-off: it can be slower than a hand tuned assignment, and with move semantics it also provides move assignment from the same function.",
        "companies": [
            "Google",
            "Microsoft",
            "Goldman Sachs",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do compiler optimization, link time optimization, static and dynamic linking and sanitizers affect a C++ build?",
        "expected_answer": "Optimization levels ( -O0 for debugging, -O2 or -O3 for release) enable inlining, loop transformations and vectorization; LTO optimizes across translation units; PGO uses profile data to guide layout and inlining. Static linking bundles libraries into the binary (simple deployment, larger size, no shared updates); dynamic linking shares libraries at run time (smaller binaries, ABI compatibility and loader issues). Sanitizers (ASan, UBSan, TSan, MSan) instrument code to detect memory errors, undefined behavior and races at run time, and should run in CI. Debug info, symbol visibility and reproducible builds matter for large codebases. Hard level, interviewers mostly probe judgment: when you would use a feature, what it costs and how you would verify it with a tool.",
        "companies": [
            "Google",
            "Microsoft",
            "Goldman Sachs",
            "Amazon",
            "Oracle"
        ]
    }
]


def validate_questions() -> None:
    expected_counts = {"EASY": 20, "MEDIUM": 20, "HARD": 20}
    actual_counts = Counter(item["difficulty"] for item in QUESTIONS)

    if len(QUESTIONS) != 60:
        raise ValueError(f"Expected 60 C++ questions; found {len(QUESTIONS)}.")

    for difficulty, expected_count in expected_counts.items():
        actual_count = actual_counts.get(difficulty, 0)
        if actual_count != expected_count:
            raise ValueError(
                f"Expected {expected_count} {difficulty} questions; found {actual_count}."
            )

    for index, item in enumerate(QUESTIONS, start=1):
        if not item["question_text"].strip() or not item["expected_answer"].strip():
            raise ValueError(f"Question {index} has an empty question or expected answer.")
        if not isinstance(item["companies"], list):
            raise ValueError(f"Question {index} has invalid company tags.")


def seed_cpp_questions() -> None:
    """Insert the 60 C++ theory questions into the existing C++ topic."""
    validate_questions()
    db = SessionLocal()

    try:
        topic = db.query(Topic).filter(Topic.name == TOPIC_NAME).first()

        if topic is None:
            raise RuntimeError(
                "The C++ topic does not exist. Create the C++ topic in the app/database first; "
                "this seeder will not create a duplicate topic."
            )

        if not topic.is_active:
            raise RuntimeError(
                f"The C++ topic (ID: {topic.id}) is inactive. Activate it first."
            )

        existing_count = (
            db.query(Question)
            .filter(Question.topic_id == topic.id)
            .count()
        )

        if existing_count > 0:
            print(
                f"C++ topic (ID: {topic.id}) already contains "
                f"{existing_count} question(s)."
            )
            print("No questions were inserted to avoid duplicates.")
            print("Inspect existing C++ questions before deciding whether to seed again.")
            return

        difficulty_map = {
            "EASY": QuestionDifficulty.EASY,
            "MEDIUM": QuestionDifficulty.MEDIUM,
            "HARD": QuestionDifficulty.HARD,
        }

        records = [
            Question(
                topic_id=topic.id,
                difficulty=difficulty_map[item["difficulty"]],
                question_text=item["question_text"],
                expected_answer=item["expected_answer"],
                companies=item["companies"],
            )
            for item in QUESTIONS
        ]

        db.add_all(records)
        db.commit()

        counts = Counter(item["difficulty"] for item in QUESTIONS)
        print("=" * 60)
        print("C++ THEORY QUESTION BANK CREATED")
        print("=" * 60)
        print(f"Topic ID        : {topic.id}")
        print(f"Topic           : {topic.name}")
        print(f"Total questions : {len(records)}")
        print(f"Easy            : {counts['EASY']}")
        print(f"Medium          : {counts['MEDIUM']}")
        print(f"Hard            : {counts['HARD']}")
        print("Company tags    : Stored in the companies JSON column")
        print("=" * 60)

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_cpp_questions()
