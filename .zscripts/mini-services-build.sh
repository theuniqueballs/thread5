#!/bin/bash

# 配置项
# 2026-11-20: путь берём от расположения скрипта — жёсткий /home/z/my-project
# ломал сборку в любой другой раскладке (dev.sh так делает с самого начала)
SCRIPT_CWD="$(pwd)"
ROOT_DIR="${T5_MINI_SERVICES_DIR:-$SCRIPT_CWD/mini-services}"
DIST_DIR="/tmp/build_fullstack_$BUILD_ID/mini-services-dist"

main() {
    echo "🚀 开始批量构建..."
    
    # 检查 rootdir 是否存在
    if [ ! -d "$ROOT_DIR" ]; then
        echo "ℹ️  目录 $ROOT_DIR 不存在，跳过构建"
        return
    fi
    
    # 创建输出目录（如果不存在）
    mkdir -p "$DIST_DIR"
    
    # 统计变量
    success_count=0
    fail_count=0
    
    # 遍历 mini-services 目录下的所有文件夹
    for dir in "$ROOT_DIR"/*; do
        # 检查是否是目录且包含 package.json
        if [ -d "$dir" ] && [ -f "$dir/package.json" ]; then
            project_name=$(basename "$dir")
            
            # 智能查找入口文件 (按优先级查找)
            entry_path=""
            for entry in "src/index.ts" "index.ts" "src/index.js" "index.js"; do
                if [ -f "$dir/$entry" ]; then
                    entry_path="$dir/$entry"
                    break
                fi
            done
            
            if [ -z "$entry_path" ]; then
                echo "⚠️  跳过 $project_name: 未找到入口文件 (index.ts/js)"
                continue
            fi
            
            echo ""
            echo "📦 正在构建: $project_name..."
            
            # 使用 bun build CLI 构建
            output_file="$DIST_DIR/mini-service-$project_name.js"
            
            if bun build "$entry_path" \
                --outfile "$output_file" \
                --target bun \
                --minify; then
                echo "✅ $project_name 构建成功 -> $output_file"
                success_count=$((success_count + 1))
                # 2026-11-20: knowledge-пак оракула (readFileSync компут-путей не
                # попадает в бандл): без файлов рядом сервис падал в деплое (ENOENT)
                if [ "$project_name" = "oracle-service" ] && [ -d "$dir/../ecchi-oracle/taxonomy" ]; then
                    _dst="$DIST_DIR/ecchi-oracle"
                    mkdir -p "$_dst"
                    cp -r "$dir/../ecchi-oracle/taxonomy" "$dir/../ecchi-oracle/distill" "$_dst/" 2>/dev/null || true
                    echo "  - knowledge-пак скопирован: ecchi-oracle/taxonomy+distill"
                fi
            else
                echo "❌ $project_name 构建失败"
                fail_count=$((fail_count + 1))
            fi
        fi
    done
    
    if [ -f ./.zscripts/mini-services-start.sh ]; then
        cp ./.zscripts/mini-services-start.sh "$DIST_DIR/mini-services-start.sh"
        chmod +x "$DIST_DIR/mini-services-start.sh"
    fi
    
    echo ""
    echo "🎉 所有任务完成！"
    if [ $success_count -gt 0 ] || [ $fail_count -gt 0 ]; then
        echo "✅ 成功: $success_count 个"
        if [ $fail_count -gt 0 ]; then
            echo "❌ 失败: $fail_count 个"
        fi
    fi
}

main

