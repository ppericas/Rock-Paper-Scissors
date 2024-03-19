import random


#piedra = 1 / papel=2 / tijeras= 3

def juego(valor):

    jugada= valor
    
    

    jugadamaquina= random.randint(1, 3)
    print(jugadamaquina)

    if jugada == jugadamaquina:

        return "empate"
        
    elif (jugada== 1 and jugadamaquina==3) or (jugada==2 and jugadamaquina==1) or (jugada==3 and jugadamaquina==2):
        return "ganas"
    else:

        return "pierdes"
    
    
