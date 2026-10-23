from __future__ import annotations

from collections import Counter

from app.database import SessionLocal
from app.enums.question_difficulty import QuestionDifficulty
from app.models.question import Question
from app.models.topic import Topic


TOPIC_NAME = "Rust"

# Extracted from "Rust Interview Questions by Difficulty (Easy, Medium, Hard).pdf".
# Company tags reflect the PDF's reported/typical interview-topic attributions,
# not confirmation that each company asked the exact question.
QUESTIONS = [{'difficulty': 'EASY',
  'question_text': 'What is Rust, and what are its key features?',
  'expected_answer': 'Rust is a statically typed, compiled systems programming language focused on memory '
                     'safety, performance and concurrency. Its key features are an ownership and borrowing '
                     'system that guarantees memory safety at compile time without a garbage collector, '
                     'zero- cost abstractions, no null pointers or data races in safe code, a strong type '
                     'system with traits and generics, pattern matching, and the Cargo build and package '
                     'manager. It targets the same space as C and C++ with far fewer memory-related bugs.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'Datadog',
                'SpaceX',
                'Tesla',
                'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What is ownership in Rust, and what are its rules?',
  'expected_answer': 'Ownership is the set of compile-time rules that manages memory without a garbage '
                     'collector. The rules are: each value has exactly one owner; there can be only one '
                     'owner at a time; and when the owner goes out of scope, the value is dropped and its '
                     'memory is freed. Assigning or passing an owned value to another variable or function '
                     'moves ownership, so the original variable can no longer be used.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'Datadog',
                'SpaceX',
                'Tesla',
                'Block',
                'Akamai']},
 {'difficulty': 'EASY',
  'question_text': 'What is borrowing, and what are the rules for references?',
  'expected_answer': 'Borrowing lets code use a value through a reference without taking ownership. &T is a '
                     'shared (immutable) reference and &mut T is an exclusive (mutable) reference. At any '
                     'time you may have either any number of shared references or exactly one mutable '
                     'reference to a value, never both, and references must never outlive the data they '
                     'point to. These rules prevent data races and dangling pointers at compile time.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'Datadog',
                'SpaceX',
                'Tesla',
                'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between move, copy and clone?',
  'expected_answer': 'A move transfers ownership; the source is invalidated. Types that implement the Copy '
                     'trait, such as integers, bool, char and tuples of copyable types, are duplicated '
                     'bit-for- bit on assignment, so both variables stay valid. Clone is an explicit, '
                     'possibly expensive deep copy requested by calling .clone(), as with String or Vec. A '
                     'type cannot be Copy if it owns heap data or implements Drop.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla']},
 {'difficulty': 'EASY',
  'question_text': 'How do let, let mut, shadowing and constants differ?',
  'expected_answer': 'Variables are immutable by default; let mut makes a binding mutable. Shadowing '
                     'declares a new variable with the same name using let, which can even change the type, '
                     'while the old one becomes inaccessible. const values must have an explicit type, are '
                     'evaluated at compile time and can be declared in any scope; they are always immutable.',
  'companies': ['Microsoft', 'Google', 'Meta', 'Amazon', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': "What are Rust's scalar and compound types, and how do arrays, slices and Vec differ?",
  'expected_answer': 'Scalar types are integers (i8 to i128, u8 to u128, isize, usize), floats (f32, f64), '
                     'bool and char. Compound types are tuples and arrays. An array [T; N] has a fixed '
                     'length known at compile time and lives on the stack; a Vec<T> is a growable, heap- '
                     'allocated vector; a slice &[T] is a borrowed view into a contiguous sequence of '
                     'elements with a length.',
  'companies': ['Microsoft', 'Google', 'Amazon', 'Arm', 'SpaceX', 'Tesla']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between String and &str?',
  'expected_answer': 'String is an owned, growable, heap-allocated UTF-8 string. &str is a borrowed string '
                     'slice, a pointer plus a length, pointing into a String, a literal in the binary or '
                     'other UTF-8 data. Functions should usually accept &str for flexibility, and use String '
                     'when they must own the text. Strings cannot be indexed by integer because characters '
                     'have variable byte width.',
  'companies': ['Microsoft', 'Google', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What are structs, enums and impl blocks?',
  'expected_answer': 'A struct groups named fields (or is a tuple struct or unit struct). An enum is a type '
                     'that is exactly one of several variants, and each variant can carry different data, '
                     'making Rust enums algebraic data types. An impl block attaches methods and associated '
                     'functions to a type; a method takes self, &self or &mut self, while an associated '
                     'function such as new does not take self.',
  'companies': ['Microsoft', 'Google', 'Meta', 'Amazon', 'Datadog', 'Block', 'Tesla']},
 {'difficulty': 'EASY',
  'question_text': 'Why does Rust have Option<T> instead of null?',
  'expected_answer': 'Null references cause a large class of runtime crashes. Rust encodes absence in the '
                     'type system with Option<T>, which is either Some(value) or None. Because Option<T> is '
                     'a different type from T, the compiler forces you to handle the None case before using '
                     'the value, through match, if let, or helper methods like unwrap_or and map.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Block', 'Datadog']},
 {'difficulty': 'EASY',
  'question_text': 'How does error handling work with Result<T, E>, and when does a program panic?',
  'expected_answer': 'Rust has no exceptions. Recoverable errors are values of type Result<T, E>, which is '
                     'Ok(T) or Err(E), and the caller must deal with them. Unrecoverable bugs trigger a '
                     'panic!, which unwinds or aborts the thread, as with an out-of-bounds index or unwrap() '
                     'on None. Libraries should return Result; panics are for violated invariants.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Block', 'SpaceX']},
 {'difficulty': 'EASY',
  'question_text': 'What does the ? operator do?',
  'expected_answer': 'The ? operator propagates errors concisely. On Ok(v) or Some(v) it evaluates to v; on '
                     'Err(e) or None it returns early from the current function, converting the error '
                     "through the From trait to the function's error type. It can only be used in functions "
                     'whose return type is compatible, such as Result or Option.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Cloudflare', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': 'How does match work, and what does exhaustive matching mean?',
  'expected_answer': 'match compares a value against patterns in order and runs the first arm that matches. '
                     'Matching is exhaustive: the compiler requires every possible value to be covered, so '
                     'adding a variant to an enum causes compile errors wherever it is not handled. Patterns '
                     'can destructure structs, tuples and enums, bind variables, use guards (if) and ranges, '
                     'and _ is the catch-all.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What is a trait?',
  'expected_answer': 'A trait defines shared behavior as a set of method signatures, optionally with default '
                     'implementations, similar to an interface. Types implement traits with impl Trait for '
                     'Type. Traits enable generic functions with bounds (T: Display), trait objects for '
                     'dynamic dispatch, and operator overloading through traits such as Add. Common standard '
                     'traits include Debug, Clone, Copy, PartialEq, Default and Iterator.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What are generics in Rust, and what is monomorphization?',
  'expected_answer': 'Generics let functions, structs and enums work over many types, such as Vec<T>. Bounds '
                     'restrict the type parameter to those implementing certain traits. Rust compiles '
                     'generics through monomorphization: the compiler generates a specialized copy of the '
                     'code for each concrete type used, so generics have no runtime cost, at the price of '
                     'larger binaries and longer compile times.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Arm', 'Cloudflare']},
 {'difficulty': 'EASY',
  'question_text': 'What is a lifetime in Rust, and why is it needed?',
  'expected_answer': 'A lifetime is the span of code for which a reference is valid. The borrow checker uses '
                     'lifetimes to ensure no reference outlives the data it points to, preventing dangling '
                     'pointers. Most lifetimes are inferred through elision rules; you write explicit '
                     "annotations like 'a when the compiler cannot tell how the lifetimes of inputs and "
                     'outputs relate, for example in a function returning one of two references.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla']},
 {'difficulty': 'EASY',
  'question_text': 'How do modules and visibility work?',
  'expected_answer': 'Modules (mod) organize code into namespaces, and use brings paths into scope. '
                     'Everything is private by default; pub makes an item visible outside its module, with '
                     'finer control such as pub(crate) for crate-wide visibility. A crate is a compilation '
                     'unit (a binary or a library), and a package can contain several crates described by '
                     'Cargo.toml.',
  'companies': ['Microsoft', 'Google', 'Amazon', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What are Cargo and crates?',
  'expected_answer': "Cargo is Rust's build tool and package manager: it compiles code, resolves "
                     'dependencies listed in Cargo.toml, runs tests (cargo test), builds docs and publishes '
                     'packages. Crates are Rust packages distributed through crates.io, and Cargo.lock pins '
                     'exact dependency versions for reproducible builds. Features and workspaces let you '
                     'configure optional functionality and manage multiple related crates.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Block', 'Arm']},
 {'difficulty': 'EASY',
  'question_text': 'What is Box<T>, and when would you use it?',
  'expected_answer': 'Box<T> is the simplest smart pointer: it allocates a value on the heap and owns it, '
                     'freeing it when the box is dropped. Use it for data whose size is not known at compile '
                     'time (such as recursive types like linked lists and trees), to move large values '
                     'without copying, and for trait objects (Box<dyn Trait>).',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'Datadog']},
 {'difficulty': 'EASY',
  'question_text': 'What does unsafe mean in Rust?',
  'expected_answer': 'unsafe lets you perform five operations the compiler cannot verify: dereferencing raw '
                     'pointers, calling unsafe functions, accessing or modifying mutable statics, '
                     'implementing unsafe traits, and accessing union fields. It does not turn off the '
                     "borrow checker. The programmer takes responsibility for upholding Rust's invariants "
                     'inside the block, so good practice is to keep unsafe small and wrap it in a safe API.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla', 'Akamai']},
 {'difficulty': 'EASY',
  'question_text': 'What is the difference between const and static?',
  'expected_answer': 'const is an inlined compile-time constant with no fixed memory address. static is a '
                     "single value with a fixed memory location for the whole program ('static lifetime); a "
                     'static mut is mutable but unsafe to access because of potential data races. Use const '
                     'for fixed values and static when you need one address, such as global tables or data '
                     'used in FFI and embedded code.',
  'companies': ['Arm', 'SpaceX', 'Tesla', 'Microsoft', 'Kepler']},
 {'difficulty': 'EASY',
  'question_text': 'How do macros differ from functions?',
  'expected_answer': 'Macros such as println! or vec! run at compile time and generate code, so they can '
                     'take a variable number of arguments, operate on syntax and produce items that '
                     'functions cannot. Declarative macros (macro_rules!) use pattern matching on syntax; '
                     'procedural macros (derive, attribute-like and function-like) are Rust programs that '
                     'transform token streams. They add power but make errors harder to read, so use '
                     'functions when possible.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Datadog', 'Block']},
 {'difficulty': 'EASY',
  'question_text': 'What is the Drop trait, and what is RAII?',
  'expected_answer': "RAII (resource acquisition is initialization) ties a resource's lifetime to an "
                     "object's lifetime. In Rust, the Drop trait's drop method runs automatically when an "
                     'owner goes out of scope, releasing memory, files, locks and sockets deterministically, '
                     'in reverse order of declaration. You cannot call drop directly; use std::mem::drop to '
                     'release a value early.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How do the stack and heap work in Rust, and what does the Sized trait mean?',
  'expected_answer': 'Values whose size is known at compile time are stored on the stack by default, and '
                     'stack data is freed automatically when a function returns. Heap data is allocated '
                     'explicitly through types such as Box, Vec and String, and freed when its owner is '
                     'dropped. The Sized trait marks types with a size known at compile time, and generic '
                     'parameters are Sized by default. Dynamically sized types such as str, [T] and dyn '
                     'Trait can only be used behind a pointer such as &, Box or Rc.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Arm', 'SpaceX', 'Tesla', 'Cloudflare']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the main collections in the standard library, and how do they compare?',
  'expected_answer': 'Vec<T> is a contiguous growable array with amortized O(1) push and O(1) index. '
                     'VecDeque<T> is a ring buffer with O(1) push and pop at both ends. HashMap<K, V> and '
                     'HashSet<T> give average O(1) lookup using a hash function (SipHash by default, which '
                     'resists hash-flooding attacks), with no ordering. BTreeMap and BTreeSet keep keys '
                     'sorted with O(log n) operations and support range queries. BinaryHeap is a priority '
                     'queue and LinkedList is rarely the best choice.',
  'companies': ['Google', 'Meta', 'Amazon', 'Microsoft', 'Datadog', 'Block', 'BlackRock']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How do iterators work, and what does lazy evaluation mean?',
  'expected_answer': 'An iterator is any type implementing the Iterator trait, whose core method is next() '
                     'returning Option<Item>. Adapters such as map, filter, take and zip are lazy: they '
                     'build a new iterator and do no work until a consumer such as collect, sum, fold or a '
                     'for loop drives it. Chained iterators compile to tight loops with no intermediate '
                     'allocations, so they are usually as fast as hand-written loops, which is an example of '
                     'a zero-cost abstraction. iter(), iter_mut() and into_iter() borrow, mutably borrow, or '
                     'consume the collection.',
  'companies': ['Google', 'Meta', 'Amazon', 'Microsoft', 'Datadog', 'Block', 'Cloudflare']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are closures, and how do Fn, FnMut and FnOnce differ?',
  'expected_answer': 'A closure is an anonymous function that can capture variables from its environment by '
                     'reference, mutable reference or by value. The compiler infers which of three traits it '
                     'implements: FnOnce (it may consume captured values, so it can be called only once), '
                     'FnMut (it mutates captured state and can be called repeatedly) and Fn (it only reads '
                     'captured state and can be called any number of times). Every closure implements '
                     'FnOnce; the move keyword forces capture by value, which is needed when sending '
                     'closures to other threads.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Datadog', 'Cloudflare', 'Block']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is the difference between static dispatch (generics) and dynamic dispatch (trait '
                   'objects)?',
  'expected_answer': 'With generics (fn f<T: Trait>(x: T) or impl Trait), the compiler monomorphizes a copy '
                     'per concrete type, so calls are resolved at compile time and can be inlined, at the '
                     'cost of code size. With a trait object (&dyn Trait or Box<dyn Trait>), the value is '
                     'accessed through a fat pointer holding a data pointer and a vtable pointer, so calls '
                     'are resolved at runtime with a small indirection cost, but one function handles many '
                     'types and collections can hold mixed types. Only object-safe traits can be made into '
                     'trait objects: no generic methods, and no returning Self.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'Datadog']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are Rc, Arc, RefCell and Mutex, and when would you use each?',
  'expected_answer': 'Rc<T> is a single-threaded reference-counted pointer for shared ownership; Arc<T> does '
                     'the same with atomic counters, so it is safe to share across threads. Both give shared '
                     'immutable access. For mutation, RefCell<T> enforces borrow rules at runtime for '
                     'single-threaded code (it panics on violation), and Mutex<T> or RwLock<T> provide '
                     'thread-safe interior mutability by locking. The common patterns are Rc<RefCell<T>> '
                     'within a thread and Arc<Mutex<T>> across threads.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Block']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What is interior mutability?',
  'expected_answer': 'Interior mutability lets you mutate data through a shared reference by moving the '
                     'borrow check from compile time to runtime or by using atomic operations. Cell<T> '
                     'copies values in and out for Copy types; RefCell<T> hands out borrowed references '
                     'checked at runtime; Mutex, RwLock and atomics do the same across threads. It is built '
                     'on UnsafeCell, the only primitive that makes shared mutation legal, and is used for '
                     'caches, counters and graph-like structures.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the lifetime elision rules, and how do lifetimes work in structs?',
  'expected_answer': 'There are three elision rules the compiler applies to function signatures: each '
                     'reference parameter gets its own lifetime; if there is exactly one input lifetime it '
                     'is assigned to all output lifetimes; and if there is a &self or &mut self parameter, '
                     'its lifetime is assigned to all outputs. When these cannot decide, you annotate '
                     "explicitly. A struct holding a reference needs a lifetime parameter (struct Parser<'a> "
                     "{ input: &'a str }) so the compiler knows the struct cannot outlive the data it "
                     "borrows. The 'static lifetime means the reference can live for the whole program.",
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How do you design error types in a Rust library versus an application?',
  'expected_answer': 'A library should expose a specific error type, usually an enum with one variant per '
                     'failure, implementing std::error::Error, Display and Debug, with From implementations '
                     'so ? converts underlying errors automatically; the thiserror crate removes the '
                     'boilerplate. An application can use a catch-all type such as Box<dyn Error> or the '
                     'anyhow crate, which adds context to errors and is easier to propagate to main. Keeping '
                     'errors as values rather than exceptions makes every failure path visible in function '
                     'signatures.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Cloudflare', 'Datadog', 'Block', 'BlackRock']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does concurrency work with threads and channels in Rust?',
  'expected_answer': "std::thread::spawn creates an OS thread and requires a 'static closure, so data is "
                     'moved in with move. Threads can communicate by message passing with std::sync::mpsc '
                     'channels (multiple producers, one consumer), where sending a value transfers '
                     'ownership, or by sharing state with Arc<Mutex<T>>. join waits for a thread and returns '
                     'its result, and a thread panic surfaces as an Err there. Scoped threads '
                     '(std::thread::scope) allow borrowing local data safely. The type system guarantees '
                     'that safe code cannot cause a data race.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Datadog',
                'Akamai',
                'SpaceX',
                'Tesla']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the Send and Sync traits?',
  'expected_answer': "Send means a value's ownership can be transferred to another thread; Sync means a "
                     'shared reference &T can be used from several threads, so T: Sync is equivalent to &T: '
                     "Send. They are auto traits: the compiler derives them from a type's fields. Rc<T> is "
                     'neither Send nor Sync because its counter is not atomic; Arc<T> is both when T is; '
                     'RefCell<T> is Send but not Sync; MutexGuard is not Send. These traits are how Rust '
                     'enforces thread safety at compile time.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Arm', 'SpaceX']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does async/await work in Rust, and what is a runtime such as Tokio for?',
  'expected_answer': 'An async fn returns a value implementing the Future trait, which is a state machine '
                     'generated by the compiler. Futures are lazy: nothing runs until they are polled. The '
                     'standard library defines Future and the async/ await syntax but not an executor, so a '
                     'runtime such as Tokio provides the scheduler, I/O reactor and timers; it polls futures '
                     'and wakes them when an I/O event makes progress possible. Async suits many concurrent '
                     'I/O-bound tasks, but blocking code inside an async task stalls other tasks on that '
                     'thread.',
  'companies': ['Cloudflare', 'Amazon', 'Microsoft', 'Google', 'Meta', 'Datadog', 'Block', 'Akamai']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are self, &self and &mut self, and how does method call syntax work?',
  'expected_answer': 'The first parameter of a method determines how it uses the instance: self takes '
                     'ownership (the value is consumed), &self borrows immutably, and &mut self borrows '
                     'mutably. The call value.method() automatically adds a reference or dereference to '
                     'match the receiver (automatic referencing and dereferencing). Associated functions '
                     'without self, such as constructors named new, are called with Type::function(). '
                     'Builder patterns often use self to chain calls by value.',
  'companies': ['Microsoft', 'Google', 'Meta', 'Amazon', 'Block', 'Datadog']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What do #[derive] and the common derivable traits do?',
  'expected_answer': '#[derive(...)] asks the compiler to generate standard trait implementations. Debug '
                     'enables {:?} formatting; Clone and Copy copy values; PartialEq and Eq enable == (with '
                     'Eq meaning equality is reflexive, which floats are not); PartialOrd and Ord enable '
                     'ordering; Hash allows use as a HashMap key and must agree with Eq; Default provides a '
                     'default value. Floats implement PartialEq and PartialOrd but not Eq or Ord because of '
                     'NaN.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Block', 'Datadog', 'BlackRock']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does operator overloading work, and what is Deref coercion?',
  'expected_answer': 'Operators map to traits in std::ops: implementing Add gives +, Index gives [], and so '
                     'on, with associated types for the output. The Deref trait lets a type behave like a '
                     'reference to another type; deref coercion makes the compiler automatically convert '
                     '&String to &str, &Vec<T> to &[T] and &Box<T> to &T where a function expects the target '
                     'type. This is why functions taking &str accept &String arguments.',
  'companies': ['Microsoft', 'Google', 'Meta', 'Amazon', 'Arm', 'Block']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are the common Option and Result combinators?',
  'expected_answer': 'map transforms the inner value; and_then chains operations that may themselves fail; '
                     'unwrap_or, unwrap_or_else and unwrap_or_default supply fallbacks; ok_or and ok_or_else '
                     'convert an Option into a Result; map_err transforms an error; ok() turns a Result into '
                     'an Option; and ? propagates early. Avoid unwrap and expect in production code except '
                     'where an invariant guarantees success, because they panic.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Block', 'Datadog', 'Cloudflare']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does testing work in Rust?',
  'expected_answer': 'Cargo has built-in support for three kinds of tests. Unit tests live in the same file '
                     'inside a #[cfg(test)] mod tests block and can test private functions. Integration '
                     'tests live in the tests/ directory and use only the public API, each file being a '
                     'separate crate. Doc tests are code examples in documentation comments that are '
                     'compiled and run, keeping docs correct. Tests use #[test] with assert!, assert_eq! and '
                     '#[should_panic], and cargo test runs them in parallel by default.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Cloudflare', 'Datadog', 'Block', 'SpaceX', 'Tesla']},
 {'difficulty': 'MEDIUM',
  'question_text': 'What are Cargo features, workspaces and editions, and how does semantic versioning '
                   'apply?',
  'expected_answer': 'Features are optional compile-time flags in Cargo.toml that enable optional code or '
                     'dependencies. A workspace groups several crates that share one Cargo.lock and one '
                     'target directory. Editions (2015, 2018, 2021, 2024) are opt-in sets of language '
                     'changes that remain interoperable, so crates of different editions can depend on each '
                     'other. Cargo follows semantic versioning: a caret requirement such as 1.2 accepts '
                     'compatible updates up to the next major version, and Cargo.lock fixes the exact '
                     'versions used.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Cloudflare', 'Datadog', 'Block', 'Arm']},
 {'difficulty': 'MEDIUM',
  'question_text': "Why can't you index a String by integer, and how do characters and bytes differ?",
  'expected_answer': 'String is stored as UTF-8, where one Unicode character can take one to four bytes, so '
                     'an integer index would be ambiguous (a byte or a character?) and O(1) character '
                     'indexing is impossible. Rust offers explicit views: .bytes() for raw bytes, .chars() '
                     'for Unicode scalar values and slicing by byte range like &s[0..2], which panics if the '
                     'range cuts through a character. For user-perceived characters (grapheme clusters), a '
                     'crate such as unicode-segmentation is needed.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Cloudflare', 'Datadog', 'Block']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does Rust handle integer overflow?',
  'expected_answer': 'In debug builds, arithmetic overflow causes a panic; in release builds, by default it '
                     "wraps in two's complement, though this can be configured. Explicit methods give "
                     'predictable behavior in every build: checked_add returns Option, wrapping_add wraps, '
                     'saturating_add clamps at the limit, and overflowing_add returns the value plus a flag. '
                     'Safety-critical, embedded and financial code should use checked or saturating '
                     'operations, or types like Decimal, because silent wrapping is a classic source of '
                     'bugs.',
  'companies': ['SpaceX', 'Tesla', 'Arm', 'BlackRock', 'Goldman Sachs', 'Block', 'Kepler']},
 {'difficulty': 'MEDIUM',
  'question_text': 'How does Rust compare with C++ and Go?',
  'expected_answer': 'Compared with C++, Rust gives similar performance and control but enforces memory and '
                     'thread safety at compile time, has no undefined behavior in safe code, and has a '
                     'modern package manager, at the cost of a steeper learning curve, longer compile times '
                     'and a younger ecosystem. Compared with Go, Rust has no garbage collector and no '
                     'runtime pauses, richer generics and enums, and finer control, whereas Go is simpler, '
                     'compiles faster and has built-in goroutines. Choose Rust for performance-critical, '
                     'safety- critical or low-level components.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'SpaceX',
                'Tesla',
                'Datadog',
                'BlackRock']},
 {'difficulty': 'MEDIUM',
  'question_text': 'Can Rust leak memory, and what is a reference cycle?',
  'expected_answer': 'Yes: memory leaks are considered safe in Rust, because the guarantees cover memory '
                     'safety, not leak freedom. Calling mem::forget, using Box::leak, or building a '
                     'reference cycle with Rc<RefCell<T>> (two values pointing to each other, so their '
                     'counts never reach zero) all leak. To avoid cycles, use Weak<T>, which holds a '
                     'non-owning reference that does not keep the value alive and must be upgraded to an Rc '
                     'before use, returning None if the value is gone.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog']},
 {'difficulty': 'HARD',
  'question_text': 'How does the borrow checker work internally, and what are non-lexical lifetimes?',
  'expected_answer': "The borrow checker runs on the compiler's mid-level IR (MIR) and builds a control-flow "
                     'graph of the function. Each borrow gets a lifetime region, and the checker verifies '
                     'that no conflicting access happens while a borrow is live and that no reference '
                     'outlives its referent. Before Rust 2018, a borrow lasted until the end of its lexical '
                     'scope; with non- lexical lifetimes (NLL), a borrow lasts only as long as the reference '
                     'is actually used afterward, so more correct programs are accepted. Two-phase borrows '
                     'allow patterns like v.push(v.len()), where a mutable borrow is reserved first and '
                     'activated later. The checker is conservative: it may reject sound programs (for '
                     'example some conditional return of a borrow, which the future Polonius analysis aims '
                     'to accept).',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla']},
 {'difficulty': 'HARD',
  'question_text': 'Explain variance and subtyping for lifetimes, and why &mut T is invariant in T.',
  'expected_answer': "Subtyping in Rust applies to lifetimes: a longer lifetime 'long is a subtype of a "
                     "shorter one 'short, so &'long T can be used where &'short T is expected. Covariant "
                     "types (such as &'a T, Box<T>, Vec<T>) keep the direction of subtyping; contravariant "
                     "positions (function arguments, as in fn(&'a T)) reverse it; invariant types (such as "
                     '&mut T and Cell<T> in T) allow no substitution. &mut T must be invariant in T, '
                     "otherwise you could store a short-lived reference through a &mut &'long str that was "
                     "coerced to &mut &'short str, creating a dangling reference after the short lifetime "
                     'ends. PhantomData<T> tells the compiler which variance and drop-check behavior a type '
                     'has when it holds no real field of type T.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Arm', 'Cloudflare']},
 {'difficulty': 'HARD',
  'question_text': "What are higher-ranked trait bounds ( for<'a>), and when are they needed?",
  'expected_answer': "A bound like F: for<'a> Fn(&'a str) -> &'a str says that F must work for every "
                     "possible lifetime 'a, not for one specific lifetime chosen by the caller. It is needed "
                     'when a closure or function is called with references whose lifetimes are created '
                     'inside the generic function itself, for example calling a callback on a local string. '
                     'Without it, the compiler would require one fixed lifetime that outlives the whole '
                     "function. In most closure signatures the compiler applies for<'a> implicitly through "
                     'elision (Fn(&str) -> &str), so explicit HRTBs appear mainly in more complex trait '
                     'bounds.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare']},
 {'difficulty': 'HARD',
  'question_text': 'What are Pin and Unpin, and why do futures need them?',
  'expected_answer': 'An async block compiles to a state machine that may hold references to its own fields '
                     'across an .await, which makes it a self-referential struct. Moving such a value in '
                     'memory would leave those internal pointers dangling. Pin<P> wraps a pointer and '
                     'guarantees that the pointee will not be moved until it is dropped (unless it '
                     'implements Unpin). Unpin is an auto trait meaning "moving this type is harmless", true '
                     'for most ordinary types. Future::poll takes Pin<&mut Self> so executors can poll '
                     'futures safely; pinning on the heap (Box::pin) or the stack (pin!) is how you hold a '
                     '!Unpin future.',
  'companies': ['Cloudflare', 'Amazon', 'Microsoft', 'Google', 'Meta', 'Datadog', 'Block']},
 {'difficulty': 'HARD',
  'question_text': 'What exactly happens at an .await, what is cancellation safety, and why must some '
                   'futures be Send?',
  'expected_answer': 'At an .await the generated state machine polls the inner future; if it returns '
                     'Pending, the outer future saves its local variables into its own state, records the '
                     'resume point and returns Pending to the executor, which will poll again after the '
                     "waker fires. Because the future's state is just data, dropping a future cancels it at "
                     'its last .await. A future is cancellation safe if dropping it at any await point loses '
                     'no data or leaves no inconsistent state; for example tokio::select! drops the losing '
                     'branches, so a read that consumed bytes into a local buffer before being dropped is '
                     'not cancellation safe. On a work-stealing multi-threaded runtime, tasks may move '
                     'between threads at an await, so the future must be Send, which means everything held '
                     'across an .await (such as an Rc or a MutexGuard from std::sync) must be Send.',
  'companies': ['Cloudflare', 'Amazon', 'Microsoft', 'Google', 'Meta', 'Datadog', 'Akamai']},
 {'difficulty': 'HARD',
  'question_text': 'Explain atomics and memory ordering: Relaxed, Acquire, Release, AcqRel and SeqCst.',
  'expected_answer': 'Rust follows the C++20 memory model. Atomic operations are indivisible, but ordering '
                     'defines how they synchronize other memory accesses. Relaxed guarantees only atomicity '
                     'and per-variable modification order, which is enough for counters. A Release store '
                     'paired with an Acquire load of the same variable creates a happens-before edge: '
                     'everything the writer did before the release is visible to the reader after the '
                     'acquire, which is how you publish data safely (for example in a spinlock or a flag). '
                     'AcqRel combines both for read-modify-write operations. SeqCst additionally enforces a '
                     'single global total order of all SeqCst operations, the easiest to reason about and '
                     'the most costly on weakly ordered CPUs such as ARM. Choosing weaker orderings requires '
                     'proving correctness, and tools such as Loom and Miri help to check them.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'Datadog', 'SpaceX']},
 {'difficulty': 'HARD',
  'question_text': 'What does Rust\'s "fearless concurrency" not prevent? Discuss deadlocks, race conditions '
                   'and mutex poisoning.',
  'expected_answer': 'Safe Rust prevents data races (unsynchronized concurrent access where at least one is '
                     'a write) but not general race conditions (logic whose outcome depends on timing, such '
                     'as check-then-act on separate locks), nor deadlocks (two threads waiting on each '
                     "other's locks), nor starvation. A Mutex becomes poisoned if a thread panics while "
                     'holding the lock; later lock() calls return an Err containing the guard so you can '
                     'choose to recover or propagate, since the protected data may be inconsistent. To '
                     'reduce deadlocks, acquire locks in a fixed order, keep critical sections short, avoid '
                     'holding locks across .await, and consider channels or lock-free designs.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Datadog',
                'Goldman Sachs',
                'BlackRock',
                'Block']},
 {'difficulty': 'HARD',
  'question_text': 'What is the ABA problem in lock-free programming, and how do crates like crossbeam '
                   'address safe memory reclamation?',
  'expected_answer': 'In a compare-and-swap loop, a thread reads value A, is paused, and meanwhile other '
                     'threads change it to B and back to A (possibly freeing and reallocating the node); the '
                     "first thread's CAS succeeds although the structure changed, which can corrupt a "
                     'lock-free stack or queue. Solutions include tagged pointers (version counters), hazard '
                     'pointers, and epoch-based reclamation as used by crossbeam-epoch: threads pin an epoch '
                     'while they access shared nodes, and removed nodes are freed only after all threads '
                     'have moved past that epoch, so a node cannot be reused while anyone may still hold a '
                     'pointer to it. Garbage-collected languages mostly avoid this, whereas Rust needs '
                     'explicit reclamation schemes.',
  'companies': ['Google', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'Tesla', 'SpaceX']},
 {'difficulty': 'HARD',
  'question_text': 'What are the invariants you must uphold in unsafe code, and what counts as undefined '
                   'behavior?',
  'expected_answer': 'Unsafe code must preserve everything safe code relies on, so that a safe API built on '
                     'it is sound (no safe use can cause undefined behavior). Undefined behavior includes: '
                     'dereferencing dangling or misaligned pointers, data races, violating aliasing rules '
                     '(having a &mut T while any other reference to the same data is used), producing '
                     'invalid values (a bool that is not 0 or 1, a null &T, an invalid enum discriminant), '
                     'reading uninitialized memory (use MaybeUninit instead), and breaking the validity '
                     'rules of str as UTF-8. Aliasing models such as Stacked Borrows and Tree Borrows '
                     'describe the rules, and Miri is an interpreter that detects many violations. Good '
                     'practice is to minimize unsafe, document // SAFETY: comments for each block, and '
                     'expose a safe wrapper.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'SpaceX',
                'Tesla',
                'Kepler',
                'Akamai']},
 {'difficulty': 'HARD',
  'question_text': 'How does FFI work in Rust: extern "C", #[repr(C)], ownership across the boundary and '
                   'panics?',
  'expected_answer': 'extern "C" selects the C calling convention, #[no_mangle] keeps symbol names stable, '
                     "and #[repr(C)] gives structs a C-compatible layout, because Rust's default layout is "
                     'unspecified and may reorder fields. Types such as CString, CStr and raw pointers cross '
                     'the boundary; ownership rules must be documented, for example memory allocated by Rust '
                     "must be freed by Rust (Box::into_raw and Box::from_raw), never by C's free. A panic "
                     'must not unwind across an FFI boundary (that is undefined behavior unless extern '
                     '"C-unwind" is used), so wrap entry points in catch_unwind or build with panic=abort. '
                     'Tools bindgen and cbindgen generate bindings in each direction, which is how companies '
                     'adopt Rust incrementally in C and C++ codebases.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'Tesla',
                'SpaceX',
                'Block',
                'Kepler']},
 {'difficulty': 'HARD',
  'question_text': 'How is data laid out in memory: repr(Rust) vs repr(C), alignment, padding, niche '
                   'optimization and zero-sized types?',
  'expected_answer': 'With the default representation, the compiler may reorder fields to minimize padding, '
                     'so you cannot rely on layout. repr(C) fixes C field order and padding rules, '
                     'repr(transparent) guarantees a single-field wrapper has the same layout as its field, '
                     'and repr(packed) removes padding at the cost of unaligned access. Each type has a size '
                     'and an alignment, and size is always a multiple of alignment. Niche optimization uses '
                     'invalid bit patterns to store enum discriminants: Option<&T>, Option<Box<T>> and '
                     'Option<NonZeroU32> are the same size as the underlying type because null (or zero) '
                     'represents None. Zero-sized types (unit (), empty structs, PhantomData) occupy no '
                     'space, which lets generic code such as HashSet<T> (a HashMap<T, ()>) cost nothing for '
                     'the unused part.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Arm', 'SpaceX', 'Tesla', 'Cloudflare']},
 {'difficulty': 'HARD',
  'question_text': 'Associated types vs generic type parameters in traits; the orphan rule and coherence; '
                   'blanket implementations.',
  'expected_answer': 'Use an associated type when each implementing type has exactly one natural choice (an '
                     'Iterator has one Item), which also keeps signatures shorter; use a generic parameter '
                     'when a type can implement the trait several ways (From<A> and From<B> for the same '
                     'type). Coherence requires that, for any type and trait, at most one implementation '
                     'applies; the orphan rule enforces this by allowing an implementation only if the trait '
                     'or the type is local to your crate, which prevents two crates from supplying '
                     'conflicting implementations. Blanket implementations (impl<T: Display> ToString for T) '
                     'provide a trait for all types meeting a bound, which is powerful but means adding such '
                     'an impl in a library can be a breaking change. The newtype pattern works around the '
                     'orphan rule.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Block']},
 {'difficulty': 'HARD',
  'question_text': 'What does it mean for a trait to be dyn-compatible (object-safe), and how are trait '
                   'objects laid out?',
  'expected_answer': 'A trait is dyn-compatible if the compiler can build a vtable for it: methods must not '
                     'be generic over type parameters, must not return Self by value, and the trait must not '
                     'require Sized. A &dyn Trait or Box<dyn Trait> is a fat pointer of two words: a pointer '
                     'to the data and a pointer to a vtable, which holds the drop function, the size and '
                     "alignment, and function pointers for the trait's methods. Calls go through the vtable "
                     '(one indirection, usually not inlinable). Methods that do not fit can be excluded with '
                     'where Self: Sized, and dyn Any allows downcasting with a type ID.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog']},
 {'difficulty': 'HARD',
  'question_text': 'Describe drop order, ManuallyDrop, mem::forget, and why leaking is safe but a Drop '
                   'guarantee is not.',
  'expected_answer': 'Local variables are dropped in reverse order of declaration; struct fields are dropped '
                     "in declaration order after the struct's own Drop::drop runs; temporaries are dropped "
                     'at the end of their statement. ManuallyDrop<T> suppresses automatic drop so unsafe '
                     'code can control it, and mem::forget consumes a value without running its destructor. '
                     'Because leaking is safe (it can happen through reference cycles or forget), unsafe '
                     'code must never rely on a destructor to maintain memory safety; this was the '
                     '"leakpocalypse" lesson that removed the original scoped-thread API and led to '
                     'closure-based thread::scope. Destructors are also not run on process::exit, aborts or '
                     'panic=abort.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Arm', 'Cloudflare', 'Tesla', 'SpaceX']},
 {'difficulty': 'HARD',
  'question_text': 'What are const fn, const generics and procedural macros, and how do they affect compile '
                   'times?',
  'expected_answer': 'const fn functions can be evaluated at compile time, which allows building lookup '
                     'tables or validating values with no runtime cost. Const generics let types be '
                     'parameterized by constant values, such as [T; N] or a fixed-capacity buffer '
                     'Buffer<const N: usize>. Procedural macros (derive, attribute and function-like) are '
                     "compiled Rust programs that take a token stream and return a new one, powering serde's "
                     'derives; they are unhygienic in some ways and can hurt compile times and error '
                     'quality. Compile time in Rust is dominated by monomorphization, LLVM optimization and '
                     'heavy macro use; mitigations include splitting into crates, avoiding unnecessary '
                     'generics at crate boundaries (use dyn or non-generic inner functions), incremental '
                     'compilation, and tuning codegen-units and LTO.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Arm', 'Datadog', 'Cloudflare']},
 {'difficulty': 'HARD',
  'question_text': 'What does "zero-cost abstraction" actually mean, and where do hidden costs remain?',
  'expected_answer': 'It means you do not pay at runtime for an abstraction you do not use, and what you do '
                     'use is as fast as hand-written code. Iterators, closures and generics compile down to '
                     'the same machine code as manual loops thanks to monomorphization and inlining. Costs '
                     'that remain: bounds checks on indexing (often eliminated by the optimizer or avoided '
                     'with iterators or get_unchecked), overflow checks in debug builds, reference counting '
                     'in Rc and Arc, vtable indirection for dyn, code bloat from monomorphization, and '
                     'allocations hidden in String, Vec and Box. Real performance work uses profiling (perf, '
                     'flamegraphs), benchmarking with criterion, and inspecting assembly rather than '
                     'assuming.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla', 'Datadog']},
 {'difficulty': 'HARD',
  'question_text': 'What changes in no_std and embedded Rust: core, alloc, std, panic handlers, allocators '
                   'and interrupts?',
  'expected_answer': '#![no_std] programs do not link the standard library. core provides language '
                     'primitives (Option, Result, iterators, atomics, fmt) with no OS or heap; alloc adds '
                     'heap types (Box, Vec, String) once you supply a global allocator; std adds threads, '
                     'files, networking and the OS. You must provide a panic handler (for example loop '
                     'forever, reset or log over a debug channel) and the entry point, and on '
                     'microcontrollers you typically use crates such as cortex-m and the embedded-hal traits '
                     'for hardware portability. Interrupt handlers share state with main code, so use '
                     'critical sections, atomics or Mutex- like wrappers from embedded crates rather than '
                     'static mut. Real-time systems avoid heap allocation, bound worst-case execution time, '
                     'and prefer fixed-capacity collections such as heapless.',
  'companies': ['SpaceX', 'Tesla', 'Arm', 'Kepler']},
 {'difficulty': 'HARD',
  'question_text': 'How do allocators work in Rust: the GlobalAlloc trait, jemalloc or mimalloc, and arena '
                   'allocation?',
  'expected_answer': 'The default global allocator is the system allocator, replaceable with # '
                     '[global_allocator] and any type implementing GlobalAlloc (alloc, dealloc, realloc). '
                     'Alternatives such as jemalloc and mimalloc reduce fragmentation and lock contention '
                     'for multithreaded servers. Arena (bump) allocators (such as bumpalo) allocate quickly '
                     'by incrementing a pointer and free everything at once, ideal for per- request or '
                     'per-phase data, at the cost of not freeing individual objects. The unstable Allocator '
                     'trait would allow per-collection allocators. Allocation strategy affects latency, '
                     'memory footprint and fragmentation, so measure before and after changing it.',
  'companies': ['Google', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Akamai', 'Arm']},
 {'difficulty': 'HARD',
  'question_text': 'How would you architect a high-throughput network proxy or service in Rust, considering '
                   'runtime model, backpressure and cancellation?',
  'expected_answer': 'Choose the runtime model: a work-stealing multi-threaded async runtime balances load '
                     'automatically but requires Send futures and some cross-thread synchronization; a '
                     'thread-per-core or sharded design avoids shared state and cache contention, at the '
                     'cost of load imbalance. Keep the hot path allocation-light and non-blocking, with '
                     'blocking work offloaded to a separate pool. Apply backpressure with bounded channels, '
                     'semaphores and limits on connections and in-flight requests so that overload slows '
                     'producers instead of exhausting memory. Handle cancellation deliberately (timeouts, '
                     'shutdown signals, cancellation-safe operations), reuse connections, and instrument '
                     'with tracing and metrics. Isolate the unsafe or FFI parts, and load-test to find tail '
                     'latency problems.',
  'companies': ['Cloudflare', 'Akamai', 'Amazon', 'Google', 'Meta', 'Datadog', 'Microsoft']},
 {'difficulty': 'HARD',
  'question_text': 'Unwinding vs abort: what is panic=abort, catch_unwind and UnwindSafe?',
  'expected_answer': 'By default a panic unwinds the stack, running destructors, and can be caught at a '
                     'thread boundary or with catch_unwind. With panic = "abort" in the Cargo profile, a '
                     'panic aborts the process immediately, producing smaller and faster binaries, and is '
                     'common in embedded systems and when panics should be fatal. catch_unwind should be '
                     'rare (for example at FFI boundaries or to isolate a task), because the data may be '
                     'left in a broken state. UnwindSafe and RefUnwindSafe are marker traits that warn when '
                     'a closure captures state that might be observed half-modified after a caught panic, '
                     'and Mutex poisoning serves a similar purpose.',
  'companies': ['Google', 'Microsoft', 'Amazon', 'Cloudflare', 'Arm', 'SpaceX', 'Tesla', 'Block']},
 {'difficulty': 'HARD',
  'question_text': 'What guarantees does Rust give, and what does it not guarantee?',
  'expected_answer': 'Safe Rust guarantees memory safety (no use-after-free, double free, buffer overflow or '
                     'null dereference) and freedom from data races, and typed errors force handling of '
                     'failures. It does not guarantee absence of logic bugs, deadlocks, memory leaks, '
                     'integer overflow in release builds, panics (such as an out-of-bounds index or unwrap '
                     'on None), resource exhaustion, timing correctness, or safety of the unsafe code and C '
                     'libraries it calls. Rust therefore reduces a large class of security vulnerabilities, '
                     'but systems still need testing, fuzzing, code review, formal methods for critical '
                     'logic and careful dependency auditing (cargo audit, cargo deny).',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'SpaceX',
                'Tesla',
                'BlackRock',
                'Goldman Sachs',
                'Block']},
 {'difficulty': 'HARD',
  'question_text': 'How do AsRef, Borrow, Into, Cow and impl Trait shape flexible API design?',
  'expected_answer': 'AsRef<T> lets a function accept anything cheaply viewable as &T (for example '
                     'AsRef<str> accepts String and &str). Into<T> accepts any value convertible into T, '
                     'useful for taking ownership flexibly (name: impl Into<String>). Borrow<T> is stricter, '
                     'requiring that the borrowed form hashes and compares identically, which is why '
                     "HashMap<String, V> can be queried with a &str. Cow<'a, B> (clone on write) holds "
                     'either a borrowed or owned value and allocates only when modification is needed, ideal '
                     'for functions that sometimes change their input. impl Trait in argument position is '
                     'sugar for a generic, and in return position hides a concrete type (such as an iterator '
                     'or closure) from the caller without boxing.',
  'companies': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Cloudflare', 'Datadog', 'Block']},
 {'difficulty': 'HARD',
  'question_text': 'How would you introduce Rust into an existing C or C++ codebase or team, and what are '
                   'the trade-offs?',
  'expected_answer': 'Start with new, isolated components or the most security-sensitive parsers and '
                     'network- facing code, where memory-safety bugs are costly, and integrate through FFI '
                     '(cxx, bindgen, cbindgen) so Rust and C++ can coexist and be replaced incrementally '
                     'rather than rewritten at once. Establish build integration (Cargo with Bazel, CMake or '
                     'other build systems), coding guidelines for unsafe, dependency review and CI with '
                     'clippy, rustfmt, Miri and fuzzing. Trade-offs include a steep learning curve for '
                     'ownership and lifetimes, longer compile times, a smaller hiring pool, ABI and '
                     'interoperability limits (no stable Rust ABI), and a younger ecosystem in areas like '
                     'certified safety-critical tooling. Benefits include fewer memory-safety defects, safer '
                     'concurrency and more confident refactoring.',
  'companies': ['Google',
                'Microsoft',
                'Meta',
                'Amazon',
                'Cloudflare',
                'Arm',
                'SpaceX',
                'Tesla',
                'Datadog',
                'Block',
                'BlackRock']}]


def seed_rust_questions() -> None:
    db = SessionLocal()
    try:
        topic = db.query(Topic).filter(Topic.name == TOPIC_NAME).first()
        if topic is None:
            raise RuntimeError(
                "The Rust topic does not exist. Create the Rust topic in the app/database first; "
                "this seeder will not create a duplicate topic."
            )
        if not topic.is_active:
            raise RuntimeError(f"The Rust topic (ID: {topic.id}) is inactive. Activate it first.")

        existing_count = db.query(Question).filter(Question.topic_id == topic.id).count()
        if existing_count > 0:
            print(f"Rust topic (ID: {topic.id}) already contains {existing_count} question(s).")
            print("No questions were inserted to avoid duplicates.")
            print("Inspect existing Rust questions before deciding whether to seed again.")
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
        print("RUST THEORY QUESTION BANK CREATED")
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
    seed_rust_questions()
