#!/bin/bash

sudo apt update -y
sudo apt install -y docker.io

sudo systemctl start docker
sudo systemctl enable docker

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 변경사항 적용을 위해 로그아웃 후 다시 로그인 필요
