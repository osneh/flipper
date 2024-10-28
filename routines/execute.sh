lastfile=$(ls ../files/combinedPulseDigital_VRefN-SCAN_24May*NOTDUMMIES*.csv | grep NOTDUMMIES | sort -r |  awk 'NR==2 { print; } END { print; }' | head -n1)
python sweeping.py -fcali $lastfile -fscan ../files/VRefN-SCAN_45to100.txt --RL
