
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket
import os
import time,collections,os, platform , pathlib
import argparse
import sys
import pandas as pd

BARS = print(40*'--')
##VREFN_TH = 42
##VREFN_TH = 41
##VREFN_TH = 40
##VREFN_TH = 39
VREFN_TH = 40
BUFFER_SIZE = 1024
##FILEDIGITAL = '../files/allDigital_VRefN-SCAN_24May2024_digital.csv'
FILEDIGITAL = '../files/allDigital_VRefN-SCAN_07Oct2024_NOTDUMMIES.csv'
df_digital = pd.read_csv(FILEDIGITAL)
##ALLDATA=1
##ALLDATA=0


def count_txt_files(directory_path):
    # Get a list of all files in the directory
    all_files = os.listdir(directory_path)
    
    # Filter out files that are not .txt files
    txt_files = [file for file in all_files if file.endswith('.txt')]
    
    # Count the number of .txt files
    txt_file_count = len(txt_files)
    
    return txt_file_count

# Fonction pour etablir une connexion TCP avec un serveur.
# ----------------------------------------------------------
##def connect_to_server(server, port, vrefn, dirname="K:\\RUNDATA\\TCPdata", df_digital):
##def connect_to_server(server, port, vrefn, dirname="K:\\RUNDATA\\TCPdata", alldata):
def connect_to_server(server, port, vrefn, dirname="K:\\RUNDATA\\TCPdata"):
    try:
        # Tentative de connexion au serveur specifie par l adresse et le port.
        print(f"Tentative de connexion au serveur {server}:{port}")
        # Creation d'un objet socket avec IPv4 et TCP.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            # Connexion effective au serveur
            client.connect((server, port))
            #client.settimeout(1.0)
            print("Connexion etablie avec le serveur.")
            # Initialisation du numero de commande a 4.
            ##command_number = 4
            command_number = 3

            # Fonction interne pour verifier si la reponse du serveur correspond a l'accuse de reception attendu.
            def check_acknowledgement(command_desc, expected_ack, data):
                # Decodage de la reponse du serveur et affichage pour debogage.
                actual_data = data.decode('utf-8').strip()
                #print(f"DEBUG: Response received for {command_desc}: '{actual_data}'")
                # Verification que la reponse contient l'accuse de reception attendu.
                if expected_ack not in actual_data:
                    raise Exception(f"Acknowledgment expected '{expected_ack}' NOT RECEIVED.")

            # Internal Function to determine the PPREG USED
            def read_ppreg(row,col) :
    
                # Sending row value
                msg = "#1 LOAD_PICMIC_I2C_REG -add 61 -val {}\n".format(row)
                client.sendall(msg.encode('utf-8'))
                data = client.recv(BUFFER_SIZE)

                # Sending col value
                msg = "#1 LOAD_PICMIC_I2C_REG -add 62 -val {}\n".format(col)
                client.sendall(msg.encode('utf-8'))
                data = client.recv(BUFFER_SIZE)

                # Reading response
                msg = "#1 READ_PICMIC_I2C_REG -add 63 ?\n"
                client.sendall(msg.encode('utf-8'))
                data = client.recv(BUFFER_SIZE)
                response = data.decode('utf-8').strip()
                ppreg = response.split('=')[-1].strip()

                print('----->> Used PPREG value '+str(ppreg)+ ' ~~ for ['+str(row)+','+str(col)+'] <<------' )
                return ppreg

            # Internal Function to Set a new PPREG
            def set_ppreg(row,col,new_ppreg):

                # Sending row value
                msg = "#1 LOAD_PICMIC_I2C_REG -add 61 -val {}\n".format(row)
                client.sendall(msg.encode('utf-8'))
                data = client.recv(BUFFER_SIZE)

                # Sending col value
                msg = "#1 LOAD_PICMIC_I2C_REG -add 62 -val {}\n".format(col)
                client.sendall(msg.encode('utf-8'))
                data = client.recv(BUFFER_SIZE)

                # Sending ppreg value
                msg = "#1 LOAD_PICMIC_I2C_REG -add 63 -val{}\n".format(new_ppreg)
                client.sendall(msg.encode('utf-8'))
                data = client.recv(BUFFER_SIZE)
                response = data.decode('utf-8').strip()
                ppreg = response.split('=')[-1].strip()

                print('----->> Set new PPREG value '+str(ppreg)+ ' ~~ for ['+str(row)+','+str(col)+'] <<------' )



            # Liste des commandes a envoyer au serveur avec leur description et l'accuse attendu.
            ##formated_string = f"#3 LOAD_PICMIC_I2C_REG -add 39 -val {vrefn} \n"
            formated_string = f"#2 LOAD_PICMIC_I2C_REG -add 39 -val {vrefn} \n"
            byte_string=formated_string.encode('utf-8')
            commands = [
                ##(b"#1 LOAD_SETUP -FROM .\\Setup\\Setup_08Jul24_V3521.dat\n", "LOAD_SETUP", "#1 LOAD_SETUP #EXECUTED OK"),
                (b"#1 LOAD_SETUP -FROM .\\Setup\\Setup_04Sep24_V3525.dat\n", "LOAD_SETUP", "#1 LOAD_SETUP #EXECUTED OK"),
                #(b"#1 LOAD_SETUP -FROM .\\Setup\\Setup_26Jun24_V3520.dat\n", "LOAD_SETUP", "#1 LOAD_SETUP #EXECUTED OK"),
                #(b"#2 LOAD_PICMIC_CONFIG_FILE -FROM .\\PICMIC_ConfigFiles\\picmic_cfg_all_columns_row3.txt \n", "Chargement du fichier de configuration PICMIC", "#2 LOAD_PICMIC_CONFIG_FILE #EXECUTED OK"),
                ####(b"#2 LOAD_PICMIC_CONFIG_FILE -FROM .\\PICMIC_ConfigFiles\\combinedPulseDigital_calib_VRefN41_New11Jul2024.txt \n", "Chargement du fichier de configuration PICMIC", "#2 LOAD_PICMIC_CONFIG_FILE #EXECUTED OK"),
                ##(b"#2 LOAD_SETUP -FROM .\\Setup\\Setup_08Jul24_V3521.dat\n", "LOAD_SETUP", "#1 LOAD_SETUP #EXECUTED OK"),
               ## (byte_string, "LOAD_PICMIC_I2C_REG", "#2 LOAD_PICMIC_I2C_REG #EXECUTED OK"),
                ##(byte_string, "LOAD_PICMIC_I2C_REG", "#3 LOAD_PICMIC_I2C_REG #EXECUTED OK"),
            ]

            # Envoi de chaque commande et attente/controle de l'accuse de reception.
            for cmd, desc, ack in commands:
                print(cmd)
                client.sendall(cmd)
                data = client.recv(BUFFER_SIZE)
                check_acknowledgement(desc, ack, data)
            line2 = 'LOAD_PICMIC_I2C_REG -add 39 -val '
            line3 = 'LOAD_PICMIC_I2C_REG -add 38 -val '
            ##line4 = 'START_RUN -TIME 5 -SAVETO '
            ##line4 = 'START_RUN -TIME 20 -SAVETO '
            line4 = 'START_RUN -TIME 1 -SAVETO '
            
            directory = dirname
            
            os.makedirs(directory, exist_ok=True)

            # Boucle pour la creation des dossiers specifiques a chaque operation et envoi des commandes correspondantes pour une boucle en VrefN. 
            ##xlimit = [5,40]
            xlimit = [5,VREFN_TH]
            loop_dir = 1
            loop_counter=0

            if ( vrefn-VREFN_TH > 0 ) :
                ##xlimit = [65,40]
                xlimit = [80,VREFN_TH]
                loop_dir = -1
            
            sweeping_flag = True

            while sweeping_flag :
                
                current_command = f"#{command_number} {line2}{vrefn}\n" 
                client.sendall(current_command.encode('utf-8'))
                try:
                    timeout=client.gettimeout()
                    client.settimeout(10.0)
                    ##client.settimeout(30.0)
                    data = client.recv(BUFFER_SIZE)
                    client.settimeout(timeout)
                    check_acknowledgement(f"{line2}{vrefn}", f"#{command_number} LOAD_PICMIC_I2C_REG #EXECUTED OK", data)
                except socket.timeout:
                    print('TIMEOUT')
                command_number += 1

                # for vrefp in range(xlimit[0],xlimit[1],loop_dir):
                for vrefp in range(40,61):
                ##for vrefp in range(30,71):
                ##for vrefp in range(40,80):
                ##for vrefp in range(40,56):
                ##for vrefp in range(50,52):
                    loop_counter+=1
                    folder_name = f"run_vrefn{vrefn}_vrefp{vrefp}"
                    # folder_path = os.path.join(directory, folder_name)
                    folder_path = directory +"\\" + folder_name
                    ##print(f"Repertoire a creer : {folder_path}")
                    if (platform.system()=="Linux") :
                        linuxDir='/group/picmic'+pathlib.PureWindowsPath(folder_path).as_posix().strip('K:')  
                        ##print('==== linux Dir;',directory)
                        os.makedirs(linuxDir, exist_ok=True)
                        # print(f"chmod -R g+w {linuxDir}")
                        os.system("chmod -R g+w "+linuxDir)
                        print(f"Repertoire LINUX cree avec succes : {linuxDir}")
                    else:
                        os.makedirs(folder_path, exist_ok=True)
                    print(f"Repertoire cree avec succes : {folder_path}")
                    time.sleep(0.1)

                    current_command = f"#{command_number} {line3}{vrefp}\n"
                    client.sendall(current_command.encode('utf-8'))
                    try:
                        timeout=client.gettimeout()
                        client.settimeout(20.0)
                        data = client.recv(BUFFER_SIZE)
                        client.settimeout(timeout)
                        check_acknowledgement(f"{line3}{vrefp}", f"#{command_number} LOAD_PICMIC_I2C_REG #EXECUTED OK", data)
                    except socket.timeout:
                        print('TIMEOUT')
                        
                    command_number += 1

                    current_command = f"#{command_number} {line4}{folder_path}\n"
                    client.sendall(current_command.encode('utf-8'))
                    data = client.recv(BUFFER_SIZE)
                    check_acknowledgement(f"{line4}{folder_path}", f"#{command_number} START_RUN #EXECUTED OK", data)
                    #time.sleep(1)
                    #client.sendall(current_command.encode('utf-8'))
                    data = client.recv(BUFFER_SIZE)
                    check_acknowledgement(f"START_RUN", f"#{command_number} RUN_FINISHED", data)
                    #time.sleep(1.0)
                    #command_number += 1

                    #current_command = f"#{command_number} STOP_RUN\n"
                    #client.sendall(current_command.encode('utf-8'))
                    #data = client.recv(1024)
                    #check_acknowledgement(f"STOP_RUN", f"#{command_number} RUN_FINISHED", data)
                    skip_next_response = False
                    command_number += 1

                    if skip_next_response:
                        #print(f"DEBUG: Reponse ignoree pour la commande #{command_number}")
                        client.recv(BUFFER_SIZE)
                        skip_next_response = False

                # Envoi de la commande pour arrêter les scripts sur le serveur.
                client.sendall(b"#{command_number} STOP_SCRIPT\n")
                #print(f"Commande envoyee #{command_number}: STOP_SCRIPT")

                # ########################################################## #
                #                data processing and analysis                #
                # ########################################################## #

                ## process data from binary to ascii
                ##os.system("/home/ilc/habreu/data_bin2ascii/readDataPicmic_bin2ascii_NOSTANDARDBREAK_VREFP.py -f /group/picmic/RUNDATA/TCPdata/run_vrefn*_vrefp*/sampic_tcp_ru*/picmic_dat*/picmic_*.bin")
                os.system("/home/ilc/habreu/data_bin2ascii/readDataPicmic_bin2ascii_NOSTANDARDBREAK_VREFP_TEST.py -f /group/picmic/RUNDATA/TCPdata/run_vrefn*_vrefp*/sampic_ru*/picmic_dat*/picmic_*.bin")
     		##os.system("/home/ilc/habreu/data_bin2ascii/readDataPicmic_bin2ascii_STANDARDBREAK_VREFP.py -f /group/picmic/RUNDATA/TCPdata/run_vrefn*_vrefp*/sampic_tcp_ru*/picmic_dat*/picmic_*.bin")
                	##os.system("/home/ilc/habreu/data_bin2ascii/readDataPicmic_bin2ascii_STANDARDBREAK_VREFP.py -f /group/picmic/RUNDATA/TCPdata/run_vrefn*_vrefp*/sampic_tcp_ru*/picmic_dat*/picmic_*.bin")
                ##else :
                ##os.system("/home/ilc/habreu/data_bin2ascii/readDataPicmic_bin2ascii_STANDARDBREAK_VREFP.py -f /group/picmic/RUNDATA/TCPdata/run_vrefn*_vrefp*/sampic_tcp_ru*/picmic_dat*/picmic_*.bin")

                ## merge decoded data
                print( 'count TXT ', count_txt_files("/group/picmic/RUNDATA/TCPdata"))
                if count_txt_files("/group/picmic/RUNDATA/TCPdata")== 0 :
                    vrefn+=loop_dir
                    os.system('rm -rf /group/picmic/RUNDATA/TCPdata/*')
                    loop_counter=0
                    if (vrefn==xlimit[1]) :
                        sweeping_flag = False
                    continue
                ##print('coutn TXT')
                os.system("python /home/ilc/habreu/data_bin2ascii/merger.py -f /group/picmic/RUNDATA/TCPdata/*txt")

                ## get produce file with list of hired pixels
                filescan = '/group/picmic/RUNDATA/TCPdata/run_vrefn'+str(vrefn)+'_VRefP-SCAN.csv'
                print('file to use :', filescan)
                df_scan = pd.read_csv(filescan)
                print(df_scan)
                scanList =  list(df_scan.select_dtypes(include=['float64']).columns)

                print('# of pixels to correct=',len(scanList))
                print('--List of pixels to correct--')
                print(scanList)

                ##if ( len(scanList)==0 or len(scanList)>2 ) :
                if len(scanList)==0  :
                    vrefn+=loop_dir
                    loop_counter=0
                    if (vrefn==xlimit[1]) :
                        sweeping_flag = False
                else :
                    for i, pixel in enumerate(scanList):
                        
                        this_row = int(pixel.split('-')[0][1:].strip())
                        this_col = int(pixel.split('-')[1][1:].strip())
                        this_ppreg = int(read_ppreg(this_row,this_col))
                        this_vrefn = vrefn
                        print('-->>', i, '--',pixel, ', iVRefN:',vrefn, 'PPREG :', this_ppreg)
                        '''
			##index_digital = df_digital[['VRefN','PulsedReg']][ (df_digital.Scan==pixel) & (df_digital.PulsedReg==int(this_ppreg)) & (df_digital.VRefN2<249)  ].index
                        index_digital = df_digital[['VRefN','PulsedReg']][ (df_digital.Scan==pixel) & (df_digital.PulsedReg==int(this_ppreg)) & (df_digital.VRefN<249)  & (df_digital.VRefN>5)  ].index
            
                        if (len(index_digital)==0) :
                        ##if (len(index_digital)==0 or len(index_digital)>2) :
                            continue
                        idx_digital= index_digital[0]

                        zval_digital = df_digital.PulsedReg[idx_digital]  # zval -- ppreg_digital
                        xval_digital = df_digital.VRefN[idx_digital]  # xval -- vrefn_digital

                        ###  HERE CONTINUE DEVELOPPING 11.07.2024
                        print('INDEX in digital   =',idx_digital)
                        print('PPREG  value digital=',zval_digital)
                        print('VREFN value digital=',xval_digital)
                        ##print('VREFN  value digital=',wval_digital)
            
                        min = 999.0
                        idx_of_min = -1
                        ppreg_of_min = -1
                        vrefn_of_min = 999.0
                        #vrefn2_of_min = 999.0
            
                        print(20*'+')
                        print('-- HERE --')
                        df_temp = df_digital[['VRefN','PulsedReg']][ (df_digital.Scan==pixel) & (df_digital.VRefN>1) ].sort_values(by='VRefN',ascending=True)
                        print(df_temp)
                        list_temp = df_temp['PulsedReg'].tolist()
                        index_current_val = list_temp.index(this_ppreg)
                        del df_temp

                        print(20*'++')
                        print(list_temp)
                        print(20*'++')

                        j = index_current_val +1
                        if (loop_dir<0) :
                            j = index_current_val -1

                        ppreg_of_min = list_temp[j]
                        ##        vrefn_of_min = xval 
            
                        print('........')
                        print('proposed PPReg =',ppreg_of_min)

                        set_ppreg(this_row,this_col,int(ppreg_of_min))

                        ##if (loop_counter==10) :

                        print('--------------------------------------------')
       			''' 
                        if this_ppreg!=64 :
                            print('proposed PPReg =',64)
                            set_ppreg(this_row,this_col,64)
                ## Sweeping --> count the pixels and change their PPReg value
                if (vrefn==xlimit[1]) :
                    sweeping_flag = False
            # --- Henso Here
            exit()


            # Boucle pour la gestion des commandes utilisateur en temps reel.
            while True:
                command = input("Envoyez une commande (tapez 'disconnect' ou Return (commande vide) pour sortir) : ")
                if command.lower() == "disconnect":
                    print("Deconnexion...")
                    break

                if command == "":
                    raise ValueError("La commande ne peut pas être nulle ou vide")

                client.sendall(f"#{command_number} {command}\n".encode("utf-8"))
                print(f"Commande envoyee #{command_number}: {command}")
                command_number += 1
                
    except Exception as e:
        print(f"Erreur: {e}")

# ################################################################################ #
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-host", "--host_ip" ,help="provide the server IP")
    parser.add_argument("-port", "--port_number" ,help="provide the port number")
    parser.add_argument("-vrefn", "--vrefn_val" ,help="provide the current vrefn value")
    parser.add_argument("-dirname", "--dir_name" ,help="provide the output directory value")
##    parser.add_argument("-alldata", "--all_data" ,help="provide the output directory value")
    ##parser.add_argument("-sweeping","--RL",help="Sweeping Right(1) or Left(0)", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    host = str(args.host_ip).strip()
    port = int(args.port_number)
    ival = int(args.vrefn_val)
    this_dirname = str(args.dir_name).strip()
##    m_alldata = int(args.all_data)

    ##print(df_digital)
    ##exit()
    if ( (str(args.host_ip)=='None') & (str(args.port_number)=='None') ) :
        print("----------------------- >>>>>>>>>>>>>>>> Host && PortNumber-- Mandatory   <<<<<<<<<<<<<<<<<<<-------------------------")
        print('Script not executed')
        exit()

    ##print('host=',host,',port=',port, ',vrefn=',ival, ',dir_name=',this_dirname, ', process all data=',m_alldata)
    print('host=',host,',port=',port, ',vrefn=',ival, ',dir_name=',this_dirname)

    ##connect_to_server(host, port, ival,this_dirname,df_dig)
    ##connect_to_server(host, port, ival,this_dirname,m_alldata)
    connect_to_server(host, port, ival,this_dirname)

    print('----- DONE ----------')
    exit()

# ################################################################################ #
if __name__ == "__main__":
    main()
