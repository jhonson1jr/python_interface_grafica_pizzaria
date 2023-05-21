import tkinter.ttk
from tkinter import *
import pymysql
from tkinter import messagebox

class JanelaAdmin():

    def produtosCadastrar(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de Produtos')

        Label(self.cadastrar, text='Cadastrar Produtos').grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        Label(self.cadastrar, text='Nome:').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Ingredientes:').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Grupo:').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Preço:').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        Button(self.cadastrar, text='Salvar', width=15, bg='green2', command=self.produtosCadastrarBackEnd).grid(row=5, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='red2', command=self.produtosDeletarBackEnd).grid(row=5, column=1, padx=5, pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='green2', command=self.produtosListagemBackend).grid(row=6, column=0, padx=5, pady=5)

        self.tree = tkinter.ttk.Treeview(self.cadastrar, selectmode='browse', columns=('coluna1', 'coluna2', 'coluna3', 'coluna4', 'coluna5'), show='headings')

        self.tree.column('coluna1', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('coluna2', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Produto')

        self.tree.column('coluna3', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Ingredientes')

        self.tree.column('coluna4', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Grupo')

        self.tree.column('coluna5', width=50, minwidth=500, stretch=NO)
        self.tree.heading('#5', text='Preço')

        self.tree.grid(row=0, column=4, padx=10, pady=10, columnspan=3, rowspan=7)

        self.produtosListagemBackend() # listagem dos produtos

        self.cadastrar.mainloop()

    def produtosListagemBackend(self):

        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='1234',
                database='bd_curso_python',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no BD')

        try:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM tb_produtos')
                resultados = cursor.fetchall()
        except:
            print('Erro ao consultar a tb_produtos')

        self.tree.delete(*self.tree.get_children()) # limpando a treeview

        linhasVisualizar = []

        for linha in resultados:
            linhasVisualizar.append(linha['id'])
            linhasVisualizar.append(linha['nome'])
            linhasVisualizar.append(linha['ingredientes'])
            linhasVisualizar.append(linha['grupo'])
            linhasVisualizar.append(linha['preco'])
            self.tree.insert('', END, values=linhasVisualizar, iid=linha['id'], tags=1) # iid é o ID de referencia do elemento
            linhasVisualizar.clear()

    def produtosCadastrarBackEnd(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()

        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='1234',
                database='bd_curso_python',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no BD')

        try:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO tb_produtos(nome, ingredientes, grupo, preco) VALUES (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
                con.commit()
        except:
            print('Erro ao cadastrar no tb_produtos')

        self.produtosListagemBackend() # cadastra e exite a listagem atualizada

    def produtosDeletarBackEnd(self):
        if messagebox.askokcancel('Remover Produto', 'Confirma exclusão?'):
            idProduto = int(self.tree.selection()[0]) # pegando o elemento selecionado da treeview

            try:
                con = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='1234',
                    database='bd_curso_python',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                print('Erro ao conectar no BD')

            try:
                with con.cursor() as cursor:
                    cursor.execute(f'DELETE FROM tb_produtos WHERE id = {idProduto}')
                    con.commit()
            except:
                print('Erro ao inserir no tb_produtos')

            self.produtosListagemBackend() # remove e exite a listagem atualizada

    def __init__(self):
        self.root = Tk()
        self.root.title('Administrador')

        Button(self.root, text='Pedidos', width=20, bg='#92DFFF', command=self.pedidosCadastrar).grid(row=0, column=0, pady=10, padx=10)
        Button(self.root, text='Cadastros', width=20, bg='#92DFFF', command=self.produtosCadastrar).grid(row=1, column=0, pady=10, padx=10)


        self.root.mainloop()


    def pedidosCadastrar(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de Pedidos')

        Label(self.cadastrar, text='Cadastrar Pedidos').grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        Label(self.cadastrar, text='Nome:').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Ingredientes:').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Grupo:').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Local Entrega:').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.localEntrega = Entry(self.cadastrar)
        self.localEntrega.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Obs.:').grid(row=5, column=0, columnspan=1, padx=5, pady=5)
        self.observacoes = Entry(self.cadastrar)
        self.observacoes.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

        Button(self.cadastrar, text='Salvar', width=15, bg='green2', command=self.pedidosCadastrarBackEnd).grid(row=6, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='red2', command=self.pedidosDeletarBackEnd).grid(row=6, column=1, padx=5, pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='green2', command=self.pedidosListagemBackend).grid(row=7, column=0, padx=5, pady=5)

        self.tree = tkinter.ttk.Treeview(self.cadastrar, selectmode='browse', columns=('coluna1', 'coluna2', 'coluna3', 'coluna4', 'coluna5', 'coluna6'), show='headings')

        self.tree.column('coluna1', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('coluna2', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Produto')

        self.tree.column('coluna3', width=150, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Ingredientes')

        self.tree.column('coluna4', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Grupo')

        self.tree.column('coluna5', width=150, minwidth=500, stretch=NO)
        self.tree.heading('#5', text='Local Entrega')

        self.tree.column('coluna5', width=50, minwidth=500, stretch=NO)
        self.tree.heading('#6', text='Obs.')

        self.tree.grid(row=0, column=4, padx=10, pady=10, columnspan=3, rowspan=7)

        self.pedidosListagemBackend() # listagem dos produtos

        self.cadastrar.mainloop()


    def pedidosListagemBackend(self):

        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='1234',
                database='bd_curso_python',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no BD')

        try:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM tb_pedidos')
                resultados = cursor.fetchall()
        except:
            print('Erro ao consultar a tb_pedidos')

        self.tree.delete(*self.tree.get_children()) # limpando a treeview

        linhasVisualizar = []

        for linha in resultados:
            linhasVisualizar.append(linha['id'])
            linhasVisualizar.append(linha['nome'])
            linhasVisualizar.append(linha['ingredientes'])
            linhasVisualizar.append(linha['grupo'])
            linhasVisualizar.append(linha['localEntrega'])
            linhasVisualizar.append(linha['observacoes'])
            self.tree.insert('', END, values=linhasVisualizar, iid=linha['id'], tags=1) # iid é o ID de referencia do elemento
            linhasVisualizar.clear()


    def pedidosCadastrarBackEnd(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        localEntrega = self.localEntrega.get()
        observacoes = self.observacoes.get()

        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='1234',
                database='bd_curso_python',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no BD')

        try:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO tb_pedidos (nome, ingredientes, grupo, localEntrega, observacoes) VALUES (%s, %s, %s, %s, %s)', (nome, ingredientes, grupo, localEntrega, observacoes))
                con.commit()
        except:
            print('Erro ao cadastrar no tb_produtos')

        self.pedidosListagemBackend() # cadastra e exite a listagem atualizada

    def pedidosDeletarBackEnd(self):
        if messagebox.askokcancel('Remover Pedido', 'Confirma exclusão?'):
            idPedido = int(self.tree.selection()[0]) # pegando o elemento selecionado da treeview

            try:
                con = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='1234',
                    database='bd_curso_python',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                print('Erro ao conectar no BD')

            try:
                with con.cursor() as cursor:
                    cursor.execute(f'DELETE FROM tb_pedidos WHERE id = {idPedido}')
                    con.commit()
            except:
                print('Erro ao excluir no tb_pedidos')

            self.pedidosListagemBackend() # remove e exite a listagem atualizada


class JanelaInicial():

    def verificaLogin(self):
        autenticado = False
        usuarioMaster = False

        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='1234',
                database='bd_curso_python',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no BD')

        usuario = self.login.get()
        senha = self.senha.get()

        try:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM tb_cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao consultar a tb_cadastros')

        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False # só por segurança
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado: # login errado
            messagebox.showinfo('Login', 'Email ou senha incorreto')

        if autenticado: # se logou com sucesso, encerra a tela de login
            self.root.destroy()
            if usuarioMaster: # se administrador, chama proxima tela:
                JanelaAdmin()

    def cadastro(self):
        Label(self.root, text='Chave de Segurança').grid(row=3, column=0, pady=5, padx=5)
        self.codigoSeguranca = Entry(self.root, show='*')
        self.codigoSeguranca.grid(row=3, column=1, padx=5, pady=5)

        Button(self.root, text='Confirmar Cadastro', width=15, bg='blue1', command=self.cadastroBackEnd).grid(row=4, column=0, columnspan=3, pady=5, padx=10)

    def cadastroBackEnd(self):
        codigoPadrao = '4321@' # codigo padrao de validacao

        if self.codigoSeguranca.get() == codigoPadrao: # se codigo ta ok
            if len(self.login.get()) <= 20:
                if len(self.senha.get()) <= 50:
                    nome = self.login.get()
                    senha =  self.senha.get()

                    try:
                        con = pymysql.connect(
                            host='localhost',
                            user='root',
                            password='1234',
                            database='bd_curso_python',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )
                    except:
                        print('Erro ao conectar no BD')

                    try:
                        with con.cursor() as cursor:
                            cursor.execute('INSERT INTO tb_cadastros (nome, senha, nivel) VALUES (%s, %s, %s)', (nome, senha, 1))
                            con.commit()
                        messagebox.showinfo('Cadastro', 'Usuário cadastrado com sucesso')
                        self.root.destroy() # encerrando a aplicação para que o novo user faca login
                    except:
                        print('Erro ao inserir na tb_cadastros')
                else:
                    messagebox.showinfo('Erro', 'Senha não pode ter mais de 20 caracteres')
            else:
                messagebox.showinfo('Erro', 'Nome não pode ter mais de 50 caracteres')
        else:
            messagebox.showinfo('Erro', 'Código de Segurança inválido')

    def visualizarCadastros(self):
        self.visualizar = Toplevel() # Depende da janela pai, se encerrada a pai, encerra tbm
        self.visualizar.resizable(False, False)
        self.visualizar.title('Listagem de Cadastros')

        self.tree = tkinter.ttk.Treeview(self.visualizar, selectmode='browse', columns=('coluna1', 'coluna2', 'coluna3', 'coluna4'), show='headings')

        self.tree.column('coluna1', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('coluna2', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuário')

        self.tree.column('coluna3', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')

        self.tree.column('coluna4', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.visualizarCadastrosBackEnd() # Fazendo select na base

        self.visualizar.mainloop()

    def visualizarCadastrosBackEnd(self):
        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='1234',
                database='bd_curso_python',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no BD')

        try:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM tb_cadastros')
                resultado = cursor.fetchall()
        except:
            print('Erro ao selecionar na tb_cadastros')

        self.tree.delete(*self.tree.get_children()) # limpando a treeview

        linhasVisualizar = []

        for linha in resultado:
            linhasVisualizar.append(linha['id'])
            linhasVisualizar.append(linha['nome'])
            linhasVisualizar.append(linha['senha'])
            linhasVisualizar.append(linha['nivel'])
            self.tree.insert('', END, values=linhasVisualizar, iid=linha['id'], tags=1)
            linhasVisualizar.clear()

    def __init__(self): # self define o escopo da variavel vinculado a classe, nisso todos os metodos podem usa-lo
        self.root = Tk()
        self.root.title('Login')
        Label(self.root, text='Faça o Login').grid(row=0, column=0, columnspan=2)

        Label(self.root, text='Usuário:').grid(row=1, column=0)
        self.login = Entry(self.root)
        self.login.grid(row=1, column=1)

        Label(self.root, text='Senha:').grid(row=2, column=0)
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)

        # Para referir à função sem executar, escrever sem () no final, senao inicia executando
        Button(self.root, text='Login', bg='green3', width=10, command=self.verificaLogin).grid(row=5, column=0, padx=5, pady=5)
        Button(self.root, text='Cadastrar', bg='orange3', width=10, command=self.cadastro).grid(row=5, column=1, padx=5, pady=5)
        Button(self.root, text='Visualizar Cadastros', bg='white', command=self.visualizarCadastros).grid(row=6, column=0, columnspan=2, padx=5, pady=5)


        self.root.mainloop()

JanelaInicial()