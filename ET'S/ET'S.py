import pyodbc
import pandas as pd
from customtkinter import *
from tkinter import filedialog, messagebox, StringVar, PhotoImage

class Principal(CTk):
    def __init__(self):
        super().__init__()
        # Configuração da janela principal
        self.title("ET'S")
        self.geometry("1024x650")
        set_appearance_mode('DARK')
        set_default_color_theme('dark-blue')
        self.iconbitmap("aliens-_1_.ico")
        icone = PhotoImage(file="ET.png")  # Substitua pelo caminho para o ícone
        self.iconphoto(True, icone)  # Define o ícone para barra de tarefas e janela
        # Variáveis para armazenar dados
        self.planilha = None
        self.servidor = None
        self.usuario = None
        self.banco = None
        self.porta = None
        self.senha = None
        self.driver = None
        self.tabela = None
        self.conn = None
        self.cursor = None
        self.table_columns = []  # Lista para armazenar as colunas da tabela selecionada
        self.selected_table_name = None
        self.dados_por_coluna = {}  # Dicionário para armazenar os dados de todas as abas
        self.dados_aba_especifica = {}  # Dicionário para armazenar os dados da aba selecionada

        # Dicionário de palavras-chave dos drivers para cada DBMS
        self.drivers_dbms_keywords = {
            "MySQL": ["MySQL"],
            "PostgreSQL": ["PostgreSQL"],
            "SQL Server": ["SQL Server", "ODBC Driver"],
            "Oracle": ["Oracle"]
        }

        ### Coluna da esquerda (Frame)
        self.left_frame = CTkFrame(self, width=70, fg_color=('#3f3e3e'))
        self.left_frame.pack(side="left", fill="y")

        ## Frame superior com os botões "Conexão" e "Suporte"
        self.left_frame.top_frame = CTkFrame(self.left_frame, height=30, width=50, fg_color=('#3f3e3e'))
        self.left_frame.top_frame.pack(side="top", fill="x")

        self.seprator_contain = CTkFrame(self.left_frame, height=2, fg_color=('white'))
        self.seprator_contain.pack(side="top", fill="x")

        # Botões "Conexão" e "Suporte" no frame superior
        self.left_frame.top_frame.not_connected_button = CTkButton(self.left_frame.top_frame, text="Conexão", command=self.show_conexao, fg_color=('#3f3e3e'))
        self.left_frame.top_frame.not_connected_button.pack(side="left", fill="both")

        self.left_frame.top_frame.help_page_button = CTkButton(self.left_frame.top_frame, text="Suporte", command=self.show_suporte, fg_color=('#3f3e3e'))
        self.left_frame.top_frame.help_page_button.pack(side="left", fill="both")

        ## Frame de conteúdo de conexão e página de suporte
        self.left_frame.contain_frame = CTkFrame(self.left_frame, height=800, fg_color=('#3f3e3e'))
        self.left_frame.contain_frame.pack(fill="both")

        self.seprator = CTkFrame(self, width=3, fg_color=('transparent'))
        self.seprator.pack(side="left", fill="y")

        self.seprator = CTkFrame(self, width=2, fg_color=('white'))
        self.seprator.pack(side="left", fill="y")

        self.seprator = CTkFrame(self, width=3, fg_color=('transparent'))
        self.seprator.pack(side="left", fill="y")

        # Variáveis para gerenciar o conteúdo
        self.conexao_content = None
        self.suporte_content = None

        # Criação do conteúdo de conexão e suporte
        self.create_conexao_content()
        self.create_suporte_content()
        self.create_initial_window()
        # self.show_conexao()

    def create_initial_window(self):
        # Conteúdo da segunda partição
            self.right_frame = CTkFrame(self, width=70, fg_color=('#3f3e3e'))
            self.right_frame.pack(expand=True, fill="both")

            self.upload_text_label = CTkLabel(
                self.right_frame, text="Carregue as planilhas aqui",
                font=("Arial", 14)
            )
            self.upload_text_label.pack(side="top", pady="100")

            # Botão "Carregar arquivos"
            self.upload_button = CTkButton(self.right_frame, text="Carregar arquivos", command=self.carregar_arquivos, fg_color=('green'))
            self.upload_button.pack(side="top", pady="250")
    def create_conexao_content(self):
        """Cria o conteúdo da área de conexão"""
        if self.conn:
            self.conected_window(self.conn)
        else:
            if self.conexao_content:
                self.conexao_content.destroy()

            self.conexao_content = CTkFrame(self.left_frame.contain_frame, fg_color=('transparent'))
            self.conexao_content.pack(expand=True, fill="both")

            # Menu de seleção de DBMS
            self.dbms_opcoes = ["MySQL", "PostgreSQL", "SQL Server", "Oracle"]
            self.dbms_var = StringVar(value=self.dbms_opcoes[0])

            dbms_label = CTkLabel(self.conexao_content, text="DBMS")
            dbms_label.pack(pady=(10, 0))

            self.dbms_menu = CTkOptionMenu(self.conexao_content, values=self.dbms_opcoes, command=self.on_dbms_select, fg_color=('gray'))
            self.dbms_menu.pack(pady=5)

            # Campos para servidor, porta, banco, usuário, senha e driver
            # Labels e entries

            # Servidor
            self.label_servidor = CTkLabel(self.conexao_content, text="Servidor")
            self.entry_servidor = CTkEntry(self.conexao_content)

            # Porta
            self.label_porta = CTkLabel(self.conexao_content, text="Porta")
            self.entry_porta = CTkEntry(self.conexao_content)

            # Banco de Dados
            self.label_banco = CTkLabel(self.conexao_content, text="Banco de Dados")
            self.entry_banco = CTkEntry(self.conexao_content)

            # Usuário
            self.label_usuario = CTkLabel(self.conexao_content, text="Usuário")
            self.entry_usuario = CTkEntry(self.conexao_content)

            # Senha
            self.label_senha = CTkLabel(self.conexao_content, text="Senha")
            self.entry_senha = CTkEntry(self.conexao_content, show="*")

            # Campo para seleção de driver (OptionMenu)
            self.label_driver = CTkLabel(self.conexao_content, text="Driver ODBC")
            self.driver_var = StringVar()
            self.driver_menu = CTkOptionMenu(self.conexao_content, values=[], fg_color=('gray'))

            # Botão de conexão
            self.conectar_button = CTkButton(self.conexao_content, text="Conectar", command=self.verificar_permissoes_e_conectar, fg_color=('green'))

    def create_suporte_content(self):
        """Cria o conteúdo da área de suporte"""
        if self.suporte_content:
            self.suporte_content.destroy()

        self.suporte_content = CTkFrame(self.left_frame.contain_frame, fg_color=('transparent'))
        # Não empacotamos ainda

        # Adiciona conteúdo de suporte
        suporte_label = CTkLabel(self.suporte_content, text="Bem-vindo ao Suporte!",
                                 font=("Arial", 16))
        suporte_label.pack(pady=20)

        suporte_text = CTkTextbox(self.suporte_content, width=400, height=500)
        suporte_text.insert("0.0", """
        
Bem-vindo à página de suporte para a nossa ferramenta Python, que facilita a conexão com bancos de dados utilizando drivers ODBC no método DSN-LESS e permite a manipulação de planilhas de maneira eficiente. Aqui, você encontrará orientações sobre configuração, solução de problemas e respostas às dúvidas mais frequentes.

Conexão com o Banco de Dados
Para garantir uma conexão bem-sucedida ao banco de dados, siga as orientações abaixo:

Permissões:

- Certifique-se de que o usuário tem as permissões adequadas para acessar o banco de dados.

- Verifique as credenciais (nome de usuário e senha) e garanta que estão corretas.

- Contate o administrador do banco para ajustar as permissões, se necessário.


Endereço do Servidor:

- Insira o endereço do servidor (IP ou nome do host) corretamente na configuração.

- Caso utilize uma VPN, verifique se a conexão está ativa antes de tentar acessar o banco.


Portas:

- Verifique qual porta está configurada para o banco de dados (ex.: 1433 para SQL Server, 3306 para MySQL).

- Certifique-se de que a porta está aberta e acessível na sua rede.

- Se a porta estiver bloqueada, entre em contato com o administrador de rede para liberar o acesso.
Planilhas

- Ao trabalhar com planilhas, é importante atentar-se a possíveis problemas que podem comprometer a funcionalidade da ferramenta.


Planilhas:


Arquivo Danificado:

- Se o arquivo da planilha estiver corrompido, a ferramenta não conseguirá processá-lo.

- Verifique se o arquivo abre corretamente em um editor de planilhas (ex.: Excel) e tente salvá-lo novamente.

- Utilize ferramentas de reparo, se necessário, ou substitua o arquivo por uma versão válida.


Campos Nulos:

- Certifique-se de que os campos essenciais para sua análise não estão em branco.

- Caso haja campos nulos, a ferramenta pode apresentar inconsistências nos resultados.

- Considere preencher os campos nulos com valores padrão ou corrigir os dados na planilha original.


Perguntas Frequentes (FAQ):

- Como configuro a conexão DSN-LESS?

Para configurar a conexão DSN-LESS, forneça as informações necessárias, como o driver ODBC, endereço do servidor, banco de dados, usuário e senha diretamente no script Python. Um exemplo básico de configuração está disponível na documentação da ferramenta.

- A ferramenta suporta quais formatos de planilhas?

A ferramenta suporta arquivos nos formatos XLSX. Para outros formatos, é necessário convertê-los antes de usar.

- O que fazer se a conexão falhar?

Revise as informações de configuração, como endereço do servidor e porta.
Verifique a conectividade com o servidor utilizando ferramentas como ping ou telnet.
Consulte o administrador do banco de dados para confirmar as permissões e credenciais.


Onde encontro mais informações sobre os drivers ODBC suportados?
Acesse a seção de documentação sobre drivers no site oficial da ferramenta, onde listamos os drivers recomendados para diferentes bancos de dados.

""")
        suporte_text.configure(state="disabled")
        suporte_text.pack(pady=30, fill="both", expand=True)

        contato_label = CTkLabel(self.suporte_content, text="Entre em contato conosco:")
        contato_label.pack(pady=10)

        email_label = CTkLabel(self.suporte_content, text="Email: ETS@gmail.com")
        email_label.pack(pady=5)

        telefone_label = CTkLabel(self.suporte_content, text="Telefone: (11) 1234-5678")
        telefone_label.pack(pady=5)

    def show_conexao(self):
        """Exibe o conteúdo de conexão"""
        self.limpar_frame(self.left_frame.contain_frame)
        self.create_conexao_content()
        if self.suporte_content:
            self.suporte_content.pack_forget()
        if self.conexao_content:
            self.conexao_content.pack(expand=True, fill="both")
            self.on_dbms_select()

    def show_suporte(self):
        """Exibe o conteúdo de suporte"""
        self.limpar_frame(self.left_frame.contain_frame)
        self.create_suporte_content()
        if self.conexao_content:
            self.conexao_content.pack_forget()
        if self.suporte_content:
            self.suporte_content.pack(expand=True, fill="both")

    def on_dbms_select(self, event=None):
        """Exibe os campos necessários para a conexão com o DBMS selecionado"""
        dbms = self.dbms_menu.get()
        # Oculta todos os campos primeiro
        for widget in self.conexao_content.pack_slaves():
            if widget not in [self.dbms_menu, self.dbms_menu.master]:
                widget.pack_forget()
        # Exibe os campos comuns para todos os DBMS
        self.label_servidor.pack(pady=(5, 0))
        self.entry_servidor.pack()
        self.label_porta.pack(pady=(5, 0))
        self.entry_porta.pack()
        self.label_usuario.pack(pady=(5, 0))
        self.entry_usuario.pack()
        self.label_senha.pack(pady=(5, 0))
        self.entry_senha.pack()

        if dbms in ["SQL Server", "PostgreSQL", "MySQL"]:
            self.label_banco.pack(pady=(5, 0))
            self.entry_banco.pack()

        # Obter a lista de drivers
        drivers = self.get_drivers_for_dbms(dbms)
        if drivers:
            self.driver_menu.configure(values=drivers)
            self.driver_menu.set(drivers[0])
        else:
            self.driver_menu.configure(values=["Nenhum driver encontrado"])
            self.driver_menu.set("Nenhum driver encontrado")

        self.label_driver.pack(pady=(5, 0))
        self.driver_menu.pack()

        # Exibe o botão de conectar
        self.conectar_button.pack(pady=(10, 5))

    def get_drivers_for_dbms(self, dbms):
        """Retorna uma lista de drivers instalados para o DBMS selecionado"""
        all_drivers = pyodbc.drivers()
        keywords = self.drivers_dbms_keywords.get(dbms, [])
        drivers = [driver for driver in all_drivers if any(keyword in driver for keyword in keywords)]
        return drivers

    def verificar_permissoes_e_conectar(self):
        """Conecta ao DBMS, verifica permissões e exibe as tabelas"""
        dbms = self.dbms_menu.get()
        servidor = self.entry_servidor.get()
        self.servidor = self.entry_servidor.get()
        porta = self.entry_porta.get()
        self.porta = self.entry_porta.get()
        banco = self.entry_banco.get()
        self.banco = self.entry_banco.get()
        usuario = self.entry_usuario.get()
        self.usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        self.senha = self.entry_senha.get()
        driver = self.driver_menu.get()
        self.driver = self.driver_menu.get()
        # Obter a string de conexão
        conn_str = self.get_connection_string(dbms, driver, servidor, banco, usuario, senha, porta)

        try:
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()

            # Verificar permissões do usuário atual
            if dbms.lower() == 'mysql':
                self.cursor.execute('SHOW GRANTS FOR CURRENT_USER')
            elif dbms.lower() == 'sql server':
                self.cursor.execute("SELECT * FROM fn_my_permissions(NULL, 'DATABASE')")
            elif dbms.lower() == 'postgresql':
                self.cursor.execute("SELECT * FROM information_schema.role_table_grants WHERE grantee = CURRENT_USER")
            elif dbms.lower() == 'oracle':
                self.cursor.execute("SELECT * FROM USER_SYS_PRIVS WHERE USERNAME = USER")

            permissions = self.cursor.fetchall()
            print(permissions)
            has_insert_permission = self.has_insert_permission(dbms, permissions)

            if has_insert_permission:
                # Obter as tabelas disponíveis no banco de dados
                tables = self.get_tables(self.cursor)

                # Exibir as tabelas para o usuário selecionar
                self.show_tables_window(tables)
            else:
                messagebox.showerror("Erro de permissão", "Usuário não tem permissão de INSERT")
                self.conn.close()
                self.conn = None

        except pyodbc.Error as e:
            messagebox.showerror("Erro de conexão", f"Erro ao conectar ou consultar: {e}")
            if self.conn:
                self.conn.close()
                self.conn = None

    def get_connection_string(self, dbms, driver, servidor, banco, usuario, senha, porta):
        """Monta a string de conexão conforme o DBMS e parâmetros fornecidos"""
        if dbms == 'MySQL':
            return f'DRIVER={{{driver}}};SERVER={servidor};PORT={porta};DATABASE={banco};UID={usuario};PWD={senha};'
        elif dbms == 'SQL Server':
            return f'DRIVER={{{driver}}};SERVER={servidor};DATABASE={banco};UID={usuario};PWD={senha};'
        elif dbms == 'PostgreSQL':
            return f'DRIVER={{{driver}}};SERVER={servidor};PORT={porta};DATABASE={banco};UID={usuario};PWD={senha};'
        elif dbms == 'Oracle':
            return f'DRIVER={{{driver}}};DBQ={servidor};UID={usuario};PWD={senha};'
        else:
            raise ValueError("DBMS não suportado. Escolha entre MySQL, SQL Server, PostgreSQL ou Oracle.")

    def has_insert_permission(self, dbms, permissions):
        """Verifica se o usuário tem a permissão de INSERT"""
        if dbms == 'MySQL':
            for row in permissions:
                grant_statement = row[0].upper()
                if 'INSERT' in grant_statement or 'ALL PRIVILEGES' in grant_statement:
                    return True
            return False
        elif dbms == 'SQL Server':
            return any('INSERT' in row[1].upper() or 'ALTER' in row[1].upper() or 'ALL' in row[1].upper() for row in permissions)
        elif dbms == 'PostgreSQL':
            return any('INSERT' in row[5].upper() or 'ALL' in row[5].upper() for row in permissions)
        elif dbms == 'Oracle':
            return any('INSERT' in row[1].upper() or 'ALL PRIVILEGES' in row[1].upper() for row in permissions)
        return False


    def get_tables(self, cursor):
        """Retorna uma lista de tabelas disponíveis no banco de dados"""
        tables = []
        for row in cursor.tables():
            if row.table_type == 'TABLE':
                tables.append(row.table_name)
        return tables

    def show_tables_window(self, tables):
        """Exibe uma janela para o usuário selecionar uma tabela"""
        self.conexao_content.pack_forget()

        label = CTkLabel(self.left_frame.contain_frame, text="Selecione uma tabela:")
        label.pack(pady=10)

        # OptionMenu para mostrar as tabelas
        self.table_var = StringVar()
        self.tables_combobox = CTkOptionMenu(self.left_frame.contain_frame, values=tables, fg_color=('gray'))
        self.tables_combobox.pack(pady=10)

        # Botão para confirmar seleção
        select_button = CTkButton(self.left_frame.contain_frame, text="Selecionar", command=self.select_table, fg_color=('green'))
        select_button.pack(pady=10)


    def select_table(self):
        """Obtém as colunas da tabela selecionada e as armazena"""
        selected_table = self.tables_combobox.get()
        if selected_table:
            # Buscar as colunas da tabela selecionada
            columns = []
            for row in self.cursor.columns(table=selected_table):
                columns.append(row.column_name)
            # Armazenar as colunas
            self.table_columns = columns
            self.selected_table_name = selected_table
            self.tabela = selected_table
            # Fechar a janela de seleção de tabela
            # Fechar a conexão
            # Exibir mensagem com as colunas obtidas
            messagebox.showinfo("Colunas obtidas", f"Colunas da tabela '{selected_table}':\n{', '.join(columns)}")
            self.limpar_frame(self.left_frame.contain_frame)
            self.conected_window(self.conn)
            # Verificar se a planilha já foi carregada
        else:
            messagebox.showwarning("Nenhuma tabela selecionada", "Por favor, selecione uma tabela.")

    def conected_window(self, conn):
        if conn:
             # Título da conexão
            conexao_label = CTkLabel(self.left_frame.contain_frame, text="Status da conexão", font=("Arial", 16, "bold"))
            conexao_label.pack(pady=(10, 20))  # Espaçamento superior maior

        # Informações de conexão
            servidor_label = CTkLabel(self.left_frame.contain_frame, text="Endereço / Servidor: " + self.servidor, anchor="w")
            servidor_label.pack(fill="x", padx=10, pady=5)

            usuario_label = CTkLabel(self.left_frame.contain_frame, text="Usuário: " + self.usuario, anchor="w")
            usuario_label.pack(fill="x", padx=10, pady=5)

            banco_label = CTkLabel(self.left_frame.contain_frame, text="Banco: " + self.banco, anchor="w")
            banco_label.pack(fill="x", padx=10, pady=5)

            tabela_label = CTkLabel(self.left_frame.contain_frame, text="Tabela: " + self.tabela, anchor="w")
            tabela_label.pack(fill="x", padx=10, pady=5)

            # Botão de desconexão
            desconectar_button = CTkButton(self.left_frame.contain_frame, text="Desconectar", command=self.desconectar, fg_color="red", text_color="white")
            desconectar_button.pack(pady=(20, 10), ipadx=20, ipady=5)

    def desconectar(self):

        if self.conn:
            self.conn.close()
            self.conn = None
        self.limpar_frame(self.left_frame.contain_frame)
        self.show_conexao()

    def limpar_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def carregar_arquivos(self):
        """Função para carregar arquivos ao clicar no botão"""
        caminho_planilha = filedialog.askopenfilename(title="Selecione a planilha Excel", filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")])
        if caminho_planilha:
            try:
                # Lendo todas as abas do arquivo Excel sem formatação
                self.planilha = os.path.basename(caminho_planilha)
                self.todas_as_abas = pd.read_excel(caminho_planilha, sheet_name=None, dtype=str)
                # Armazenando os dados de cada coluna em arrays separados dentro de um dicionário
                self.dados_por_coluna = {}
                for nome_aba, df_aba in self.todas_as_abas.items():
                    # Removendo espaços extras dos nomes das colunas
                    df_aba.columns = df_aba.columns.str.strip()
                    self.dados_por_coluna[nome_aba] = {coluna: df_aba[coluna].tolist() for coluna in df_aba.columns}
                # Exibir as abas disponíveis para o usuário selecionar
                self.show_sheets_window(list(self.dados_por_coluna.keys()))
            except Exception as e:
                messagebox.showerror("Erro ao ler o arquivo", f"Ocorreu um erro ao ler a planilha:\n{e}")
        else:
            messagebox.showwarning("Nenhum arquivo selecionado", "Por favor, selecione um arquivo.")

    def show_sheets_window(self, sheet_names):
        """Exibe uma janela para o usuário selecionar uma aba (sheet)"""
        self.limpar_frame(self.right_frame)
        label = CTkLabel(self.right_frame, text="Selecione uma aba:")
        label.pack(pady=10)

        # OptionMenu para mostrar as abas
        self.sheet_var = StringVar()
        self.sheets_combobox = CTkOptionMenu(self.right_frame, values=sheet_names, fg_color=('gray'))
        self.sheets_combobox.pack(pady=10)

        # Botão para confirmar seleção
        select_button = CTkButton(self.right_frame, text="Selecionar", command=self.select_sheet, fg_color=('green'))
        select_button.pack(pady=10)

    def select_sheet(self):
        """Armazena os dados da aba selecionada"""
        selected_sheet = self.sheets_combobox.get()
        if selected_sheet:
            # Armazenar os dados da aba selecionada
            self.dados_aba_especifica = self.dados_por_coluna[selected_sheet]
            # Fechar a janela de seleção de aba
            # Exibir mensagem com as colunas obtidas
            colunas = list(self.dados_aba_especifica.keys())
            messagebox.showinfo("Aba selecionada", f"Aba '{selected_sheet}' selecionada com sucesso!\nColunas disponíveis:\n{', '.join(colunas)}")
            self.planilha_window()
            # Verificar se a tabela já foi selecionada
            # if self.table_columns:
            #     self.correlate_columns()
        else:
            messagebox.showwarning("Nenhuma aba selecionada", "Por favor, selecione uma aba.")

    def planilha_window(self):
        self.limpar_frame(self.right_frame)

        # Crie um CTkLabel dentro de self.right_frame e atribua a imagem
        self.label_imagem = CTkLabel(self.right_frame, text=self.planilha)
        self.label_imagem.pack(pady=10)
        self.right_frame.bottom_frame = CTkFrame(self.right_frame, height=50, fg_color=("transparent"))
        self.right_frame.bottom_frame.pack(side="bottom", fill="x", pady="50")

        self.avancar_button = CTkButton(self.right_frame.bottom_frame, text="Avançar", fg_color="green", command= self.correlate_columns)
        self.avancar_button.pack(side="right")
        self.avancar_button = CTkButton(self.right_frame.bottom_frame, text="Cancelar", fg_color="red", command= self.drop_planilha)
        self.avancar_button.pack(side="left")

    def drop_planilha(self):
        self.planilha = None
        self.right_frame.destroy()
        self.create_initial_window()

    def correlate_columns(self):
        """Abre uma janela para correlacionar os campos da planilha com os campos da tabela"""
        if not self.table_columns:
            messagebox.showwarning("Sem colunas", "Nenhuma coluna foi encontrada na tabela selecionada.")
            return
        if not self.dados_aba_especifica:
            messagebox.showwarning("Sem dados", "Nenhuma aba de planilha foi selecionada ou não contém dados.")
            return


        # Variáveis para a lógica de correlação
        self.counter = 1
        self.selected_first_button = None  # Armazena o botão da primeira coluna selecionado

        # Dicionários para armazenar valores e atributos
        self.first_column_values = {}  # Campos da planilha Excel
        self.second_column_values = {}  # Campos da tabela do banco de dados
        self.first_button_attributes = {}
        self.second_button_attributes = {}
        self.correlations = {}  # chave: número do atributo, valor: (id_botão_primeira_coluna, id_botão_segunda_coluna)
        self.limpar_frame(self.right_frame)
        # Frames para as colunas
        first_column_frame = CTkFrame(self.right_frame, fg_color=("transparent"))
        first_column_frame.pack(side="left", fill="both", expand=True)

        planilha_title = CTkLabel(first_column_frame, text=self.planilha)
        planilha_title.pack()

        second_column_frame = CTkFrame(self.right_frame, fg_color=("transparent"))
        second_column_frame.pack(side="left", fill="both", expand=True)

        tabela_title = CTkLabel(second_column_frame, text=self.tabela)
        tabela_title.pack()

        # Cria os botões da primeira coluna (planilha Excel)
        self.first_buttons = {}
        for idx, column_name in enumerate(self.dados_aba_especifica.keys()):
            btn_id = idx + 1
            self.first_column_values[btn_id] = column_name
            self.first_button_attributes[btn_id] = None  # Inicializa o atributo como None
            btn = CTkButton(first_column_frame, text=column_name, width=150)
            btn.configure(command=lambda b=btn, idx=btn_id: self.first_button_click(b, idx), fg_color=('gray'))
            btn.pack(padx=5, pady=5)
            self.first_buttons[btn_id] = btn

        # Cria os botões da segunda coluna (tabela do banco de dados)
        self.second_buttons = {}
        for idx, column_name in enumerate(self.table_columns):
            btn_id = idx + 1
            self.second_column_values[btn_id] = column_name
            self.second_button_attributes[btn_id] = None  # Inicializa o atributo como None
            btn = CTkButton(second_column_frame, text=column_name, width=150, fg_color=('gray'))
            btn.configure(command=lambda b=btn, idx=btn_id: self.second_button_click(b, idx))
            btn.pack(padx=5, pady=5)
            self.second_buttons[btn_id] = btn

        # Botão para finalizar a correlação
        self.right_frame.bottom_frame = CTkFrame(self.right_frame, height=50, fg_color=("transparent"))
        self.right_frame.bottom_frame.pack(side="bottom", fill="x")

        finish_button = CTkButton(self.right_frame.bottom_frame, text="Finalizar", command=self.finish_correlation, fg_color=('green'))
        finish_button.pack(side="right", pady="50")

    def first_button_click(self, button, btn_id):
        current_attr = self.first_button_attributes.get(btn_id, None)
        if current_attr:
            # O botão já tem um atributo, remove-o
            button.configure(text=self.first_column_values[btn_id], fg_color=('gray'))
            self.first_button_attributes[btn_id] = None

            # Decrementa o contador se o atributo removido for igual ao contador - 1
            if current_attr == self.counter - 1:
                self.counter -= 1

            # Remove todas as correlações associadas
            attrs_to_remove = []
            for attr_num, (first_id, second_id) in self.correlations.items():
                if first_id == btn_id:
                    # Remove atributo do botão da segunda coluna
                    second_button = self.second_buttons[second_id]
                    second_button.configure(text=self.second_column_values[second_id], fg_color=('gray'))
                    self.second_button_attributes[second_id] = None
                    attrs_to_remove.append(attr_num)
            # Remove as correlações
            for attr_num in attrs_to_remove:
                del self.correlations[attr_num]
        else:
            # Atribui o valor atual do contador ao botão da primeira coluna
            button.configure(text=f"{self.first_column_values[btn_id]} ({self.counter})", fg_color=('green'))
            self.first_button_attributes[btn_id] = self.counter
            self.selected_first_button = (button, btn_id)
            self.counter += 1

    def second_button_click(self, button, btn_id):
        current_attr = self.second_button_attributes.get(btn_id, None)
        if current_attr:
            # O botão já tem um atributo, remove-o
            button.configure(text=self.second_column_values[btn_id])
            self.second_button_attributes[btn_id] = None

            # Remove a correlação, se existir
            if current_attr in self.correlations:
                first_id = self.correlations[current_attr][0]
                # Não remove o atributo do botão da primeira coluna
                # Apenas remove a correlação
                del self.correlations[current_attr]
        else:
            # Verifica se há um botão da primeira coluna selecionado
            if self.selected_first_button is not None:
                first_button, first_id = self.selected_first_button
                first_attr = self.first_button_attributes.get(first_id, None)

                # Atribui o atributo do botão da primeira coluna ao botão da segunda coluna
                button.configure(text=f"{self.second_column_values[btn_id]} ({first_attr})", fg_color=('green'))
                self.second_button_attributes[btn_id] = first_attr

                # Registra a correlação
                self.correlations[first_attr] = (first_id, btn_id)

                # Reseta a seleção
                self.selected_first_button = None

            else:
                # Verifica se há um botão da primeira coluna com atributo e sem correlação
                uncorrelated_first_buttons = [id for id, attr in self.first_button_attributes.items()
                                              if attr is not None and attr not in self.correlations]
                if len(uncorrelated_first_buttons) == 1:
                    # Usa o botão da primeira coluna não correlacionado
                    first_id = uncorrelated_first_buttons[0]
                    first_button = self.first_buttons[first_id]
                    first_attr = self.first_button_attributes[first_id]

                    # Atribui o atributo ao botão da segunda coluna
                    button.configure(text=f"{self.second_column_values[btn_id]} ({first_attr})",fg_color=('gray'))
                    self.second_button_attributes[btn_id] = first_attr

                    # Registra a correlação
                    self.correlations[first_attr] = (first_id, btn_id)

    def finish_correlation(self):
        """Processa as correlações e insere os dados no banco de dados"""
        self.column_mappings = {}  # Dicionário para armazenar os mapeamentos
        for attr_num, (first_id, second_id) in self.correlations.items():
            excel_column = self.first_column_values[first_id]
            db_column = self.second_column_values[second_id]
            self.column_mappings[excel_column] = db_column
        # Fecha a janela de correlação
        self.drop_planilha()
        # Prosseguir para inserir os dados no banco de dados
        self.insert_data_into_db()

    def insert_data_into_db(self):
        """Insere os dados da planilha no banco de dados usando os mapeamentos"""
        # Abre uma nova conexão ao banco de dados
        dbms = self.dbms_menu.get()
        servidor = self.servidor
        porta = self.porta
        banco = self.banco
        usuario = self.usuario
        senha = self.senha
        driver = self.driver

        # Obter a string de conexão
        conn_str = self.get_connection_string(dbms, driver, servidor, banco, usuario, senha, porta)

        try:
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()

            # Inserir dados no banco de dados usando os mapeamentos
            # Obter a lista de colunas do Excel que têm mapeamentos
            excel_columns = list(self.column_mappings.keys())

            try:
                num_rows = len(self.dados_aba_especifica[excel_columns[0]])

                # Construir a lista de linhas a serem inseridas
                rows_to_insert = []
                for i in range(num_rows):
                    row = {}
                    for excel_col in excel_columns:
                        db_col = self.column_mappings[excel_col]
                        value = self.dados_aba_especifica[excel_col][i]
                        row[db_col] = value
                    rows_to_insert.append(row)

                # Inserir as linhas no banco de dados
                table_name = self.selected_table_name  # Nome da tabela selecionada
                for row in rows_to_insert:
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join(['?' for _ in row])
                    values = list(row.values())
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    self.cursor.execute(query, values)

                self.conn.commit()
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
            except:
                messagebox.showinfo("Erro", "Correlacione ao menos um campo!")
        except pyodbc.Error as e:
            messagebox.showerror("Erro de conexão", f"Erro ao conectar ou inserir dados: {e}")
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

if __name__ == "__main__":
    app = Principal()
    app.mainloop()