# Contributing to VynoBotRepo

We welcome and appreciate contributions to this project! Here are some guidelines to help you get started.

## How to Contribute

1.  **Fork the repository:** Start by forking our `vyno-bot-repo` repository on GitHub.
2.  **Clone your fork:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/vyno-bot-repo.git](https://github.com/YOUR_USERNAME/vyno-bot-repo.git)
    cd vyno-bot-repo
    ```
3.  **Create a new branch:** For each new feature or bug fix, create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
    or
    ```bash
    git checkout -b bugfix/issue-description
    ```
4.  **Make your changes:** Implement your feature or fix the bug. Ensure your code adheres to our style guidelines (PEP 8 for Python).
5.  **Run tests:** Before submitting, run all existing tests and add new ones for your changes.
    ```bash
    python -m unittest discover tests
    ```
6.  **Commit your changes:** Write clear, concise commit messages.
    ```bash
    git commit -m "feat: Add new awesome feature"
    ```
7.  **Push to your fork:**
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request (PR):** Go to your forked repository on GitHub and open a pull request to the `main` branch of the original `MrLiPx/vyno-bot-repo`. Provide a detailed description of your changes.

## Code Style

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
* Use meaningful variable and function names.
* Include docstrings for all modules, classes, and functions.
* Add comments where logic is complex.

## Reporting Bugs

If you find a bug, please open an issue on GitHub. Include:
* A clear, concise description of the bug.
* Steps to reproduce the behavior.
* Expected behavior.
* Screenshots or logs if helpful.

Thank you for contributing!
