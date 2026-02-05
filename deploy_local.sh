#!/bin/bash
# PsychoAI Bot - Local Docker deployment
# Usage: ./deploy_local.sh [start|stop|remove]

IMAGE="psychoai-bot"
CONTAINER="psychoai"

case "$1" in
    start)
        docker build -t $IMAGE .
        docker rm -f $CONTAINER 2>/dev/null
        docker run -d --name $CONTAINER --env-file .env --restart unless-stopped $IMAGE
        echo "✅ Started. Logs: docker logs -f $CONTAINER"
        ;;
    stop)
        docker stop $CONTAINER
        echo "✅ Stopped"
        ;;
    remove)
        docker rm -f $CONTAINER
        docker rmi $IMAGE
        echo "✅ Removed"
        ;;
    *)
        echo "Usage: ./deploy_local.sh [start|stop|remove]"
        ;;
esac
