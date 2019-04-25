#!/bin/bash

dim_x=$2
dim_y=$3
dim_z=$4
shift_x=$5
shift_y=$6
shift_z=$7
pix_x=$8
pix_y=$9
pix_z=${10}

#patient_CT=$2
for organe in $1
do
	mkdir dosimetrie/stdGATE/output/${organe}
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
		echo "        *****************  Creating bash script for:  " $organe "  **************"
		echo
		echo "        ---------------------  Emission Type:" $emission "  ---------------------"
		echo "        ---------------------   Intensity:" $nombrePrim "   ---------------------"

	cat > dosimetrie/stdGATE/docker_gate_${emission}.sh << EOF
		#!/bin/sh

		# set up environment variables
		source /geant4/geant4.10.03.p01-install/bin/geant4.sh
        	export PATH=$PATH:/sbin:/bin:/gate/gate_v8.0-install/bin
		# start
		cd /data/mac

		Gate -a [testNumber,${organe}_${emission}][particule,${particleType}][tissue,${organe}][nPrimaries,${nombrePrim}][emissionType,${emission}][resolution_x,${dim_x}][resolution_y,${dim_y}][resolution_z,${dim_z}][sourceShift_x,${shift_x}][sourceShift_y,${shift_y}][sourceShift_z,${shift_z}][pixel_x,${pix_x}][pixel_y,${pix_y}][pixel_z,${pix_z}] mainMacro.mac > ../output/${organe}/run_${emission}.log ;
		#Gate -a [testNumber,${organe}_${emission}][particule,${particleType}][tissue,${organe}][nPrimaries,${nombrePrim}][emissionType,${emission}][patientCT,${organe}] mainMacro.mac > ../output/${organe}/run_${emission}.log ;

EOF


	cat > dosimetrie/stdGATE/docker_${emission}.sh << EOF
		#!/bin/sh

		#Remove stopped Docker containers
		docker rm \$(docker ps -aq)

		# create and run a new container in the background from the image ubuntu-gate
		START_cluster=\$(date +%s)
		name=\$(docker run -id manureva/ubuntu-gate:16.04-8.0)

		# copy files to the container
		docker cp dosimetrie/stdGATE \$name:/data

		START=\$(date +%s)

		# execute the script in the container
		docker exec \$name bash /data/docker_gate_${emission}.sh

		END=\$(date +%s)
		DIFF=\$(echo \$END-\$START | bc -l)

		# get back the results
		docker cp \$name:/data/. dosimetrie/stdGATE


		# stop and remove the container
		docker stop \$name
				docker rm \$name
EOF
					
		#echo " Running GATE"
	done
done


for emission in G betaMinus X IE AE
	do
	  echo "Simulating" $emission
      ./dosimetrie/docker_multi.sh $emission
    done
