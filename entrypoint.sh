#!/bin/bash


echo "     ____             __        __                       ___                    __  "
echo "    / __ \____  _____/ /_____ _/ /_  ____ _________     /   | ____ ____  ____  / /_ "
echo "   / /_/ / __ \/ ___/ __/ __  / __ \/ __  / ___/ _ \   / /| |/ __  / _ \/ __ \/ __/ "
echo "  / ____/ /_/ / /  / /_/ /_/ / /_/ / /_/ (__  )  __/  / ___ / /_/ /  __/ / / / /_   "
echo " /_/    \____/_/   \__/\__,_/_.___/\__,_/____/\___/  /_/  |_\__, /\___/_/ /_/\__/   "
echo "                                                           /____/                   "


# Start Redis in the background
echo "Starting Redis server..."
redis-server --loglevel notice &>/dev/null &

# Start Celery worker in the background
echo "Starting Celery worker..."
celery -A main worker --loglevel=INFO  &

# Start Celery Beat in the background
echo "Starting Celery Beat..."
celery -A main beat --loglevel=info &

# Wait for all background processes
wait