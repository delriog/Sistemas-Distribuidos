    
    #   Como Executar

    python chat.py 1
    python chat.py 2

    Execute cada um destes comandos em uma aba diferente do terminal

    # Bibliotecas usadas

    threading: usada para implementar threads (https://docs.python.org/3/library/threading.html)
    socket: usada para implementar sockets (https://docs.python.org/3/library/socket.html)
    sys: usada para a função argv pega a lista de argumentos passado para um script (https://docs.python.org/3/library/sys.html)
    emoji: usada para obter os emojis usados (https://pypi.org/project/emoji/) instalação necessária: pip install emoji --upgrade
    
    # Exemplo de uso

    Usuário 1: Escreva seu apelido >> Caio

    Usuário 2: Escreva seu apelido >> Rio

    Usuário 1: 1:oi
    Usuário 2 recebe: Caio : oi

    Usuário 1: 2:🤣
    Usuário 2 recebe: Caio : 🤣

    Usuário 1: 3:https://www.youtube.com/watch?v=dQw4w9WgXcQ
    Usuário 2 recebe: Caio : https://www.youtube.com/watch?v=dQw4w9WgXcQ

    Usuário 1: 4:ECHO
    Usuário 1 recebe: Rio : ECHO
    Usuário 2 recebe: Caio : ECHO
    