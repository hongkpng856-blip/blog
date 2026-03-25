#!/bin/bash
# 部落格備份腳本
# 使用方式: ./scripts/backup.sh

# 設定顏色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 取得腳本所在目錄的父目錄（blog 根目錄）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLOG_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$BLOG_DIR/backup"

# 建立備份目錄（如果不存在）
mkdir -p "$BACKUP_DIR"

# 生成備份檔名（含時間戳）
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/blog_backup_$TIMESTAMP.tar.gz"

echo -e "${YELLOW}開始備份部落格...${NC}"
echo "來源目錄: $BLOG_DIR"
echo "備份檔案: $BACKUP_FILE"

# 建立備份（排除備份目錄本身和 Git 目錄）
cd "$BLOG_DIR"
tar --exclude='backup' --exclude='.git' -czf "$BACKUP_FILE" .

# 檢查備份是否成功
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 備份成功！${NC}"
    echo "備份檔案: $BACKUP_FILE"
    
    # 顯示備份檔案大小
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "備份大小: $BACKUP_SIZE"
    
    # 清理舊備份（保留最近 5 個）
    echo -e "${YELLOW}清理舊備份（保留最近 5 個）...${NC}"
    cd "$BACKUP_DIR"
    ls -t blog_backup_*.tar.gz | tail -n +6 | xargs -r rm
    echo -e "${GREEN}✓ 清理完成${NC}"
    
    # 顯示目前備份列表
    echo -e "${YELLOW}目前備份列表:${NC}"
    ls -lh blog_backup_*.tar.gz 2>/dev/null | head -5
else
    echo -e "\033[0;31m✗ 備份失敗！${NC}"
    exit 1
fi