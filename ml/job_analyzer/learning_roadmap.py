"""
CareerAI learning roadmap engine.

One reusable engine turns a whole skill gap into ONE ordered roadmap:

    missing skills ──► curriculum catalogue (modules + prerequisites)
                   ──► merge / dedupe / drop what the resume already proves
                   ──► prioritise by job importance + shared dependencies
                   ──► order topologically ──► attach resources + combined projects

Maintain MODULES (reusable learning units) and SKILL_MODULES (which modules a
skill needs). Never write a roadmap per job or per skill.

Coverage levels reported for every gap skill:
    detailed       - skill has dedicated modules in SKILL_MODULES
    family         - only a generic family module exists (needs real content)
    unsupported    - no curriculum at all: flagged, never faked
    non_technical  - soft skills etc.: flagged, not given a fake syllabus
"""

import heapq

from resume_parser.skill_extractor import SKILL_ONTOLOGY

STAGES = ["Foundation", "Core Development", "Advanced"]
_STAGE_RANK = {stage: i for i, stage in enumerate(STAGES)}
EVIDENCE_THRESHOLD = 0.4  # resume skills with weaker evidence count as gaps


# =============================================================================
# 1. CURRICULUM CATALOGUE  (reusable modules)
# =============================================================================
MODULES = {}


def _module(mid, title, stage, topics, exercise, *, teaches=(), requires=(),
            hours=6, resources=(), family=False):
    """Register a module.

    teaches  - skills this module is evidence for. The module is skipped when
               ALL of them are already proven by the resume. Empty = never skipped.
    requires - module ids that must come first.
    hours    - rough self-study estimate, for planning only.
    """
    assert mid not in MODULES, f"duplicate module id: {mid}"
    MODULES[mid] = {
        "id": mid, "title": title, "stage": stage, "topics": list(topics),
        "exercise": exercise, "teaches": list(teaches),
        "requires": list(requires), "hours": hours,
        "resources": list(resources), "family": family,
        "order": len(MODULES),
    }


# ---- Programming foundations ------------------------------------------------
_module("py_core", "Python fundamentals", "Foundation",
        ["Syntax, variables and data types", "Control flow and functions",
         "Lists, dicts, sets and comprehensions", "File I/O and modules",
         "Virtual environments and pip"],
        "Write a CLI tool that reads a CSV file and prints summary statistics.",
        teaches=["Python"], hours=25,
        resources=[("Official Python tutorial", "https://docs.python.org/3/tutorial/")])
_module("py_intermediate", "Python OOP, errors and packaging", "Core Development",
        ["Classes and inheritance", "Exceptions and context managers",
         "Decorators and generators", "Packages and imports", "Type hints"],
        "Refactor the CSV tool into a small package with classes and error handling.",
        teaches=["Python"], requires=["py_core"], hours=15,
        resources=[("Python tutorial: classes", "https://docs.python.org/3/tutorial/classes.html")])
_module("oop_core", "Object-oriented programming", "Foundation",
        ["Classes and objects", "Encapsulation", "Inheritance and polymorphism",
         "Composition vs inheritance", "SOLID basics"],
        "Model a library system (books, members, loans) with a clean class design.",
        teaches=["Object-Oriented Programming"], hours=10)
_module("design_patterns", "Object-oriented design and patterns", "Advanced",
        ["Common creational/structural/behavioural patterns", "Design principles",
         "UML class diagrams", "Refactoring towards patterns"],
        "Redesign the library system using at least three patterns, with a diagram.",
        teaches=["Object-Oriented Design"], requires=["oop_core"], hours=12)
_module("java_core", "Java fundamentals", "Foundation",
        ["Syntax and types", "Control flow and methods", "Classes and interfaces",
         "Collections and generics", "Exceptions", "Build tools (Maven/Gradle)"],
        "Build a console inventory manager using collections and custom exceptions.",
        teaches=["Java"], hours=30,
        resources=[("Dev.java learn", "https://dev.java/learn/")])
_module("cpp_core", "C++ fundamentals", "Foundation",
        ["Syntax and types", "Pointers and references", "Classes and RAII",
         "STL containers and algorithms", "Memory management"],
        "Implement a generic stack and queue using templates and the STL.",
        teaches=["C++"], hours=35,
        resources=[("Get started with C++", "https://isocpp.org/get-started")])
_module("dart_core", "Dart fundamentals", "Foundation",
        ["Variables and datatypes", "Operators and control flow",
         "Functions and collections", "Object-oriented Dart", "Null safety"],
        "Build a command-line task manager in Dart.",
        teaches=["Dart"], hours=15,
        resources=[("Dart language tour", "https://dart.dev/language")])
_module("dart_async", "Asynchronous Dart", "Core Development",
        ["Futures and async/await", "Streams", "Exception handling in async code",
         "Packages and pub"],
        "Fetch and cache data from a public API in a Dart console app.",
        teaches=["Dart"], requires=["dart_core"], hours=8,
        resources=[("Asynchronous programming", "https://dart.dev/libraries/async/async-await")])

# ---- Web fundamentals -------------------------------------------------------
_module("html_css_basics", "HTML and CSS essentials", "Foundation",
        ["Semantic HTML", "Forms", "CSS selectors and the box model",
         "Flexbox and grid", "Responsive design"],
        "Build a responsive portfolio page without any framework.",
        teaches=["HTML", "CSS"], hours=15,
        resources=[("MDN Learn web development", "https://developer.mozilla.org/en-US/docs/Learn")])
_module("js_core", "JavaScript fundamentals", "Foundation",
        ["Variables, types and functions", "Arrays and objects", "Scope and closures",
         "ES6+ syntax and modules"],
        "Build a to-do list that runs entirely in the browser.",
        teaches=["JavaScript"], requires=["html_css_basics"], hours=20,
        resources=[("MDN JavaScript guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide")])
_module("js_async_dom", "Async JavaScript and the DOM", "Core Development",
        ["DOM manipulation and events", "Promises and async/await",
         "fetch and JSON handling", "Error handling"],
        "Add a live data panel to the to-do app using a public REST API.",
        teaches=["JavaScript"], requires=["js_core", "http_basics"], hours=12)
_module("ts_core", "TypeScript essentials", "Core Development",
        ["Static types and interfaces", "Generics", "Narrowing",
         "tsconfig and tooling", "Typing React/Node code"],
        "Convert the to-do app to TypeScript with strict mode on.",
        teaches=["TypeScript"], requires=["js_core"], hours=10,
        resources=[("TypeScript docs", "https://www.typescriptlang.org/docs/")])

# ---- HTTP / APIs / data formats --------------------------------------------
_module("http_basics", "HTTP fundamentals", "Foundation",
        ["Request/response cycle", "Methods and status codes", "Headers and cookies",
         "HTTPS basics", "Inspecting traffic with browser dev tools/curl"],
        "Call three public APIs with curl and explain each request and response.",
        teaches=["HTTP"], hours=4,
        resources=[("MDN: HTTP", "https://developer.mozilla.org/en-US/docs/Web/HTTP")])
_module("rest_api_design", "REST API design", "Core Development",
        ["Resources and URL design", "Idempotency and status codes",
         "Pagination, filtering and versioning", "Error format conventions",
         "API documentation (OpenAPI)"],
        "Design (on paper) the endpoints for a notes service, with OpenAPI spec.",
        teaches=["REST API"], requires=["http_basics"], hours=8,
        resources=[("MDN: REST", "https://developer.mozilla.org/en-US/docs/Glossary/REST")])
_module("json_basics", "JSON fundamentals", "Foundation",
        ["JSON syntax and data types", "Nesting and structure",
         "JSON vs other formats"],
        "Model a user profile and an order as JSON documents.",
        teaches=["JSON"], hours=2,
        resources=[("Introducing JSON", "https://www.json.org/json-en.html")])
_module("json_in_code", "Working with JSON in code", "Core Development",
        ["Parsing and serialization", "Reading/writing JSON files",
         "Validation with JSON Schema", "JSON in REST APIs"],
        "Write a config manager that loads, validates and saves JSON settings.",
        teaches=["JSON Schema"], requires=["json_basics"], hours=5,
        resources=[("Python json module", "https://docs.python.org/3/library/json.html")])
_module("graphql_core", "GraphQL basics", "Advanced",
        ["Schema and types", "Queries and mutations", "Resolvers",
         "GraphQL vs REST trade-offs"],
        "Expose the notes service through a small GraphQL schema.",
        teaches=["GraphQL"], requires=["rest_api_design", "json_basics"], hours=8,
        resources=[("Learn GraphQL", "https://graphql.org/learn/")])
_module("auth_core", "Authentication and authorization", "Core Development",
        ["Password hashing", "Sessions vs tokens (JWT)", "OAuth2 basics",
         "Authorization checks", "Common auth vulnerabilities"],
        "Add register/login with hashed passwords and token auth to a small API.",
        teaches=["Authentication", "Authorization"], requires=["http_basics"], hours=10,
        resources=[("OWASP Authentication Cheat Sheet",
                    "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html")])
_module("rbac_core", "Role-based access control", "Advanced",
        ["Roles, permissions and policies", "Protecting routes by role",
         "Designing a permission model"],
        "Add admin/editor/viewer roles to the authenticated API.",
        teaches=["RBAC"], requires=["auth_core"], hours=5)
_module("websockets_realtime", "WebSockets and real-time communication", "Advanced",
        ["WebSocket handshake and lifecycle", "Broadcast and rooms",
         "Reconnection and heartbeats", "Scaling concerns"],
        "Build a multi-user chat room.",
        teaches=["WebSockets"], requires=["http_basics"], hours=8,
        resources=[("MDN: WebSockets API", "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API")])

# ---- Databases --------------------------------------------------------------
_module("sql_basics", "SQL fundamentals", "Foundation",
        ["SELECT, WHERE, ORDER BY", "INSERT/UPDATE/DELETE", "Aggregates and GROUP BY",
         "Creating tables and constraints"],
        "Create a small schema and answer ten questions about it with queries.",
        teaches=["SQL"], hours=12,
        resources=[("PostgreSQL tutorial", "https://www.postgresql.org/docs/current/tutorial.html")])
_module("sql_joins_design", "Joins, normalisation and indexes", "Core Development",
        ["INNER/LEFT joins", "Subqueries and CTEs", "Normalisation",
         "Indexes and EXPLAIN", "Transactions"],
        "Normalise a messy spreadsheet into 3NF tables and query across them.",
        teaches=["SQL"], requires=["sql_basics"], hours=12)
_module("db_design", "Database design", "Core Development",
        ["Entity-relationship modelling", "Keys and relationships",
         "Normal forms", "Schema evolution/migrations"],
        "Design the ER diagram and schema for an e-commerce app.",
        teaches=["Database Design"], requires=["sql_basics"], hours=8)
_module("rdbms_engine_practice", "Operating a relational database engine", "Advanced",
        ["Install and configure the engine", "Users and privileges",
         "Backup and restore", "Query performance and monitoring"],
        "Install the engine, load sample data, take and restore a backup.",
        requires=["sql_basics"], hours=10)
_module("mongodb_core", "MongoDB and document databases", "Core Development",
        ["Documents and collections", "CRUD and queries", "Indexes",
         "Aggregation pipeline", "Schema design trade-offs"],
        "Store and query a blog's posts and comments in MongoDB.",
        teaches=["MongoDB"], requires=["json_basics"], hours=10,
        resources=[("MongoDB manual", "https://www.mongodb.com/docs/manual/tutorial/getting-started/")])

# ---- Developer tools / OS ---------------------------------------------------
_module("git_basics", "Git fundamentals", "Foundation",
        ["Commits, branches and merging", "Resolving conflicts", "Remotes",
         "Undoing changes"],
        "Create a repo, branch, introduce a conflict and resolve it.",
        teaches=["Git"], hours=5,
        resources=[("Pro Git book", "https://git-scm.com/book")])
_module("github_workflow", "GitHub collaboration workflow", "Core Development",
        ["Forks and pull requests", "Code review", "Issues and projects",
         "Branch protection"],
        "Open a pull request on an open-source repository.",
        teaches=["GitHub"], requires=["git_basics"], hours=4,
        resources=[("GitHub docs", "https://docs.github.com/en/get-started")])
_module("linux_basics", "Linux fundamentals", "Foundation",
        ["File system layout and navigation", "Core commands (ls, cp, grep, find)",
         "Pipes and redirection", "Text editors in the terminal"],
        "Organise a messy folder tree using only the command line.",
        teaches=["Linux"], hours=8,
        resources=[("Linux man pages", "https://man7.org/linux/man-pages/")])
_module("linux_admin", "Linux administration basics", "Core Development",
        ["Users, permissions and ownership", "Process management",
         "Package management", "Services (systemd) and logs", "SSH and basic networking"],
        "Set up a VM with a non-root user, SSH keys and a service that restarts on failure.",
        teaches=["Linux"], requires=["linux_basics"], hours=12)
_module("shell_scripting", "Shell scripting", "Core Development",
        ["Variables and conditionals", "Loops and functions", "Arguments and exit codes",
         "Cron and automation"],
        "Write a backup script with logging, run nightly via cron.",
        teaches=["Bash"], requires=["linux_basics"], hours=8,
        resources=[("Bash reference manual", "https://www.gnu.org/software/bash/manual/")])

# ---- Testing ----------------------------------------------------------------
_module("testing_fundamentals", "Software testing fundamentals", "Foundation",
        ["Why test; the test pyramid", "Writing good test cases",
         "Arrange-Act-Assert", "Bug reports"],
        "Write 15 test cases (positive, negative, edge) for a login form.",
        teaches=["Test Cases"], hours=5)
_module("test_types", "Types of testing", "Core Development",
        ["Functional, system and integration testing", "Regression testing",
         "Exploratory and manual testing", "Web UI testing"],
        "Create a regression checklist and run an exploratory session on a web app.",
        requires=["testing_fundamentals"], hours=6)
_module("pyunit_core", "Unit testing with unittest (PyUnit)", "Core Development",
        ["TestCase and assertions", "Fixtures: setUp/tearDown", "Test discovery and suites",
         "Running tests from the CLI"],
        "Unit-test a calculator module to 90% coverage.",
        teaches=["PyUnit"], requires=["testing_fundamentals", "py_core"], hours=6,
        resources=[("unittest docs", "https://docs.python.org/3/library/unittest.html")])
_module("pyunit_mocking", "Mocking and coverage", "Advanced",
        ["unittest.mock and patching", "Testing code with I/O or APIs",
         "Coverage measurement"],
        "Test an API client without network access using mocks.",
        teaches=["PyUnit"], requires=["pyunit_core"], hours=5,
        resources=[("unittest.mock", "https://docs.python.org/3/library/unittest.mock.html")])
_module("selenium_core", "Browser automation with Selenium", "Core Development",
        ["WebDriver and locators", "Waits", "Page object pattern", "Running in CI"],
        "Automate sign-up and checkout flows on a demo shop.",
        teaches=["Selenium"], requires=["testing_fundamentals"], hours=10,
        resources=[("Selenium docs", "https://www.selenium.dev/documentation/")])

# ---- Backend / frontend frameworks -----------------------------------------
_module("django_core", "Django fundamentals", "Foundation",
        ["Project and app structure", "URLs and views", "Templates", "Settings and admin"],
        "Build a polls or notes app with the Django admin.",
        teaches=["Django"], requires=["py_intermediate", "http_basics"], hours=12,
        resources=[("Django tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/")])
_module("django_orm", "Django models and ORM", "Core Development",
        ["Models and migrations", "QuerySets and relations", "Query optimisation"],
        "Model a blog with authors, posts and tags.",
        teaches=["Django"], requires=["django_core", "sql_basics"], hours=10)
_module("django_forms_auth", "Django forms and authentication", "Core Development",
        ["Forms and validation", "Built-in auth", "Permissions"],
        "Add registration, login and per-user content to the blog.",
        teaches=["Django"], requires=["django_core", "auth_core"], hours=8)
_module("drf", "Django REST Framework", "Advanced",
        ["Serializers", "ViewSets and routers", "Token/JWT auth", "Pagination and filtering"],
        "Expose the blog as a REST API.",
        teaches=["Django"], requires=["django_orm", "rest_api_design", "json_basics"], hours=12,
        resources=[("DRF quickstart", "https://www.django-rest-framework.org/tutorial/quickstart/")])
_module("django_testing", "Testing Django applications", "Advanced",
        ["Django test client", "Fixtures and factories", "Testing APIs"],
        "Reach solid coverage on the blog API.",
        teaches=["Django"], requires=["django_orm", "testing_fundamentals"], hours=5)
_module("flask_core", "Flask fundamentals", "Foundation",
        ["Routing and view functions", "Jinja2 templates", "Forms and requests",
         "Configuration and blueprints"],
        "Build a small bookmarks site with Flask.",
        teaches=["Flask"], requires=["py_intermediate", "http_basics"], hours=8,
        resources=[("Flask tutorial", "https://flask.palletsprojects.com/en/stable/tutorial/")])
_module("flask_data_api", "Flask databases and REST APIs", "Core Development",
        ["SQLite/SQLAlchemy integration", "Building JSON APIs", "Error handling",
         "Testing Flask apps"],
        "Turn the bookmarks site into a REST API backed by SQLite.",
        teaches=["Flask"], requires=["flask_core", "sql_basics", "rest_api_design"], hours=10)
_module("pydantic_models", "Data validation with Pydantic", "Core Development",
        ["Models and types", "Validation and custom validators", "Settings management",
         "Serialization"],
        "Validate a nested JSON payload and report friendly errors.",
        teaches=["Pydantic"], requires=["py_intermediate"], hours=4,
        resources=[("Pydantic docs", "https://docs.pydantic.dev/latest/")])
_module("fastapi_core", "FastAPI fundamentals", "Foundation",
        ["Routing and path/query parameters", "Request and response models",
         "Dependency injection", "Automatic OpenAPI docs"],
        "Build a CRUD notes API.",
        teaches=["FastAPI"], requires=["py_intermediate", "http_basics", "pydantic_models"],
        hours=8, resources=[("FastAPI tutorial", "https://fastapi.tiangolo.com/tutorial/")])
_module("fastapi_db_auth", "FastAPI with databases, auth and tests", "Advanced",
        ["Database integration (SQLAlchemy)", "OAuth2/JWT authentication",
         "Background tasks", "Testing with TestClient"],
        "Add persistent storage, login and tests to the notes API.",
        teaches=["FastAPI"], requires=["fastapi_core", "sql_basics", "auth_core"], hours=12)
_module("react_core", "React fundamentals", "Foundation",
        ["Components and JSX", "Props and state", "Event handling", "Lists and forms"],
        "Build a recipe browser with reusable components.",
        teaches=["React"], requires=["js_core"], hours=12,
        resources=[("React: Learn", "https://react.dev/learn")])
_module("react_state_hooks", "React hooks and state management", "Core Development",
        ["useState/useEffect/useRef", "Custom hooks", "Context and reducers",
         "Performance basics"],
        "Add favourites and filters with context and a custom hook.",
        teaches=["React"], requires=["react_core"], hours=10)
_module("react_data_routing", "React data fetching and routing", "Advanced",
        ["API integration", "Loading/error states", "Client-side routing",
         "Testing components"],
        "Make the recipe browser consume a real REST API.",
        teaches=["React"], requires=["react_state_hooks", "js_async_dom", "rest_api_design"], hours=10)
_module("nextjs_core", "Next.js fundamentals", "Core Development",
        ["Pages/app router and layouts", "Server vs client components",
         "Data fetching", "Deployment"],
        "Rebuild the recipe browser in Next.js with server-side rendering.",
        teaches=["Next.js"], requires=["react_core"], hours=10,
        resources=[("Learn Next.js", "https://nextjs.org/learn")])
_module("nextjs_fullstack", "Full-stack Next.js", "Advanced",
        ["API routes / server actions", "Authentication", "Database integration"],
        "Add accounts and a database to the Next.js app.",
        teaches=["Next.js"], requires=["nextjs_core", "react_data_routing", "auth_core", "sql_basics"],
        hours=12)
_module("node_core", "Node.js fundamentals", "Core Development",
        ["Event loop and modules", "File system and streams", "npm", "Async patterns"],
        "Write a Node CLI that processes files asynchronously.",
        teaches=["Node.js"], requires=["js_async_dom"], hours=8,
        resources=[("Learn Node.js", "https://nodejs.org/en/learn")])
_module("express_api", "Building APIs with Express", "Core Development",
        ["Routing and middleware", "Validation and error handling",
         "Database integration", "Authentication"],
        "Build a REST API for a task tracker with Express.",
        teaches=["Express"], requires=["node_core", "rest_api_design"], hours=10,
        resources=[("Express guide", "https://expressjs.com/en/starter/installing.html")])
_module("flutter_core", "Flutter fundamentals", "Core Development",
        ["Project setup and structure", "Widgets and the widget tree",
         "Layouts and responsive UI"],
        "Build a static multi-screen UI for an expense tracker.",
        teaches=["Flutter"], requires=["dart_core"], hours=12,
        resources=[("Flutter codelab", "https://docs.flutter.dev/get-started/codelab")])
_module("flutter_state_nav", "Flutter state management and navigation", "Core Development",
        ["State management fundamentals", "Navigation and routing", "Forms"],
        "Make the expense tracker interactive across screens.",
        teaches=["Flutter"], requires=["flutter_core"], hours=10)
_module("flutter_data_storage", "Flutter APIs and local storage", "Advanced",
        ["Calling REST APIs and parsing JSON", "Local storage (SQLite/shared prefs)",
         "Testing Flutter apps"],
        "Persist expenses locally and sync with a mock API.",
        teaches=["Flutter"], requires=["flutter_state_nav", "dart_async", "json_basics"], hours=10)

# ---- AI / ML ----------------------------------------------------------------
_module("numpy_pandas", "NumPy and pandas for data work", "Foundation",
        ["Arrays and vectorisation", "DataFrames", "Cleaning and joining data",
         "Basic plotting"],
        "Clean and explore a messy public dataset.",
        teaches=["NumPy", "Pandas"], requires=["py_core"], hours=12,
        resources=[("pandas 10-minute guide", "https://pandas.pydata.org/docs/user_guide/10min.html"),
                   ("NumPy absolute beginners", "https://numpy.org/doc/stable/user/absolute_beginners.html")])
_module("ml_core", "Machine learning foundations", "Core Development",
        ["Probability/statistics refresher", "Supervised vs unsupervised learning",
         "Regression, trees and clustering", "Train/validation/test splits",
         "Overfitting and regularisation"],
        "Train and compare three models on a tabular dataset.",
        teaches=["Machine Learning"], requires=["numpy_pandas", "py_core"], hours=30,
        resources=[("scikit-learn user guide", "https://scikit-learn.org/stable/user_guide.html")])
_module("ml_model_eval", "Model evaluation and tuning", "Advanced",
        ["Metrics (precision/recall/F1/ROC)", "Cross-validation",
         "Hyperparameter search", "Error analysis"],
        "Tune and error-analyse the model, then write up results.",
        teaches=["Machine Learning"], requires=["ml_core"], hours=10)
_module("sklearn_workflow", "scikit-learn pipelines", "Core Development",
        ["Estimator API", "Pipelines and preprocessing", "Model persistence"],
        "Package preprocessing and model into one saved pipeline.",
        teaches=["Scikit-learn"], requires=["ml_core"], hours=6)
_module("deep_learning_core", "Deep learning foundations", "Core Development",
        ["Neural networks and backpropagation", "Optimisers and loss functions",
         "Regularisation", "Training loops and GPUs"],
        "Train a small network on MNIST/CIFAR-10 and plot learning curves.",
        teaches=["Deep Learning"], requires=["ml_core"], hours=30,
        resources=[("PyTorch tutorials", "https://pytorch.org/tutorials/")])
_module("dl_architectures", "CNNs, RNNs and transformers", "Advanced",
        ["Convolutional networks", "Sequence models", "Attention and transformers",
         "Transfer learning"],
        "Fine-tune a pretrained model on a custom dataset.",
        teaches=["Deep Learning"], requires=["deep_learning_core"], hours=25)
_module("pytorch_core", "PyTorch in practice", "Core Development",
        ["Tensors and autograd", "Datasets and DataLoaders", "nn.Module and training loops"],
        "Re-implement the CIFAR-10 classifier in PyTorch.",
        teaches=["PyTorch"], requires=["deep_learning_core"], hours=10,
        resources=[("PyTorch tutorials", "https://pytorch.org/tutorials/")])
_module("tf_keras_core", "TensorFlow and Keras in practice", "Core Development",
        ["Keras layers and models", "tf.data pipelines", "Callbacks and saving models"],
        "Re-implement the CIFAR-10 classifier in Keras.",
        teaches=["TensorFlow", "Keras"], requires=["deep_learning_core"], hours=10,
        resources=[("TensorFlow tutorials", "https://www.tensorflow.org/tutorials")])
_module("opencv_basics", "Image processing with OpenCV", "Core Development",
        ["Reading and transforming images", "Filtering and edges", "Contours and features"],
        "Detect and crop documents in photographs.",
        teaches=["OpenCV", "Image Processing"], requires=["numpy_pandas"], hours=10,
        resources=[("OpenCV tutorials", "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html")])
_module("cv_core", "Computer vision with deep learning", "Advanced",
        ["Image classification", "Object detection", "Segmentation basics", "Augmentation"],
        "Train an object detector on a small custom dataset.",
        teaches=["Computer Vision"], requires=["opencv_basics", "deep_learning_core"], hours=20)
_module("nlp_core", "Natural language processing foundations", "Core Development",
        ["Tokenisation and text cleaning", "TF-IDF and embeddings",
         "Text classification", "Evaluation of NLP systems"],
        "Build a sentiment classifier and compare TF-IDF vs embeddings.",
        teaches=["Natural Language Processing"], requires=["ml_core"], hours=20,
        resources=[("Hugging Face NLP course", "https://huggingface.co/learn/nlp-course")])
_module("nlp_transformers", "Transformers for NLP", "Advanced",
        ["Attention and transformer architecture", "Fine-tuning pretrained models",
         "Sequence labelling and generation"],
        "Fine-tune a transformer on a text classification task.",
        teaches=["Natural Language Processing"], requires=["nlp_core", "deep_learning_core"], hours=20)
_module("llm_foundations", "Large language model fundamentals", "Core Development",
        ["How LLMs work and their limits", "Tokens and context windows",
         "Running local models (e.g. Ollama) vs hosted APIs", "Evaluating outputs"],
        "Run a local model and compare its answers on a fixed question set.",
        teaches=["Large Language Models"], requires=["py_core"], hours=8,
        resources=[("Ollama", "https://github.com/ollama/ollama")])
_module("prompt_engineering", "Prompt engineering", "Core Development",
        ["Instruction and few-shot prompting", "Structured/JSON outputs",
         "Prompt evaluation and iteration"],
        "Write and test prompts that extract structured data from text.",
        teaches=["Prompt Engineering"], requires=["llm_foundations"], hours=5)
_module("llm_integration", "Integrating LLMs into applications", "Advanced",
        ["Calling model APIs from code", "Retrieval-augmented generation",
         "Output validation and guardrails", "Cost/latency considerations"],
        "Build a document Q&A app with retrieval over your own files.",
        teaches=["LLM Integration"], requires=["llm_foundations", "rest_api_design", "json_basics"],
        hours=15)

# ---- Cloud / DevOps ---------------------------------------------------------
_module("cloud_fundamentals", "Cloud computing fundamentals", "Foundation",
        ["IaaS/PaaS/SaaS", "Regions, availability and pricing", "Identity and access basics",
         "Shared responsibility"],
        "Compare how three providers price a small web app.",
        teaches=["Cloud Computing"], hours=6)
_module("aws_core", "AWS core services", "Core Development",
        ["Account setup and IAM", "EC2 and networking (VPC basics)", "S3 and databases (RDS)",
         "Cost management"],
        "Launch a VM, attach a role, and serve a static site from S3.",
        teaches=["AWS"], requires=["cloud_fundamentals", "linux_basics"], hours=15,
        resources=[("AWS documentation", "https://docs.aws.amazon.com/")])
_module("aws_storage", "Working with S3", "Core Development",
        ["Buckets and objects", "Access policies and presigned URLs", "Lifecycle rules",
         "SDK access from code"],
        "Upload files to S3 from an app using presigned URLs.",
        teaches=["AWS S3"], requires=["aws_core"], hours=5)
_module("aws_deploy_monitor", "Deploying and monitoring on AWS", "Advanced",
        ["Deploy an app (EC2, ECS or Lambda)", "Load balancing and scaling",
         "CloudWatch logs and alarms", "Least-privilege IAM"],
        "Deploy a containerised API on AWS with logging and an alarm.",
        teaches=["AWS"], requires=["aws_core"], hours=15)
_module("azure_core", "Microsoft Azure core services", "Core Development",
        ["Subscriptions and resource groups", "VMs and App Service", "Storage and identity",
         "Cost management"],
        "Deploy a web app to Azure App Service.",
        teaches=["Microsoft Azure"], requires=["cloud_fundamentals"], hours=15,
        resources=[("Microsoft Learn: Azure", "https://learn.microsoft.com/en-us/training/azure/")])
_module("gcp_core", "Google Cloud core services", "Core Development",
        ["Projects and IAM", "Compute Engine and Cloud Run", "Cloud Storage",
         "Cost management"],
        "Deploy a container to Cloud Run.",
        teaches=["Google Cloud"], requires=["cloud_fundamentals"], hours=15,
        resources=[("Google Cloud docs", "https://cloud.google.com/docs")])
_module("docker_basics", "Docker fundamentals", "Core Development",
        ["Images and containers", "Dockerfile", "Volumes and networking", "Docker Hub"],
        "Containerise a small web API.",
        teaches=["Docker"], requires=["linux_basics"], hours=8,
        resources=[("Docker get started", "https://docs.docker.com/get-started/")])
_module("docker_compose_images", "Docker Compose and production images", "Advanced",
        ["Multi-container apps with Compose", "Multi-stage builds", "Image security",
         "Environment configuration"],
        "Run an API plus database with Compose and a slim production image.",
        teaches=["Docker"], requires=["docker_basics"], hours=6)
_module("k8s_core", "Kubernetes essentials", "Advanced",
        ["Pods, Deployments and Services", "ConfigMaps and Secrets", "Ingress",
         "Scaling and rollouts"],
        "Deploy the Compose app to a local cluster (kind/minikube).",
        teaches=["Kubernetes"], requires=["docker_basics"], hours=15,
        resources=[("Kubernetes tutorials", "https://kubernetes.io/docs/tutorials/")])
_module("cicd_basics", "CI/CD pipelines", "Core Development",
        ["Pipeline stages: build, test, deploy", "GitHub Actions or similar",
         "Secrets and environments", "Deployment strategies"],
        "Add a pipeline that tests and builds on every push.",
        teaches=["CI/CD"], requires=["git_basics", "testing_fundamentals"], hours=8,
        resources=[("GitHub Actions docs", "https://docs.github.com/en/actions")])

# ---- Networking / software architecture ------------------------------------
_module("net_fundamentals", "Networking fundamentals", "Foundation",
        ["OSI and TCP/IP models", "IP addressing and subnetting", "Ports and protocols",
         "Common tools (ping, traceroute, curl)"],
        "Subnet a network on paper and verify paths with traceroute.",
        teaches=["TCP/IP", "Networking"], hours=12)
_module("dns_core", "DNS in depth", "Core Development",
        ["Resolution process and record types", "Caching and TTL", "Debugging with dig"],
        "Trace a full DNS resolution with dig and explain each hop.",
        teaches=["DNS"], requires=["net_fundamentals"], hours=4,
        resources=[("Cloudflare: What is DNS", "https://www.cloudflare.com/learning/dns/what-is-dns/")])
_module("routing_switching", "Routing and switching", "Core Development",
        ["VLANs and switching", "Static and dynamic routing", "LAN/WAN design", "NAT"],
        "Simulate a two-site network with routing in a simulator.",
        teaches=["Routing", "Switching"], requires=["net_fundamentals"], hours=20)
_module("net_security", "Firewalls and VPNs", "Advanced",
        ["Firewall rules and zones", "VPN types and set-up", "Network segmentation"],
        "Configure a firewall and a site-to-site or WireGuard VPN in a lab.",
        teaches=["Firewall", "VPN"], requires=["net_fundamentals"], hours=12)
_module("net_troubleshooting", "Network administration and troubleshooting", "Advanced",
        ["Monitoring and logging", "Systematic troubleshooting", "Packet capture",
         "Documentation and change control"],
        "Diagnose three injected faults in a lab network.",
        teaches=["Network Administration"], requires=["net_fundamentals"], hours=10)
_module("microservices_core", "Microservices architecture", "Advanced",
        ["Service boundaries", "Inter-service communication", "Data consistency",
         "Observability", "When not to use microservices"],
        "Split a monolith into two services that talk over HTTP.",
        teaches=["Microservices"], requires=["rest_api_design", "docker_basics"], hours=12,
        resources=[("Microservices patterns", "https://microservices.io/patterns/")])

# ---- Family placeholders: shallow, generic, always flagged ------------------
_FAMILY_NOTE = "Generic placeholder - replace with a real module for this technology."
_module("fam_language", "Learn a programming language (generic)", "Foundation",
        ["Install toolchain and run hello-world", "Types, control flow, functions",
         "Standard library and package manager", "Write tests"],
        "Re-implement a small project you built before in this language.",
        requires=["py_core"], hours=30, family=True)
_module("fam_framework", "Learn a web framework (generic)", "Core Development",
        ["Official getting-started tutorial", "Routing and project structure",
         "Data access and templates/components", "Deploy a sample app"],
        "Build a CRUD app with the framework's official tutorial as a base.",
        requires=["http_basics"], hours=15, family=True)
_module("fam_database", "Learn a database technology (generic)", "Core Development",
        ["Install and connect", "Data model and queries", "Indexing", "Backup"],
        "Load a sample dataset and write ten representative queries.",
        requires=["sql_basics"], hours=10, family=True)
_module("fam_ai_ml", "Learn an AI/ML technique or library (generic)", "Advanced",
        ["Official tutorials", "Reproduce an example end to end", "Evaluate results"],
        "Reproduce an official example, then adapt it to your own data.",
        requires=["ml_core"], hours=12, family=True)
_module("fam_cloud", "Learn a cloud/container tool (generic)", "Advanced",
        ["Getting-started guide", "Deploy a sample workload", "Security and cost"],
        "Deploy a sample workload using only the official docs.",
        requires=["cloud_fundamentals"], hours=10, family=True)
_module("fam_devops", "Learn a DevOps tool (generic)", "Advanced",
        ["Install and configure", "Automate one real task", "Integrate with CI/CD"],
        "Automate one repeatable task from your previous projects with this tool.",
        requires=["linux_basics", "git_basics"], hours=10, family=True)
_module("fam_tool", "Learn a developer tool (generic)", "Core Development",
        ["Install and configure", "Core workflow", "Integrate into a project"],
        "Use the tool on one of your existing projects.",
        hours=4, family=True)
_module("fam_backend", "Learn a backend concept (generic)", "Core Development",
        ["Concept and use cases", "Official documentation example", "Implement in a small service"],
        "Add the concept to a small API.",
        requires=["rest_api_design"], hours=6, family=True)
_module("fam_software_eng", "Learn a software engineering practice (generic)", "Advanced",
        ["Concept and when to apply it", "Apply to existing code", "Review trade-offs"],
        "Apply the practice to one of your earlier projects.",
        hours=6, family=True)
_module("fam_networking", "Learn a networking protocol or tool (generic)", "Core Development",
        ["Purpose and message flow", "Lab with packet capture", "Common failures"],
        "Capture and annotate the protocol's traffic.",
        requires=["net_fundamentals"], hours=5, family=True)
_module("fam_testing", "Learn a testing tool or technique (generic)", "Core Development",
        ["Official tutorial", "Write tests for a sample app", "Run in CI"],
        "Write a small suite using the tool on an existing project.",
        requires=["testing_fundamentals"], hours=6, family=True)
_module("fam_mobile", "Learn a mobile development technology (generic)", "Core Development",
        ["Official getting-started guide", "Build a two-screen app", "Run on a device"],
        "Build a small app following the official codelab.",
        hours=15, family=True)
_module("fam_os", "Learn an operating system / admin tool (generic)", "Core Development",
        ["Install and navigate", "Users and permissions", "Services and logs"],
        "Set up a VM and perform common administration tasks.",
        hours=8, family=True)
_module("fam_security", "Learn a security technology (generic)", "Advanced",
        ["Threat model", "Official documentation", "Lab deployment"],
        "Deploy the technology in an isolated lab.",
        hours=10, family=True)
_module("fam_data_eng", "Learn a data engineering tool (generic)", "Advanced",
        ["Concepts and architecture", "Run a local example", "Build a small pipeline"],
        "Process a medium-sized dataset using the tool.",
        requires=["py_core", "sql_basics"], hours=15, family=True)


# =============================================================================
# 2. SKILL -> MODULE MAPPING  (canonical ontology names)
# =============================================================================
# Skills listed here have "detailed" coverage. Prerequisites are resolved from
# each module's `requires`, so lists only need the skill's own modules.
SKILL_MODULES = {
    # languages
    "Python": ["py_core", "py_intermediate"],
    "Java": ["java_core", "oop_core"],
    "C++": ["cpp_core", "oop_core"],
    "JavaScript": ["js_core", "js_async_dom"],
    "TypeScript": ["ts_core"],
    "SQL": ["sql_basics", "sql_joins_design"],
    "Dart": ["dart_core", "dart_async"],
    "HTML": ["html_css_basics"],
    "CSS": ["html_css_basics"],
    # frameworks
    "Django": ["django_core", "django_orm", "django_forms_auth", "drf", "django_testing"],
    "Flask": ["flask_core", "flask_data_api"],
    "FastAPI": ["fastapi_core", "fastapi_db_auth"],
    "Pydantic": ["pydantic_models"],
    "React": ["react_core", "react_state_hooks", "react_data_routing"],
    "Next.js": ["nextjs_core", "nextjs_fullstack"],
    "Node.js": ["node_core"],
    "Express": ["express_api"],
    "Flutter": ["flutter_core", "flutter_state_nav", "flutter_data_storage"],
    # databases
    "Database": ["sql_basics", "db_design"],
    "Database Design": ["sql_basics", "db_design"],
    "Relational Database Design": ["sql_basics", "db_design"],
    "MySQL": ["sql_basics", "sql_joins_design", "rdbms_engine_practice"],
    "PostgreSQL": ["sql_basics", "sql_joins_design", "rdbms_engine_practice"],
    "SQLite": ["sql_basics", "sql_joins_design", "rdbms_engine_practice"],
    "Oracle": ["sql_basics", "sql_joins_design", "rdbms_engine_practice"],
    "Microsoft SQL Server": ["sql_basics", "sql_joins_design", "rdbms_engine_practice"],
    "Database Administration": ["sql_basics", "rdbms_engine_practice"],
    "Database Management": ["sql_basics", "rdbms_engine_practice"],
    "Database Backup": ["sql_basics", "rdbms_engine_practice"],
    "Database Monitoring": ["sql_basics", "rdbms_engine_practice"],
    "MongoDB": ["mongodb_core"],
    # AI / ML
    "Machine Learning": ["numpy_pandas", "ml_core", "ml_model_eval"],
    "Deep Learning": ["deep_learning_core", "dl_architectures"],
    "Artificial Neural Networks (ANN)": ["deep_learning_core"],
    "Natural Language Processing": ["nlp_core", "nlp_transformers"],
    "Computer Vision": ["opencv_basics", "cv_core"],
    "Image Processing": ["opencv_basics"],
    "OpenCV": ["opencv_basics"],
    "Large Language Models": ["llm_foundations"],
    "Generative AI": ["llm_foundations"],
    "LLM Integration": ["llm_foundations", "llm_integration"],
    "Prompt Engineering": ["prompt_engineering"],
    "TensorFlow": ["tf_keras_core"],
    "Keras": ["tf_keras_core"],
    "PyTorch": ["pytorch_core"],
    "Scikit-learn": ["sklearn_workflow"],
    "Pandas": ["numpy_pandas"],
    "NumPy": ["numpy_pandas"],
    # cloud / devops
    "Cloud Computing": ["cloud_fundamentals"],
    "AWS": ["aws_core", "aws_deploy_monitor"],
    "AWS S3": ["aws_storage"],
    "Microsoft Azure": ["azure_core"],
    "Google Cloud": ["gcp_core"],
    "Docker": ["docker_basics", "docker_compose_images"],
    "Kubernetes": ["k8s_core"],
    "CI/CD": ["cicd_basics"],
    "DevOps": ["git_basics", "cicd_basics", "docker_basics"],
    # developer tools / OS
    "Git": ["git_basics"],
    "GitHub": ["github_workflow"],
    "Version Control": ["git_basics"],
    "Bash": ["shell_scripting"],
    "Linux": ["linux_basics", "linux_admin"],
    # backend concepts
    "REST API": ["rest_api_design"],
    "RESTful Backend": ["rest_api_design", "auth_core"],
    "WebSockets": ["websockets_realtime"],
    "Authentication": ["auth_core"],
    "Authorization": ["auth_core"],
    "RBAC": ["rbac_core"],
    "JSON": ["json_basics"],
    "JSON Schema": ["json_basics", "json_in_code"],
    "GraphQL": ["graphql_core"],
    # software engineering
    "Object-Oriented Programming": ["oop_core"],
    "Object-Oriented Design": ["oop_core", "design_patterns"],
    "Microservices": ["microservices_core"],
    "Full-Stack Development": ["html_css_basics", "js_core", "js_async_dom", "rest_api_design", "sql_basics"],
    "Web Application Development": ["html_css_basics", "js_core", "js_async_dom", "rest_api_design", "sql_basics"],
    # networking
    "HTTP": ["http_basics"],
    "DNS": ["dns_core"],
    "TCP/IP": ["net_fundamentals"],
    "Networking": ["net_fundamentals", "routing_switching"],
    "Routing": ["routing_switching"],
    "Switching": ["routing_switching"],
    "LAN": ["routing_switching"],
    "WAN": ["routing_switching"],
    "Router": ["routing_switching"],
    "VPN": ["net_security"],
    "Firewall": ["net_security"],
    "Network Administration": ["net_troubleshooting"],
    # testing
    "PyUnit": ["pyunit_core", "pyunit_mocking"],
    "Selenium": ["selenium_core"],
    "Test Cases": ["testing_fundamentals"],
    "Manual Testing": ["test_types"],
    "Functional Testing": ["test_types"],
    "Regression Testing": ["test_types"],
    "Integration Testing": ["test_types"],
    "System Testing": ["test_types"],
    "Exploratory Testing": ["test_types"],
    "Web Testing": ["test_types"],
}

# Ontology category -> generic family module (coverage "family", flagged)
CATEGORY_FAMILY_MODULE = {
    "programming_languages": "fam_language",
    "web_frameworks": "fam_framework",
    "databases": "fam_database",
    "ai_ml": "fam_ai_ml",
    "cloud": "fam_cloud",
    "devops": "fam_devops",
    "developer_tools": "fam_tool",
    "backend_concepts": "fam_backend",
    "software_engineering": "fam_software_eng",
    "networking": "fam_networking",
    "testing": "fam_testing",
    "mobile_development": "fam_mobile",
    "operating_systems": "fam_os",
    "cybersecurity": "fam_security",
    "data_engineering": "fam_data_eng",
}
NON_TECHNICAL_CATEGORIES = {"soft_skills"}  # "other" stays unsupported on purpose


# =============================================================================
# 3. COMBINED PROJECTS  (one project exercising several missing skills)
# =============================================================================
# uses      - skills the project exercises
# uses_any  - groups where ONE member is enough (e.g. any backend framework)
PROJECTS = [
    {"id": "backend_api", "title": "Authenticated REST API with a database",
     "uses": ["REST API", "Authentication", "JSON", "SQL", "PyUnit", "Docker", "Git", "Linux",
              "Pydantic", "RBAC"],
     "uses_any": [["Django", "FastAPI", "Flask", "Express"]],
     "milestones": ["Design the resources and database schema",
                    "Implement CRUD endpoints with validation",
                    "Add registration, login and protected routes",
                    "Write automated tests",
                    "Containerise it and document the API"]},
    {"id": "deploy_service", "title": "Containerise and deploy a service to the cloud",
     "uses": ["Docker", "AWS", "Microsoft Azure", "Google Cloud", "Kubernetes", "CI/CD",
              "Linux", "AWS S3", "Git"],
     "uses_any": [],
     "milestones": ["Containerise an existing API",
                    "Provision a VM or managed container service",
                    "Deploy with a CI/CD pipeline triggered on push",
                    "Add logging, an alarm and a cost budget"]},
    {"id": "fullstack_web", "title": "Full-stack web application",
     "uses": ["React", "Next.js", "JavaScript", "TypeScript", "HTML", "CSS", "REST API",
              "Node.js", "Express", "Authentication", "SQL", "MongoDB"],
     "uses_any": [],
     "milestones": ["Build the UI with reusable components",
                    "Create the API and database layer",
                    "Connect front end and back end with auth",
                    "Deploy and write a README"]},
    {"id": "mobile_app", "title": "Cross-platform mobile app with an API",
     "uses": ["Flutter", "Dart", "REST API", "JSON"],
     "uses_any": [],
     "milestones": ["Design screens and navigation",
                    "Implement state management",
                    "Consume a REST API and parse JSON",
                    "Persist data locally and test"]},
    {"id": "ml_pipeline", "title": "End-to-end machine learning project",
     "uses": ["Machine Learning", "Pandas", "NumPy", "Scikit-learn", "Python", "Git"],
     "uses_any": [],
     "milestones": ["Choose a dataset and define the problem",
                    "Clean data and engineer features",
                    "Train, tune and compare models",
                    "Evaluate honestly and write up results"]},
    {"id": "dl_project", "title": "Deep learning model with a reproducible training pipeline",
     "uses": ["Deep Learning", "PyTorch", "TensorFlow", "Keras", "Computer Vision",
              "Artificial Neural Networks (ANN)", "OpenCV", "Image Processing"],
     "uses_any": [],
     "milestones": ["Prepare the dataset and baseline",
                    "Train a network and track metrics",
                    "Improve with augmentation or transfer learning",
                    "Analyse errors and document results"]},
    {"id": "nlp_llm_app", "title": "NLP / LLM application using a local model",
     "uses": ["Natural Language Processing", "Large Language Models", "LLM Integration",
              "Prompt Engineering", "Generative AI", "REST API"],
     "uses_any": [],
     "milestones": ["Define a task and evaluation set",
                    "Build the text pipeline and prompts",
                    "Run with a local model (e.g. via Ollama)",
                    "Add output validation and evaluate"]},
    {"id": "linux_automation", "title": "Linux automation toolkit",
     "uses": ["Linux", "Bash", "Git", "Networking", "Python"],
     "uses_any": [],
     "milestones": ["Write scripts for backups and log rotation",
                    "Schedule them with cron/systemd",
                    "Add monitoring of processes and disk use",
                    "Document and version-control the toolkit"]},
    {"id": "test_automation", "title": "Automated test suite for a web application",
     "uses": ["PyUnit", "Selenium", "Test Cases", "Regression Testing", "Functional Testing",
              "Integration Testing", "Manual Testing", "CI/CD", "Web Testing"],
     "uses_any": [],
     "milestones": ["Write a test plan and test cases",
                    "Automate unit and UI tests",
                    "Create a regression suite",
                    "Run it automatically in CI"]},
    {"id": "database_project", "title": "Designed, tuned and backed-up relational database",
     "uses": ["SQL", "Database Design", "PostgreSQL", "MySQL", "Database Administration",
              "Database Backup", "Database Monitoring", "Database Management"],
     "uses_any": [],
     "milestones": ["Design and normalise the schema",
                    "Load data and write representative queries",
                    "Add indexes and measure with EXPLAIN",
                    "Script backup and restore"]},
    {"id": "network_lab", "title": "Segmented network lab",
     "uses": ["Networking", "TCP/IP", "DNS", "Routing", "Switching", "Firewall", "VPN",
              "Network Administration"],
     "uses_any": [],
     "milestones": ["Design addressing and VLANs",
                    "Configure routing and DNS",
                    "Add firewall rules and a VPN",
                    "Troubleshoot injected faults"]},
]


# =============================================================================
# 4. SKILL NAME HANDLING
# =============================================================================
_CANONICAL = {}   # casefolded name or alias -> canonical ontology name
_CATEGORY = {}    # canonical name -> ontology category

for _cat, _skills in SKILL_ONTOLOGY.items():
    for _canon in _skills:
        _CANONICAL[_canon.casefold()] = _canon
        _CATEGORY.setdefault(_canon, _cat)
for _cat, _skills in SKILL_ONTOLOGY.items():
    for _canon, _aliases in _skills.items():
        for _alias in _aliases:
            _CANONICAL.setdefault(_alias.casefold(), _canon)


def canonical_skill(name):
    """Map a skill or alias to its canonical ontology name (case-insensitive)."""
    name = name.strip()
    return _CANONICAL.get(name.casefold(), name)


def classify_skill(skill):
    """Return (coverage, module_ids, message) for one canonical skill."""
    if skill in SKILL_MODULES:
        return "detailed", SKILL_MODULES[skill], ""
    category = _CATEGORY.get(skill)
    if category is None:
        return "unsupported", [], "Skill is not in the ontology; no curriculum available."
    if category in NON_TECHNICAL_CATEGORIES:
        return "non_technical", [], "Soft skill: build it through team projects, not a syllabus."
    family_module = CATEGORY_FAMILY_MODULE.get(category)
    if family_module:
        return ("family", [family_module],
                "Only a generic placeholder exists; add a dedicated module for this skill.")
    return "unsupported", [], "No curriculum content exists for this skill yet."


# =============================================================================
# 5. CATALOGUE VALIDATION / AUDIT
# =============================================================================
def validate_catalogue():
    """Return a list of problems (empty list = catalogue is consistent)."""
    problems = []
    for mid, mod in MODULES.items():
        if mod["stage"] not in _STAGE_RANK:
            problems.append(f"{mid}: unknown stage {mod['stage']!r}")
        for req in mod["requires"]:
            if req not in MODULES:
                problems.append(f"{mid}: requires unknown module {req!r}")
    for skill, mids in SKILL_MODULES.items():
        if skill not in _CATEGORY:
            problems.append(f"SKILL_MODULES: {skill!r} is not an ontology skill")
        for mid in mids:
            if mid not in MODULES:
                problems.append(f"SKILL_MODULES[{skill!r}]: unknown module {mid!r}")
    for cat, mid in CATEGORY_FAMILY_MODULE.items():
        if mid not in MODULES:
            problems.append(f"CATEGORY_FAMILY_MODULE[{cat!r}]: unknown module {mid!r}")

    state = {}  # cycle detection

    def visit(mid, trail):
        if state.get(mid) == "done":
            return
        if state.get(mid) == "active":
            problems.append("prerequisite cycle: " + " -> ".join(trail + [mid]))
            return
        state[mid] = "active"
        for req in MODULES[mid]["requires"]:
            if req in MODULES:
                visit(req, trail + [mid])
        state[mid] = "done"

    for mid in MODULES:
        visit(mid, [])
    return problems


def audit_catalogue():
    """List every ontology skill by coverage level - your content to-do list."""
    report = {"detailed": [], "family": [], "unsupported": [], "non_technical": []}
    for skills in SKILL_ONTOLOGY.values():
        for skill in skills:
            coverage, _, _ = classify_skill(skill)
            if skill not in report[coverage]:
                report[coverage].append(skill)
    return report


# =============================================================================
# 6. ROADMAP ENGINE
# =============================================================================
def _split_known(resume_skills, skill_evidence):
    """Known skills (strong evidence) and weakly evidenced skills."""
    evidence = {canonical_skill(k): v for k, v in (skill_evidence or {}).items()}
    known, weak = set(), []
    for raw in resume_skills or []:
        if not isinstance(raw, str) or not raw.strip():
            continue
        skill = canonical_skill(raw)
        if evidence.get(skill, 1.0) >= EVIDENCE_THRESHOLD:
            known.add(skill)
        elif skill not in weak:
            weak.append(skill)
    return known, weak


def _collect_modules(module_ids, known, kept, skipped):
    """Depth-first expansion of prerequisites, pruning what is already proven.

    Returns the module ids (prerequisites first) that this request needs.
    """
    result, seen = [], set()

    def visit(mid):
        if mid in seen:
            return
        seen.add(mid)
        mod = MODULES[mid]
        if mod["teaches"] and all(t in known for t in mod["teaches"]):
            skipped.setdefault(mid, "resume already evidences: " + ", ".join(mod["teaches"]))
            return
        for req in mod["requires"]:
            visit(req)
        result.append(mid)
        kept.add(mid)

    for mid in module_ids:
        visit(mid)
    return result


def _order_modules(nodes, priority):
    """Topological order; ties broken by stage, then priority, then catalogue order."""
    dependents = {m: [] for m in nodes}
    indegree = {m: 0 for m in nodes}
    for m in nodes:
        for req in MODULES[m]["requires"]:
            if req in nodes:
                dependents[req].append(m)
                indegree[m] += 1

    def key(m):
        return (_STAGE_RANK[MODULES[m]["stage"]], -priority[m], MODULES[m]["order"], m)

    heap = [key(m) for m in nodes if indegree[m] == 0]
    heapq.heapify(heap)
    ordered = []
    while heap:
        mid = heapq.heappop(heap)[-1]
        ordered.append(mid)
        for dep in dependents[mid]:
            indegree[dep] -= 1
            if indegree[dep] == 0:
                heapq.heappush(heap, key(dep))
    return ordered


def _select_projects(gap_skills, known, max_projects):
    """Greedy: pick projects that cover the most still-uncovered gap skills."""
    gaps = set(gap_skills)
    uncovered = set(gaps)
    chosen = []
    for _ in range(max_projects):
        best, best_covered = None, set()
        for project in PROJECTS:
            if any(p["id"] == project["id"] for p in chosen):
                continue
            if any(not (set(group) & (gaps | known)) for group in project["uses_any"]):
                continue
            covered = (set(project["uses"]) & uncovered)
            for group in project["uses_any"]:
                covered |= (set(group) & uncovered)
            if len(covered) > len(best_covered):
                best, best_covered = project, covered
        if best is None or len(best_covered) < (2 if not chosen else 1):
            break
        chosen.append({**best, "covers": sorted(best_covered)})
        uncovered -= best_covered
    return chosen


def generate_learning_roadmap(missing_skills, resume_skills,
                              skill_importance=None, skill_evidence=None,
                              max_projects=2):
    """Build ONE prioritised roadmap for the whole skill gap.

    missing_skills   - skills the job needs and the resume lacks
    resume_skills    - skills the resume has
    skill_importance - optional {skill: weight}; default 1.0 (e.g. required=1.0,
                       preferred=0.5)
    skill_evidence   - optional {skill: 0..1} confidence from the skill-evidence
                       module; resume skills below EVIDENCE_THRESHOLD are treated
                       as gaps rather than known
    """
    importance = {canonical_skill(k): v for k, v in (skill_importance or {}).items()}
    known, weak = _split_known(resume_skills, skill_evidence)

    gaps = []

    for raw in missing_skills or []:
        skill = canonical_skill(raw) if isinstance(raw, str) else None

        if skill and skill not in known and skill not in gaps:
                gaps.append(skill)

    kept, skipped = set(), {}
    per_skill, coverage, flagged = {}, {}, []
    needed_for = {}
    priority = {}

    for skill in gaps:
        level, base_modules, message = classify_skill(skill)
        coverage[skill] = level
        if level in ("unsupported", "non_technical"):
            flagged.append({"skill": skill, "status": level, "message": message})
            continue
        if level == "family":
            flagged.append({"skill": skill, "status": level, "message": message})

        modules = _collect_modules(base_modules, known, kept, skipped)
        per_skill[skill] = modules
        weight = importance.get(skill, 1.0)
        for mid in modules:
            needed_for.setdefault(mid, []).append(skill)
            priority[mid] = priority.get(mid, 0.0) + weight

    # Skill fully covered by existing evidence needs no modules at all.
    nodes = set(priority)
    ordered = _order_modules(nodes, priority)

    steps = []
    for number, mid in enumerate(ordered, start=1):
        mod = MODULES[mid]
        steps.append({
            "order": number, "module_id": mid, "title": mod["title"],
            "stage": mod["stage"], "topics": mod["topics"],
            "practice": mod["exercise"], "resources": mod["resources"],
            "hours": mod["hours"], "needed_for": sorted(needed_for[mid]),
            "priority": round(priority[mid], 2),
            "coverage": "family" if mod["family"] else "detailed",
            "note": _FAMILY_NOTE if mod["family"] else "",
        })

    stages = {stage: [s for s in steps if s["stage"] == stage] for stage in STAGES}
    stages = {stage: items for stage, items in stages.items() if items}

    covered_gaps = [s for s in gaps if s in per_skill]
    projects = _select_projects(covered_gaps, known, max_projects)

    return {
        "summary": {
            "gap_skills": gaps,
            "known_skills": sorted(known),
            "modules": len(steps),
            "estimated_hours": sum(s["hours"] for s in steps),
            "coverage": coverage,
        },
        "steps": steps,
        "stages": stages,
        "projects": projects,
        "flagged_skills": flagged,
        "skipped_modules": [{"module_id": m, "reason": r} for m, r in skipped.items()],
        # internal / debugging view: modules each skill pulled in
        "per_skill": per_skill,
    }


# =============================================================================
# 7. PRESENTATION
# =============================================================================
def format_roadmap(roadmap):
    """Plain-text rendering of the roadmap."""
    lines = []
    summary = roadmap["summary"]
    lines.append(f"Skills to learn: {', '.join(summary['gap_skills']) or 'none'}")
    lines.append(f"{summary['modules']} modules, roughly {summary['estimated_hours']} hours "
                 "(estimates, not promises)")

    for stage, steps in roadmap["stages"].items():
        lines.append(f"\n== {stage} ==")
        for s in steps:
            tag = " [generic placeholder]" if s["coverage"] == "family" else ""
            lines.append(f"{s['order']}. {s['title']}{tag}  (~{s['hours']}h; for: {', '.join(s['needed_for'])})")
            lines.append("   Topics: " + "; ".join(s["topics"]))
            lines.append("   Practice: " + s["practice"])
            for label, url in s["resources"]:
                lines.append(f"   Resource: {label} - {url}")

    if roadmap["projects"]:
        lines.append("\n== Combined projects ==")
        for p in roadmap["projects"]:
            lines.append(f"* {p['title']}  (exercises: {', '.join(p['covers'])})")
            for i, step in enumerate(p["milestones"], 1):
                lines.append(f"    {i}. {step}")
    else:
        lines.append("\nNo combined project fits this gap; use each module's practice task.")

    if roadmap["flagged_skills"]:
        lines.append("\n== Needs attention ==")
        for f in roadmap["flagged_skills"]:
            lines.append(f"! {f['skill']} ({f['status']}): {f['message']}")

    if roadmap["skipped_modules"]:
        lines.append("\n== Skipped (already evidenced) ==")
        for sk in roadmap["skipped_modules"]:
            lines.append(f"- {MODULES[sk['module_id']]['title']}: {sk['reason']}")
    return "\n".join(lines)


if __name__ == "__main__":
    problems = validate_catalogue()
    print("Catalogue problems:", problems or "none")

    print("\n##### Example 1: FastAPI job, resume has Python + SQL #####")
    roadmap = generate_learning_roadmap(
        missing_skills=["FastAPI", "Docker", "AWS"],
        resume_skills=["Python", "SQL"],
        skill_importance={"FastAPI": 1.0, "Docker": 0.8, "AWS": 0.6},
    )
    print(format_roadmap(roadmap))

    print("\n##### Example 2: Django job from your earlier test #####")
    roadmap = generate_learning_roadmap(
        missing_skills=["Django", "JSON", "PyUnit", "Linux"],
        resume_skills=["Python", "REST API"],
    )
    print(format_roadmap(roadmap))

    print("\n##### Coverage audit #####")
    audit = audit_catalogue()
    for level, skills in audit.items():
        print(f"{level}: {len(skills)}")
