#!/bin/sh

declare -a ParslExecutors=("local_few_htex" "local_high_htex" "local_few_threads" "local_high_threads")
declare -a arguments=(3 10 31)
program=mandlebrot
argm="-w"

for exec in ${ParslExecutors[@]}
do
	for d in ${arguments[@]}
	do
		echo $exec $d
		someString=`python ${program}.py ${argm} $d -e ${exec}`
		someString=`python -m pyinstrument -r json -o outputs/${program}-${d}-${exec}.json ${program}.py ${argm} ${d} -e ${exec}`
		echo $someString
		echo "$someString"
	done
done
