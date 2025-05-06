#!/bin/bash

# echo -e "PPID\tPID\tCOMM\tSTATE\tTTY\tRRS\tPGID\tSID\tOPEN_FILES"
for pid_dir in /proc/[0-9]*; do
	pid=$(basename "$pid_dir")

	if [[ -f /proc/$pid/status && -f  /proc/$pid/stat && -d /proc/$pid/fd ]]; then

		ppid=$(grep -s "^PPid:" /proc/$pid/status | cut -f2);
		
		stat_line=$(cat /proc/$pid/stat)
		comm=$(echo "$stat_line" | cut -d' ' -f2 | tr -d '()')
		state=$(echo "$stat_line" | cut -d' ' -f3)
		pgid=$(echo "$stat_line" | cut -d' ' -f5)
		sid=$(echo "$stat_line" | cut -d' ' -f6)
		tty_nr=$(echo "$state_line" | cut -d' ' -f7)

		tty_name=$(ls -l /proc/$pid/fd 2>/dev/null | grep -oP '/dev/tty[0-9]+' | head -n 1)
		tty=${tty_name:-"?"}

		rss=$(grep -s "^VmRSS:" /proc/$pid/status | tr -s ' ' | cut -d' ' -f2)
		rss=${rss:-0}

		open_files=$(ls -1 /proc/$pid/fd 2>/dev/null | wc -l)

		echo -e "${ppid}\t${pid}\t${comm}\t${state}\t${tty}\t${rss}\t${pgid}\t${sid}\t${open_files}"
	fi
done | column -t -N  PPID,PID,COMM,STATE,TTY,RRS,PGID,SID,OPEN_FILES -s $'\t'
