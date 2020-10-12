# Shell Tutorial

## Hello Shell

```shell script
#!/bin/bash

echo "hello shell"
```

## Shell 注释

- 单行注释

```shell script
#!/bin/bash
echo "hello shell"
#echo "hello world"
```

- 多行注释

```shell script
#!/bin/bash

echo "hello shell"
:<<!

echo "hello world"
echo "hello world"
!
```

## 变量

### 本地变量

- 普通变量

```shell script
#!/bin/bash
name="root"
age=20
gender='male'
```

其中双引号会解析变量内容而单引号不会，比如：

```shell script
#!/bin/bash
name="root"

user1="$name 666"
# root 666

user2='$name 666'
# $name 666
```

### 命令变量

```shell script
#!/bin/bash

ppp=`pwd`

echi $ppp

dir=$(pwd)
echo $dir
```

### 全局变量

当前系统环境下所有的变量，查看全局变量

```shell script
env
env | grep SHELL
```

定义全局变量

```shell script
NAME="ROOT"
export NAME

export AGE=20
```

内置变量：bash 内部定义的变量参数

### 删除变量

```shell script
#!/bin/bash
who=$(whoami)
echo $who
# 删除变量
unset who
echo $who
```

### 内置变量

- $0：获取脚本文件名
- $#：获取脚本执行时候的参数总个数
- $n：获取脚本执行时候的指定位置参数的内容
- $?：上一条指令执行后的状态返回值。0成功 ，非0失败

```shell script
#!/bin/bash
# 获取脚本文件名
echo "current filename $0"

# 获取传入脚本参数个数
echo "params:$#"

# 获取传入脚本第一个参数
echo "params-1:$1"

echo $?
```

### 精确获取

格式：`${变量名:起始位置:截取长度}`

```shell script
#!/bin/bash
file="hello shell hello python"

# 从第1个字符开始，截取5个字符
echo ${file:0:5} 

# 从第6个字符开始，截取5个字符
echo ${file:5:5} 

# 从倒数第6个字符开始，向后截取3个字符
echo ${file:0-6:3} 
```

### 默认值

条件默认值，格式：`${变量名:-默认值}`

```shell script
#!/bin/bash

param=$1

echo "param ${param:-'没有参数'}"
```

强制生效默认值，格式：`$(变量名+默认值)`

```shell script
#!/bin/bash

param=$1
echo "param ${param+'强制生效默认值'}"
```

## 表达式

### 测试语句

```shell script
#!/bin/bash
test 1=1

[ 1 = 1 ]
```

### 逻辑表达式

```shell script
#!/bin/bash

[ 1 = 1 ] && echo "条件成立，执行"
[ 1 = 2 ] || echo "条件不成立执行"
```

### 文件表达式

- `-f`：判断输入内容是否是一个文件
- `-d`：判断输入内容是否是一个目录
- `-x`：判断输入内容是否可执行

```shell script
#!/bin/bash

filename=$0

[ -f $filename ] && cat $filename

[ -d dir ] || mkdir dir

[ -x $filename ] && ./$filename

[ -x $filename ] && ./$filename


#　这个命令会死循环
[ -x $filename ] || bash $filename
```

### 数值表达式

- `[1 -eq 1]`：相等
- `[2 -gt 1]`：大于
- `[1 -lt 2]`：小于
- `[1 -ne 2]`：不等于

### 字符串表达式

- `str1 == str2`：str1 和 str2 字符串内容一致
- `str1 != str2`：str1 和 str2 字符串内容不一致， ! 表示相反的意思


### 计算表达式

整数场景：

- $((计算表达式))
- let 计算表达式

注意：对于 let 来说，计算表达式必须是一个整体，不能有空格

```shell script
#!/bin/bash
echo $((1 + 3))
echo $((1 + 4))
echo $((1 + 44))
i=4
let j=3+4
echo $j
let j=i+5
echo $j
```

小数场景

```shell script
#!/usr/bin

# 5/3 保留十位小数
bc <<< "scale=10; 5 / 3"

# 5/2 取整
bc <<< "5/2"
```

### 数组

定义格式：array_name=(value1 ... valuen) ，元素彼此间使用空格隔开

```shell script
#!/bin/bash
array=(1 2 3 4 5)

# 查看内容 ，下标从 0 开始
echo ${array[1]}

# 获取全部
echo ${array[@]}
echo ${array[*]}

# 查询下标
echo ${!array[*]}

# 获取长度

# 如果索引 2 有值，则返回当前索引元素的长读
echo ${#array_name[2]}

# 数组元素个数
echo ${#array_name[@]}
echo ${#array_name[*]}
```

- 查看
    - 整体 `echo ${array[index]}`
    - 部分 `echo ${array[index]:起始位置:获取长度}`
    
- 设置
    - `array[index]=value`

- 更改
    - 整体 `array[index]=value`
    - 模拟替换(内容不会变) `${array[index]/原内容/修改后内容}`
    
- 删除
    - 单个元素 `unset array[index]`
    - 整体 `unset array`

## 常见符号

###　重定向

- `>`：覆盖原内容
- `>>`：追加到元内容

```shell script
#!/bin/bash

echo "hello" > file.txt
echo "hello" >> file.txt
```

### 管道符

- `|`：管道符左侧内容的输出作为管道符右侧的输入

```shell script
#!/bin/bash

ls | grep file.txt
```

### 后台

- `&`：任务处于后台

```shell script
#!/bin/bash

sleep 20 &
```

### 信息符号

```shell script
#!/bin/bash

# 1 表示文件描述符1，表示标准输出
echo $SHELL 1>> out.file

# 2 表示文件描述符2，意思是标准错误输出
echo $aaa 2>> out.file

# 2>&1 表示标准输出和错误输出合并
echo command >> out.file 2>&1
```

```shell script
#!/bin/bash

# /dev/null 可以接收无限容量内容
echo command >> /dev/null 2>&1
```

/dev/null 称空设备、位桶（bit bucket）或者黑洞（black hole）是一个特殊的设备文件，它丢弃一切写入其中的数据。通常被用于丢弃不需要的输出流，或作为用于输入流的空文件。当读它的时候，它会提供无限的空字符（NULL，ASCII NUL，0x00）。


## 流程控制

- 单分支

```shell script
if [ 条件 ]; 
then
    指令
fi
```

- 双分支

```shell script
if [ 条件 ];
then
  指令1
else
  指令2
fi
```

- 多分支

```shell script
if [ 条件 ]
then
    指令1
elif [ 条件2 ]
then
    指令2
else
    指令3
fi


#!/bin/bash
# 多if语句的服务使用场景
arg="$1"
if [ "${arg}" == "start" ]
then
  echo "服务启动中..."
elif [ "${arg}" == "stop" ]
then
  echo "服务关闭中..."
elif [ "${arg}" == "restart" ]
then
  echo "服务重启中..."
else
  echo "脚本 $0 的使用方式: /bin/bash $0 [ start|stop|restart ]"
fi			
```
