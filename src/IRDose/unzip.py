userName = 'test'
import subprocess as sp

sp.Popen(['mkdir', '-p', 'media/'+userName])
sp.call('unzip media/*.zip -d media/'+userName, shell=True)
sp.call('rm -r media/*.zip media/__*', shell=True)

