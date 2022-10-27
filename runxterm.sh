while IFS=- read -r varTeste varHostSrc varPodSrc varHostDst varPodDst
do
   echo "$varTeste"
   echo "source:  H"$varHostSrc"C"$varPodSrc
   echo "destino: H"$varHostDst"C"$varPodDst

   macSRC="08:00:00:0"$varPodSrc":0"$varHostSrc":"$varHostSrc$varHostSrc
   macDST="08:00:00:0"$varPodDst":0"$varHostDst":"$varHostDst$varHostDst
   cmdSRC="./send.py 10."$varPodDst"."$varHostDst"."$varHostDst" 760 500"
   cmdDST="./receive.py "$varTeste".log "$varTeste
   echo $macSRC
   echo $macDST
   echo $cmdSRC
   echo $cmdDST

   ifconfig | awk -v varMac="$macDST" -v varCMD="$cmdDST" '{if($5~varMac) {command=varCMD;system(command)}}'  
   ifconfig | awk -v varMac="$macSRC" -v varCMD="$cmdSRC" '{if($5~varMac) {command=varCMD;system(command)}}'  
done < /home/p4/FRRFTK4/teste.txt