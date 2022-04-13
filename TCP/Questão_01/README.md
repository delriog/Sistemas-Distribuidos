    #   Como Executar

    python3 client.py
    python3 server.py

    Execute cada um destes comandos em uma aba diferente do terminal 

    # Bibliotecas usadas

    threading: usada para implementar threads (https://docs.python.org/3/library/threading.html)
    socket: usada para implementar sockets (https://docs.python.org/3/library/socket.html) 
    os: usada para implementar funcionalidades de  sistema operacional (https://docs.python.org/3/library/os.html)
    hashlib: usada para implementar hash para a criptografia (https://docs.python.org/3/library/hashlib.html)

    # Exemplo de uso

    Client: CONNECT caio,123mudar
    Server: SUCCESS

    Client: PWD
    Server: F:\UTFPR\Sistemas-Distribuidos\TCP\Questão_01

    Client: CHDIR
    Server: 

    Client: GETFILES
    Server: Número de arquivos:  ['2']
            Arquivos:
            client.py
            server.py

    Client: GETDIRS
    Server: Número de pastas:  ['0']
            Pastas:

    Client: EXIT
    Server: *Encerra o programa*
