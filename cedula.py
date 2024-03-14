import json
import uuid

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

# Função para verificar se um candidato já foi assinalado em pelo menos duas cédulas
def candidato_assinalado_em_duas_cedulas(candidato):
    cedulas_com_assinatura = 0
    for cedula in cedulas:
        if cedula[candidato] > 0:
            cedulas_com_assinatura += 1
            if cedulas_com_assinatura >= 2:
                return True
    return False

# Função para votar em um candidato específico
def votar_candidato(cedula_id, candidato):
    for cedula in cedulas:
        if cedula["Id"] == cedula_id:
            if candidato in cedula:
                if candidato_assinalado_em_duas_cedulas(candidato):
                    cedula[candidato] += 1
                    return True
                else:
                    print(f"{candidato} não foi assinalado em pelo menos duas cédulas.")
                    return False
            else:
                print("Candidato inválido.")
                return False
    print("Cédula não encontrada.")
    return False

# Exemplo de como usar a função:
if votar_candidato(cedulas[0]["Id"], "Candidato A"):
    print("Voto registrado para Candidato A na primeira cédula.")
if votar_candidato(cedulas[1]["Id"], "Candidato A"):
    print("Voto registrado para Candidato A na segunda cédula.")

# Para verificar o resultado, você pode imprimir as cédulas:
print(json.dumps(cedulas, indent=4))