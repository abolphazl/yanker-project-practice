if !(type tmux >/dev/null 2>/dev/null); then
    echo "Tmux is not installed!";
    echo "Run it: sudo apt install tmux";
    exit;
fi

if [ ! -d ".venv" ]; then
    "python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
fi

export FLASK_DEBUG=true;

tmux kill-session -t yarnker-project;
tmux new-session -d -s yarnker-project 'source .venv/bin/activate && flask --app web run --reload ';
tmux split-window;
tmux send 'npx tailwindcss -i ./web/static/src/input.css -o ./web/static/css/output.css --watch' ENTER;
tmux a;