#!/bin/bash

if [ 1 = 1 ];
then
    echo "1=1"
fi

if [ 1 = 2 ];
then
  echo "1=2"
else
  echo "1!=2"
fi

n=15

if [ $n -qe 10 ]
then
    echo "n>10"
elif [[ $n -gt 5 ]] && [[ $n -lt 10 ]]
then
    echo "5<n<10"
else
    echo $n
fi
