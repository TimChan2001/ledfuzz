#!/bin/bash
# 新建target中的BugXXX文件夹
set -e
TARGET = "tiff"
cd targets
for i in {1..14}
do
  # Create folder named xxx-i (e.g., xxx-1, xxx-2, ..., xxx-10)
  folder_name="$TARGET-$i"
  mkdir "$folder_name"
  
  cd "$folder_name"
  
  touch bug-report name source-code
  mkdir out
  cd ..
done

echo "Folders and files have been created."