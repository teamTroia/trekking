from encoder import distRodas
from gyro import readAngularSpeed

Lrobo = 15

def Travel(): 
    Enc = distRodas()
    distanciaAntigaDireita = Enc['D']
    distanciaAntigaEsquerda = Enc['E']
    if(Enc['D'] != distanciaAntigaDireita):
        distanciaNovaDireita = Enc['D']
    
    if(Enc['E'] != distanciaAntigaEsquerda):
        distanciaNovaEsquerda = Enc['E']

    deltaDDireita = distanciaNovaDireita - distanciaAntigaDireita
    deltaDEsquerda = distanciaNovaEsquerda - distanciaAntigaEsquerda

    return {"deltaDDireita": deltaDDireita, 'deltaDEsquerda': deltaDEsquerda}

def velocity():
    odd = Travel
    Enc = distRodas()
    gyro = readAngularSpeed()
    veldireita = odd['deltaDDireita']
    velesquerda = odd['deltaDEsquerda']
    velocity = abs((veldireita+velesquerda)/2)
    if(veldireita<velesquerda):
        velangular = abs((veldireita-velesquerda)/Lrobo)
    elif(velesquerda<veldireita):
        velangular = abs((velesquerda-veldireita)/Lrobo)
    else:
        velangular = 0

    return {'foward': velocity, 'angular': velangular}


if __name__ == '__main__':
  while(1):
      velocity()
