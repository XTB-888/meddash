#!/bin/bash
# MedDash 云端部署脚本
# 使用 localtunnel 暴露服务到公网

echo "========================================"
echo "  MedDash 云端部署工具"
echo "========================================"

# 检查服务是否运行
echo "检查服务状态..."

BACKEND_RUNNING=$(lsof -ti:5000)
FRONTEND_RUNNING=$(lsof -ti:5173)

if [ -z "$BACKEND_RUNNING" ]; then
    echo "启动后端服务..."
    cd /workspace/api && python app.py > /tmp/backend.log 2>&1 &
    sleep 3
fi

if [ -z "$FRONTEND_RUNNING" ]; then
    echo "启动前端服务..."
    cd /workspace && npx vite preview --host 0.0.0.0 --port 5173 > /tmp/frontend.log 2>&1 &
    sleep 3
fi

echo ""
echo "创建公网隧道..."
echo ""

# 为后端创建隧道
echo "后端 API 隧道:"
lt --port 5000 &
LT_PID=$!

sleep 5

echo ""
echo "========================================"
echo "  部署完成！"
echo "========================================"
echo ""
echo "前端地址: http://localhost:5173"
echo "后端 API: http://localhost:5000"
echo ""
echo "公网地址请查看上方 localtunnel 输出"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "kill $LT_PID; exit" INT
wait
