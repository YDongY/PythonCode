#!/bin/bash

test 1=1

[ 1 = 1 ]

echo $?


[ 1 = 1 ] && echo "条件成立，执行"
[ 1 = 2 ] || echo "条件不成立执行"

filename=$0

[ -f $filename ] && cat $filename

[ -d dir ] || mkdir dir

[ -x $filename ] && ./$filename

#[ -x $filename ] || bash $filename


echo $((1 + 3))
echo $((1 + 4))
echo $((1 + 44))
echo $((2 * 44))
i=4
let j=3+4
echo $j
let j=i+5
echo $j

bc <<< "scale=10; 5 / 3"

bc <<< "5/2"

array=(1 2 3 4 5)

echo ${array[2]}

echo ${array[@]}
echo ${array[*]}

# 查询下标
echo ${!array[*]}

echo ${#array[2]}

# 数组元素个数
echo ${#array[@]}
echo ${#array[*]}
