#!/data/data/com.termux/files/usr/bin/bash
clear
echo "=== AUGUSTINE SOC TOOLKIT | Enugu | GREEN ==="
echo "="
echo "Threat Score: 95/100"
echo "-------------------------------------------------------"

# Map menu number to actual day folder + script name
declare -A TOOLS
TOOLS[1]="day1:Port Scanner"
TOOLS[2]="day2:Banner Grabber" 
TOOLS[3]="day3:Subdomain Finder"
TOOLS[4]="day4:IP Validator"
TOOLS[5]="day6:Advanced Port Scanner"
TOOLS[6]="day7:Hash Checker"
TOOLS[7]="day8:SOC Password Checker"
TOOLS[8]="day9:Log Analyzer"
TOOLS[9]="day10:Vuln Scanner"
TOOLS[10]="day11:URL Scanner"
TOOLS[11]="day12:File Integrity Monitor"
TOOLS[12]="day13:Packet Sniffer"
TOOLS[13]="day14:SOC Dashboard"

mapfile -t CLI_TOOLS < <(find /data/data/com.termux/files/usr/bin -maxdepth 1 -type f -executable! -name '*.*'! -name '['! -name '[['! -name '.'! -name '..' -printf '%f\n' 2>/dev/null | sort -u)
TOTAL=$((${#CLI_TOOLS[@]} + 13))

for i in {1..13}; do
    IFS=':' read -r day name <<< "${TOOLS[$i]}"
    printf "%2d. %-25s - %s\n" $i "$name" "$day"
done

echo "-------------------------------------------------------"
echo "[+] CLI Tools: 14-${TOTAL} | Total: ${TOTAL}"
echo "-------------------------------------------------------"
echo " 0. Exit"
echo "999. Show All ${TOTAL} Tools Numbered"
echo "-------------------------------------------------------"

read -p "Select tool [0-999]: " choice

if [[ $choice -ge 1 && $choice -le 13 ]]; then
    IFS=':' read -r day name <<< "${TOOLS[$choice]}"
    echo "Launching: $name from $day..."
    echo "-------------------------------------------------------"
    python ~/cyber_course/$day/*.py 2>/dev/null || echo "Script not found in ~/$day/"
    echo "-------------------------------------------------------"
    echo "Press Enter to return to menu..."
    read
    exec $0
elif [[ $choice -ge 14 && $choice -le $TOTAL ]]; then
    CLI_INDEX=$((choice - 14))
    TOOL=${CLI_TOOLS[$CLI_INDEX]}
    echo "Launching CLI Tool #$choice: $TOOL"
    echo "-------------------------------------------------------"
    timeout 5 $TOOL --help 2>&1 | head -20 || echo "$TOOL installed. Run: $TOOL"
    echo "-------------------------------------------------------"
    echo "Press Enter to return to menu..."
    read
    exec $0
elif [[ $choice == 0 ]]; then
    exit 0
elif [[ $choice == 999 ]]; then
    python ~/cyber_course/day14/soc_dashboard.py
    echo "Press Enter to return to menu..."
    read
    exec $0
else
    echo "Invalid. Press Enter."
    read
    exec $0
fi
