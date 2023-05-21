import pymysql.cursors # maniplar o mysql
import matplotlib.pyplot as plt # gerar gráficos


con = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='bd_curso_python',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

autenticou = False


def logarCadastrar(): # Funcao para validar as ações de login ou cadastro de usuarios
    usuarioExistente = 0
    autenticado = False # Guardar se autenticou
    usuarioMaster = False # identificar se o usuario logado é ADM

    if decisao == 1: # decidiu Logar
        nome = input('Digite seu nome:\n')
        senha = input('Digite sua senha:\n')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                autenticado = True
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                break # achou o usuario e autenticou, sai
            else: # Ta cagado aqui!
                autenticado = False
        if not autenticado:
            print('Nome ou Senha errado.')

    elif decisao == 2: # decidiu Cadastrar
        print('Faça seu cadastro...')
        nome = input('Digite seu nome: ').lower()
        senha = input('Digite sua senha: ').lower()

        for linha in resultado: # validando se o usuario ja existe
            if nome == linha['nome']:
                usuarioExistente = 1
        if usuarioExistente == 1:
            print('Usuário existente, tente outro Nome de login.')
        elif usuarioExistente == 0:
            try:
                with con.cursor() as cursor:
                    cursor.execute(f'INSERT INTO tb_cadastros(nome, senha, nivel) values ("{nome}", "{senha}", 1)')
                    con.commit()
            except:
                print('Erro ao cadastrar')
    return autenticado, usuarioMaster
# Fim funcao logarCadastrar

def cadastrarProduto():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo do produto: ')
    preco = float(input('Digite o preço do produto: '))

    try:
        with con.cursor() as cursor:
            cursor.execute('INSERT INTO tb_produtos (nome, ingredientes, grupo, preco) values (%s,%s,%s,%s)',(nome, ingredientes, grupo, preco))
            con.commit()
            print('Produto cadastrado com sucesso.')
    except:
        print('Erro ao cadastrar o produto no BD.')
# Fim funcao cadastrarProduto

def listarProdutos():
    produtosAll = []
    try:
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM tb_produtos')
            produtos = cursor.fetchall()
    except:
        print('Erro ao pesquisar o produto no BD.')

    for p in produtos:
        produtosAll.append(p)

    if len(produtosAll) > 0:
        for i in range(0, len(produtosAll)): # percorrer a listagem pelos IDs
            print(produtosAll[i])
    else:
        print('Nenhum produto cadastrado')
# Fim funcao cadastrarProduto

def excluirProduto():
    idRemover = int(input('Digite o ID do produto para excluir: '))
    try:
        with con.cursor() as cursor:
            cursor.execute(f'DELETE FROM tb_produtos WHERE id = {idRemover}')
            con.commit()
    except:
        print('Erro ao excluir o produto.')
# Fim funcao excluirProduto

def listarPedidos():
    pedidosAll = []
    decisaoPedido = 0
    while decisaoPedido != 2:
        pedidosAll.clear() # limpando a array

        try:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM tb_pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('Erro')

        for p in listaPedidos:
            pedidosAll.append(p)

        if len(listaPedidos) > 0:
            for i in range(0, len(listaPedidos)):
                print(pedidosAll[i])
        else:
            print('Nenhum pedido feito')

        decisaoPedido = int(input('Selecione:\n 1 - Dar baixa no pedido \n 2 - Voltar \n'))
        if decisaoPedido == 1:
            idPedidoEntregue = int(input('Digite o ID do pedido a dar baixa: '))

            try:
                with con.cursor() as cursor:
                    cursor.execute(f'DELETE FROM tb_pedidos WHERE id={idPedidoEntregue}')
                    con.commit()
                    print('Pedido dado baixa com sucesso')
            except:
                print('Erro ao dar baixa no pedido no BD')
# Fim listarPedidos

def gerarEstatisticas():
    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM tb_produtos')
            produtos = cursor.fetchall()
    except:
        print('Erro ao consultar o BD')

    try:
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM tb_estatisticas_vendas')
            vendas = cursor.fetchall()
    except:
        print('Erro ao consultar o BD')

    tipo_pesquisa = int(input('Digite:\n 0 Sair\n 1 Pesquisar por Nome\n 2 Pesquisar por Grupo\n'))

    if tipo_pesquisa == 1:
        decisaoEstatistica = int(input('Digite:\n 1 Pesquisar por Dinheiro\n 2 Pesquisar por Qtde\n'))
        if decisaoEstatistica == 1: # Por Dinheiro
            for i in produtos:
                nomeProdutos.append(i['nome']) # guardando os nomes dos produtos

            valores = []
            valores.clear()

            for a in range(0, len(nomeProdutos)): # varrendo toda a lista
                somaValor = -1
                for i in vendas:
                    if i['nome'] == nomeProdutos[a]:
                        somaValor += i['preco']

                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1) # +1 por termos iniciado em -1

            plt.plot(nomeProdutos, valores) # (eixoX, eixoY)
            plt.ylabel('Qtde Vendida em R$')
            plt.xlabel('Produtos')
            plt.show() # Gerando os graficos

        if decisaoEstatistica == 2: # Por Quantidade
            grupoUnico = []
            grupoUnico.clear()

            try:
                with con.cursor() as cursor:
                    cursor.execute('SELECT * FROM tb_produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro ao consultar o BD')

            try:
                with con.cursor() as cursor:
                    cursor.execute('SELECT * FROM tb_estatisticas_vendas')
                    vendasGrupo = cursor.fetchall()
            except:
                print('Erro ao consultar o BD')

            for i in grupo:
                grupoUnico.append(i['nome'])

            # limpando dados repetidos:
            grupoUnico = sorted(set(grupoUnico))

            qtdeFinal = []
            qtdeFinal.clear()

            for h in range(0, len(grupoUnico)):
                qtdeUnitaria = 0
                for i in vendasGrupo:
                    if grupoUnico[h] == i['nome']:
                        qtdeUnitaria += 1
                qtdeFinal.append(qtdeUnitaria)

            plt.plot(grupoUnico, qtdeFinal) # (eixoX, eixoY)
            plt.ylabel('Qtde Unitária Vendida')
            plt.xlabel('Produtos')
            plt.show() # Gerando os graficos
    elif tipo_pesquisa == 2:
        decisaoEstatistica = int(input('Digite:\n 1 Pesquisar por Dinheiro\n 2 Pesquisar por Qtde\n'))
        if decisaoEstatistica == 1:  # Por Dinheiro
            for i in produtos:
                nomeProdutos.append(i['grupo'])  # guardando os nomes dos produtos

            valores = []
            valores.clear()

            for a in range(0, len(nomeProdutos)):  # varrendo toda a lista
                somaValor = -1
                for i in vendas:
                    if i['grupo'] == nomeProdutos[a]:
                        somaValor += i['preco']

                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)  # +1 por termos iniciado em -1

            plt.plot(nomeProdutos, valores)  # (eixoX, eixoY)
            plt.ylabel('Qtde Vendida em R$')
            plt.xlabel('Produtos')
            plt.show()  # Gerando os graficos

        if decisaoEstatistica == 2: # Por Quantidade
            grupoUnico = []
            grupoUnico.clear()

            try:
                with con.cursor() as cursor:
                    cursor.execute('SELECT * FROM tb_produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro ao consultar o BD')

            try:
                with con.cursor() as cursor:
                    cursor.execute('SELECT * FROM tb_estatisticas_vendas')
                    vendasGrupo = cursor.fetchall()
            except:
                print('Erro ao consultar o BD')

            for i in grupo:
                grupoUnico.append(i['grupo'])

            # limpando dados repetidos:
            grupoUnico = sorted(set(grupoUnico))

            qtdeFinal = []
            qtdeFinal.clear()

            for h in range(0, len(grupoUnico)):
                qtdeUnitaria = 0
                for i in vendasGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qtdeUnitaria += 1
                qtdeFinal.append(qtdeUnitaria)

            plt.plot(grupoUnico, qtdeFinal) # (eixoX, eixoY)
            plt.ylabel('Qtde Unitária Vendida')
            plt.xlabel('Produtos')
            plt.show() # Gerando os graficos

# Fim gerarEstatisticas


# Rotina de login:
while not autenticou:
    decisao = int(input('Digite 1 para logar e 2 para cadastrar: '))

    try:
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM tb_cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar ao BD')

    autenticou, usuarioSupremo = logarCadastrar()
# Fim rotina de Login

if autenticou:
    print('Logado com sucesso.')

    if usuarioSupremo:
        decisaoUsuario = 1
        while decisaoUsuario != 0:
            decisaoUsuario = int(input('Selecione: \n 0 Sair \n 1 Cadastrar Produto \n 2 Listar Produtos \n 3 Listar Pedidos\n 4 Visualizar Estatísticas\n'))
            if decisaoUsuario == 1:
                cadastrarProduto()
            elif decisaoUsuario == 2:
                listarProdutos()
                deletarProd = int(input('Selecione: \n 1 Excluir Produto \n 2 Voltar \n')) # Apos listar, pergunta se quer remover algum
                if deletarProd == 1:
                    excluirProduto()
            elif decisaoUsuario == 3:
                listarPedidos()
            elif decisaoUsuario == 4:
                gerarEstatisticas()
# Fim rotina painel de seleçao de opçoes