#!/bin/bash

for organe in Kidneys
do
	mkdir stdGATE/output/${organe}
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
		echo "******************************  Comp. 1:  " $organe "  *******************************"
		echo
		echo "        ---------------------  n Primaries:" $nombrePrim "  ---------------------"
		echo "        ---------------------  Emission Type:" $emission "  ---------------------"

	cat > stdGATE/docker_gate_${emission}.sh << EOF
		#!/bin/sh

		# set up environment variables
		source /geant4/geant4.10.03.p01-install/bin/geant4.sh
        	export PATH=$PATH:/sbin:/bin:/gate/gate_v8.0-install/bin
		# start
		cd /data/mac

		Gate -a [testNumber,${organe}_${emission}][particule,${particleType}][tissue,${organe}][nPrimaries,${nombrePrim}][emissionType,${emission}] mainMacro.mac > ../output/${organe}/run_${emission}.log ;

EOF


	cat > stdGATE/docker_${emission}.sh << EOF
		#!/bin/sh

		#Remove stopped Docker containers
		docker rm \$(docker ps -aq)

		# create and run a new container in the background from the image ubuntu-gate
		START_cluster=\$(date +%s)
		name=\$(docker run -id manureva/ubuntu-gate:16.04-8.0)

		# copy files to the container
		docker cp stdGATE \$name:/data

		START=\$(date +%s)

		# execute the script in the container
		docker exec \$name bash /data/docker_gate_${emission}.sh

		END=\$(date +%s)
		DIFF=\$(echo \$END-\$START | bc -l)

		# get back the results
		docker cp \$name:/data/. stdGATE


		# stop and remove the container
		docker stop \$name
				docker rm \$name
EOF
					
		echo " Running GATE"
	done
done

echo
echo "			DONE !!"
echo

