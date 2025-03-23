### Prerequisites

- pyenv (Python version manager)
- pip package manager

### Installation

1. Install pyenv:
```bash
# On Ubuntu/Debian
curl https://pyenv.run | bash
```

2. Add pyenv to your shell configuration (~/.bashrc, ~/.zshrc, or similar):
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

3. Install Python 3.8.20 using pyenv:
```bash
pyenv install 3.8.20
pyenv local 3.8.20
```

4. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-boilerplate.git
cd fastapi-boilerplate
```

5. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

6. Install dependencies:
```bash
pip install -r requirements.txt
```
