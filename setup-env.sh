# 1. Установи pyenv
brew install pyenv

# 2. Добавь в ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 3. Перезагрузи шелл
source ~/.zshrc

# 4. Установи нужную версию Python
pyenv install 3.11.9

# 5. В проекте
cd ~/Projects/zcode/promt_engineer_study
pyenv local 3.11.9    # создаст файл .python-version

# 6. Виртуальное окружение
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


cursor --install-extension ms-python.python \
       --install-extension charliermarsh.ruff \
       --install-extension ms-azuretools.vscode-docker \
       --install-extension eamodio.gitlens \
       --install-extension usernamehw.errorlens \
       --install-extension oderwat.indent-rainbow \
       --install-extension redhat.vscode-yaml \
       --install-extension tamasfe.even-better-toml \
       --install-extension pkief.material-icon-theme \
       --install-extension rangav.vscode-thunder-client \
       --install-extension ms-toolsai.jupyter

