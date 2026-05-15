#!/bin/bash
# 系统操作脚本 - 用于高危操作和重启操作

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示警告信息
show_warning() {
    echo -e "${RED}⚠️  高危操作警告！${NC}"
    echo -e "${YELLOW}此操作可能会影响系统正常运行${NC}"
    echo ""
}

# 重启系统
restart_system() {
    show_warning
    echo "即将执行系统重启..."
    echo ""
    read -p "确认要重启系统吗？(输入 yes 确认): " confirm
    if [ "$confirm" = "yes" ]; then
        echo "正在重启系统..."
        sudo shutdown -r now
    else
        echo -e "${GREEN}操作已取消${NC}"
    fi
}

# 关机系统
shutdown_system() {
    show_warning
    echo "即将执行系统关机..."
    echo ""
    read -p "确认要关机系统吗？(输入 yes 确认): " confirm
    if [ "$confirm" = "yes" ]; then
        echo "正在关闭系统..."
        sudo shutdown -h now
    else
        echo -e "${GREEN}操作已取消${NC}"
    fi
}

# 查看系统状态
check_system_status() {
    echo -e "${GREEN}=== 系统状态信息 ===${NC}"
    echo ""
    echo "系统信息:"
    uname -a
    echo ""
    echo "运行时间:"
    uptime
    echo ""
    echo "当前登录用户:"
    who
    echo ""
}

# 主菜单
main() {
    echo "=============================="
    echo "     系统操作管理工具"
    echo "=============================="
    echo ""
    echo "请选择操作:"
    echo "1. 重启系统"
    echo "2. 关机系统"
    echo "3. 查看系统状态"
    echo "4. 退出"
    echo ""
    read -p "请输入选项 (1-4): " choice
    
    case $choice in
        1)
            restart_system
            ;;
        2)
            shutdown_system
            ;;
        3)
            check_system_status
            ;;
        4)
            echo "退出程序"
            exit 0
            ;;
        *)
            echo "无效选项"
            ;;
    esac
}

# 如果直接执行脚本则运行主菜单
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi
