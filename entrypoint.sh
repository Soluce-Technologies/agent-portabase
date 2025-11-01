#!/bin/bash


echo "     ____             __        __                       ___                    __  "
echo "    / __ \____  _____/ /_____ _/ /_  ____ _________     /   | ____ ____  ____  / /_ "
echo "   / /_/ / __ \/ ___/ __/ __  / __ \/ __  / ___/ _ \   / /| |/ __  / _ \/ __ \/ __/ "
echo "  / ____/ /_/ / /  / /_/ /_/ / /_/ / /_/ (__  )  __/  / ___ / /_/ /  __/ / / / /_   "
echo " /_/    \____/_/   \__/\__,_/_.___/\__,_/____/\___/  /_/  |_\__, /\___/_/ /_/\__/   "
echo "                                                           /____/                   "

# Print project version (from pyproject.toml via Hatch)
PROJECT_VERSION=$(python3 -c "from importlib.metadata import version; print(version('portabase-agent'))")
echo "[INFO] Project version: $PROJECT_VERSION"

#
#echo "/usr/lib/x86_64-linux-gnu" | tee /etc/ld.so.conf.d/libpq.conf
#ldconfig
#ldconfig -p | grep libpq
#ldd /usr/lib/postgresql/17/bin/pg_isready

# Add PostgreSQL lib path silently
echo "/usr/lib/x86_64-linux-gnu" | tee /etc/ld.so.conf.d/libpq.conf &>/dev/null
# Update linker cache silently
ldconfig &>/dev/null
# Optional: check for libpq without echoing output
ldconfig -p | grep libpq &>/dev/null
# Optional: check pg_isready without echoing output
ldd /usr/lib/postgresql/17/bin/pg_isready &>/dev/null || true




# Apply timezone from environment
if [ -n "$TZ" ]; then
    if [ -f "/usr/share/zoneinfo/$TZ" ]; then
        ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
        echo "$TZ" > /etc/timezone
        echo "[INFO] Timezone set to $TZ"
    else
        echo "[WARN] Timezone '$TZ' not found. Using default."
    fi
fi

# Start Redis in the background
echo "Starting Redis server..."
redis-server --loglevel notice &>/dev/null &

# Start Celery
if [ "$ENVIRONMENT" = "development" ]; then
    echo "[INFO] Starting Celery worker with hot reload..."
    watchmedo auto-restart \
        --directory=./src \
        --pattern="*.py" \
        --recursive \
        -- \
        celery -A main worker --loglevel=info &
else
    echo "[INFO] Starting Celery worker..."
    celery -A main worker --loglevel=info &
fi


# Start Celery Beat in the background
echo "Starting Celery Beat..."
celery -A main beat -S redbeat.RedBeatScheduler --loglevel=info &

# Wait for all background processes
wait