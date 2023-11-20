#!/bin/bash


# 构建 Docker 镜像
docker build -t bot .

# 查找并停止当前正在运行的 bot 容器
running_container=$(docker ps -q --filter ancestor=bot)
if [ ! -z "$running_container" ]; then
    echo "Stopping running bot container..."
    docker stop $running_container
fi

# 重新启动 bot 容器
echo "Starting bot container..."
docker run -d --name bot bot
