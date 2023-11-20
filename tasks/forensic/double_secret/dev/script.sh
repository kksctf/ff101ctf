#!/bin/bash

zip_name="definitely_not_part_of_task.zip"
input_name="maybe_flag_maybe_not.txt"
flag="ptctf{s3cr3t_0f_B0r1s_1s_g00d_n1ght_sl33p}"
input_pic="mem.png"
rnddata="randomdata"
password="GSnLMxTGTCXilKhFCSZbLVDMSttdyUow"


echo -n "[>] flag="
echo $flag | tee $input_name 

dd if=/dev/random of=$rnddata bs=16M count=1
echo "[>] Created random data in " $rnddata

zip -m -P $password $zip_name $input_name $rnddata 
echo "[>] Created zip", $zip_name

cp ./mem.png ./mem.task.png
echo "[>] Copied image file"

cat $zip_name >> ./mem.task.png
echo "[+] Container with Task Created"

rm $zip_name