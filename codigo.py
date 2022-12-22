import MySQLdb as sql
import os
from time import sleep
from sys import exit
#Cria uma conexão com o banco de dados.
try:
    host = 'localhost'
    user = 'root'
    password = 'jvcraft199'
    db = 'dados_pessoas'
    port = 3306
    con = sql.connect(host=host, user=user, passwd=password, port=port, db=db)
    c = con.cursor()
except:
    os.system('clear')
    print('Conexão não estabelecida com o banco de dados')
    exit()
    
c.execute('use dados_pessoas')
con.commit()


def InsertDds(cx, table, camp = None, v=[]):
    if camp == None:
        camp = ' '
    else:
        text = ' ('
        for i in range(len(camp)):
              text += f'{camp[i]}' + ', '
        camp = text[:-2]
        camp += ') '
        
    valores = '(DEFAULT'
    for i in range(len(v)):
              valores += ', ' + f'{v[i]}'
            
    valores += ')'
    cmd =  f'INSERT INTO {table}{camp}VALUES {valores}'
    
    try:
       cx.execute(cmd)
    except:
        print('Erro a o inserir dados na base de dados')
        
        
def CreateBds(cx,nome):
    comandos = [f'create database {nome}', f'use {nome}']
    try:
        for cmd in comandos: cx.execute(cmd)
    except:
        print('Database já foi criada!')
        
        
def CreateTable(cx, nome):
    try:
        cmd = f'create table {nome} (`id_{nome}` INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id_{nome}`))'
        cx.execute(cmd)
    except:
        print('Tabela já foi criada.')
        
        
def AddCamp(cx, campos, tabela, tipo, atributos, pos):
    cmd = f'ALTER TABLE {tabela} ADD COLUMN `{campos}` {tipo} {atributos.upper()} AFTER `{pos}`;'
    try:     
        cx.execute(cmd)
    except:
        print('Erro possivel ou Coluna já adcionada')
        

def Menu(cx):
    try:
        comandos = ['1 -> adciona pessoas','2 -> criar nova base dados', '3 -> visualizar base de dados']
        for cm in comandos: print(cm)
        op = input('Digite (s para sair): ')
        if op[0] == 's':
            return 's'
        else:
            if op[0].isnumeric():
                op = int(op[0])
                if (op == 1):
                    lista_de_colunas = list()
                    quant = input('Digite a quantidade de registros: ')
                    if quant.isnumeric():
                        quant = int(quant)
                        for i in range(quant):
                            os.system('clear')
                            lista_de_colunas.append([f"'{input('nome: ')}'", f"'{input('cpf: ')}'", f"'{input('email: ')}'", f"'{input('data ex: aaaa-mm-dd: ')}'"])
                    
                        for i in lista_de_colunas:
                            InsertDds(cx, 'alunos', camp=None, v=i)
                            con.commit()
                    
                    elif (op == 2):
                        name = input('Nome da base de dados: ')
                        CreateBds(c, name)
                        c.commit()
                
                    elif (op == 3):
                        c.execute('SELECT * FROM alunos')
                        con.commit()
                        input('Enter para voltar')
    except:
        print('Erro Retornando para o menu!')
        return 1
      
#Criando tabela alunos!
CreateTable(c, 'alunos')
con.commit()

#Adcionando campos: cpf, email, data_de_nacimento
lista_de_colunas = [['cpf', 'alunos', 'varchar(11)', 'NOT NULL' , 'nome' ], ['email', 'alunos', 'varchar(100)', 'NOT NULL' , 'cpf' ], ['data_de_nacimento', 'alunos', 'DATE', 'NOT NULL' , 'email']]

for coluna in lista_de_colunas:
    AddCamp(c, coluna[0], coluna[1], coluna[2], coluna[3], coluna[4])
    con.commit()
 
ext = 'n'
while (ext != 's'):
    sleep(1)
    os.system('clear')
    ext = Menu(c)
