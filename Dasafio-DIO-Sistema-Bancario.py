from datetime import datetime

data_atual = datetime.now()

def menu (): 
    menu = """
    ======== MENU ========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """
    return input(menu)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f} {data_atual}\n"
        print ("Deposito feito com sucesso")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar (*, saldo, valor, extrato, limite, numero_saques, limite_saques): 

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques diarios excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f} {data_atual}\n"
        numero_saques += 1
        print ("Saque realizado !")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def exibir_extrato (saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def cadastrar_usuario (usuarios): 
    cpf = input ("Informe seu CPF (Somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n Já existe usuario com esse CPF ")
        return
    
    nome = input ("Informe seu nome completo: ")
    data_nascimento = input ("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereço = input ("Informe seu endereço (logadouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append ({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})

    print("Usuário Cadastrado !!")

def cadastrar_conta (agencia, numero_conta, usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Contra Criada!!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuário nao encontrado, tentar novamente!!")

def filtrar_usuario (cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario ['cpf']== cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_conta (contas):
    for conta in contas:
        linha = f"""\
            Agência:{conta['agencia']}
            C/C:{conta['numero_conta']}
            Titular:{conta['usuario']['nome']}
        """
        print("="*100)

def main (): 
    LIMITE_SAQUES = 10
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = [] 

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar (saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato (saldo, extrato=extrato)

        elif opcao == "nu":
            cadastrar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = cadastrar_conta (AGENCIA, numero_conta, usuarios)

            if conta:
               contas.append(conta)

        elif opcao == "lc":
            listar_conta (contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()