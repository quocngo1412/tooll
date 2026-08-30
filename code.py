cat << 'EOF' > petsim.sh
#!/bin/bash
PACKAGES=("free.nokaA" "free.nokaB" "free.nokaC" "free.nokaD" "free.nokaE" "free.nokaF")
LABELS=("Bản sao A" "Bản sao B" "Bản sao C" "Bản sao D" "Bản sao E" "Bản sao F")
PLACE_ID="8737899170"
RAM_APPS=("0 MB" "0 MB" "0 MB" "0 MB" "0 MB" "0 MB")

while true; do
    for i in "${!PACKAGES[@]}"; do
        pkg="${PACKAGES[$i]}"
        
        # Kiểm tra ứng dụng có đang chạy bằng pidof hoặc dumpsys
        if ! pidof "$pkg" > /dev/null 2>&1; then
            # Gọi intent mở game nếu app bị sập
            am start -a android.intent.action.VIEW -d "roblox://placeID=$PLACE_ID" "$pkg" > /dev/null 2>&1
            RAM_APPS[$i]="Đang hồi sinh..."
        else
            # Tối ưu lấy TOTAL RAM chính xác từ dumpsys meminfo (bỏ chữ TOTAL:, lấy số đầu tiên)
            ram_kb=$(dumpsys meminfo "$pkg" 2>/dev/null | grep -i "TOTAL:" | tr -s ' ' | cut -d' ' -f3)
            
            if [ ! -z "$ram_kb" ] && [[ "$ram_kb" =~ ^[0-9]+$ ]]; then
                RAM_APPS[$i]="$((ram_kb / 1024)) MB"
            else
                RAM_APPS[$i]="Đang tải..."
            fi
        fi
    done

    # Lấy thông tin RAM hệ thống
    total_kb=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    free_kb=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    
    # Sửa lỗi bc hoặc fallback dùng awk để tính số thập phân chuẩn hơn trên Android
    total_gb=$(awk "BEGIN {printf \"%.1f\", $total_kb/1024/1024}")
    free_gb=$(awk "BEGIN {printf \"%.1f\", $free_kb/1024/1024}")

    clear
    echo "========================================="
    echo "       📊 THEO DÕI RAM ROBLOX REAL-TIME   "
    echo "========================================="
    echo " 📱 RAM THIẾT BỊ  : ${total_gb} GB"
    echo " 🟢 RAM ĐANG TRỐNG: ${free_gb} GB"
    echo "-----------------------------------------"
    for i in "${!PACKAGES[@]}"; do
        printf " 🔹 %-12s : %s\n" "${LABELS[$i]}" "${RAM_APPS[$i]}"
    done
    echo "========================================="
    echo " (Hệ thống chống crash đang chạy ngầm...)"
    sleep 3
done
EOF
