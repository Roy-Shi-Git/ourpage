#!/bin/bash
cd "$(dirname "$0")"
python3 -m http.server 8080 &
sleep 1
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:8080
elif command -v open >/dev/null 2>&1; then
    open http://localhost:8080
else
    echo "请手动打开浏览器访问：http://localhost:8080"
fi
