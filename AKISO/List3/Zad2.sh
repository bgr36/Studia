#!/bin/bash

prev_b_in=0
prev_b_out=0
prev_time=$(date +%s)

declare -a prev_in=(0 0 0 0 0 0 0 0 0 0)
declare -a prev_out=(0 0 0 0 0 0 0 0 0 0)
max_entries=10  
graph_width=50  

print_row() {
    local value=$1
    local max_value=$2
    if (( $(echo "$max_value==0" | bc -l) )); then
        local width=0
    else
		local width=$(echo "scale=0; $value * $graph_width / $max_value" | bc -l)
    fi

    for ((i = 0; i < width; i++)); do
        echo -n "#"
    done
    echo "|)"
}

print_graph() {
    local max_value=0
    for value in "${prev_in[@]}" "${prev_out[@]}"; do
        if (( $(echo "$value > $max_value" | bc -l) )) then
			max_value=$value
		fi
    done

    echo "Speed(in) - Max: $max_value"
    for value in "${prev_in[@]}"; do
        print_row "$value" "$max_value"
    done


    echo "Speed(out) - Max: $max_value"
    for value in "${prev_out[@]}"; do
        print_row "$value" "$max_value"
    done

}


showNetworkSpeed(){
	local b_in=$(grep -e "enp0s3"  /proc/net/dev | awk '{print $2}')
	local b_out=$(grep -e "enp0s3" /proc/net/dev | awk '{print $10}')
	local current_time=$(date +%s)
	local delta_time=$((current_time - prev_time))
	local units_in="B/s"
	local units_out="B/s"

	if [ "$prev_b_in" -eq 0 ] && [ "$prev_b_out" -eq 0 ]; then
        prev_b_in=$b_in
        prev_b_out=$b_out
        prev_time=$current_time
        return
    fi

	if [ "$delta_time" -gt 0 ]; then
		local delta_in=$((b_in - prev_b_in))
		local delta_out=$((b_out - prev_b_out))

		local speed_in=$(echo "scale=2; $delta_in / $delta_time" | bc)
		local speed_out=$(echo "scale=2; $delta_out / $delta_time" | bc)

        prev_in+=($speed_in)
        prev_out+=($speed_out)

        if [ ${#prev_in[@]} -gt $max_entries ]; then
            prev_in=("${prev_in[@]:1}")
            prev_out=("${prev_out[@]:1}")
        fi

		if (( $(echo "$speed_in > 1048576" | bc -l) )); then
			units_in="MB/s"
			speed_in=$(echo "scale=2; $speed_in / 1048576" | bc);
		elif (( $(echo "$speed_in > 1024" | bc -l) )); then
			units_in="KB/s"
			speed_in=$(echo "scale=2; $speed_in / 1024" | bc);
		fi
			
		if (( $(echo "$speed_out > 1048576" | bc -l) )); then
			units_out="MB/s"
			speed_out=$(echo "scale=2; $speed_out / 1048576" | bc);
		elif (( $(echo "$speed_out > 1024" | bc -l) )); then
			units_out="KB/s"
			speed_out=$(echo "scale=2; $speed_out / 1024" | bc);
		fi
		echo "Network Speed(in): $speed_in $units_in | Speed(out): $speed_out $units_out"
		print_graph
	fi
	
	prev_b_in=$b_in;
	prev_b_out=$b_out;
	prev_time=$current_time;
}

show_cpu_usage() {
    echo "CPU Usage:"
    for i in $(seq 0 3); do
        local cpu_usage=$(grep "cpu$i" /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}')
        local freq=$(grep "cpu MHz" /proc/cpuinfo | awk "NR==$((i+1)) {print \$4}")
        echo "Core $i: ${cpu_usage}% at ${freq} Hz"
    done
}

show_uptime() {
    uptime_seconds=$(cat /proc/uptime | awk '{print $1}')
    uptime_days=$(echo "$uptime_seconds / 86400" | bc)
    uptime_hours=$(echo "($uptime_seconds % 86400) / 3600" | bc)
    uptime_minutes=$(echo "($uptime_seconds % 3600) / 60" | bc)
    uptime_seconds=$(echo "$uptime_seconds % 60" | bc)
    echo "System Uptime: ${uptime_days}d ${uptime_hours}h ${uptime_minutes}m ${uptime_seconds}s"
}

show_battery_status() {
	local battery_status=$(cat /sys/class/power_supply/BAT0/uevent | grep -e "POWER_SUPPLY_STATUS" | cut -d'=' -f2)
    local battery_capacity=$(cat /sys/class/power_supply/BAT0/uevent | grep -e "POWER_SUPPLY_CAPACITY" | cut -d'=' -f2)
	echo "Battery Status: ${battery_status}, ${battery_capacity}%"
}

show_loadavg() {
    local loadavg=$(cat /proc/loadavg)
    local num_cpus=4

    local load1=$(echo $loadavg | awk '{print $1}')
    local load5=$(echo $loadavg | awk '{print $2}')
    local load15=$(echo $loadavg | awk '{print $3}')

    local load1_percent=$(awk "BEGIN {print ($load1 / $num_cpus) * 100}")
    local load5_percent=$(awk "BEGIN {print ($load5 / $num_cpus) * 100}")
    local load15_percent=$(awk "BEGIN {print ($load15 / $num_cpus) * 100}")

    echo "System Load 1min: ${load1} (${load1_percent}%) 5min: ${load5} (${load5_percent}%) 15min: ${load15} (${load15_percent}%)"
}

show_memory_usage() {
	local units_used="KB/s"
	local units_total="KB/s"
    local meminfo=$(cat /proc/meminfo)
    local total_memory=$(echo "$meminfo" | grep MemTotal | awk '{print $2}')
    local free_memory=$(echo "$meminfo" | grep MemFree | awk '{print $2}')
    local used_memory=$((total_memory - free_memory))
    local memory_percentage=$(echo "scale=2; $used_memory / $total_memory * 100" | bc)

	if (( $(echo "$used_memory > 1048576" | bc -l) )); then
		units_used="GB/s"
		used_memory=$(echo "scale=2; $used_memory / 1048576" | bc);
	elif (( $(echo "$used_memory > 1024" | bc -l) )); then
		units_used="MB/s"
		used_memory=$(echo "scale=2; $used_memory / 1024" | bc);
	fi
			
	if (( $(echo "$total_memory > 1048576" | bc -l) )); then
		units_total="GB/s"
		total_memory=$(echo "scale=2; $total_memory / 1048576" | bc);
	elif (( $(echo "$total_memory > 1024" | bc -l) )); then
		units_total="MB/s"
		total_memory=$(echo "scale=2; $total_memory / 1024" | bc);
	fi

    echo "Memory Usage: $used_memory kB used / $total_memory kB total ($memory_percentage%)"
}

while true; do
	tput clear
	show_cpu_usage
	show_uptime
	show_battery_status
	show_loadavg
	show_memory_usage
	showNetworkSpeed
	sleep 1
done

