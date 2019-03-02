#!/usr/bin/python

import subprocess
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


#Get information from a virtual machine
@app.route('/', methods=['GET'])
def prueba():
	return "Hola Mundo"
''' 
Punto1
Muesta las maquinas virtuales que hay en el equipo
'''
@app.route('/vms', methods=['GET'])
def showvmlist():
	output = subprocess.check_output(['vboxmanage', 'list' , 'vms'])
	str = output.splitlines()
	return jsonify({'list': str})
''' 
Punto2
Muestra las máquinas virtuales que esta corriendo
'''
@app.route('/running', methods=['GET'])
def showvmsrunning():
	output = subprocess.check_output(['vboxmanage', 'list' , 'runningvms'])
	str = output.splitlines()
	return jsonify({'list': str})
''' 
Punto3
Muestra toda la información de una máquina virtual
'''
@app.route('/vms/<string:vm>', methods=['GET'])
def showvminfo(vm):
	output = subprocess.check_output(['vboxmanage', 'showvminfo', vm ])
	str = output.splitlines()
	return jsonify({'list': str})
''' 
Punto4
Muestra la memoria RAM de una máquina virtual
'''
@app.route('/vms/ram/<string:vm>', methods=['GET'])
def showvmram(vm):
	output = subprocess.Popen(['vboxmanage', 'showvminfo', vm ], stdout = subprocess.PIPE)
	tail = subprocess.check_output(['grep', 'Memory'], stdin = output.stdout)
	str = tail.splitlines()
	return jsonify({'list': str})
''' 
Punto5
Muestra el numero de tarjetas de red de una máquina virtual
'''
@app.route('/vms/nic/<string:vm>', methods=['GET'])
def showvmnetworkcard(vm):
	output = subprocess.Popen(['vboxmanage', 'showvminfo', vm ], stdout = subprocess.PIPE)
	tail1 = subprocess.Popen(['grep', 'NIC'], stdin = output.stdout, stdout = subprocess.PIPE)
	tail2 = subprocess.Popen(['grep', 'MAC'], stdin = tail1.stdout, stdout = subprocess.PIPE)
	out = subprocess.check_output(['wc', '-l'], stdin = tail2.stdout)
	return jsonify({'list': out})
#Modify a virtual machine
@app.route('/vms/modify/cpu/<string:vm>/<string:cpu>', methods=['PUT'] )
def modifyvmcpu(vm, cpu):
	subprocess.run(['vboxmanage', 'modifyvm', vm, '--cpus' , cpu ])
	return jsonify({'list': "Se cambio a la maquina virtual "})
@app.route('/vms/modify/ram/<string:vm>/<string:ram>', methods=['PUT'] )
def modifyvmram(vm, ram):
	subprocess.run(['vboxmanage', 'modifyvm', vm, '--memory' , ram ])
	return jsonify({'list': "Se cambio a la maquina virtual "})
@app.route('/vms/modify/cpupercentage/<string:vm>/<string:cpupercentage>', methods=['PUT'] )
def modifyvmcpupercentage(vm, cpupercentage):
	subprocess.run(['vboxmanage', 'modifyvm', vm, '--cpuexecutioncap' , cpupercentage ])
	return jsonify({'list': "Se cambio a la maquina virtual "})
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port = 5000)















#curl -i -H "Content-Type: application/json" -X POST -d '{"title": "read a book"}' http://localhost:5000/tasks
#asi se accede  al post
#curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/tasks/2
#asi se accede  al put
#si es con delete el -X me dice que metodo usar si no lo pongo por defecto el get pero si lo pongo lo puedo cambiar como yo quiera.


