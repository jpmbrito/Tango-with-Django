#!/bin/bash
recurse() {
 for i in "$1"/*;do
    if [ -d "$i" ];then
        recurse "$i"
    elif [ -f "$i" ]; then
	extension="${i##*.}"
	if [ $extension == "py" ]; then
		echo $i
		#python -m tabnanny $i
		python -m py_compile $i
	fi
    fi
 done
}

recurse .