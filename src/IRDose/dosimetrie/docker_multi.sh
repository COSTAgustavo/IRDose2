				#!/bin/sh
				#Remove stopped Docker containers
				docker rm $(docker ps -aq)

				# create and run a new container in the background from the image ubuntu-gate
				START_cluster=$(date +%s)
				name=$(docker run -id manureva/ubuntu-gate:16.04-8.0)

				# copy files to the container
				docker cp dosimetrie/stdGATE $name:/data

				START=$(date +%s)
                                echo "Juste avant lancer la simu"
				# execute the script in the container
     docker ps -a

				#docker exec $name bash /data/docker_gate_AE.sh
				docker exec $name bash /data/docker_gate_$1.sh

				END=$(date +%s)
				DIFF=$(echo $END-$START | bc -l)

				# get back the results
				docker cp $name:/data/. dosimetrie/stdGATE


				# stop and remove the container
				docker stop $name
				docker rm $name
