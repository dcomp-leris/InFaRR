make stop
make clean
clear
rm *.p4
rm script_mininet
cp /InFaRR/P4/$1.p4 .
cp /InFaRR/P4/script_mininet.$2 /InFaRR/script_mininet
if [ -s script_mininet ]; then
    echo "Vai rodar script" $1 "Erro " $2
else
    rm script_mininet
fi

make run 