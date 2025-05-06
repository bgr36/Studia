
for file in *; do
	if [ -f "$file" ]; then
		lower_case_name=$(echo "$file" | tr '[:upper:]' '[:lower:]')

		if [ "$file" != "$lower_case_name" ]; then
			mv -- "$file" "$lower_case_name"
		fi
	fi
done
