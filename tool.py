pkg update && pkg install bc -y




cat << 'EOF' > petsim.sh
#!/bin/bash

# 6 bản clone của bạn
PACKAGES=("free.nokaA" "free.nokaB" "free.nokaC" "free.nokaD" "free.nokaE" "free.nokaF")
LABELS=("Bản sao A" "Bản sao B" "Bản sao C" "Bản sao D" "Bản sao E" "Bản sao F")
PLACE_ID="8737899170"

# Biến lưu trữ lượng RAM chiếm dụng của từng tab để in ra bảng
RAM_APPS=("0 MB" "0 MB" "0 MB" "0 MB" "0 MB" "0 MB")

while true; do
    # 1. KIỂM TRA CHỐNG CRASH TRONG NỀN AM THẦM
    for i in "${!PACKAGES[@]}"; do
        pkg="${PACKAGES[$i]}"
        
        # Nếu tab bị tắt/văng, tự động mở lại âm thầm
        if ! pidof "$pkg" > /dev/null 2>&1; then
            am start -a android.intent.action.VIEW -d "roblox://placeID=$PLACE_ID" "$pkg" > /dev/null 2>&1
            RAM_APPS[$i]="Đang hồi sinh..."
        else
            # Nếu app đang chạy bình thường, đọc dữ liệu RAM của nó
            ram_kb=$(dumpsys meminfo "$pkg" 2>/dev/null | grep "TOTAL:" | awk '{print $2}')
            if [ ! -z "$ram_kb" ] && [ "$ram_kb" -ne 0 ]; then
                RAM_APPS[$i]="$((ram_kb / 1024)) MB"
            else
                RAM_APPS[$i]="Đang tải..."
            fi
        fi
    done

    # 2. ĐỌC RAM TỔNG CỦA HỆ THỐNG
    total_kb=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    free_kb=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    total_gb=$(echo "scale=1; $total_kb/1024/1024" | bc 2>/dev/null || echo $((total_kb/1024/1024)))
    free_gb=$(echo "scale=1; $free_kb/1024/1024" | bc 2>/dev/null || echo $((free_kb/1024/1024)))

    # 3. LÀM SẠCH MÀN HÌNH VÀ IN BẢNG THEO THỜI GIAN THỰC
    clear
    echo "========================================="
    echo "       📊 THEO DÕI RAM ROBLOX REAL-TIME  "
    echo "========================================="
    echo " RAM THIẾT BỊ: ${total_gb} GB"
    echo " RAM ĐANG TRỐNG: ${free_gb} GB"
    echo "-----------------------------------------"
    for i in "${!PACKAGES[@]}"; do
        printf " 🔹 %-12s : %s\n" "${LABELS[$i]}" "${RAM_APPS[$i]}"
    done
    echo "========================================="
    echo " (Hệ thống chống crash đang chạy ngầm...)"
    
    # Cứ mỗi 3 giây sẽ tự động cập nhật lại thông số RAM một lần
    sleep 3
done
EOF




chmod +x petsim.sh



./petsim.sh









