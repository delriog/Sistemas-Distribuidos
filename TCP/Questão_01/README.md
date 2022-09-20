    #   Como Executar

    python3 server.py
    python3 client.py

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

    Client: CHDIR F:\UTFPR\SD\Sistemas-Distribuidos\TCP\
    Server: SUCCESS

    Client: GETFILES
    Server: client.py, README.md, server.py, Numero de arquivos: 3

    Client: GETDIRS
    Server: Numero de pastas: 0

    Client: EXIT
    Server: *Encerra o programa*
