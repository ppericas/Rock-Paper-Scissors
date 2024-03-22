import random


#piedra = 1 / papel=2 / tijeras= 3

def juego(valor):

    jugada= valor

    valores=[1,2,3]

    jugadamaquina= random.choice(valores)
    print(jugadamaquina)
    # print(jugada)

    if jugada == jugadamaquina:

        return 1, jugadamaquina
        
    elif (jugada== 1 and jugadamaquina==3) or (jugada==2 and jugadamaquina==1) or (jugada==3 and jugadamaquina==2):
        return 2, jugadamaquina
    else:

        return 3, jugadamaquina
    
    
