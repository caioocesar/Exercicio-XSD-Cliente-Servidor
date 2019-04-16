#!/bin/bash

echo "Limpando output/"
rm -fr output/
mkdir output/

echo "Compilando..."
javac -d output/ serverTCP/*

echo -e "\n\e[32mIniciando servidor\e[0m\n"
java -cp output serverTCP.MainServerTcp
