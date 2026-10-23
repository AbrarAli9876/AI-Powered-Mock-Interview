from __future__ import annotations

from collections import Counter

from app.database import SessionLocal
from app.enums.question_difficulty import QuestionDifficulty
from app.models.question import Question
from app.models.topic import Topic


TOPIC_NAME = "C#"

# Extracted from "C# Interview Questions by Difficulty (Easy, Medium, Hard).pdf".
# Company attributions follow the PDF and are not official company question banks.
QUESTIONS = [{'difficulty': 'EASY',
  'question_text': 'What is C#, and what are its key features?',
  'expected_answer': 'C# is a statically typed, object-oriented, type-safe language developed by Microsoft '
                     'that compiles to Intermediate Language (IL) and runs on the .NET runtime. Its key '
                     'features are strong typing, automatic garbage collection, generics, LINQ, properties, '
                     'delegates and events, async/await, pattern matching and records. Because the compiler '
                     'checks types before the program runs, many errors are caught early.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop', 'Taksh IT Solutions', 'Zoho']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between value types and reference types?',
  'expected_answer': 'A value type (int, double, bool, char, struct, enum) stores its data directly, usually '
                     'on the stack or inline inside its container, and assignment copies the value. A '
                     'reference type (class, interface, delegate, array, string, object) stores a reference '
                     'to an object on the managed heap, and assignment copies the reference, so two '
                     'variables can point to the same object and a change through one is visible through the '
                     'other.',
  'companies': ['Microsoft', 'Zoho', 'Goldman Sachs', 'Amazon', 'Google']},
 {'difficulty': 'EASY',
  'question_text': 'What are boxing and unboxing?',
  'expected_answer': 'Boxing converts a value type to object (or an interface) by allocating an object on '
                     'the heap and copying the value into it. Unboxing extracts the value back with an '
                     'explicit cast. Both cost an allocation plus a type check and add garbage-collection '
                     'pressure, so generic collections such as List<int> are preferred over ArrayList. C# '
                     '',
  'companies': ['Microsoft', 'Zoho', 'AllianceTek', 'SynergyTop']},
 {'difficulty': 'EASY',
  'question_text': 'What are the four pillars of object-oriented programming?',
  'expected_answer': 'Encapsulation hides state behind members with access modifiers. Abstraction exposes '
                     'what an object does through abstract classes and interfaces. Inheritance lets a '
                     'derived class reuse and extend a base class. Polymorphism lets one call behave '
                     'differently by type: overloading is resolved at compile time, overriding with virtual '
                     'and override at runtime.',
  'companies': ['Microsoft', 'Zoho', 'Goldman Sachs', 'Oracle', 'Flipkart', 'Amazon', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between class and struct?',
  'expected_answer': 'A class is a reference type with inheritance and a default value of null. A struct is '
                     'a value type copied on assignment, cannot inherit from another struct or class (it can '
                     'implement interfaces), and suits small, immutable data. Large structs are costly to '
                     'copy, so use classes for bigger objects.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between const and readonly?',
  'expected_answer': 'const is a compile-time constant, implicitly static, and its value is baked into the '
                     'calling assembly. readonly is assigned at declaration or in a constructor, so it can '
                     'differ per instance and is read at runtime. Use const only for values that truly never '
                     'change, such as mathematical constants.',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions', 'Zoho']},
 {'difficulty': 'EASY',
  'question_text': 'Why is string immutable, and when should you use StringBuilder?',
  'expected_answer': 'Once created, a string cannot be changed; every modification creates a new string. '
                     'This makes strings thread-safe and safe to use as dictionary keys, and it allows '
                     'string interning. Repeated concatenation in a loop creates many temporary strings, so '
                     'use StringBuilder, which edits a mutable buffer.',
  'companies': ['AllianceTek', 'Taksh IT Solutions', 'Zoho', 'Goldman Sachs']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between an abstract class and an interface?',
  'expected_answer': 'An abstract class can hold '
                     'fields, constructors, state and implemented methods, and a class can inherit only one. '
                     'An interface defines a contract; since C# 8 it may have default implementations but no '
                     'instance state, and a class can implement many interfaces. Use an abstract class for '
                     'shared base behavior and an interface for a capability that unrelated types can share.',
  'companies': ['Microsoft', 'Oracle', 'Amazon', 'AllianceTek', 'Taksh IT Solutions', 'Flipkart']},
 {'difficulty': 'EASY',
  'question_text': 'What is method overloading, and how does it differ from overriding?',
  'expected_answer': 'Overloading means several methods with the same name but different parameter lists in '
                     'the same type, chosen at compile time. Overriding means a derived class replaces a '
                     'virtual or abstract base method with the same signature, chosen at runtime based on '
                     "the object's actual type.",
  'companies': ['Goldman Sachs', 'Zoho', 'Oracle', 'Microsoft']},
 {'difficulty': 'EASY',
  'question_text': 'What are the access modifiers in C#?',
  'expected_answer': 'public (anywhere), private (same type only), protected (same type and derived types), '
                     'internal (same assembly), protected internal (same assembly or derived types) and '
                     'private protected (derived types in the same assembly). The default for class members '
                     'is private, and for top-level types it is internal.',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between Array, List<T> and ArrayList?',
  'expected_answer': 'An array has a fixed size and is the fastest for indexed access. List<T> is a '
                     'resizable, strongly typed collection built on an array. ArrayList is non-generic, '
                     'stores object, and needs casts and boxing for value types, so it is considered '
                     'obsolete.',
  'companies': ['Zoho', 'AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What are the var and dynamic keywords?',
  'expected_answer': 'var asks the compiler to infer the type from the right-hand side at compile time; the '
                     'type is then fixed. dynamic skips compile-time type checking and resolves members at '
                     'runtime, so mistakes appear only when the code runs. Prefer var for readability and '
                     'avoid dynamic unless interoperating with dynamic sources. C# Interview Questions by '
                     '',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between == and .Equals()?',
  'expected_answer': '== is an operator that can be overloaded; for reference types it compares references '
                     'by default, but string overloads it to compare content. .Equals() is a virtual method '
                     'that compares according to what the type defines, such as value equality for structs. '
                     'ReferenceEquals always checks whether two references point to the same object.',
  'companies': ['Microsoft', 'Zoho', 'Goldman Sachs', 'AllianceTek']},
 {'difficulty': 'EASY',
  'question_text': 'What is exception handling, and how do try, catch and finally work?',
  'expected_answer': 'Code that might fail goes in try. If an exception is thrown, control moves to the '
                     'first matching catch block, so specific exceptions should come before general ones. '
                     'finally always runs afterward, even on return or exception, and is used to release '
                     'resources.',
  'companies': ['Goldman Sachs', 'AllianceTek', 'SynergyTop', 'Taksh IT Solutions', 'Oracle']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between throw and throw ex?',
  'expected_answer': 'throw; rethrows the current exception and preserves the original stack trace. throw '
                     'ex; rethrows the same object but resets the stack trace to the current line, hiding '
                     'where the error began. Use throw; inside a catch block unless you are wrapping the '
                     'exception in a new one.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop']},
 {'difficulty': 'EASY',
  'question_text': 'What are properties, and how do they differ from fields?',
  'expected_answer': 'A property exposes a field through get and set accessors, allowing validation, lazy '
                     'loading, change notification and different access levels for reading and writing. '
                     'Auto- properties (public int Age { get; set; }) generate a hidden backing field. '
                     'Fields should normally be private, with properties as the public surface.',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What is a constructor, and what is a static constructor?',
  'expected_answer': 'A constructor is a special method that runs when an object is created and initializes '
                     'its state; it can be overloaded and chained with this(...) or base(...). A static '
                     'constructor runs once, automatically, before the first instance is created or any '
                     'static member is used, takes no parameters and has no access modifier. C# Interview '
                     'Questions by ',
  'companies': ['Microsoft', 'Zoho', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What are static members?',
  'expected_answer': 'Static members belong to the type itself rather than to an instance, so they are '
                     'shared by all instances and accessed through the type name. Static classes cannot be '
                     'instantiated and are used for utilities and extension methods. Mutable static state is '
                     'shared across threads, so it needs care.',
  'companies': ['AllianceTek', 'Taksh IT Solutions', 'Zoho']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between Convert.ToInt32, int.Parse and int.TryParse?',
  'expected_answer': 'int.Parse throws on null or invalid text. Convert.ToInt32 returns 0 for null but still '
                     'throws on invalid text. int.TryParse returns a bool and an out value without throwing, '
                     'so it is the right choice for untrusted input and avoids the cost of exceptions.',
  'companies': ['Zoho', 'AllianceTek', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What are nullable value types and the ?? operator?',
  'expected_answer': 'int? is shorthand for Nullable<int> and lets a value type hold null, useful for '
                     'optional database columns. The null-coalescing operator ?? returns the right operand '
                     'when the left is null, ??= assigns only when the variable is null, and ?. safely '
                     'accesses a member only when the object is not null.',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'EASY',
  'question_text': 'What is garbage collection in .NET?',
  'expected_answer': 'Garbage collection automatically reclaims memory used by managed objects that are no '
                     'longer reachable from any root such as stack variables or static fields. Developers do '
                     'not free memory manually. The GC works in generations (0, 1, 2) so that short-lived '
                     'objects are cleaned up cheaply and often.',
  'companies': ['Microsoft', 'Oracle', 'Amazon', 'Goldman Sachs']},
 {'difficulty': 'EASY',
  'question_text': 'What is LINQ?',
  'expected_answer': 'Language Integrated Query provides one consistent syntax for querying in-memory '
                     'collections, databases (through Entity Framework) and XML. It offers query syntax and '
                     'method syntax, which compile to the same calls, and most operators use deferred C# '
                     ' execution, meaning the query runs '
                     'only when you enumerate the result.',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions', 'Microsoft']},
 {'difficulty': 'MEDIUM',
  'question_text': 'Explain generics and constraints in C#. What problems do they solve?',
  'expected_answer': 'Generics let you write classes and methods with a type parameter, such as List<T>, '
                     'giving compile-time type safety, no casts, no boxing for value types and code reuse '
                     'across types. Constraints restrict what T can be: where T : class (reference type), '
                     'struct (value type), new() (parameterless constructor), a base class, or an interface '
                     'such as IComparable<T>. Constraints let the generic code safely call members of T.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop', 'Google']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are covariance and contravariance?',
  'expected_answer': 'Variance describes how generic type assignment follows the inheritance of type '
                     'arguments. Covariance (out) lets a generic interface or delegate that only returns T '
                     'be assigned to a version with a base type, for example IEnumerable<string> to '
                     'IEnumerable<object>. Contravariance (in) lets one that only consumes T accept a less '
                     'derived type, for example Action<object> to Action<string>. It works only for '
                     'interfaces and delegates with reference types.',
  'companies': ['Microsoft', 'Google']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does Dictionary<TKey, TValue> work internally?',
  'expected_answer': "It is a hash table. The key's GetHashCode() selects a bucket, and Equals() resolves "
                     'collisions by comparing keys within the bucket (chaining). Lookups, inserts and '
                     'removals are O(1) on average and O(n) in the worst case when many keys collide. Keys '
                     'must have a stable hash code, so mutating a key after insertion breaks lookups. The '
                     'table resizes when it becomes too full.',
  'companies': ['Zoho', 'Goldman Sachs', 'Google', 'Meta', 'Amazon']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is the difference between IEnumerable<T>, ICollection<T>, IList<T> and '
                   'IQueryable<T>?',
  'expected_answer': 'IEnumerable<T> supports '
                     'forward-only iteration. ICollection<T> adds Count, Add and Remove. IList<T> adds index '
                     'access and insertion at a position. IQueryable<T> builds an expression tree that a '
                     'provider such as Entity Framework translates into another language like SQL, so '
                     'filtering runs at the data source instead of in memory. Returning IEnumerable after '
                     'ToList() runs in memory; staying on IQueryable keeps the query composable.',
  'companies': ['AllianceTek', 'SynergyTop', 'Microsoft', 'Taksh IT Solutions']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is deferred execution in LINQ, and what are its consequences?',
  'expected_answer': 'Operators like Where and Select only build a query; it runs when you enumerate it '
                     '(foreach, ToList, Count, First). Consequences: the query sees data changes made before '
                     'enumeration, enumerating twice runs it twice (possibly hitting the database twice), '
                     'and exceptions appear at enumeration time. Call ToList() or ToArray() to run it once '
                     'and cache the results.',
  'companies': ['AllianceTek', 'SynergyTop', 'Microsoft']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is the difference between Select and SelectMany, and between First, FirstOrDefault, '
                   'Single and SingleOrDefault?',
  'expected_answer': 'Select projects each item to one result; SelectMany flattens nested sequences into '
                     'one. First throws if the sequence is empty; FirstOrDefault returns the default value '
                     'instead. Single throws unless exactly one item matches, which also guards against '
                     'unexpected duplicates; SingleOrDefault allows zero but still throws on more than one.',
  'companies': ['AllianceTek', 'SynergyTop', 'Taksh IT Solutions']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are delegates, Func, Action and Predicate?',
  'expected_answer': 'A delegate is a type-safe reference to a method with a specific signature. Action<...> '
                     'is a built-in delegate returning void, Func<..., TResult> returns a value, and '
                     'Predicate<T> returns bool. Delegates can be multicast (invoking several methods in '
                     'order) and are the basis of events, callbacks and LINQ.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How do events differ from delegates?',
  'expected_answer': 'An event wraps a delegate so '
                     'outside code can only subscribe (+=) or unsubscribe (-=); it cannot invoke the event '
                     'or replace the subscriber list, and only the declaring class can raise it. This '
                     'protects the publisher in the publisher-subscriber pattern. Forgetting to unsubscribe '
                     'long-lived publisher events is a common memory leak.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are lambda expressions and closures?',
  'expected_answer': 'A lambda is a concise anonymous function (x => x * 2) that can convert to a delegate '
                     'or an expression tree. A closure occurs when a lambda captures variables from its '
                     'enclosing scope; the compiler moves those variables into a generated class so they '
                     'live as long as the lambda does. Capturing loop variables or large objects '
                     'unintentionally can cause bugs or leaks.',
  'companies': ['Microsoft', 'AllianceTek', 'Google']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does async/ await work?',
  'expected_answer': 'The compiler turns an async method into a state machine. At an await on an incomplete '
                     'task, the method returns control to its caller and registers a continuation; when the '
                     'task completes, execution resumes, possibly on the captured synchronization context. '
                     'No thread is blocked while waiting for I/O, which lets a few threads serve many '
                     'requests.',
  'companies': ['Microsoft', 'AllianceTek', 'Ailoitte', 'Amazon', 'Google']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is the difference between asynchronous programming and multithreading?',
  'expected_answer': 'Asynchronous code releases the thread while waiting (best for I/O-bound work), so one '
                     'thread can serve many operations. Multithreading runs work on several threads at the '
                     'same time and suits CPU-bound work. async does not by itself create threads; Task.Run '
                     'is what offloads CPU work to the thread pool.',
  'companies': ['Microsoft', 'Amazon', 'Google', 'Akamai']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is a race condition, and how do you prevent it?',
  'expected_answer': 'A race condition occurs when correctness depends on the timing of concurrent access to '
                     'shared mutable state, for example two threads incrementing the same counter. Prevent '
                     'it with lock, Interlocked operations, immutable data, thread-safe collections such as '
                     'ConcurrentDictionary, or by avoiding shared state altogether. C# Interview Questions '
                     'by ',
  'companies': ['Microsoft', 'Goldman Sachs', 'Google', 'Meta', 'Amazon']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is IDisposable and the using statement?',
  'expected_answer': 'IDisposable.Dispose() releases unmanaged resources such as files, sockets and database '
                     'connections deterministically. The using statement (or using declaration) guarantees '
                     'Dispose is called even if an exception occurs. Relying on the garbage collector for '
                     'these resources is unreliable because collection timing is unpredictable.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop', 'Goldman Sachs']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are extension methods and when would you use them?',
  'expected_answer': 'An extension method is a static method in a static class whose first parameter is '
                     'marked this; it appears as an instance method on that type without modifying or '
                     'inheriting from it. LINQ is built on them. Use them to add helpers to types you do not '
                     'own; avoid overuse because they are resolved at compile time and can hide where '
                     'behavior lives.',
  'companies': ['AllianceTek', 'SynergyTop', 'Microsoft']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are records, and how do they differ from classes?',
  'expected_answer': 'Records (C# 9) provide value-based equality, a built-in ToString, with expressions for '
                     'non-destructive copies and concise positional syntax. A record is a reference type, '
                     'while a record struct is a value type. They suit immutable data models and DTOs; a '
                     'normal class compares by reference by default.',
  'companies': ['Microsoft', 'Ailoitte', 'SynergyTop']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is dependency injection and what are the service lifetimes in ASP.NET Core?',
  'expected_answer': "Dependency injection supplies a class's dependencies from outside, so code depends on "
                     'interfaces and is easy to test and swap. The built-in container has three lifetimes: '
                     'Transient (new instance every time), Scoped (one per HTTP request) and Singleton (one '
                     'for the whole application). A singleton must not depend on a scoped service, which is '
                     'called a captive dependency.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop', 'Ailoitte', 'Flipkart']},
 {'difficulty': 'MEDIUM',
  'question_text': 'Explain the ASP.NET Core request pipeline and middleware.',
  'expected_answer': 'A request passes through a '
                     'pipeline of middleware components in the order they are registered. Each can do work '
                     'before and after calling the next component and can short- circuit the pipeline. Order '
                     'matters: for example exception handling comes first, and authentication must run '
                     'before authorization. The pipeline ends at an endpoint such as a controller action.',
  'companies': ['Microsoft', 'AllianceTek', 'SynergyTop', 'Ailoitte']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are lazy, eager and explicit loading in Entity Framework Core?',
  'expected_answer': 'Eager loading fetches related data in the same query with Include. Lazy loading '
                     'fetches related data the first time a navigation property is accessed (it needs '
                     'proxies) and can cause the N+1 query problem. Explicit loading loads related data on '
                     'demand with Load(). Choose eager loading when you know you need the related data.',
  'companies': ['AllianceTek', 'SynergyTop', 'Flipkart', 'Amazon']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is change tracking in EF Core, and what does AsNoTracking do?',
  'expected_answer': 'The DbContext tracks entity states (Added, Modified, Deleted, Unchanged) so '
                     'SaveChanges can generate the right SQL. AsNoTracking turns tracking off for a query, '
                     'which makes read-only queries faster and lighter on memory. Do not use it for entities '
                     'you plan to update.',
  'companies': ['AllianceTek', 'SynergyTop', 'Ailoitte']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the common HTTP verbs and status codes in a REST API?',
  'expected_answer': 'GET reads (safe and idempotent), POST creates, PUT replaces (idempotent), PATCH '
                     'updates partially, DELETE removes (idempotent). Common status codes: 200 OK, 201 '
                     'Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not '
                     'Found, 409 Conflict and 500 Internal Server Error.',
  'companies': ['Flipkart', 'Ailoitte', 'Bytes Technolab', 'SynergyTop', 'Meta']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the SOLID principles?',
  'expected_answer': 'Single responsibility: a class has one reason to change. Open/closed: open for '
                     'extension, closed for modification. Liskov substitution: derived types must be usable '
                     'wherever the base type is expected. Interface segregation: prefer several small '
                     'interfaces to one large one. Dependency inversion: depend on abstractions, not '
                     'concrete classes. ',
  'companies': ['Microsoft', 'Flipkart', 'Amazon', 'Goldman Sachs']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the ACID properties, and what is the difference between a clustered and a '
                   'non-clustered index?',
  'expected_answer': 'ACID means Atomicity (all or nothing), Consistency (valid state to valid state), '
                     'Isolation (concurrent transactions do not interfere) and Durability (committed data '
                     'survives failure). A clustered index defines the physical order of rows, so a table '
                     'has only one. A non-clustered index is a separate structure holding keys and pointers '
                     'to rows, and a table can have many. Indexes speed up reads but slow writes and use '
                     'storage.',
  'companies': ['Microsoft', 'Goldman Sachs', 'Oracle', 'Zoho', 'AllianceTek']},
 {'difficulty': 'HARD',
  'question_text': 'Explain how the .NET garbage collector works in detail: generations, the Large Object '
                   'Heap, compaction and GC modes.',
  'expected_answer': 'The GC finds live objects by tracing from roots (stack variables, statics, CPU '
                     'registers, finalization queue), then reclaims everything unreachable. The heap has '
                     'three generations: Gen 0 holds new objects and is collected often and cheaply, '
                     'survivors move to Gen 1 and then Gen 2, which is collected rarely and costs the most. '
                     'Objects of about 85,000 bytes or more go to the Large Object Heap, which is collected '
                     'with Gen 2 and is not compacted by default, so repeated large allocations can fragment '
                     'it. After marking, the GC compacts survivors to remove gaps. Workstation GC favors '
                     'responsiveness for client apps; Server GC uses a heap and thread per core for '
                     'throughput; concurrent (background) GC runs Gen 2 marking alongside the application to '
                     'shorten pauses. Reduce pressure by allocating less, pooling buffers (ArrayPool<T>), '
                     'and avoiding large short-lived objects.',
  'companies': ['Microsoft', 'Goldman Sachs', 'Amazon', 'Oracle', 'Akamai']},
 {'difficulty': 'HARD',
  'question_text': 'How does the C# compiler implement async/ await, and what is the role of the '
                   'synchronization context?',
  'expected_answer': 'The compiler rewrites an async method into a struct or class implementing '
                     'IAsyncStateMachine, with a field for each local variable and a state number recording '
                     'where to resume. At each await, if the awaited task is incomplete, the method stores '
                     'its state, registers a continuation and returns an incomplete task to the caller. When '
                     'the awaited operation completes, the continuation runs MoveNext to resume. By default '
                     'the continuation resumes on '
                     'the captured SynchronizationContext or TaskScheduler (for example the UI thread), '
                     'which is why ConfigureAwait(false) is used in library code to skip the capture. '
                     'ASP.NET Core has no synchronization context, so it matters less there.',
  'companies': ['Microsoft', 'Amazon', 'Google', 'AllianceTek']},
 {'difficulty': 'HARD',
  'question_text': 'What is a deadlock in async code, and how do you avoid it?',
  'expected_answer': 'If code blocks on an async operation with .Result or .Wait() while holding a single- '
                     'threaded synchronization context (UI thread, classic ASP.NET), the continuation needs '
                     'that same thread to resume, but the thread is blocked waiting, so neither can proceed. '
                     'Avoid it by using await all the way up the call chain ("async all the way"), never '
                     'blocking on tasks, and using ConfigureAwait(false) in library code. Classic lock '
                     'deadlocks need four conditions at once (mutual exclusion, hold and wait, no '
                     'preemption, circular wait); breaking any one, for instance acquiring locks in a fixed '
                     'order, prevents them.',
  'companies': ['Microsoft', 'Amazon', 'Goldman Sachs', 'Google']},
 {'difficulty': 'HARD',
  'question_text': 'Compare lock, Monitor, Mutex, Semaphore/ SemaphoreSlim, ReaderWriterLockSlim and '
                   'Interlocked.',
  'expected_answer': 'lock is syntax over Monitor for in-process mutual exclusion; never lock on this, a '
                     'public object or a string. Mutex works across processes but is heavier. Semaphore '
                     'limits access to N threads and SemaphoreSlim is a lightweight version that supports '
                     'WaitAsync for async code. ReaderWriterLockSlim allows many readers or one writer, '
                     'useful for read-heavy data. Interlocked provides lock-free atomic operations such as '
                     'increment and compare-and-exchange for single variables. You cannot await inside a '
                     'lock, so use SemaphoreSlim for async critical sections.',
  'companies': ['Microsoft', 'Goldman Sachs', 'Amazon', 'Meta', 'Google']},
 {'difficulty': 'HARD',
  'question_text': "What does volatile do, and what is the C# memory model's guarantee about reordering?",
  'expected_answer': 'volatile marks a field so reads have acquire semantics and writes have release '
                     'semantics, preventing certain compiler and CPU reorderings and stale cached reads, so '
                     'other threads see recent values. It does not make compound operations such as x++ '
                     'atomic, and it does not give mutual exclusion. Without such barriers, the compiler, '
                     'JIT and CPU may reorder independent reads and writes, so shared state needs lock, '
                     'Interlocked, Volatile.Read/Write or other synchronization to be correct. C# Interview '
                     'Questions by ',
  'companies': ['Microsoft', 'Goldman Sachs', 'Google']},
 {'difficulty': 'HARD',
  'question_text': 'How does ConcurrentDictionary achieve thread safety, and what is the catch with '
                   'GetOrAdd?',
  'expected_answer': 'It uses fine-grained locking: the table is split into segments each guarded by its own '
                     'lock, and reads are mostly lock-free, so many threads can work in parallel. The catch '
                     'is that GetOrAdd(key, factory) may run the factory more than once under contention, '
                     'and only one result is stored, so the factory must be free of side effects, or you can '
                     'wrap values in Lazy<T> to ensure one initialization. Compound operations across '
                     'several keys are still not atomic.',
  'companies': ['Microsoft', 'Goldman Sachs', 'Amazon']},
 {'difficulty': 'HARD',
  'question_text': 'Explain Span<T>, Memory<T> and ref struct. Why were they introduced?',
  'expected_answer': 'Span<T> is a stack-only ref struct giving a typed, bounds-checked view over contiguous '
                     'memory (arrays, stack memory, native memory) without copying or allocating, which '
                     'reduces garbage in parsing and buffer-processing code. Because it can point to the '
                     'stack, it cannot be stored on the heap, captured in lambdas, used across await, or be '
                     'a field of a normal class. Memory<T> is the heap-safe counterpart that can be stored '
                     'and used in async code, and you get a Span from it when you need to work on the data.',
  'companies': ['Microsoft', 'Goldman Sachs', 'Akamai']},
 {'difficulty': 'HARD',
  'question_text': 'Explain the finalization process, the dispose pattern and resurrection.',
  'expected_answer': 'Objects with a finalizer (~Class) are placed on the finalization queue when allocated. '
                     'When the GC finds one unreachable, it moves it to the f-reachable queue, so the object '
                     'survives that collection while the finalizer thread runs its finalizer, and it is only '
                     'reclaimed in a later collection, which makes finalizable objects costly. The dispose '
                     'pattern implements Dispose(bool disposing): the public Dispose() frees managed and '
                     'unmanaged resources and calls GC.SuppressFinalize(this), while the finalizer calls '
                     'Dispose(false) to free only unmanaged resources as a safety net. Resurrection happens '
                     'when a finalizer makes the object reachable again; it is almost always a bug.',
  'companies': ['Microsoft', 'Oracle', 'Goldman Sachs']},
 {'difficulty': 'HARD',
  'question_text': 'What are SafeHandle and why prefer it to raw IntPtr?',
  'expected_answer': 'SafeHandle wraps an unmanaged '
                     'handle in a critical finalizer-backed object that is reliably released even under '
                     'thread aborts or out-of-memory conditions and prevents handle recycling attacks and '
                     'double-free bugs. Raw IntPtr offers none of these guarantees, so P/Invoke code should '
                     'use SafeHandle subclasses.',
  'companies': ['Microsoft', 'Akamai']},
 {'difficulty': 'HARD',
  'question_text': 'How do expression trees work, and how does Entity Framework use them to produce SQL?',
  'expected_answer': 'An Expression<Func<T, bool>> is not compiled into executable code; the compiler '
                     'instead builds a data structure, a tree of nodes representing operations, parameters '
                     'and constants. A LINQ provider like EF Core walks this tree and translates it to SQL. '
                     'This is why you must use IQueryable with expression-typed lambdas for database '
                     'filtering; if you use IEnumerable and a Func, the filter runs in memory after loading '
                     'all rows. Methods that cannot be translated cause an exception or client-side '
                     'evaluation.',
  'companies': ['AllianceTek', 'Microsoft', 'SynergyTop']},
 {'difficulty': 'HARD',
  'question_text': 'What are the isolation levels in SQL Server and EF Core, and how do you handle '
                   'concurrency conflicts?',
  'expected_answer': 'Read uncommitted allows dirty reads; read committed prevents them; repeatable read '
                     'also prevents non-repeatable reads; serializable also prevents phantom reads, with the '
                     'most locking. Snapshot isolation uses row versions so readers do not block writers. In '
                     'EF Core, optimistic concurrency uses a concurrency token or rowversion column; '
                     'SaveChanges throws DbUpdateConcurrencyException if the row changed since it was read, '
                     'and the app chooses to retry, merge or reject. Pessimistic concurrency uses locks and '
                     'reduces throughput.',
  'companies': ['Goldman Sachs', 'Oracle', 'Microsoft', 'Flipkart', 'Amazon']},
 {'difficulty': 'HARD',
  'question_text': 'What is the N+1 query problem, and how do you detect and fix it?',
  'expected_answer': 'It occurs when code loads a list with one query and then issues one more query per '
                     'item to load related data, such as a list of 100 orders producing 101 queries. It is '
                     'common with lazy loading and loops. Detect it by logging generated SQL or using a '
                     'profiler. Fix with eager loading (Include), projection into DTOs with Select so only '
                     'needed columns are fetched in one query, split queries for large graphs, or batching. '
                     '',
  'companies': ['AllianceTek', 'Flipkart', 'Amazon', 'Microsoft']},
 {'difficulty': 'HARD',
  'question_text': 'Explain the CAP theorem and eventual consistency, with a design example.',
  'expected_answer': 'When a network partition occurs, a distributed system must choose between consistency '
                     '(every read sees the latest write) and availability (every request gets a non-error '
                     'response); partition tolerance is not optional. A shopping cart can favor availability '
                     'and accept eventual consistency, where replicas converge later with conflict '
                     'resolution such as last-write-wins or merging. A payment ledger should favor '
                     'consistency and reject or delay operations during a partition. Real systems also trade '
                     'latency against consistency even without partitions.',
  'companies': ['Flipkart', 'Amazon', 'Meta', 'Google', 'Akamai']},
 {'difficulty': 'HARD',
  'question_text': 'How would you design an idempotent payment or order API?',
  'expected_answer': 'Idempotency means repeating a request has the same effect as doing it once, which '
                     'makes client retries after timeouts safe. The client sends a unique idempotency key '
                     'with the request; the server stores the key with the result in the same transaction as '
                     'the operation, enforced by a unique constraint. If the same key arrives again, it '
                     'returns the stored result instead of repeating the work. Also use correct status '
                     'codes, handle concurrent duplicates with a lock or unique-key conflict, expire stored '
                     'keys after a retention window, and make webhook handlers idempotent too.',
  'companies': ['Flipkart', 'Amazon', 'Goldman Sachs', 'Meta', 'Ailoitte']},
 {'difficulty': 'HARD',
  'question_text': 'Compare monolith, microservices and serverless architectures, and describe the problems '
                   'microservices introduce.',
  'expected_answer': 'A monolith deploys as one unit: simple to build, test and debug, but scaling and '
                     'releases are coupled. Microservices split a system into independently deployable '
                     'services with their own data, enabling team autonomy and independent scaling, but '
                     'introducing network latency and failures, distributed transactions, data consistency '
                     'issues, versioning, service discovery and observability costs. Serverless runs '
                     'event-driven functions billed by execution, removing server management but adding cold '
                     'starts, execution limits and vendor coupling. Techniques for microservices include '
                     'sagas for cross-service transactions, circuit breakers, retries with backoff, an API '
                     'gateway and distributed tracing.',
  'companies': ['Flipkart', 'Amazon', 'AllianceTek', 'Ailoitte', 'Microsoft']},
 {'difficulty': 'HARD',
  'question_text': 'What is the saga pattern, and how does it differ from a distributed transaction?',
  'expected_answer': 'A distributed transaction '
                     '(two-phase commit) locks resources across services until all commit, which hurts '
                     'availability and is rarely supported across independent services. A saga splits the '
                     'business transaction into a sequence of local transactions, each publishing an event '
                     'or command; if a step fails, compensating transactions undo earlier steps (for example '
                     'refund after a failed shipment). Sagas can be choreographed through events or '
                     'orchestrated by a coordinator, and provide eventual consistency rather than isolation.',
  'companies': ['Flipkart', 'Amazon', 'Microsoft']},
 {'difficulty': 'HARD',
  'question_text': 'How do caching strategies (cache-aside, write-through, write-behind) differ, and what '
                   'are cache stampede and invalidation problems?',
  'expected_answer': 'Cache-aside: the app checks the cache, loads from the database on a miss and stores '
                     'the result. Write-through: writes go to the cache and database together, keeping them '
                     'consistent but slower. Write-behind: writes go to the cache first and are flushed to '
                     'the database later, which is fast but risks data loss. A cache stampede occurs when a '
                     'popular key expires and many requests rebuild it at once; mitigate with request '
                     'coalescing, locks, jittered expiry or serving stale data while refreshing. '
                     'Invalidation is hard because stale data can persist; use short TTLs, event-based '
                     'invalidation and versioned keys.',
  'companies': ['Flipkart', 'Amazon', 'Meta', 'Akamai', 'Google']},
 {'difficulty': 'HARD',
  'question_text': 'Explain consistent hashing and how it applies to distributed caches and sharding.',
  'expected_answer': 'Keys and servers are hashed onto a ring; each key belongs to the first server '
                     'clockwise from its position. When a server is added or removed, only the keys between '
                     'it and its neighbor move, instead of nearly all keys as with hash(key) % N. Virtual '
                     'nodes (many ring positions per server) smooth uneven load and make weights possible. '
                     'It is used in distributed caches, CDNs and partitioned databases.',
  'companies': ['Akamai', 'Amazon', 'Meta', 'Google']},
 {'difficulty': 'HARD',
  'question_text': 'Explain how TLS and JWT-based authentication work and the main pitfalls.',
  'expected_answer': 'TLS negotiates a cipher suite, authenticates the server by a certificate chain signed '
                     'by a trusted authority, agrees on session keys via asymmetric key exchange, and then '
                     'encrypts traffic with fast symmetric encryption. A JWT has a header, payload and '
                     'signature; the server verifies the signature with a secret or public key, so it needs '
                     'no session store. Pitfalls: JWTs are hard to revoke before expiry (use short lifetimes '
                     'plus refresh tokens), the '
                     'payload is only encoded, not encrypted, so never put secrets in it, the alg header '
                     'must be validated (reject none), and tokens stored in browser storage are exposed to '
                     'XSS.',
  'companies': ['Akamai', 'Ailoitte', 'SynergyTop', 'Microsoft', 'Amazon']},
 {'difficulty': 'HARD',
  'question_text': 'What is the difference between a process, a thread, a fiber and a coroutine, and how is '
                   'a context switch costly?',
  'expected_answer': "A process has its own address space and resources; threads share the process's memory "
                     'and have separate stacks and registers; fibers and coroutines are cooperatively '
                     'scheduled units within a thread (async/await compiles to a coroutine-like state '
                     'machine). A context switch saves and restores registers and scheduling state, switches '
                     'kernel structures and often invalidates CPU caches and TLB entries, so large numbers '
                     'of threads waste time switching. This is why async I/O and thread pools beat one '
                     'thread per request at scale.',
  'companies': ['Microsoft', 'Akamai', 'Google', 'Amazon']},
 {'difficulty': 'HARD',
  'question_text': 'Explain virtual memory, paging, page faults and thrashing.',
  'expected_answer': 'Virtual memory gives each process its own address space, mapped to physical frames by '
                     'page tables, with a TLB caching recent translations. Pages not in RAM trigger a page '
                     'fault; the OS loads the page from disk (a major fault, very slow) or maps it (a minor '
                     'fault), possibly evicting another page with a policy such as LRU approximations. '
                     'Thrashing happens when the working sets of running processes exceed physical memory, '
                     'so the system spends most of its time swapping pages instead of doing work; fix by '
                     'reducing memory pressure or the degree of multiprogramming.',
  'companies': ['Microsoft', 'Zoho', 'Akamai', 'Oracle', 'Google']},
 {'difficulty': 'HARD',
  'question_text': 'What are the differences between HTTP/1.1, HTTP/2 and HTTP/3, and how does a CDN reduce '
                   'latency?',
  'expected_answer': 'HTTP/1.1 handles one request at a time per connection, so browsers open several '
                     'connections. HTTP/2 multiplexes many streams over one TCP connection with header '
                     'compression, but TCP head-of-line blocking still stalls all streams on packet loss. '
                     'HTTP/3 runs over QUIC on UDP, with per-stream loss recovery, faster handshakes and '
                     'connection migration. A CDN caches content on edge servers close to users, routes '
                     'requests to a nearby edge, terminates TLS near the user and offloads the origin, '
                     'cutting round-trip time and bandwidth cost; cache keys, TTLs and purge mechanisms '
                     'control freshness. ',
  'companies': ['Akamai', 'Google', 'Meta', 'Amazon']},
 {'difficulty': 'HARD',
  'question_text': 'How do SQL and NoSQL stores compare for a large-scale system, and how do sharding and '
                   'replication work?',
  'expected_answer': 'Relational databases offer joins, strong consistency and ACID transactions with a '
                     'fixed schema, and usually scale vertically with read replicas. NoSQL stores '
                     '(key-value, document, wide-column, graph) scale horizontally with flexible schemas and '
                     'predictable latency, but limit joins and often relax consistency. Sharding splits data '
                     'across nodes by a shard key (range, hash or directory), scaling writes and storage; a '
                     'poor key creates hot spots and cross-shard queries are expensive. Replication copies '
                     'data to several nodes for availability and read scaling, using leader-follower '
                     '(replication lag causes stale reads) or multi-leader and leaderless designs (conflict '
                     'resolution needed). ',
  'companies': ['Flipkart', 'Amazon', 'Meta', 'Oracle', 'Google', 'Goldman Sachs']}]


def seed_csharp_questions() -> None:
    db = SessionLocal()
    try:
        topic = db.query(Topic).filter(Topic.name == TOPIC_NAME).first()
        if topic is None:
            raise RuntimeError(
                "The C# topic does not exist. Create the C# topic in the app/database first; "
                "this seeder will not create a duplicate topic."
            )
        if not topic.is_active:
            raise RuntimeError(f"The C# topic (ID: {topic.id}) is inactive. Activate it first.")

        existing_count = db.query(Question).filter(Question.topic_id == topic.id).count()
        if existing_count > 0:
            print(f"C# topic (ID: {topic.id}) already contains {existing_count} question(s).")
            print("No questions were inserted to avoid duplicates.")
            print("Inspect existing C# questions before deciding whether to seed again.")
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
        print("C# THEORY QUESTION BANK CREATED")
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
    seed_csharp_questions()
