import os
from subprocess import Popen, PIPE
import arcpy 
import logging


def tnspingTeste(instancia):
	tnsping=Popen(['tnsping', instancia],stdin=PIPE, stdout=PIPE, stderr=PIPE)
	dados=str(tnsping.communicate())
	return dados.find("OK")

def sqlrun(sqlCommand,connectString):
 session = Popen(['sqlplus', '-S', connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
 session.stdin.write(sqlCommand)
 return session.communicate()
 
#caminho 
caminho_log='C:\\GitHub\\disconect\\disconect_sde\LocGeoDbExclMode.log'
file_connect='c:\\temp\\LocGeoDbExclMode.sde'
#Input da instancia
instancia = raw_input("Digite a instancia:")
#Nome do script
script="LocGeoDbExclMode"
logger = logging.getLogger('disconect_sde')
#caminho do log
hdlr = logging.FileHandler(caminho_log)
#formatacao da string
formatter = logging.Formatter('%(asctime)-15s %(HOSTNAME)-7s %(SCRIPT)-7s %(USER)-10s %(BANCO)-8s %(PID)-8s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
#Nivel do log
logger.setLevel(logging.INFO) 
#variaveis do log
f_temp = {'USER': os.environ['USERNAME'], 'HOSTNAME': os.environ['COMPUTERNAME'], 'BANCO' : instancia, 'SCRIPT' : script , 'PID' : os.getpid() }

logger.info('Inciado a execucao do script',extra=f_temp)
#usuario e senha em formato de numeor
user=[1725, 1815, 1725, 1740, 1515, 1635, 705, 1470, 1500, 735, 735, 1455, 1500, 1635, 960]
teste=""
#loop para converte senha em string
for x in range(0, len(user)):	
 teste+=chr(user[x] /15)
#teste disponibilidade da instancia
resultado= tnspingTeste(instancia)
#criacao da string de conexao
teste= teste + instancia
if (resultado != -1) :
	try:
		#privilegio de dba
		sqlrun('GRANT "DBA" TO SDE;',teste) 
		sqlrun('ALTER USER SDE DEFAULT ROLE ALL;',teste)
		logger.info('Privilegios configurado',extra=f_temp)
		#teste da existencia do arquivo de conexao
		if (os.path.isfile(file_connect)):
			logger.info('Removendo arquivos de conexao antigo',extra=f_temp)
			#removendo arquivo de conexoes antiga
			os.remove(file_connect)
		#teste da existencia do arquivo de conexao
		if not (os.path.isfile(file_connect)):
			logger.info('Criando arquivo de conexao',extra=f_temp)
			#criando arquivo de conexao
			arcpy.CreateArcSDEConnectionFile_management (
				out_folder_path = "C:\\temp",
				out_name = "LocGeoDbExclMode.sde",
				server = " ", #E preciso um espaco simples.
				service = "sde:oracle11g:"+ instancia, #Se nao tiver string e criado como servico.
				account_authentication = "DATABASE_AUTH", 
				username = "sde",
				password = "sde",
				save_username_password = "SAVE_USERNAME" # Deixar a senha salva.
			)
			logger.info('Arquivo de conexao criado',extra=f_temp)		 
		#os.system("pause")
		#Definindo arquivo de worksapce
		arcpy.env.workspace=file_connect
		#Disconectar todos usuarios
		arcpy.DisconnectUser(file_connect,'ALL')
		logger.info('Usuario desconectado',extra=f_temp)
		#Bloquear conexao do banco
		arcpy.AcceptConnections(file_connect, False)
		logger.info('Bloqueio de conexao do banco',extra=f_temp)
		#os.system("pause")
		sqlrun('REVOKE "DBA" FROM SDE;',teste)
		sqlrun('ALTER USER SDE DEFAULT ROLE ALL;',teste)
		logger.info('Removendo privilegios adiconais',extra=f_temp)
		logger.info('Aguardando comando para desbloquear sessoes',extra=f_temp)
		raw_input("Precionar enter para desbloquear conexoes")		
		#Liberacao de conexao
		arcpy.AcceptConnections(file_connect,True)
		logger.info('Conexoes do banco liberadas',extra=f_temp)
		#remover arquivo de conexao
		os.remove(file_connect)
		logger.info('Removendo o arquivo de conexao',extra=f_temp)
		raw_input("Finalizado com sucesso")
		logger.info('Finalizado com sucesso',extra=f_temp)
	except:
		logger.info('Falha de execucao',extra=f_temp)
		#Remover privilegios em caso de falha
		sqlrun('REVOKE "DBA" FROM SDE;',teste)
		sqlrun('ALTER USER SDE DEFAULT ROLE ALL;',teste)
		logger.info('Privilegios removidos',extra=f_temp)
else:
	logger.info('TSname nao configurado ou instancia indisponivel',extra=f_temp)
	raw_input("A instancia " + instancia + " nao esta disponivel ou tnsname da instancia nao configurado. ")