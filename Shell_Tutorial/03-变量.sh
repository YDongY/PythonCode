#!/bin/bash

# 本地变量

name="root"

user1="$name 666"
# root 666
echo $user1

user2='$name 666'
# $name 666
echo $user2

# 命令变量
who=`whoami`
echo $who

dir=$(pwd)
echo $dir

# 全局变量
env | grep SHELL

NAME="ROOT"
export NAME

export AGE=20

env | grep $NAME$

# 删除变量
#unset who

echo $who

# 内置变量

echo "current filename $0"
echo "params:$#"
echo "params-1:$1"
echo $?


file="hello shell hello python"

# 从第1个字符开始，截取5个字符
echo ${file:0:5}

# 从第6个字符开始，截取5个字符
echo ${file:5:5}

# 从倒数第6个字符开始，截取之后的3个字符
echo ${file:0-6:3}

param=$1

echo "param ${param:-'没有参数'}"

echo "param ${param+'强制生效默认值'}"
