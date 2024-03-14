import json
import uuid

# Inicialização das cédulas
num_cedulas = 3
cedulas = []

for _ in range(num_cedulas):
    cedula = {
        "Id": str(uuid.uuid4()),
        "Candidato A": 0,
        "Candidato B": 0,
        "Candidato C": 0,
        "Nulo": 0
    }
    cedulas.append(cedula)

# Função para que o usuário assinale um candidato em duas cédulas
def usuario_assinala_candidato(candidato):
    cedulas_assinaladas = 0
    for cedula in cedulas:
        if cedulas_assinaladas < 2:
            cedula[candidato] = 1
            cedulas_assinaladas += 1

# Solicita ao usuário que escolha um candidato para assinalar
candidato_escolhido = input("Escolha o candidato (A, B ou C): ").strip().upper()

if candidato_escolhido in ["A", "B", "C"]:
    usuario_assinala_candidato("Candidato " + candidato_escolhido)
else:
    print("Opção de candidato inválida. Escolha entre A, B ou C.")

# Para verificar o resultado, você pode imprimir as cédulas:
#print(json.dumps(cedulas, indent=4))
