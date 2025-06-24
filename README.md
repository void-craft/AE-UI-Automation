# AutomationExercise Selenium POM UI Test Automation
This project contains automated UI tests for Automation Exercise using Selenium WebDriver with Python and the Page Object Model (POM) design pattern. Tests are implemented with PyTest to ensure maintainability and scalability.

### Features
- Clean Page Object Model architecture
- Selenium 4.6+ with automatic WebDriver management (no manual driver setup)
- PyTest integration with fixtures and markers
- Secure handling of credentials via environment variables and GitHub Secrets
- Continuous Integration configured with GitHub Actions

### Project Structure
```bash
Copy code
automationexercise-selenium-pom/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions workflow for CI
├── pages/                    # Page Object Model classes
│   ├── base_page.py
│   ├── login_page.py
│   └── register_page.py
├── tests/                    # Test cases using PyTest
│   ├── test_login.py
│   └── test_register.py
├── utils/                    # Utility modules (config, helpers)
│   ├── config.py
│   └── helpers.py
├── .gitignore                # Files and folders to ignore in git
├── conftest.py               # PyTest fixtures and setup
├── requirements.txt          # Python dependencies
├── pytest.ini                # PyTest configuration
├── .env                      # Local environment variables (ignored in git)
└── README.md                 # Project documentation
```

### Getting Started
Prerequisites
Python 3.11 or higher
pip package manager

### Installation
Clone the repository:

```bash
Copy code
git clone <repo-url>
cd automationexercise-selenium-pom
```

### Create and activate a virtual environment:

```bash
Copy code
python -m venv venv
source venv/bin/activate     # Linux/Mac
.\venv\Scripts\activate      # Windows
```

### Install dependencies:

```bash
Copy code
pip install -r requirements.txt
```

### Create a .env file in the project root with your credentials:

```ini
Copy code
AE_USERNAME=your_email@example.com
AE_PASSWORD=your_password
BASE_URL=https://automationexercise.com
```

Note: Since this project uses Selenium 4.6 or later, the WebDriver binaries (e.g., ChromeDriver) are managed automatically by Selenium — no manual driver downloads or PATH setup needed.

### Running Tests
Run all tests with:

```bash
Copy code
pytest -v
```

### CI/CD Integration
The project is configured to run tests automatically on push and pull requests via GitHub Actions. Credentials are securely injected using GitHub Secrets.

### Contributing
Feel free to open issues or submit pull requests to improve test coverage or add features.

### License
MIT License

### Contact me:
hemapriyaweb@gmai.com
linkedin.com/in/hemaps
