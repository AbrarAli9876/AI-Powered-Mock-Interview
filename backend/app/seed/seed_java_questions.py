"""Idempotently seed the Java theory interview questions from the supplied PDF.

Company labels are presented as "frequently reported at" because the source document
states they are based on reported interview experiences, not official company banks.
"""
from app.database import SessionLocal
from app.enums.question_difficulty import QuestionDifficulty
from app.models.question import Question
from app.models.topic import Topic

TOPIC_NAME = "Java"

QUESTIONS = [{'difficulty': 'easy',
  'question_text': 'What is the difference between JDK, JRE and JVM?',
  'expected_answer': 'JVM (Java Virtual Machine) executes bytecode. It is platform specific and '
                     'provides memory management and garbage collection. JRE (Java Runtime '
                     'Environment) = JVM + core libraries (such as java.lang, java.util) needed to '
                     'run Java programs. JDK (Java Development Kit) = JRE + development tools '
                     '(javac, jar, javadoc, debugger). You need it to compile code.',
  'companies': ['Oracle', 'Zoho', 'Flipkart']},
 {'difficulty': 'easy',
  'question_text': 'How is Java platform independent?',
  'expected_answer': 'The compiler converts source code into platform neutral bytecode (.class '
                     'files), not machine code. Each OS has its own JVM that interprets or '
                     'JIT-compiles that bytecode for the local hardware. So the same .class file '
                     'runs anywhere a JVM exists ("write once, run anywhere"). Note that the JVM '
                     'itself is platform dependent; the bytecode is not.',
  'companies': ['Oracle', 'Zoho']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between == and .equals()?',
  'expected_answer': '== compares primitives by value and objects by reference (same object in '
                     'memory). .equals() compares logical content and can be overridden. String '
                     'overrides it to compare characters, so new String("a") == new String("a") is '
                     'false but .equals() returns true.',
  'companies': ['Zoho', 'Amazon', 'Flipkart']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between String, StringBuilder and StringBuffer?',
  'expected_answer': 'String: immutable; every change creates a new object. StringBuilder: '
                     'mutable, not thread safe, fastest for single-threaded concatenation. '
                     'StringBuffer: mutable and thread safe (methods are synchronized), so slower.',
  'companies': ['Zoho', 'Microsoft']},
 {'difficulty': 'easy',
  'question_text': 'Why is String immutable in Java?',
  'expected_answer': 'String pool: literals can be shared safely only if they never change. '
                     'Security: strings hold class names, file paths, URLs and credentials; '
                     'mutation after validation would be dangerous. Thread safety: immutable '
                     'objects need no synchronization. Hash caching: hashCode() is computed once '
                     'and cached, which makes strings ideal HashMap keys.',
  'companies': ['Oracle', 'Zoho', 'Goldman Sachs']},
 {'difficulty': 'easy',
  'question_text': 'What are the four pillars of OOP? Give an example of each.',
  'expected_answer': 'Encapsulation: bundling data with methods and hiding it (private fields with '
                     'getters/setters). Inheritance: a class acquires properties of another (Dog '
                     'extends Animal). Polymorphism: one interface, many forms (overloading at '
                     'compile time, overriding at runtime). Abstraction: exposing essential '
                     'behavior and hiding detail (abstract classes, interfaces).',
  'companies': ['Zoho', 'Microsoft']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between method overloading and overriding?',
  'expected_answer': 'Overloading: same method name, different parameter lists, in the same class. '
                     'Resolved at compile time. Return type alone cannot differentiate. '
                     'Overriding: a subclass redefines a superclass method with the same '
                     'signature. Resolved at runtime (dynamic dispatch). The access level cannot '
                     'be reduced, and static, final and private methods cannot be overridden.',
  'companies': ['Zoho', 'Flipkart']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between an abstract class and an interface?',
  'expected_answer': 'An abstract class can have state (instance fields), constructors and any '
                     'access modifiers. A class can extend only one. An interface defines a '
                     'contract. Fields are public static final. Since Java 8 it can have default '
                     'and static methods, and since Java 9 private methods. A class can implement '
                     'many. Use an abstract class for shared state and code in a closely related '
                     'family; use an interface for capabilities across unrelated classes.',
  'companies': ['Oracle', 'Microsoft', 'Zoho']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between final, finally and finalize()?',
  'expected_answer': 'final: a keyword. A final variable cannot be reassigned, a final method '
                     'cannot be overridden, a final class cannot be extended. finally: a block '
                     'that runs after try/catch whether or not an exception occurred (except '
                     'System.exit() or a JVM crash). finalize(): a method called by the GC before '
                     'reclaiming an object. It is deprecated (since Java 9, for removal) and '
                     'unreliable. Use try-with-resources or Cleaner instead.',
  'companies': ['Zoho', 'Oracle']},
 {'difficulty': 'easy',
  'question_text': 'What are the access modifiers in Java, and how do they differ?',
  'expected_answer': 'public: accessible everywhere. protected: same package plus subclasses in '
                     'any package. default (no keyword): same package only. private: same class '
                     'only.',
  'companies': ['Zoho']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between checked and unchecked exceptions?',
  'expected_answer': 'Checked exceptions (subclasses of Exception but not RuntimeException, e.g. '
                     'IOException, SQLException) are verified at compile time and must be caught '
                     'or declared with throws. Unchecked exceptions (RuntimeException and Error '
                     'subclasses, e.g. NullPointerException) are not enforced by the compiler and '
                     'usually indicate programming bugs.',
  'companies': ['Amazon', 'Microsoft']},
 {'difficulty': 'easy',
  'question_text': 'What does the static keyword do?',
  'expected_answer': 'static ties a member to the class rather than an instance. Static variable: '
                     'one copy shared by all instances. Static method: callable without an object; '
                     'cannot access instance members directly. Static block: runs once when the '
                     'class is loaded. Static nested class: does not hold a reference to an outer '
                     'instance.',
  'companies': ['Zoho', 'Oracle']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between this and super?',
  'expected_answer': 'this refers to the current object (and this(...) calls another constructor '
                     'of the same class). super refers to the parent class (super.method() calls '
                     "the parent's version, super(...) calls the parent constructor). Both must be "
                     'the first statement when used to call a constructor, and you cannot use both '
                     'in the same constructor.',
  'companies': ['Zoho']},
 {'difficulty': 'easy',
  'question_text': 'Can a constructor be private, overloaded or inherited?',
  'expected_answer': 'Private: yes. It is used in Singletons, utility classes and factory '
                     'patterns. Overloaded: yes, with different parameter lists. Inherited: no. '
                     'Constructors are not inherited, but a subclass constructor always calls a '
                     'parent constructor (implicitly super() if you do not write one).',
  'companies': ['Zoho', 'Oracle']},
 {'difficulty': 'easy',
  'question_text': 'What are wrapper classes, autoboxing and unboxing?',
  'expected_answer': 'Wrapper classes (Integer, Double, Boolean, etc.) represent primitives as '
                     'objects, which is needed for collections and generics. Autoboxing is '
                     'automatic conversion from primitive to wrapper (Integer x = 5;); unboxing is '
                     'the reverse. Pitfalls: unboxing a null throws NullPointerException, and '
                     'Integer values from -128 to 127 are cached, so == can behave unexpectedly '
                     'outside that range.',
  'companies': ['Oracle', 'Flipkart']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between an array and an ArrayList?',
  'expected_answer': 'An array has a fixed size, can hold primitives, and has no built-in methods. '
                     'An ArrayList is dynamically resizable (internally it grows its backing array '
                     'by about 1.5x), holds only objects (via autoboxing), and offers methods like '
                     'add, remove and contains. Both give O(1) index access.',
  'companies': ['Amazon', 'Flipkart']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between ArrayList and LinkedList?',
  'expected_answer': 'ArrayList is backed by a dynamic array: O(1) random access, O(n) '
                     'insert/delete in the middle, better cache locality. LinkedList is a doubly '
                     'linked list: O(n) access, O(1) insert/delete once you hold the node, and '
                     'extra memory per element for pointers. In practice ArrayList wins in most '
                     'real workloads.',
  'companies': ['Amazon', 'Goldman Sachs']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between HashMap and Hashtable?',
  'expected_answer': 'HashMap is not synchronized, allows one null key and multiple null values, '
                     'and is faster. Hashtable is legacy, fully synchronized, and does not allow '
                     'null keys or values. For thread safety prefer ConcurrentHashMap.',
  'companies': ['Zoho', 'Goldman Sachs']},
 {'difficulty': 'easy',
  'question_text': 'What is the difference between stack and heap memory?',
  'expected_answer': 'Stack: per thread. Stores method frames, local primitives and object '
                     'references. Fast, LIFO, freed automatically when a method returns. Overflow '
                     'causes StackOverflowError. Heap: shared by all threads. Stores all objects '
                     'and arrays. Managed by the garbage collector. Exhaustion causes '
                     'OutOfMemoryError.',
  'companies': ['Oracle', 'Microsoft']},
 {'difficulty': 'easy',
  'question_text': 'Can we overload or override the main() method? What if it is not static?',
  'expected_answer': 'You can overload main (different parameters), but the JVM only calls public '
                     'static void main(String[] args). You cannot truly override it because static '
                     'methods are hidden, not overridden. If main is not static, the program '
                     'compiles but fails at launch because the JVM has no instance to call it on. '
                     '(Java 21+ previews relax this with "unnamed classes and instance main '
                     'methods".)',
  'companies': ['Zoho']},
 {'difficulty': 'medium',
  'question_text': 'How does HashMap work internally?',
  'expected_answer': 'HashMap stores entries in an array of buckets (default capacity 16, load '
                     'factor 0.75). 1. put(k, v) computes hashCode(), spreads the bits (h ^ (h >>> '
                     '16)), and picks a bucket with (n - 1) & hash. 2. If the bucket is empty, a '
                     'new node is stored. If not, the chain is walked using equals() to find an '
                     'existing key (update) or append a new node (collision). 3. When a bucket '
                     'reaches 8 nodes and the table has at least 64 buckets, the linked list '
                     'converts to a red-black tree (worst case O(log n)). It reverts below 6 '
                     'nodes. 4. When size exceeds capacity x load factor, the table doubles and '
                     'entries are redistributed (rehashing). Average get/put is O(1). It is not '
                     'thread safe.',
  'companies': ['Amazon', 'Flipkart', 'Goldman Sachs', 'Microsoft']},
 {'difficulty': 'medium',
  'question_text': 'What is the hashCode() and equals() contract? What breaks if you violate it?',
  'expected_answer': 'If a.equals(b) is true, then a.hashCode() == b.hashCode() must hold. Equal '
                     'hash codes do not imply equal objects (collisions are allowed). hashCode() '
                     'must be consistent across calls while the fields used by equals() are '
                     'unchanged. If you override equals() but not hashCode(), equal objects land '
                     'in different buckets, so HashMap.get() and HashSet.contains() fail to find '
                     "them and duplicates appear in sets. Mutating a key's fields after insertion "
                     'has the same effect.',
  'companies': ['Goldman Sachs', 'Amazon', 'Zoho']},
 {'difficulty': 'medium',
  'question_text': 'What is the difference between ConcurrentHashMap, Hashtable and '
                   'Collections.synchronizedMap?',
  'expected_answer': 'Hashtable and synchronizedMap lock the entire map on every operation, so '
                     'there is one lock and heavy contention. Iteration still requires manual '
                     'synchronization. ConcurrentHashMap uses fine-grained locking (bin level) '
                     'plus CAS in Java 8+. Reads are mostly lock-free, many writers can proceed in '
                     'parallel, and iterators are weakly consistent (no '
                     'ConcurrentModificationException). ConcurrentHashMap does not allow null keys '
                     'or values. It also offers atomic operations like putIfAbsent, compute and '
                     'merge.',
  'companies': ['Goldman Sachs', 'Flipkart']},
 {'difficulty': 'medium',
  'question_text': 'What is the difference between fail-fast and fail-safe iterators?',
  'expected_answer': 'Fail-fast iterators (ArrayList, HashMap) throw '
                     'ConcurrentModificationException if the collection is structurally modified '
                     'during iteration, detected via an internal modCount. This is best effort, '
                     'not guaranteed. Fail-safe (more accurately weakly consistent) iterators '
                     '(CopyOnWriteArrayList, ConcurrentHashMap) never throw; they iterate over a '
                     'snapshot or tolerate concurrent changes, but may not reflect the latest '
                     'updates.',
  'companies': ['Oracle', 'Amazon']},
 {'difficulty': 'medium',
  'question_text': 'How does garbage collection work? Explain the generational heap.',
  'expected_answer': 'GC reclaims objects that are no longer reachable from GC roots (thread '
                     'stacks, static fields, JNI references). The heap is split on the weak '
                     'generational hypothesis (most objects die young): Young generation (Eden + '
                     'two Survivor spaces): new objects start in Eden. A minor GC copies live '
                     'objects to a survivor space and increments their age. Old generation: '
                     'objects surviving enough minor GCs are promoted. Collected by a major/mixed '
                     'GC, which is more expensive. Metaspace (Java 8+, native memory): class '
                     'metadata. It replaced PermGen. Full GC cleans everything and causes the '
                     'longest pauses.',
  'companies': ['Oracle', 'Goldman Sachs', 'Amazon']},
 {'difficulty': 'medium',
  'question_text': 'What is the difference between synchronized and volatile?',
  'expected_answer': 'volatile guarantees visibility (writes are seen by other threads) and '
                     'ordering for a single variable, but not atomicity for compound actions like '
                     'count++. synchronized provides mutual exclusion plus visibility; only one '
                     'thread at a time enters the block, and it establishes a happens-before edge '
                     'on unlock/lock. volatile is lightweight and non-blocking; synchronized can '
                     'block threads.',
  'companies': ['Goldman Sachs', 'Flipkart', 'Microsoft']},
 {'difficulty': 'medium',
  'question_text': 'Explain the thread lifecycle. How do wait(), notify() and sleep() differ?',
  'expected_answer': 'States: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED. '
                     'sleep(ms): pauses the current thread, keeps any locks it holds. It is a '
                     "Thread static method. wait(): releases the object's monitor and waits until "
                     'notify()/ notifyAll(). It must be called inside a synchronized block on the '
                     'same object, and is defined in Object. Always call it in a loop that '
                     'rechecks the condition (spurious wakeups). notify() wakes one waiting '
                     'thread; notifyAll() wakes all.',
  'companies': ['Zoho', 'Goldman Sachs', 'Amazon']},
 {'difficulty': 'medium',
  'question_text': 'What is the difference between Runnable and Callable? What is a Future?',
  'expected_answer': 'Runnable.run() returns nothing and cannot throw checked exceptions. '
                     'Callable<V>.call() returns a value and may throw checked exceptions. '
                     'Submitting a task to an ExecutorService returns a Future<V>, a handle to the '
                     'pending result: get() blocks until done (wrapping failures in '
                     'ExecutionException), plus isDone(), cancel() and timeouts.',
  'companies': ['Amazon', 'Flipkart']},
 {'difficulty': 'medium',
  'question_text': 'How does ExecutorService work? What are the types of thread pools?',
  'expected_answer': 'An executor decouples task submission from execution by reusing a pool of '
                     'worker threads that pull tasks from a queue. Common factories: '
                     'newFixedThreadPool(n): fixed workers with an unbounded queue. '
                     'newCachedThreadPool(): grows on demand and reclaims idle threads; can create '
                     'too many threads. newSingleThreadExecutor(): one worker, tasks run in order. '
                     'newScheduledThreadPool(n): delayed and periodic tasks. '
                     'newWorkStealingPool(): ForkJoinPool based. In production prefer a hand-built '
                     'ThreadPoolExecutor with a bounded queue, a named thread factory and an '
                     'explicit rejection policy. Always call shutdown().',
  'companies': ['Goldman Sachs', 'Amazon', 'Flipkart']},
 {'difficulty': 'medium',
  'question_text': 'What causes deadlock, and how do you prevent or detect it?',
  'expected_answer': 'Deadlock needs four conditions (Coffman): mutual exclusion, hold and wait, '
                     'no preemption, circular wait. Prevention: acquire locks in a consistent '
                     'global order, use tryLock with timeouts, keep critical sections small, avoid '
                     'nested locks, or prefer higher level concurrency utilities. Detection: take '
                     'a thread dump (jstack, jcmd Thread.print), which reports "Found one '
                     'Java-level deadlock", or use ThreadMXBean.findDeadlockedThreads().',
  'companies': ['Goldman Sachs', 'Microsoft', 'Oracle']},
 {'difficulty': 'medium',
  'question_text': 'What are lambdas and functional interfaces? How do map and flatMap differ?',
  'expected_answer': 'A functional interface has exactly one abstract method (Runnable, '
                     'Comparator, Function, Predicate; annotated with @FunctionalInterface). A '
                     'lambda is a concise implementation of one: (a, b) -> a + b. In streams, map '
                     'transforms each element one- to-one (Stream<T> to Stream<R>), while flatMap '
                     'maps each element to a stream and flattens the results into one stream (for '
                     'example, turning a List<List<String>> into a flat list of strings).',
  'companies': ['Flipkart', 'Amazon', 'Zoho']},
 {'difficulty': 'medium',
  'question_text': 'What is Optional, and when should you avoid it?',
  'expected_answer': 'Optional<T> is a container that may or may not hold a value, making "absent" '
                     'explicit in return types. Use map, orElse, orElseGet, ifPresent. Avoid it '
                     'for fields, method parameters, collection elements and serialization (it is '
                     'not Serializable), and avoid calling get() without checking. It is intended '
                     'mainly as a return type.',
  'companies': ['Flipkart', 'Amazon']},
 {'difficulty': 'medium',
  'question_text': 'What are default and static methods in interfaces, and why were they added?',
  'expected_answer': 'They were added in Java 8 to evolve interfaces without breaking existing '
                     'implementers (for example, adding stream() or forEach() to Collection/ '
                     'Iterable). A default method provides an inherited implementation that '
                     'classes may override. If two interfaces supply the same default, the class '
                     'must override and may pick one with InterfaceName.super.method(). static '
                     'methods are utility helpers called on the interface itself and are not '
                     'inherited.',
  'companies': ['Oracle', 'Microsoft']},
 {'difficulty': 'medium',
  'question_text': 'What are generics, type erasure and wildcards?',
  'expected_answer': 'Generics give compile-time type safety and remove casts. Type erasure means '
                     'generic type information is removed at compile time (List<String> becomes '
                     'List in bytecode), so you cannot do new T(), instanceof List<String>, or '
                     'create generic arrays. Wildcards follow PECS (Producer Extends, Consumer '
                     'Super): ? extends T for reading (producer), ? super T for writing '
                     '(consumer), ? for unknown.',
  'companies': ['Oracle', 'Google', 'Goldman Sachs']},
 {'difficulty': 'medium',
  'question_text': 'How does serialization work? What do transient and serialVersionUID do?',
  'expected_answer': 'A class implementing Serializable can be converted to a byte stream with '
                     'ObjectOutputStream and restored with ObjectInputStream. transient fields are '
                     'skipped (reset to default on deserialization), and static fields are not '
                     'serialized. serialVersionUID is a version stamp; a mismatch throws '
                     'InvalidClassException. Notes: a non-serializable parent needs an accessible '
                     'no-arg constructor, and Java deserialization of untrusted data is a known '
                     'security risk, so prefer JSON or Protobuf.',
  'companies': ['Goldman Sachs', 'Oracle']},
 {'difficulty': 'medium',
  'question_text': 'What is the difference between Comparable and Comparator?',
  'expected_answer': 'Comparable<T> defines the natural ordering inside the class via compareTo(T '
                     'o); there can be only one. Comparator<T> is an external strategy via '
                     'compare(T a, T b); you can define many (by name, by age, etc.), and it '
                     'supports chaining such as '
                     'Comparator.comparing(Person::getAge).thenComparing(Person::getName).',
  'companies': ['Amazon', 'Zoho']},
 {'difficulty': 'medium',
  'question_text': 'How do you create an immutable class?',
  'expected_answer': '1. Declare the class final (or make constructors private with factories). 2. '
                     'Make all fields private final. 3. No setters. 4. Initialize everything in '
                     'the constructor. 5. Defensively copy mutable inputs in the constructor and '
                     'mutable outputs in getters (or return unmodifiable views). Java 16+ record '
                     'types give shallow immutability with much less code.',
  'companies': ['Goldman Sachs', 'Amazon', 'Microsoft']},
 {'difficulty': 'medium',
  'question_text': 'How do you implement a thread-safe Singleton? What is double-checked locking?',
  'expected_answer': 'Best options: an enum singleton (also safe against reflection and '
                     'serialization) or the initialization-on-demand holder idiom (a static inner '
                     'class that holds the instance, lazily loaded and thread safe by '
                     'class-loading guarantees). Double-checked locking checks instance == null, '
                     'enters a synchronized block, checks again, then creates it. It is only '
                     'correct if the field is declared volatile, which prevents reordering of '
                     'construction and reference publication.',
  'companies': ['Amazon', 'Microsoft', 'Flipkart']},
 {'difficulty': 'medium',
  'question_text': 'What happens if you return inside try and finally? What is try-with- '
                   'resources?',
  'expected_answer': 'finally runs even after a return in try. If finally itself returns, it '
                     'overrides the earlier return value (and swallows exceptions), so avoid that. '
                     'Try-with-resources (try (var r = open()) { ... }) automatically calls '
                     'close() on any AutoCloseable resource in reverse order, even on exceptions. '
                     'Exceptions from close() are attached as suppressed exceptions rather than '
                     'hiding the primary one.',
  'companies': ['Zoho', 'Oracle']},
 {'difficulty': 'medium',
  'question_text': 'What is the String constant pool, and what does intern() do?',
  'expected_answer': 'The pool (on the heap since Java 7) stores one canonical copy of each string '
                     'literal. "abc" literals reuse the pooled instance, while new String("abc") '
                     'always creates a new heap object. intern() returns the pooled reference, '
                     'adding the string if absent, so new String("abc").intern() == "abc" is true. '
                     'Overusing intern() can strain the pool.',
  'companies': ['Zoho', 'Oracle']},
 {'difficulty': 'medium',
  'question_text': 'What is the difference between shallow and deep copy? How does clone() work?',
  'expected_answer': 'A shallow copy duplicates the object but shares references to nested '
                     'objects; a deep copy recursively duplicates nested objects too. '
                     'Object.clone() (requires Cloneable, otherwise CloneNotSupportedException) is '
                     'a shallow field-by-field copy and is widely considered flawed. Better '
                     'alternatives: copy constructors, static factories, or serialization/library '
                     'based deep copies.',
  'companies': ['Microsoft', 'Zoho']},
 {'difficulty': 'medium',
  'question_text': 'What is reflection, and what are its uses and drawbacks?',
  'expected_answer': 'Reflection (java.lang.reflect) lets code inspect and manipulate classes, '
                     'methods, fields and constructors at runtime, even private ones with '
                     'setAccessible(true). Uses: frameworks like Spring and Hibernate, JUnit, '
                     'serializers, dependency injection. Drawbacks: slower than direct calls, '
                     'bypasses compile-time checks and encapsulation, can break under the module '
                     'system (strong encapsulation) and complicates security and AOT/native-image '
                     'builds.',
  'companies': ['Oracle', 'Microsoft']},
 {'difficulty': 'hard',
  'question_text': 'Explain the Java Memory Model and the happens-before relationship.',
  'expected_answer': 'The Java Memory Model (JMM) defines when writes by one thread are guaranteed '
                     'visible to reads by another, since CPUs and compilers cache and reorder '
                     'operations. Happens- before is the guarantee: if action A happens-before B, '
                     "A's effects are visible to B. Key rules: Program order within a single "
                     'thread. An unlock of a monitor happens-before every later lock of the same '
                     'monitor. A volatile write happens-before every later volatile read of that '
                     'variable. Thread.start() happens-before any action in the started thread; '
                     "all actions in a thread happen-before another thread's successful join() on "
                     'it. Transitivity. Without a happens-before edge, a data race exists and '
                     'behavior is undefined with respect to visibility and ordering. final fields '
                     'also get special safe-publication guarantees after construction.',
  'companies': ['Google', 'Goldman Sachs', 'Oracle']},
 {'difficulty': 'hard',
  'question_text': 'Compare GC algorithms (Parallel, G1, ZGC, Shenandoah). How do you tune them '
                   'and diagnose long pauses?',
  'expected_answer': 'Parallel GC: multi-threaded stop-the-world collector optimized for '
                     'throughput; long pauses on big heaps. G1 (default since Java 9): splits the '
                     'heap into regions, collects regions with the most garbage first, targets a '
                     'pause goal (-XX:MaxGCPauseMillis). Good general balance. ZGC: concurrent, '
                     'region based, colored pointers and load barriers; pauses typically under a '
                     'few milliseconds regardless of heap size (multi-TB). Generational ZGC is '
                     'available in recent versions. Shenandoah: concurrent compaction with '
                     'Brooks-style forwarding or load barriers; low pauses, similar goals to ZGC. '
                     'Tuning and diagnosis: enable GC logging (-Xlog:gc*), analyze with GCViewer '
                     'or GCeasy, check allocation rate, promotion rate and humongous allocations '
                     '(G1), right-size heap (- Xms/ -Xmx), and fix the cause (object churn, leaks) '
                     'before touching flags. Long pauses often come from full GCs, to-space '
                     'exhaustion, large object allocations or safepoint delays.',
  'companies': ['Google', 'Oracle', 'Goldman Sachs', 'Amazon']},
 {'difficulty': 'hard',
  'question_text': 'How does class loading work? What is the difference between '
                   'ClassNotFoundException and NoClassDefFoundError?',
  'expected_answer': 'Class loading has three phases: loading (read bytecode), linking (verify, '
                     'prepare static fields, resolve references) and initialization (static '
                     'initializers). The parent delegation model means a loader first asks its '
                     'parent: Bootstrap, then Platform (formerly Extension), then Application. '
                     'Custom class loaders are used for plugins, hot reload, app servers and '
                     'isolation. ClassNotFoundException: a checked exception thrown when code '
                     'explicitly loads a class by name (Class.forName, loadClass) and it is not on '
                     'the classpath. NoClassDefFoundError: an Error thrown when a class was '
                     'present at compile time but is missing at runtime, or when its static '
                     'initializer previously failed.',
  'companies': ['Oracle', 'Microsoft']},
 {'difficulty': 'hard',
  'question_text': 'What do the JIT compiler, tiered compilation, inlining and escape analysis do?',
  'expected_answer': 'The JVM starts by interpreting bytecode, profiles it, and compiles hot '
                     'methods to native code. Tiered compilation uses the quick C1 compiler first '
                     'and the heavily optimizing C2 (or Graal) for the hottest code. Optimizations '
                     'include inlining (removing call overhead and enabling further optimization), '
                     'loop unrolling, dead code elimination and escape analysis: if an object '
                     'never escapes a method, the JIT can allocate it on the stack or eliminate it '
                     '(scalar replacement) and drop unnecessary locks (lock elision). Code can be '
                     'deoptimized if assumptions break. This is why microbenchmarks need warm-up '
                     '(use JMH).',
  'companies': ['Oracle', 'Google', 'Goldman Sachs']},
 {'difficulty': 'hard',
  'question_text': 'Why does double-checked locking need volatile? How do memory barriers and '
                   'instruction reordering come into this?',
  'expected_answer': 'instance = new Singleton() is roughly three steps: allocate memory, run the '
                     'constructor, assign the reference. The compiler or CPU may reorder so the '
                     'reference is assigned before the constructor finishes. Another thread doing '
                     'the unsynchronized first check could then see a non-null but '
                     'half-constructed object. Declaring the field volatile inserts memory '
                     'barriers that forbid this reordering and guarantee that the reference is '
                     'published only after construction completes (Java 5+ semantics).',
  'companies': ['Goldman Sachs', 'Google']},
 {'difficulty': 'hard',
  'question_text': 'What is CAS, and how do Atomic* classes and LongAdder work? What is the ABA '
                   'problem?',
  'expected_answer': 'Compare-And-Swap is a hardware atomic instruction: update a location to a '
                     'new value only if it currently holds an expected value. '
                     'AtomicInteger.incrementAndGet() loops on CAS until it succeeds, giving '
                     'lock-free progress. Under heavy contention many threads retry; LongAdder '
                     'reduces this by spreading updates across internal cells and summing on read, '
                     'trading exact instantaneous reads for throughput. ABA problem: a value '
                     'changes A to B and back to A, so a CAS succeeds even though state changed in '
                     'between. Fix with a version stamp (AtomicStampedReference) or '
                     'AtomicMarkableReference.',
  'companies': ['Goldman Sachs', 'Amazon', 'Meta']},
 {'difficulty': 'hard',
  'question_text': 'How do ReentrantLock and AbstractQueuedSynchronizer (AQS) work internally? How '
                   'do they compare to synchronized?',
  'expected_answer': 'AQS maintains an integer state (updated by CAS) and a FIFO CLH-style queue '
                     'of waiting threads, parking and unparking them with LockSupport. '
                     'ReentrantLock, Semaphore, CountDownLatch and ReentrantReadWriteLock are '
                     'built on it. ReentrantLock adds capabilities over synchronized: tryLock() '
                     '(with timeout), interruptible locking, fair mode, multiple Condition '
                     'objects, and inspection methods. Downsides: you must unlock in finally. '
                     'Modern JVMs optimize synchronized well, so use ReentrantLock only when you '
                     'need those features.',
  'companies': ['Goldman Sachs', 'Oracle']},
 {'difficulty': 'hard',
  'question_text': 'How did ConcurrentHashMap change from Java 7 to Java 8?',
  'expected_answer': 'Java 7: the map was divided into segments (default 16), each a mini hash '
                     'table with its own ReentrantLock; concurrency was limited by segment count. '
                     'Java 8: segments were removed. It uses a single table of bins. Empty-bin '
                     'inserts use CAS; non-empty bins are locked with synchronized on the first '
                     'node only. Long chains convert to trees, resizing is cooperative (multiple '
                     'threads help transfer), and size is tracked with a LongAdder-like counter. '
                     'Reads are lock-free via volatile reads.',
  'companies': ['Goldman Sachs', 'Amazon', 'Flipkart']},
 {'difficulty': 'hard',
  'question_text': 'How do ForkJoinPool, work stealing and parallel streams work? What are the '
                   'pitfalls?',
  'expected_answer': 'ForkJoinPool runs divide-and-conquer tasks (RecursiveTask/ RecursiveAction: '
                     'fork() subtasks, join() results). Each worker has its own deque; idle '
                     "workers steal tasks from the tail of others' deques, balancing load. "
                     'Parallel streams use the shared common pool. Pitfalls: blocking or I/O tasks '
                     'starve the shared pool for the whole JVM, overhead exceeds gains for small '
                     'or cheap workloads, poor splitting sources (LinkedList) hurt, shared mutable '
                     'state causes races, and ordering-sensitive operations are costly.',
  'companies': ['Google', 'Amazon']},
 {'difficulty': 'hard',
  'question_text': 'How does CompletableFuture compose async work, and how do you handle '
                   'exceptions and thread pools?',
  'expected_answer': 'CompletableFuture supports non-blocking pipelines: supplyAsync, thenApply '
                     '(transform), thenCompose (flat-map to another future), thenCombine (join '
                     'two), allOf/ anyOf. Errors propagate through the chain and are handled with '
                     'exceptionally, handle or whenComplete. By default async stages run on the '
                     'common ForkJoinPool; pass your own Executor for blocking or I/O work. Add '
                     'timeouts with orTimeout/ completeOnTimeout (Java 9+) and avoid calling '
                     'join()/ get() inside the pipeline.',
  'companies': ['Amazon', 'Flipkart', 'Microsoft']},
 {'difficulty': 'hard',
  'question_text': 'What are common causes of memory leaks in Java? How do you analyze an OOM with '
                   'heap and thread dumps?',
  'expected_answer': 'Causes: static collections that grow forever, unbounded caches, '
                     'listeners/callbacks never deregistered, un-closed resources (streams, '
                     'connections), ThreadLocal values in pooled threads, inner classes holding '
                     'outer references, and class loader leaks. Analysis: run with '
                     '-XX:+HeapDumpOnOutOfMemoryError, open the .hprof in Eclipse MAT or VisualVM, '
                     'inspect the dominator tree and path to GC roots for the largest retained '
                     'sizes. Use jmap, jcmd GC.heap_dump, jstack for threads, and '
                     'JFR/async-profiler for allocation hot spots. Compare dumps over time to see '
                     'what grows.',
  'companies': ['Amazon', 'Flipkart', 'Goldman Sachs']},
 {'difficulty': 'hard',
  'question_text': 'Explain strong, soft, weak and phantom references. When would you use '
                   'WeakHashMap?',
  'expected_answer': 'Strong: normal references; never collected while reachable. Soft: collected '
                     'only when memory is low; suited to memory-sensitive caches. Weak: collected '
                     'at the next GC if only weakly reachable. Phantom: used with a ReferenceQueue '
                     'to run cleanup after an object is finalized/unreachable (the basis of '
                     'Cleaner); get() always returns null. WeakHashMap holds keys weakly, so an '
                     'entry disappears when the key is no longer strongly referenced elsewhere. '
                     'Use it for metadata or canonicalizing maps keyed by objects whose lifecycle '
                     'you do not control. Caution: values must not strongly reference their own '
                     'key.',
  'companies': ['Oracle', 'Google']},
 {'difficulty': 'hard',
  'question_text': 'What are virtual threads (Project Loom)? How do they differ from platform '
                   'threads, and where do they not help?',
  'expected_answer': 'Virtual threads (final in Java 21) are lightweight threads scheduled by the '
                     'JVM onto a small pool of carrier platform threads. When a virtual thread '
                     'blocks on I/O it is unmounted, freeing the carrier, so you can run millions '
                     'of them using simple blocking- style code instead of reactive callbacks. '
                     'They do not help CPU-bound work (cores are the limit), and they can get '
                     'pinned to the carrier when blocking inside synchronized blocks or native '
                     'calls (reduced in newer JDKs). Do not pool them; create one per task. Limit '
                     'access to scarce downstream resources with semaphores. Beware ThreadLocal '
                     'overuse.',
  'companies': ['Oracle', 'Amazon', 'Microsoft']},
 {'difficulty': 'hard',
  'question_text': 'Design a thread-safe LRU cache or a bounded blocking queue without using '
                   'library classes.',
  'expected_answer': 'LRU cache: combine a HashMap<K, Node> with a doubly linked list ordered by '
                     'recency. get moves the node to the head; put inserts at the head and evicts '
                     'the tail when over capacity. Both are O(1). For thread safety, guard '
                     'operations with one lock (simple) or use striping/segmenting for higher '
                     'concurrency. (LinkedHashMap with accessOrder=true and removeEldestEntry is '
                     'the library shortcut.) Bounded blocking queue: a circular array or linked '
                     'list, one lock, and two conditions (notFull, notEmpty): put(x): lock; while '
                     '(count == cap) notFull.await(); enqueue(x); notEmpty.signal(); unlock '
                     'take(): lock; while (count == 0) notEmpty.await(); x = dequeue(); '
                     'notFull.signal(); unlock Always use a while loop around await() (spurious '
                     'wakeups). The same can be written with synchronized, wait() and notifyAll().',
  'companies': ['Amazon', 'Google', 'Meta', 'Microsoft']},
 {'difficulty': 'hard',
  'question_text': 'How do dynamic proxies and CGLIB work, and how does Spring AOP use them?',
  'expected_answer': 'JDK dynamic proxy (java.lang.reflect.Proxy): creates a runtime class '
                     'implementing given interfaces; all calls go to an InvocationHandler. CGLIB '
                     '(or ByteBuddy): generates a subclass of the target at runtime, overriding '
                     'methods, so it works without interfaces. It cannot proxy final classes or '
                     'methods. Spring AOP wraps beans in such proxies to add cross-cutting '
                     'behavior (@Transactional, @Async, @Cacheable, logging). Known gotcha: '
                     'self-invocation (calling another proxied method on this) bypasses the proxy, '
                     'so the advice does not run.',
  'companies': ['Flipkart', 'Oracle', 'Goldman Sachs']},
 {'difficulty': 'hard',
  'question_text': 'Why can ThreadLocal leak memory in thread pools? What is false sharing, and '
                   'what does @Contended do?',
  'expected_answer': 'ThreadLocal values live in a map inside the Thread object. Pool threads live '
                     'for a long time, so values (and the classes or class loaders they reference) '
                     'are never released unless you call remove() in a finally. The map keys are '
                     'weak references, but values are strong, which causes stale entries. False '
                     'sharing: independent variables on the same CPU cache line (typically 64 '
                     'bytes) are written by different threads, forcing constant cache- line '
                     'invalidation and hurting performance. @jdk.internal.vm.annotation.Contended '
                     'pads fields so they occupy separate cache lines (needs '
                     "-XX:-RestrictContended outside the JDK); this is used in LongAdder's cells "
                     'and ConcurrentHashMap.',
  'companies': ['Goldman Sachs', 'Google']},
 {'difficulty': 'hard',
  'question_text': 'What are StampedLock, read-write locks and lock-free data structures? When is '
                   'each appropriate?',
  'expected_answer': 'ReentrantReadWriteLock: many concurrent readers or one writer; good for '
                     'read- heavy data, but can starve writers and has overhead. StampedLock: adds '
                     'an optimistic read mode: read without locking, then validate(stamp); fall '
                     'back to a real read lock on failure. Faster for very read-heavy cases, but '
                     'it is not reentrant and has no conditions. Lock-free structures '
                     '(ConcurrentLinkedQueue, ConcurrentSkipListMap, Disruptor- style ring '
                     'buffers): use CAS rather than locks, so there is no deadlock and better '
                     'scalability, but they are harder to reason about and can suffer from retry '
                     'storms. Choose the simplest option that meets contention needs; measure '
                     'before optimizing.',
  'companies': ['Goldman Sachs', 'Meta']},
 {'difficulty': 'hard',
  'question_text': 'Why was HashMap unsafe under concurrent resize in Java 7 (infinite loop)? What '
                   'changed later?',
  'expected_answer': "Java 7's resize reversed bucket linked lists while transferring entries "
                     '(head insertion). Two threads resizing at once could create a circular '
                     'reference in a bucket chain, so later get() calls looped forever and '
                     'consumed 100% CPU. Java 8 preserves node order during resize (tail insertion '
                     'with lo/hi lists), removing that specific loop. But HashMap is still not '
                     'thread safe (lost updates, stale reads, inconsistent state); use '
                     'ConcurrentHashMap.',
  'companies': ['Amazon', 'Flipkart']},
 {'difficulty': 'hard',
  'question_text': 'What are safepoints and stop-the-world pauses, and how do they affect '
                   'latency-sensitive systems?',
  'expected_answer': 'A safepoint is a point where all application threads are at a known state so '
                     'the JVM can perform global operations (GC phases, deoptimization, biased '
                     'lock revocation in old versions, thread dumps, class redefinition). Threads '
                     'must reach it before the pause starts; a long counted loop without a '
                     'safepoint poll, or a slow thread, causes time-to- safepoint delays. These '
                     'stop-the-world pauses add tail latency. Mitigations: low-pause collectors '
                     '(ZGC/Shenandoah), right-sized heaps, reducing allocation rate, pre-touching '
                     'memory (-XX:+AlwaysPreTouch), avoiding large pauses from logging, and '
                     'diagnosing with -Xlog:safepoint.',
  'companies': ['Goldman Sachs', 'Google']},
 {'difficulty': 'hard',
  'question_text': 'Explain records, sealed classes, pattern matching and the Java Module System '
                   '(JPMS). What problems do they solve?',
  'expected_answer': 'Records (Java 16): concise immutable data carriers; the compiler generates '
                     'constructor, accessors, equals, hashCode, toString. They replace boilerplate '
                     'DTOs. Sealed classes/interfaces (Java 17): sealed ... permits A, B restricts '
                     'which classes may extend a type, giving a closed hierarchy that enables '
                     'exhaustive checks. Pattern matching: instanceof patterns (if (o instanceof '
                     'String s)) and switch patterns (Java 21) remove casts and allow exhaustive, '
                     'type-based switches, combined with records for deconstruction. JPMS (Java '
                     '9): module-info.java declares what a module requires and exports, giving '
                     'strong encapsulation (no deep reflection into internals by default), '
                     'reliable configuration and smaller runtime images with jlink. Tip: for each '
                     'answer, practice explaining the "why" and one real-world trade-off. '
                     'Interviewers at the Hard level mostly probe depth, not memorized '
                     'definitions.',
  'companies': ['Oracle', 'Microsoft']}]

DIFFICULTIES = {
    "easy": QuestionDifficulty.EASY,
    "medium": QuestionDifficulty.MEDIUM,
    "hard": QuestionDifficulty.HARD,
}


def seed_java_questions() -> None:
    db = SessionLocal()
    try:
        topic = db.query(Topic).filter(Topic.name == TOPIC_NAME).first()
        if topic is None:
            topic = Topic(
                name=TOPIC_NAME,
                description=(
                    "Java interview questions covering core fundamentals, "
                    "collections, concurrency, JVM internals, and design."
                ),
                is_active=True,
            )
            db.add(topic)
            db.flush()
        else:
            topic.is_active = True

        existing_texts = {
            row[0]
            for row in db.query(Question.question_text)
            .filter(Question.topic_id == topic.id)
            .all()
        }

        inserted = 0
        for item in QUESTIONS:
            if item["question_text"] in existing_texts:
                continue
            db.add(
                Question(
                    topic_id=topic.id,
                    difficulty=DIFFICULTIES[item["difficulty"]],
                    question_text=item["question_text"],
                    expected_answer=item["expected_answer"],
                    companies=item["companies"],
                )
            )
            existing_texts.add(item["question_text"])
            inserted += 1

        db.commit()
        counts = {
            level: sum(1 for item in QUESTIONS if item["difficulty"] == level)
            for level in ("easy", "medium", "hard")
        }
        print(f"Java topic ID: {topic.id}")
        print(f"Inserted new questions: {inserted}")
        print(f"Question bank total in source: {len(QUESTIONS)}")
        print(f"Easy: {counts['easy']}, Medium: {counts['medium']}, Hard: {counts['hard']}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_java_questions()
