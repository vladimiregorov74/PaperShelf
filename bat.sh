#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
VENV_PATH="$SCRIPT_DIR/.venv"
PYTHON_BIN="$VENV_PATH/bin/python"
MAIN_PY_PATH="$SCRIPT_DIR/src/papershelf/app.py"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "Python не найден: $PYTHON_BIN"
    exit 1
fi

# Добавляем корень проекта в PYTHONPATH
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/src"

cd "$SCRIPT_DIR" || exit 1

echo "Запуск приложения: $MAIN_PY_PATH"
nohup "$PYTHON_BIN" "$MAIN_PY_PATH" > server.log 2>&1 &
