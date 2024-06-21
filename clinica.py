import textwrap
import datetime
import json
import os

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tCadastrar Paciente
    [2]\tMarcar Consulta
    [3]\tCancelar Consulta
    [4]\tSair
    => """
    return input(textwrap.dedent(menu))

def cadastrar_paciente(pacientes):
    nome = input("Informe o nome do paciente: ")
    telefone = input("Informe o telefone do paciente: ")

    for paciente in pacientes:
        if paciente['telefone'] == telefone:
            print("Paciente já cadastrado!")
            return

    pacientes.append({"nome": nome, "telefone": telefone})
    print("Paciente cadastrado com sucesso")

def listar_pacientes(pacientes):
    if not pacientes:
        print("Não há pacientes cadastrados.")
        return

    print("\nPacientes Cadastrados:")
    for i, paciente in enumerate(pacientes, start=1):
        print(f"[{i}] {paciente['nome']} - {paciente['telefone']}")

def marcar_consulta(pacientes, consultas):
    if not pacientes:
        print("Não há pacientes cadastrados para marcar consultas.")
        return

    listar_pacientes(pacientes)
    paciente_idx = int(input("Selecione o paciente pelo número: ")) - 1
    if paciente_idx < 0 or paciente_idx >= len(pacientes):
        print("Paciente inválido.")
        return

    dia = input("Informe o dia da consulta (dd-mm-aaaa): ")
    hora = input("Informe a hora da consulta (hh:mm): ")
    especialidade = input("Informe a especialidade desejada: ")

    data_hora = datetime.datetime.strptime(f"{dia} {hora}", "%d-%m-%Y %H:%M")

    if data_hora < datetime.datetime.now():
        print("Não é possível agendar consultas em datas passadas.")
        return

    for consulta in consultas:
        if consulta['data_hora'] == data_hora:
            print("Já existe uma consulta agendada para este horário.")
            return

    consultas.append({
        "paciente": pacientes[paciente_idx],
        "data_hora": data_hora,
        "especialidade": especialidade
    })
    print("Consulta marcada com sucesso")

def cancelar_consulta(consultas):
    if not consultas:
        print("Não há consultas agendadas.")
        return

    print("\nConsultas Agendadas:")
    for i, consulta in enumerate(consultas, start=1):
        paciente = consulta['paciente']
        data_hora = consulta['data_hora'].strftime("%d-%m-%Y %H:%M")
        especialidade = consulta['especialidade']
        print(f"[{i}] {paciente['nome']} - {data_hora} - {especialidade}")

    consulta_idx = int(input("Selecione a consulta pelo número: ")) - 1
    if consulta_idx < 0 or consulta_idx >= len(consultas):
        print("Consulta inválida.")
        return

    consultas.pop(consulta_idx)
    print("Consulta cancelada com sucesso")

def salvar_dados(pacientes, consultas):
    dados = {
        "pacientes": pacientes,
        "consultas": [
            {
                "paciente": consulta['paciente'],
                "data_hora": consulta['data_hora'].strftime("%d-%m-%Y %H:%M"),
                "especialidade": consulta['especialidade']
            } for consulta in consultas
        ]
    }
    with open("dados_clinica.json", "w") as f:
        json.dump(dados, f)

def carregar_dados():
    if os.path.exists("dados_clinica.json"):
        with open("dados_clinica.json", "r") as f:
            dados = json.load(f)
            dados['consultas'] = [
                {
                    "paciente": consulta['paciente'],
                    "data_hora": datetime.datetime.strptime(consulta['data_hora'], "%d-%m-%Y %H:%M"),
                    "especialidade": consulta['especialidade']
                } for consulta in dados['consultas']
            ]
            return dados['pacientes'], dados['consultas']
    return [], []

def main():
    pacientes, consultas = carregar_dados()

    while True:
        opcao = menu()

        if opcao == "1":
            cadastrar_paciente(pacientes)
        elif opcao == "2":
            marcar_consulta(pacientes, consultas)
        elif opcao == "3":
            cancelar_consulta(consultas)
        elif opcao == "4":
            salvar_dados(pacientes, consultas)
            break
        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
