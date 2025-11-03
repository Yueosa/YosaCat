#!/usr/bin/env bash
set -e

SERVICE_NAME="yosacat"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_PATH="${PROJECT_DIR}/.venv/bin/python"
MAIN_FILE="${PROJECT_DIR}/main.py"

# 检查是否为root
if [ "$EUID" -ne 0 ]; then
  echo "❌ 请以 root 权限运行该脚本"
  echo "👉 示例：sudo bash $0"
  exit 1
fi

deploy_service() {
  echo "🧩 项目路径: $PROJECT_DIR"
  echo "🐍 解释器: $PYTHON_PATH"
  echo "⚙️  正在生成 systemd 服务文件..."

  cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=YosaCat QQ Bot
After=network.target

[Service]
WorkingDirectory=${PROJECT_DIR}
ExecStart=${PYTHON_PATH} ${MAIN_FILE}
Restart=always
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONPATH=${PROJECT_DIR}"

[Install]
WantedBy=multi-user.target
EOF

  echo "🔄 重新加载 systemd..."
  systemctl daemon-reload
  echo "📦 启用并启动服务..."
  systemctl enable ${SERVICE_NAME}
  systemctl restart ${SERVICE_NAME}
  echo "✅ 服务部署完成"
  systemctl status ${SERVICE_NAME} --no-pager
}

remove_service() {
  echo "🗑️ 正在停止并卸载服务..."
  systemctl stop ${SERVICE_NAME} || true
  systemctl disable ${SERVICE_NAME} || true
  rm -f "$SERVICE_FILE"
  systemctl daemon-reload
  echo "✅ 服务 ${SERVICE_NAME} 已完全卸载"
}

restart_service() {
  echo "🔁 正在重启服务 ${SERVICE_NAME}..."
  systemctl restart ${SERVICE_NAME}
  echo "✅ 服务已重启完成"
  systemctl status ${SERVICE_NAME} --no-pager
}

case "$1" in
  --deploy|"")
    deploy_service
    ;;
  --remove|--uninstall)
    remove_service
    ;;
  --restart)
    restart_service
    ;;
  *)
    echo "❓ 用法: sudo bash $0 [--deploy|--remove|--restart]"
    ;;
esac

