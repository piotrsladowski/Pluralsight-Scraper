#!/bin/bash
# make sure you have ffmpeg 4.x installed (3.x is not supported)
# e.g. for ubuntu 18.04 sudo snap install ffmpeg

scriptName=$0
kind=$1
path=$2
start=$3
end=$4
concat_filename=$5

case $kind in
  ""|help)
  echo "Usage:"
  echo "$scriptName help"
  echo "$scriptName merge folder_path starting_index ending_index (inclusive)"
  echo "$scriptName concat folder_path starting_index ending_index (inclusive) filename"
  ;;

  merge)
  i=$start
  while (( $i <= $end ))
  do
    video=$(echo `ls $path | grep -E "video_${i}_.*"`)
    audio=$(echo `ls $path | grep -E "audio_${i}_.*"`)
    filename=$(echo $path/$video | sed 's/^.*\(video\|audio\)_[0-9]\+_//' | sed 's/.\(ts\|aac\)$//')
    output="$path/${i}_${filename}.mp4"

    ffmpeg -i $path/$video -i $path/$audio -c:v copy -c:a aac $output

    i=$(( $i + 1 ))
  done
  ;;

  concat)

  for f in $path/*.mp4; do
  index=$(echo $f | cut -d'_' -f 1 | sed 's/^.\///')
  if (( $index >= $start && $index <= $end )); then
    echo "file '$f'" >> $path/mylist.txt;
  fi
  done

  ffmpeg -f concat -safe 0 -i $path/mylist.txt -c copy $concat_filename.mp4

  rm -f $path/mylist.txt

  ;;
esac
