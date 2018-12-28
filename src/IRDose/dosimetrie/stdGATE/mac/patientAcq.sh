#!/bin/bash
#echo -e "Please type the setScale parameter: \c "
#read setScale

#sleep 7000

for Organe in liver #blood #fev bladder kidneys tumeur1 tumeur2 spleen
do
	for emission in betaMinus G X IE AE
	do
		if [ $emission == betaMinus ]
			then 
				nombrePrim=1
				particleType=e-
		elif [ $emission == G ]
			then 
				nombrePrim=0.1803
				particleType=gamma
		elif [ $emission == X ]
			then 
				nombrePrim=1.374
				particleType=gamma
		elif [ $emission == IE ]
			then 
				nombrePrim=0.1548
				particleType=e-
		elif [ $emission == AE ]
			then 
				nombrePrim=1.117
				particleType=e-	
		fi

		echo
		echo "******************************  Comp. 1:  " $Organe "  *******************************"
		echo
		echo "        ---------------------  n Primaries:" $nombrePrim "  ---------------------"
		echo "        ---------------------  Emission Type:" $emission "  ---------------------"
	
		#echo CRCT_eq15 | sudo -S purge
		#echo ""
		#sleep 5
	
		echo " Running GATE"
		date & gate -a [testNumber,${Organe}_${emission}][particule,${particleType}][tissue,Liver][nPrimaries,${nombrePrim}][emissionType,${emission}] mainMacro.mac ;

		
    done
done

echo
echo "			DONE !!"
echo

#####      gate -a [CHANGECOMPARTMENT,Liver][testNumber,1][folderName,OLD][changeSetScale,0.0000012] tomoUseARF.mac