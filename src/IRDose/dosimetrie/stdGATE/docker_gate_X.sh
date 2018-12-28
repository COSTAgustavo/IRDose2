		#!/bin/sh

		# set up environment variables
		source /geant4/geant4.10.03.p01-install/bin/geant4.sh
        	export PATH=/media/sf_Debian/Python/Django/django_v2/django_v2/bin:/usr/share/geant4/geant4.10.03.p01-install/bin:/home/gustavo/bin:/home/gustavo/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/share/gate/gate_v8.0-install/bin:/sbin:/bin:/gate/gate_v8.0-install/bin
		# start
		cd /data/mac

		Gate -a [testNumber,LiverWoman_X][particule,gamma][tissue,LiverWoman][nPrimaries,1.374][emissionType,X][resolution_x,512][resolution_y,512][resolution_z,76][sourceShift_x,249.999872][sourceShift_y,249.999872][sourceShift_z,190.0][pixel_x,0.976562][pixel_y,0.976562][pixel_z,5] mainMacro.mac > ../output/LiverWoman/run_X.log ;
		#Gate -a [testNumber,LiverWoman_X][particule,gamma][tissue,LiverWoman][nPrimaries,1.374][emissionType,X][patientCT,LiverWoman] mainMacro.mac > ../output/LiverWoman/run_X.log ;

