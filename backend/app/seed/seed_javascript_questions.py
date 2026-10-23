from __future__ import annotations

from collections import Counter

from app.database import SessionLocal
from app.enums.question_difficulty import QuestionDifficulty
from app.models.question import Question
from app.models.topic import Topic


TOPIC_NAME = "JavaScript"

# Extracted from "JavaScript Interview Questions with Answers (Top Companies).pdf".
# Company labels are reported/inferred attributions from the PDF, not official question banks.
QUESTIONS = [
    {
        "difficulty": "EASY",
        "question_text": "What is JavaScript? What are its main characteristics?",
        "expected_answer": "JavaScript is a high-level, dynamically typed, multi-paradigm language (object-oriented via prototypes, functional and event-driven) that runs in browsers and, with Node.js, on servers. It is single-threaded per execution context with a non-blocking, event-driven model, runs on engines that use just-in-time compilation (V8, SpiderMonkey, JavaScriptCore), and is standardized as ECMAScript. Java and JavaScript are unrelated languages.",
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
        "question_text": "What is the difference between var , let and const ?",
        "expected_answer": "var : function scoped, hoisted and initialized as undefined , can be redeclared. let : block scoped, hoisted but not usable before its declaration (temporal dead zone), cannot be redeclared in the same scope. const : block scoped like let , must be initialized and cannot be reassigned. The value is not made immutable: a const object can still be mutated. Prefer const by default, let when reassigning, and avoid var .",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Amazon",
            "Meta"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are the data types in JavaScript?",
        "expected_answer": "Seven primitives: string , number , boolean , undefined , null , symbol and bigint , which are immutable and compared by value. Everything else is an object (including arrays, functions, dates and maps), compared by reference. typeof null returns \"object\" (a historical bug), typeof a function returns \"function\" , and arrays report \"object\" , so use Array.isArray .",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between == and === ?",
        "expected_answer": "=== (strict equality) compares value and type without conversion. == (loose equality) applies type coercion before comparing, which produces surprises ( 0 == \"\" is true, null == undefined is true, NaN is not equal to itself). Use === by default; Object.is additionally distinguishes +0 from -0 and treats NaN as equal to itself.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Goldman Sachs",
            "Meta"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between undefined , null and NaN ?",
        "expected_answer": "undefined means a variable was declared but has no value (or a missing property or argument). null is an intentional \"no value\" assigned by the programmer. NaN (Not-a- Number) is a numeric value produced by invalid math operations, and its type is number . Check it with Number.isNaN , not with equality.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is hoisting? What is the temporal dead zone?",
        "expected_answer": "Before code runs, declarations are processed during creation of the execution context, so they appear \"moved to the top\". Function declarations are hoisted with their body; var variables are hoisted as undefined ; let , const and class are hoisted but cannot be accessed until their declaration runs, and that gap is the temporal dead zone (access throws a ReferenceError ). Function expressions and arrow functions are not hoisted as callable values.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Meta",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is scope? What is lexical scope?",
        "expected_answer": "Scope determines where a variable is accessible: global, function and block scope (plus module scope). Lexical (static) scope means that a function's accessible variables are determined by where it is written in the source, not where it is called. Name lookup walks outward through the scope chain until it finds the variable or reaches the global scope.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Meta",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between function declarations, function expressions and arrow functions?",
        "expected_answer": "A declaration is hoisted and callable before its position; an expression is created when execution reaches it. Arrow functions (ES6) have shorter syntax and differ in important ways: no own this (they use the enclosing one), no own arguments , cannot be used with new , and have no prototype , so they suit callbacks but not methods that need their own this or constructors.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Meta",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What does the this keyword refer to?",
        "expected_answer": "this is determined by how a function is called: as a method it is the object before the dot; as a plain function it is undefined in strict mode (the global object in sloppy mode); with new it is the new object; with call , apply or bind it is whatever you pass; in an arrow function it is inherited from the enclosing scope. At the top level of a module it is undefined .",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Meta",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is a closure?",
        "expected_answer": "A closure is a function together with the lexical environment in which it was created, so it can keep accessing the outer function's variables even after the outer function has returned. Uses: data privacy (module pattern), function factories, callbacks, memoization and partial application. Caution: closures keep variables alive, which can retain memory, and var in loops causes the classic shared-variable bug that let fixes.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Meta",
            "Amazon",
            "Google"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are map , filter , reduce and forEach ?",
        "expected_answer": "These are array methods that take callbacks. forEach runs a function per element and returns nothing; map returns a new array of transformed elements; filter returns a new array of elements that pass a test; reduce folds the array into a single value using an accumulator. map , filter and reduce do not mutate the original array, and they can be chained.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Amazon",
            "Akamai",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are objects and how do you create them?",
        "expected_answer": "Objects are collections of key-value properties (keys are strings or symbols). They can be created with object literals, constructor functions with new , Object.create(proto) , ES6 class syntax and factory functions. Useful tools: Object.keys , Object.values , Object.entries , Object.assign and spread for copying, the in operator and hasOwnProperty / Object.hasOwn for checking properties.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are template literals, destructuring, and the spread and rest operators?",
        "expected_answer": "Template literals (backticks) allow interpolation and multi-line strings. Destructuring unpacks values from arrays or properties from objects into variables (with defaults and renaming). Spread ( ... ) expands an iterable or object into elements or properties (copying, merging). Rest ( ... ) collects remaining items into an array in function parameters or destructuring. All came in ES6 (object spread in ES2018).",
        "companies": [
            "Zoho",
            "Flipkart",
            "Microsoft",
            "Amazon",
            "Akamai"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are truthy and falsy values?",
        "expected_answer": "In a boolean context, these values are falsy: false , 0 , -0 , 0n , \"\" , null , undefined and NaN . Everything else is truthy, including \"0\" , \"false\" , empty arrays [] and empty objects {} . This is why if (arr) is not a check for \"non-empty\".",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Amazon"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is a callback function? What is callback hell?",
        "expected_answer": "A callback is a function passed to another function to be called later (for example after a timer or an I/O operation). Deeply nested callbacks for sequential async steps create callback hell (the pyramid of doom): hard to read, handle errors in and maintain. Promises and async / await flatten that structure.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Amazon",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is a Promise?",
        "expected_answer": "A Promise represents the eventual result of an asynchronous operation. It is pending, then settles as fulfilled (with a value) or rejected (with a reason), and once settled it never changes. You consume it with .then , .catch and .finally , which return new promises so calls can be chained, or with await .",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Amazon",
            "Meta",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the DOM? How do you select and change elements?",
        "expected_answer": "The Document Object Model is the browser's tree representation of an HTML document that JavaScript can read and change. Elements are selected with getElementById , querySelector / querySelectorAll (CSS selectors) and older methods like getElementsByClassName ; they are changed through properties ( textContent , classList , style , setAttribute ) and structure methods ( append , remove ). textContent is safer than innerHTML for untrusted text. The DOM is not part of the JavaScript language itself; it is a browser API.",
        "companies": [
            "Meta",
            "Zoho",
            "Flipkart",
            "Amazon",
            "Akamai",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What are event bubbling and capturing?",
        "expected_answer": "When an event happens on an element it goes through three phases: capturing (from the window down to the target), target, then bubbling (from the target back up to the window). Listeners run in the bubbling phase by default; passing the capture option makes them run during capturing. stopPropagation() halts the travel and preventDefault() cancels the browser's default action (they are different).",
        "companies": [
            "Meta",
            "Zoho",
            "Flipkart",
            "Amazon",
            "Akamai"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is the difference between localStorage , sessionStorage and cookies?",
        "expected_answer": "localStorage : key-value strings (about 5 to 10 MB), persists until cleared, same origin only, never sent to the server automatically. sessionStorage : same API, but cleared when the tab or window closes. Cookies: small (about 4 KB), sent with every matching HTTP request, can have expiry and flags ( HttpOnly , Secure , SameSite ), and are the usual way to hold session identifiers. Never store secrets in localStorage , because any script on the page (including injected XSS) can read it.",
        "companies": [
            "Akamai",
            "Zoho",
            "Flipkart",
            "Amazon",
            "Microsoft"
        ]
    },
    {
        "difficulty": "EASY",
        "question_text": "What is JSON? What can and cannot be serialized?",
        "expected_answer": "JSON is a text format for data exchange. JSON.stringify converts a value to a string and JSON.parse converts back. JSON supports strings, numbers, booleans, null , arrays and plain objects. undefined , functions and symbols are dropped (or become null in arrays), Date becomes a string, Map and Set become empty objects, BigInt throws, and circular references throw an error. A toJSON method or a replacer can customize the output.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Amazon",
            "Microsoft",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Explain the event loop, the call stack, and the task and microtask queues.",
        "expected_answer": "JavaScript runs one piece of code at a time on the call stack. Asynchronous work (timers, network, events) is handled by the host environment (browser or Node), and when it finishes, its callback is placed in a queue. The event loop takes the next task only when the call stack is empty. There are two kinds of queues: the task (macrotask) queue ( setTimeout , I/O, UI events) and the microtask queue (promise reactions, queueMicrotask , MutationObserver ). After each task the engine drains the entire microtask queue before the next task or a render, so promise callbacks run before a setTimeout(0) callback. A long synchronous task blocks everything, including rendering.",
        "companies": [
            "Google",
            "Meta",
            "Flipkart",
            "Amazon",
            "Goldman Sachs",
            "Zoho"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How do Promises work in depth? Explain Promise.all , allSettled , race and any .",
        "expected_answer": "A .then callback is run as a microtask, and each .then / .catch returns a new promise, so a returned value becomes the next value and a thrown error becomes a rejection that skips to the next .catch . Combinators: Promise.all : fulfills with all results, or rejects as soon as one rejects. Promise.allSettled : waits for all, and reports each result or failure (never rejects). Promise.race : settles with the first promise to settle (fulfil or reject). Promise.any : fulfills with the first fulfilled promise; rejects with an AggregateError only if all reject. An unhandled rejection is reported (and in recent Node versions terminates the process by default).",
        "companies": [
            "Flipkart",
            "Amazon",
            "Meta",
            "Goldman Sachs",
            "Microsoft"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How does async / await work? How do you handle errors?",
        "expected_answer": "async functions always return a promise; await pauses the function (not the thread), subscribes to the awaited promise and resumes later as a microtask. It is syntactic sugar over promises that makes sequential async code readable. Errors are handled with try / catch or by attaching .catch to the returned promise. Common pitfalls: awaiting independent operations one after another (slower than starting them together and awaiting Promise.all ), await inside forEach (which does not wait), and forgetting that an unawaited promise's error is easily lost.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Meta",
            "Zoho",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Explain closures in more depth: use cases and pitfalls.",
        "expected_answer": "A closure captures variables by reference (the binding, not a copy), so changes made inside are visible outside. Uses: encapsulation and private state, function factories, memoization, once-only wrappers, event handlers and partial application. Pitfalls: loops with var where every callback sees the final value (use let , which creates a fresh binding per iteration); accidental retention of large objects that prevents garbage collection; and stale closures in UI code that captured an old value.",
        "companies": [
            "Meta",
            "Zoho",
            "Flipkart",
            "Oracle",
            "Google",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are the rules of this binding? How do call , apply and bind differ?",
        "expected_answer": "Precedence from highest to lowest: new binding, explicit binding ( call , apply , bind ), implicit binding (a method call on an object), then default binding (global object or undefined in strict mode); arrow functions ignore these rules and use the enclosing this . call(thisArg, a, b) invokes immediately with arguments listed; apply(thisArg, [a, b]) invokes immediately with an array; bind(thisArg, ...) returns a new function with this (and optionally leading arguments) fixed. A method extracted from its object (passed as a callback) loses its this .",
        "companies": [
            "Zoho",
            "Flipkart",
            "Meta",
            "Oracle",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How does prototypal inheritance work?",
        "expected_answer": "Every object has an internal link to another object, its prototype. When a property is not found on the object, the engine follows the prototype chain until it finds it or reaches null . Functions have a prototype property used as the prototype of objects created with new . Object.create(proto) makes an object with a chosen prototype, and Object.getPrototypeOf reads it. Properties set on an instance shadow those on the prototype, and methods placed on the prototype are shared by all instances, which saves memory.",
        "companies": [
            "Zoho",
            "Oracle",
            "Flipkart",
            "Google",
            "Microsoft",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are ES6 classes? How do they relate to prototypes?",
        "expected_answer": "class is syntactic sugar over prototypes and constructor functions: methods are placed on the prototype, extends sets up the prototype chain and super calls the parent constructor or method. Classes support static members, getters and setters, and private fields ( #name , enforced by the language). Differences from plain functions: class declarations are not hoisted like functions (they have a temporal dead zone), class bodies run in strict mode, and calling a class without new throws.",
        "companies": [
            "Zoho",
            "Flipkart",
            "Oracle",
            "Microsoft",
            "Amazon"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is event delegation? How does it relate to bubbling?",
        "expected_answer": "Instead of attaching a listener to every child, you attach one listener to a common ancestor and use the fact that events bubble up. Inside the handler, event.target identifies the real source ( event.currentTarget is the element with the listener). Benefits: fewer listeners (less memory), works for elements added later and simpler cleanup. Limits: events that do not bubble (such as focus , blur and mouseenter ) need alternatives like focusin or the capture phase, and stopping propagation can break delegation.",
        "companies": [
            "Meta",
            "Flipkart",
            "Zoho",
            "Amazon",
            "Akamai"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are debouncing and throttling? When do you use each?",
        "expected_answer": "Both limit how often a function runs in response to frequent events. Debounce waits until events stop for a set time and then runs once (search-as-you-type, auto-save, window resize end). Throttle runs at most once per interval while events keep coming (scroll tracking, mouse move, rate-limited analytics). Debounce favors the last event after quiet; throttle gives steady updates during activity. requestAnimationFrame is another tool for visual updates tied to rendering.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Meta",
            "Google",
            "Zoho"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is the difference between shallow and deep copy? How does immutability help?",
        "expected_answer": "A shallow copy (spread, Object.assign , slice , Array.from ) copies only the top level, so nested objects are still shared. A deep copy duplicates nested structures: structuredClone (handles dates, maps, sets, cycles but not functions or class prototypes), JSON round-tripping (lossy), or a library. Object.freeze is shallow. Immutability (creating new objects instead of mutating) makes change detection simple, avoids shared-state bugs and underpins React and Redux style state management.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Goldman Sachs",
            "Microsoft",
            "Zoho"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are higher-order functions, pure functions, currying and composition?",
        "expected_answer": "A higher-order function takes functions as arguments or returns a function ( map , filter , bind ). A pure function returns the same output for the same input and has no side effects (no mutation, I/O or hidden state), which makes it testable and cacheable. Currying transforms a multi-argument function into a chain of single-argument functions; partial application fixes some arguments in advance. Composition combines small functions so the output of one feeds the next. These rely on first-class functions and closures.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Meta",
            "Zoho",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "Compare CommonJS and ES modules.",
        "expected_answer": "CommonJS ( require / module.exports ): synchronous loading, dynamic (can require conditionally), exports are a copy of values at load time, the original Node.js format. ES modules ( import / export ): static syntax analyzed before running (enabling tree shaking), asynchronous loading, live bindings (imports reflect later changes to the exported variable), strict mode by default, top-level await , supported natively in browsers ( type=\"module\" ) and in Node.js. Interop and the dual package problem still cause real-world friction, and bundlers (webpack, Rollup, esbuild, Vite) paper over differences.",
        "companies": [
            "Amazon",
            "Microsoft",
            "Flipkart",
            "Google",
            "Snyk"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How do Map , Set , WeakMap and WeakSet differ from plain objects and arrays?",
        "expected_answer": "Map allows keys of any type, keeps insertion order, has a reliable size and performs well with frequent additions and removals; plain objects only use string or symbol keys and carry prototype properties. Set stores unique values with fast membership checks. WeakMap and WeakSet hold their keys weakly (keys must be objects), so entries disappear when the key is no longer referenced elsewhere; they are not iterable and have no size . Use them for private metadata and caches tied to object lifetime without causing leaks.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Google",
            "Meta",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are iterators, iterables and generators?",
        "expected_answer": "An iterable has a [Symbol.iterator]() method that returns an iterator, an object with next() returning { value, done } . Arrays, strings, maps and sets are iterable, which is why they work with for...of , spread and destructuring. A generator function ( function* ) can pause at yield and resume later, producing values lazily; they enable infinite sequences, custom iteration and, historically, async flow control. Async generators and for await...of handle streams of promises.",
        "companies": [
            "Google",
            "Flipkart",
            "Microsoft",
            "Oracle",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How do cookies, sessions and tokens work, and what do cookie flags do?",
        "expected_answer": "HTTP is stateless, so the server identifies a user across requests with a session identifier stored in a cookie (the data stays on the server) or with a token such as a JWT (the claims are signed and carried by the client). Cookie flags: HttpOnly blocks JavaScript access (protects against token theft via XSS), Secure sends it over HTTPS only, SameSite ( Strict , Lax , None ) limits cross-site sending (helps against CSRF), plus Domain , Path and expiry. JWTs in localStorage are exposed to XSS; many teams prefer HttpOnly cookies.",
        "companies": [
            "Akamai",
            "Amazon",
            "Microsoft",
            "Goldman Sachs",
            "Flipkart"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are the same-origin policy and CORS? What is a preflight request?",
        "expected_answer": "The same-origin policy stops a page from reading responses from a different origin (scheme, host and port). CORS is how a server opts in to cross-origin reads by sending headers such as Access-Control-Allow-Origin . For \"non-simple\" requests (custom headers, methods like PUT or DELETE , JSON content types) the browser first sends an OPTIONS preflight to ask permission. CORS is enforced by browsers, not servers; it does not stop other clients and it is not authentication. Credentialed requests cannot use a wildcard origin.",
        "companies": [
            "Amazon",
            "Microsoft",
            "Flipkart",
            "Goldman Sachs",
            "Google"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What are XSS and CSRF attacks, and how do you prevent them?",
        "expected_answer": "XSS (cross-site scripting) injects attacker-controlled script into a page (stored, reflected or DOM based). Prevention: escape or encode output by context, avoid innerHTML and eval with untrusted data, sanitize any HTML you must render, and add a Content Security Policy. CSRF (cross-site request forgery) tricks a logged-in browser into sending an unwanted request. Prevention: SameSite cookies, anti-CSRF tokens and checking origin headers. Related: never trust client-side validation alone, and keep dependencies patched.",
        "companies": [
            "Amazon",
            "Microsoft",
            "Snyk",
            "Goldman Sachs",
            "Akamai"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "How does garbage collection work in JavaScript? What causes memory leaks?",
        "expected_answer": "Engines use reachability: memory that cannot be reached from roots (globals, the stack, active closures) is reclaimed, mainly by mark-and-sweep with generational and incremental techniques (V8 splits the heap into young and old generations). Typical leaks: accidental globals, forgotten timers and intervals, event listeners that are never removed, detached DOM nodes still referenced, unbounded caches and arrays, and closures holding large objects. Use DevTools heap snapshots and allocation timelines to find them, and WeakMap or explicit cleanup to prevent them.",
        "companies": [
            "Google",
            "Meta",
            "Amazon",
            "Goldman Sachs",
            "Oracle"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What is the difference between fetch , XMLHttpRequest and libraries like Axios?",
        "expected_answer": "XMLHttpRequest is the older callback and event based API. fetch is promise based and streaming-friendly, but it does not reject on HTTP error statuses (only on network failure), so check response.ok ; it needs manual JSON parsing, and cancellation uses AbortController . Axios adds conveniences (automatic JSON handling, interceptors, timeouts, rejection on error statuses). Whichever you use, also consider retries with backoff, timeouts, caching and handling of concurrent requests.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Zoho",
            "Microsoft"
        ]
    },
    {
        "difficulty": "MEDIUM",
        "question_text": "What do package.json , lockfiles and semantic versioning do? What are the risks of npm dependencies?",
        "expected_answer": "package.json declares dependencies ( dependencies , devDependencies , peerDependencies ) and scripts. Semantic versioning (major.minor.patch) with ranges like ^1.2.3 allows compatible updates. The lockfile ( package-lock.json , yarn.lock , pnpm-lock.yaml ) records the exact resolved tree so installs are reproducible, and should be committed; npm ci installs strictly from it. Risks: transitive dependencies you never chose, vulnerable or abandoned packages, typosquatting (a malicious package with a near-identical name), compromised maintainers, and install scripts that run code. Mitigations: lockfiles, vulnerability scanning and auditing, pinning, limiting install scripts and reviewing updates.",
        "companies": [
            "Snyk",
            "Amazon",
            "Microsoft",
            "Flipkart"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Compare the browser event loop with the Node.js event loop. Where do process.nextTick and setImmediate fit?",
        "expected_answer": "The browser loop is organized around tasks, microtasks and rendering opportunities (animation frames and style/layout/paint run between tasks). Node's loop (libuv) runs in phases: timers, pending callbacks, idle/prepare, poll (waiting for and processing I/O), check ( setImmediate callbacks) and close callbacks. Between phases Node drains process.nextTick callbacks first and then promise microtasks, so nextTick runs before promise callbacks. Inside an I/O callback, setImmediate always runs before a zero-delay timer, while from the main module their order is not guaranteed. CPU-heavy work blocks the loop in both environments; Node offloads some work (file system, DNS, crypto) to a thread pool.",
        "companies": [
            "Google",
            "Amazon",
            "Goldman Sachs",
            "Microsoft",
            "Flipkart"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How does the V8 engine execute JavaScript? Explain JIT compilation, hidden classes and inline caches.",
        "expected_answer": "V8 parses source into an AST and bytecode, runs it in the Ignition interpreter, profiles hot functions and compiles them with optimizing compilers (Sparkplug baseline and TurboFan, with newer tiers in recent versions). Optimizations rely on assumptions: objects with the same property order share a hidden class (shape), and inline caches remember shapes at property access sites so lookups become fast direct offsets. If assumptions break (a function sees different shapes or types), the engine deoptimizes back to slower code. Practical advice: initialize properties in a consistent order, avoid changing object shapes and types in hot paths, and keep functions monomorphic where it matters. Measure with profilers rather than guessing.",
        "companies": [
            "Google",
            "Meta",
            "Oracle",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain execution contexts, the lexical environment and the scope chain.",
        "expected_answer": "When code runs, the engine creates an execution context (global, function or eval) containing a lexical environment (the bindings declared in that scope plus a reference to the outer environment) and a variable environment. Creation happens in two phases: setup (hoisting, let and const bindings placed in the temporal dead zone, function declarations initialized) and execution. A closure is a function object holding a reference to the environment in which it was created, which is why scope lookup follows that chain, not the call stack. This model explains hoisting, TDZ errors, closures and why this is separate from scope.",
        "companies": [
            "Google",
            "Oracle",
            "Zoho",
            "Goldman Sachs",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What really happens with new ? Explain prototype internals, __proto__ and instanceof .",
        "expected_answer": "The new operator (1) creates an empty object, (2) links its internal prototype to the constructor's prototype property, (3) calls the constructor with this set to that object and (4) returns the object (unless the constructor returns a different object). __proto__ is a legacy accessor for the internal [[Prototype]] ; prefer Object.getPrototypeOf / setPrototypeOf , and avoid changing prototypes after creation because it deoptimizes code. a instanceof F checks whether F.prototype appears in a 's prototype chain (customizable with Symbol.hasInstance ). Classes with extends configure two chains: instance methods and static inheritance.",
        "companies": [
            "Oracle",
            "Zoho",
            "Google",
            "Microsoft",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What are Proxy , Reflect , property descriptors and symbols used for?",
        "expected_answer": "Property descriptors ( writable , enumerable , configurable , or accessor get / set ) control property behavior ( Object.defineProperty , Object.freeze , Object.seal ). A Proxy wraps an object and intercepts operations through traps ( get , set , has , deleteProperty , apply , and others), enabling validation, reactive state (as in Vue 3), logging and virtualization; Reflect provides the default behavior for each operation so traps can forward correctly. Symbols are unique keys that avoid name collisions and provide hooks ( Symbol.iterator , Symbol.toPrimitive , Symbol.asyncIterator ). Proxies add overhead and have invariants the engine enforces.",
        "companies": [
            "Google",
            "Microsoft",
            "Oracle",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do Web Workers, service workers and shared memory ( SharedArrayBuffer , Atomics ) work?",
        "expected_answer": "JavaScript on the main thread cannot run in parallel, so Web Workers run scripts on separate threads with their own event loop and no DOM access; they communicate by message passing using structured cloning (large buffers can be transferred instead of copied). SharedArrayBuffer lets threads share memory, and Atomics provides atomic operations and waiting (needed to avoid data races); it requires cross-origin isolation headers for security reasons. Service workers are event-driven proxies between the page and the network, enabling offline support, caching strategies, push notifications and background sync; they have their own lifecycle (install, activate, fetch) and can be terminated at any time. Node equivalents: worker_threads and cluster .",
        "companies": [
            "Google",
            "Meta",
            "Amazon",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Describe the browser rendering pipeline. What causes reflow and repaint, and how do you avoid layout thrashing?",
        "expected_answer": "The browser parses HTML into the DOM and CSS into the CSSOM, combines them into a render tree, then runs layout (geometry), paint (pixels into layers) and compositing (layers combined, often on the GPU). Changing geometry (width, margins, adding elements) triggers layout and everything after it; changing colors triggers paint; changing transform and opacity can often be done by compositing alone. Layout thrashing happens when code alternates reads (such as offsetHeight ) and writes to styles in a loop, forcing synchronous layout each time; batch reads then writes, use requestAnimationFrame , and prefer CSS transforms. Scripts block parsing unless marked defer or async .",
        "companies": [
            "Meta",
            "Google",
            "Akamai",
            "Amazon",
            "Flipkart"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do you optimize front-end performance? Explain Core Web Vitals, code splitting and caching.",
        "expected_answer": "Core Web Vitals measure user experience: LCP (largest contentful paint, loading), INP (interaction to next paint, responsiveness; it replaced FID) and CLS (cumulative layout shift, visual stability). Techniques: ship less JavaScript (code splitting, lazy loading, tree shaking, minification, compression such as Brotli), optimize images and fonts, use defer and preloading for critical resources, avoid long main-thread tasks (break up work, use workers), reserve space to prevent layout shifts, and cache aggressively (HTTP cache headers, service workers, CDNs). Always measure with Lighthouse, field data and performance profiles first.",
        "companies": [
            "Meta",
            "Google",
            "Amazon",
            "Flipkart",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do JavaScript module systems work internally? What are tree shaking and circular dependencies?",
        "expected_answer": "ES modules load in three phases: construction (find, fetch and parse the module graph), instantiation (allocate memory for exports and link imports to those bindings) and evaluation (run code and fill the bindings). Because imports are live bindings to the exporter's variables, circular imports may see uninitialized values (TDZ errors for let / const ) depending on evaluation order. Tree shaking removes unused exports at build time and relies on static import / export syntax and side-effect free modules (the sideEffects flag). CommonJS can only be shaken in limited cases because it is dynamic. Bundlers also handle code splitting, scope hoisting and dynamic import() .",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "Snyk",
            "Flipkart"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Compare WebSockets, Server-Sent Events and long polling for real-time features.",
        "expected_answer": "Long polling: the client repeatedly makes requests that the server holds open until data arrives; works everywhere but is wasteful and adds latency and overhead. Server-Sent Events (SSE): one-way server to client stream over HTTP with automatic reconnection and event IDs; simple, works through most proxies, text only. WebSockets: full-duplex, low-overhead messaging over one persistent TCP connection after an HTTP upgrade; supports binary data but needs its own handling for reconnection, heartbeats, authentication, scaling across servers (sticky sessions or a pub/sub backplane) and backpressure. Choose based on direction of data flow, scale, infrastructure and delivery guarantees. Managed pub/sub services build ordering, fan-out and presence on top of these transports.",
        "companies": [
            "Amazon",
            "Microsoft",
            "Goldman Sachs",
            "Google",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do Node.js streams, buffers and backpressure work? When do you use worker threads or the cluster module?",
        "expected_answer": "Streams process data in chunks instead of loading everything into memory (readable, writable, duplex and transform streams, plus pipeline for safe chaining and error handling). Backpressure is the mechanism where a slow consumer signals the producer to pause ( write returns false and a drain event signals resume), preventing unbounded memory growth. Buffers hold raw binary data outside the V8 heap. Node runs your JavaScript on one thread, so to use multiple cores you either run several processes (cluster or a process manager) or move CPU-heavy work to worker threads; I/O-heavy workloads usually do not need them.",
        "companies": [
            "Amazon",
            "Goldman Sachs",
            "Microsoft",
            "Flipkart"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain advanced web security: CSP, prototype pollution, ReDoS, Subresource Integrity and supply-chain attacks.",
        "expected_answer": "Content Security Policy: an HTTP header that restricts where scripts, styles and other resources may load from, limiting XSS impact (avoid unsafe-inline and use nonces or hashes). Prototype pollution: attacker-controlled keys such as __proto__ or constructor.prototype in a merge or assignment alter Object.prototype , changing behavior app-wide (mitigate by validating keys, using Object.create(null) or Map , and freezing prototypes). ReDoS: a regular expression with catastrophic backtracking lets crafted input freeze the single thread. Subresource Integrity: a hash on script or link tags ensures a CDN-hosted file has not been changed. Supply chain: malicious or compromised packages, typosquatting, dependency confusion and install scripts; defend with lockfiles, audits, scoped registries and minimal dependencies.",
        "companies": [
            "Snyk",
            "Amazon",
            "Microsoft",
            "Goldman Sachs",
            "Akamai"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "What happens inside promises and async functions at the engine level? What are async iterators and unhandled rejections?",
        "expected_answer": "Resolving a promise schedules its reaction jobs on the microtask queue; resolving with another promise or a thenable takes extra microtask ticks (a promise that resolves to a promise costs more ticks than a plain value), which can change callback ordering in subtle ways. await x wraps x in a promise and resumes the async function as a microtask, so code after an await is always asynchronous even if x is not a promise. Async iterators ( Symbol.asyncIterator , for await...of ) consume sequences of promises, such as streams. A rejection with no handler by the end of a turn triggers unhandledrejection (browsers) or unhandledRejection (Node, where the default is to crash). Best practice: always handle or return promises, and never leave floating promises.",
        "companies": [
            "Google",
            "Meta",
            "Amazon",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain how numbers work: floating point precision, BigInt and typed arrays.",
        "expected_answer": "number is an IEEE 754 double (64-bit), so decimals like 0.1 and 0.2 cannot be represented exactly (their sum is not exactly 0.3), and integers are exact only up to Number.MAX_SAFE_INTEGER (2^53 - 1). For money, use integer minor units or a decimal library; compare floats with a tolerance ( Number.EPSILON ). BigInt represents arbitrarily large integers (cannot be mixed with number in arithmetic and does not work with Math methods or JSON.stringify directly). Typed arrays ( Uint8Array , Float64Array ) and ArrayBuffer give fixed-type, contiguous memory for binary data, graphics, audio and WebAssembly. Bitwise operators convert operands to 32-bit integers.",
        "companies": [
            "Goldman Sachs",
            "Google",
            "Microsoft",
            "Amazon"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Explain TypeScript's type system: structural typing, generics, unions, narrowing, and any vs unknown vs never .",
        "expected_answer": "TypeScript adds static types that are erased at compile time, so it gives no runtime checks. It uses structural typing: compatibility depends on shape, not declared names. Generics parameterize types and functions; union types ( A | B ) model alternatives and intersection types ( A & B ) combine shapes; narrowing (via typeof , in , equality, discriminated unions and custom type guards) refines a union within a branch. any disables checking, unknown is the safe top type (you must narrow before use) and never is the empty type (unreachable code and exhaustive checks). Utility types ( Partial , Pick , Omit , Record ), strict mode and readonly improve safety; declaration files describe untyped JavaScript.",
        "companies": [
            "Microsoft",
            "Google",
            "Amazon",
            "Flipkart",
            "Goldman Sachs"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do the Virtual DOM, reconciliation and keys work in React? What are the rules of Hooks?",
        "expected_answer": "React keeps an in-memory description of the UI (elements and fibers). When state changes it renders a new tree, reconciles it with the previous one using heuristics (different element types rebuild the subtree; keys identify list items so moves are not treated as remounts) and commits only the necessary DOM changes. The Virtual DOM is not inherently faster than hand-tuned DOM updates; its value is a declarative model with acceptable performance. Hooks ( useState , useEffect , useMemo , useRef and others) must be called at the top level and only from components or custom hooks so React can match state by call order. Effects need correct dependency arrays and cleanup; stale closures and unnecessary re-renders are common pitfalls. Concurrent features (transitions, Suspense) let React interrupt rendering.",
        "companies": [
            "Flipkart",
            "Meta",
            "Amazon",
            "Goldman Sachs",
            "Microsoft"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How does React Native work? Explain the old bridge, the new architecture (JSI, Fabric) and the Hermes engine.",
        "expected_answer": "React Native runs your JavaScript in a JS engine (usually Hermes, which precompiles to bytecode for faster startup and lower memory) and renders native views, not a WebView. In the old architecture JavaScript and native code talked through an asynchronous, serialized JSON bridge, which added latency and made synchronous access impossible. The new architecture uses JSI (JavaScript Interface), letting JavaScript hold direct references to native objects and call them synchronously; Fabric is the new renderer and TurboModules the new native modules system, with Codegen providing typed interfaces. Performance guidance: keep the JS thread free, memoize list items, use FlatList , avoid unnecessary re-renders and large images, and use native drivers for animations.",
        "companies": [
            "Flipkart",
            "Amazon",
            "Microsoft",
            "Meta"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "Which design patterns are common in JavaScript? What are micro-frontends?",
        "expected_answer": "Common patterns: module (encapsulation through closures or ES modules), singleton (modules are singletons by nature), factory, observer / pub-sub (event emitters, DOM events), mediator, decorator, strategy, and middleware chains (Express, Redux). Architecture patterns include component-based UI, unidirectional data flow and state management with selectors. Micro-frontends split a large UI into independently built and deployed pieces owned by different teams (composition via Module Federation, iframes, web components or server-side includes). Trade-offs: team autonomy and independent releases versus duplicated dependencies, inconsistent UX, performance overhead and harder cross-app communication.",
        "companies": [
            "Amazon",
            "Flipkart",
            "Microsoft",
            "Goldman Sachs",
            "Oracle"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How should you design a testing strategy for JavaScript apps? Why do tests become flaky, and how do end-to-end tools like Cypress and Playwright differ?",
        "expected_answer": "Use a pyramid or trophy: many fast unit tests (pure functions, components with mocks), a good number of integration tests (components with real collaborators, API contracts) and fewer end-to-end tests for critical user journeys. Prefer testing behavior over implementation details, and use test doubles (mocks, stubs, fakes) at system boundaries. Flakiness comes from timing and async races, shared or leaked state between tests, reliance on real networks, animations and non-deterministic data; fix with explicit waits on conditions (not fixed sleeps), test isolation, controlled network stubbing and deterministic seeds. Cypress runs inside the browser alongside the app with automatic retrying of assertions and a command queue; Playwright drives browsers from outside through the automation protocol, supports multiple browsers and tabs, and parallelizes well.",
        "companies": [
            "Amazon",
            "Microsoft",
            "Google",
            "Flipkart"
        ]
    },
    {
        "difficulty": "HARD",
        "question_text": "How do you diagnose memory problems and leaks in browser and Node applications? What are WeakRef and FinalizationRegistry ?",
        "expected_answer": "In the browser, use DevTools: take heap snapshots and compare them over time, use the allocation timeline and the Performance panel to watch heap growth and GC frequency, and inspect retainers (the reference chain that keeps an object alive) and detached DOM nodes. In Node, use --inspect with DevTools, heap snapshots, process.memoryUsage() and tools like clinic or heap profilers. A leak is shown by memory that keeps growing across repeated identical actions even after forced garbage collection. WeakRef holds a reference that does not keep its target alive, and FinalizationRegistry runs a callback after an object is collected; both are non-deterministic and should be a last resort for caches and cleanup, never for program logic. level, interviewers mostly probe judgment: why a behavior exists, what it costs and how you would verify it with a tool.",
        "companies": [
            "Google",
            "Meta",
            "Amazon",
            "Goldman Sachs",
            "Flipkart"
        ]
    }
]


def validate_questions() -> None:
    expected_counts = {"EASY": 20, "MEDIUM": 20, "HARD": 20}
    actual_counts = Counter(item["difficulty"] for item in QUESTIONS)

    if len(QUESTIONS) != 60:
        raise ValueError(f"Expected 60 JavaScript questions; found {len(QUESTIONS)}.")

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


def seed_javascript_questions() -> None:
    """Insert the 60 JavaScript theory questions into the existing JavaScript topic."""
    validate_questions()
    db = SessionLocal()

    try:
        topic = db.query(Topic).filter(Topic.name == TOPIC_NAME).first()

        if topic is None:
            raise RuntimeError(
                "The JavaScript topic does not exist. Create the JavaScript topic in the app/database first; "
                "this seeder will not create a duplicate topic."
            )

        if not topic.is_active:
            raise RuntimeError(
                f"The JavaScript topic (ID: {topic.id}) is inactive. Activate it first."
            )

        existing_count = db.query(Question).filter(Question.topic_id == topic.id).count()
        if existing_count > 0:
            print(
                f"JavaScript topic (ID: {topic.id}) already contains "
                f"{existing_count} question(s)."
            )
            print("No questions were inserted to avoid duplicates.")
            print("Inspect existing JavaScript questions before deciding whether to seed again.")
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
        print("JAVASCRIPT THEORY QUESTION BANK CREATED")
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
    seed_javascript_questions()
