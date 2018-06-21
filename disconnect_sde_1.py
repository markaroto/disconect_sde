import os
from subprocess import Popen, PIPE
import arcpy 

user=[1725, 1815, 1725, 1740, 1515, 1635, 705, 1470, 1500, 735, 735, 1455, 1500, 1635, 960]
teste=""
for x in range(0, len(user)):	
 teste+=chr(user[x] /15)
 
instancia = raw_input("Digite a instancia:")
def tnspingTeste(instancia):
	tnsping=Popen(['tnsping', instancia],stdin=PIPE, stdout=PIPE, stderr=PIPE)
	dados=str(tnsping.communicate())
	return dados.find("OK")

def sqlrun(sqlCommand,connectString):
 session = Popen(['sqlplus', '-S', connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
 session.stdin.write(sqlCommand)
 return session.communicate()
 
resultado= tnspingTeste(instancia)
teste= teste + instancia
file_connect="c:\\temp\\disconect_sessions.sde"
if (resultado != -1) :	
	sqlrun('GRANT "DBA" TO SDE;',teste) 
	sqlrun('ALTER USER SDE DEFAULT ROLE ALL;',teste)
	if (os.path.isfile(file_connect)):
		os.remove(file_connect)		
	if not (os.path.isfile(file_connect)):
		arcpy.CreateArcSDEConnectionFile_management (
			out_folder_path = "C:\\temp",
			out_name = "disconect_sessions.sde",
			server = " ", #E preciso um espaco simples.
			service = "sde:oracle11g:"+ instancia, #Se nao tiver string e criado como servico.
			account_authentication = "DATABASE_AUTH", 
			username = "sde",
			password = "sde",
			save_username_password = "SAVE_USERNAME" # Deixar a senha salva.
		)
	 
	#os.system("pause")
	arcpy.env.workspace=file_connect
	arcpy.DisconnectUser(file_connect,'ALL')
	arcpy.AcceptConnections(file_connect, False)
	#os.system("pause")
	sqlrun('REVOKE "DBA" FROM SDE;',teste)
	sqlrun('ALTER USER SDE DEFAULT ROLE ALL;',teste)
	raw_input("Precionar enter para desbloquear conexoes")		
	arcpy.AcceptConnections(file_connect,True)
	os.remove(file_connect)
	raw_input("Finalizado com sucesso")
else:
	raw_input("A instancia " + instancia + " nao esta disponivel ou tnsname da instancia nao configurado. ")