# linkedin.com/in/viniciusrodmusic/

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
# from faker import Faker

# faker = Faker()

colors = {
    "bg": "#C6DEEF", 
    "input_bg": "#AECBE0", 
    "gray": "#5E708B", 
    "darkgray": "#2A3B55",
    "red": "#F25E65", 
    "darkred": "#930D0D",
    "yellow": "#f2c772"
}

fonte_padrao, fonte_padrao_menor = (("Bahnschrift SemiBold", 25), ("Bahnschrift SemiBold", 15))

class myFunctions:

    @staticmethod
    def clear_inputs(name_stringvar, preco_stringvar, quant_stringvar):
        name_stringvar.set("")
        preco_stringvar.set("")
        quant_stringvar.set("")




    @staticmethod
    def cancel(submit_btn, update_btn, del_btn, cancel_edit_btn, name_stringvar, preco_stringvar, quant_stringvar):
        # Se o usuário desistir de editar um produto
        update_btn.grid_forget()
        cancel_edit_btn.grid_forget()

        submit_btn.grid(column=2, row=0, sticky="s", pady=(0, 20))
        del_btn.grid(column=0, row=0, sticky="s", pady=(0, 20))  

        # limpando entries
        myFunctions.clear_inputs(name_stringvar, preco_stringvar, quant_stringvar)




    @staticmethod
    def onDoubleClick(event, name_stringvar, preco_stringvar, quant_stringvar, treeview, submit_btn, update_btn, del_btn, cancel_edit_btn):
        """
        ESSA FUNÇÃO COLOCA OS VALORES DO ITEM SELECIONADO 
        DE VOLTA NO INPUT, PARA SER EDITADO
        """
        # Pegando a seleção
        item_selection = treeview.focus() 
        # retorna um array com os valores da linha: [id, nome, preco, quantidade]
        [id, nome, preco, quantidade] = treeview.item(item_selection)["values"]

        answer = messagebox.askyesno("Confirmação", f'Você quer editar o item "{nome}" ?')
        if answer == 1:
            # removendo botão de salvar e excluir
            submit_btn.grid_forget()
            del_btn.grid_forget()

            # atualizando as entries com valor do item selecionado
            name_stringvar.set(nome)
            preco_stringvar.set(preco)
            quant_stringvar.set(quantidade)

            # colocando um botão novo de atualizar
            update_btn.grid(column=2, row=0, sticky="s", pady=(0, 20))
            cancel_edit_btn.grid(column=0, row=0, sticky="s", pady=(0, 20))
        else:
            return
    

    # FUNÇÕES DE LOG
    @staticmethod
    def create_log(nome, quantidade):
        now = datetime.now()
        now = now.strftime("[%d/%m/%Y %H:%M:%S]")
        with open ("log_estoque.txt", "a", encoding="utf-8") as f:
            f.write(f'{now} INSERÇÃO - Produto "{nome}" (Qtd: {quantidade}) cadastrado com sucesso.\n')

    @staticmethod
    def update_log(nome_antigo, nome, preco, quantidade):
        now = datetime.now()
        now = now.strftime("[%d/%m/%Y %H:%M:%S]")
        with open ("log_estoque.txt", "a", encoding="utf-8") as f:
            f.write(f'{now} ATUALIZAÇÃO - Produto "{nome_antigo}" alterado para "{nome}" (Nova Qtd: {quantidade}, Novo Preço: {preco}).\n')
            
    @staticmethod
    def delete_log(nome):
        now = datetime.now()
        now = now.strftime("[%d/%m/%Y %H:%M:%S]")
        with open ("log_estoque.txt", "a", encoding="utf-8") as f:
            f.write(f'{now} EXCLUSÃO - Produto "{nome}" removido do sistema.\n')
        



class myDatabase:
    def __init__(self, db_name):
        self.create_table_sql = """
        CREATE TABLE IF NOT EXISTS estoque(
        id INTEGER PRIMARY KEY,
        nome_produto TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
        )
        """

        self.select_all_sql = """
        SELECT * FROM estoque;
        """

        self.insert_sql = """
        INSERT INTO estoque(nome_produto, preco, quantidade) VALUES (?, ?, ?);
        """
        self.update_sql = """
        UPDATE estoque SET nome_produto = ?, preco = ?, quantidade = ? WHERE id = ?;
        """

        # Conexão
        self.conn = sqlite3.connect(db_name)




    # Create table
    def create_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.create_table_sql)
            self.conn.commit()
        except sqlite3.Error as er:
            messagebox.showerror("ALGO DEU ERRADO", er)
        finally:
            cursor.close()
            



    # INSERT
    def insert(self, nome_entry, preco_entry, quant_entry, treeview, name_stringvar, preco_stringvar, quant_stringvar):

        # Validando se todos os campos estão preenchidos
        if not nome_entry.get() or not preco_entry.get() or not quant_entry.get():
            messagebox.showinfo("Informação", "Preencha todos os campos")
            return

        # Fazendo as conversões dos valores
        try:
            nome = nome_entry.get().strip()
            preco = float(preco_entry.get())
            quantidade = float(quant_entry.get())
        except ValueError:
            messagebox.showerror("ERRO", "Você só poderá incluir número nos campos 'preço' e 'quantidade'")
            return
        except Exception as er:
            print(er)

        cursor = self.conn.cursor()

        try:
            cursor.execute(self.insert_sql, (nome, preco, quantidade))
            self.conn.commit()
            myFunctions.create_log(nome, quantidade)

        except sqlite3.Error as er:
            messagebox.showerror("ALGO DEU ERRADO", er)
        finally:
            cursor.close()

            # Atualizando a treeview
            self.read(treeview)
            # Limpando inputs
            myFunctions.clear_inputs(name_stringvar, preco_stringvar, quant_stringvar)




    # READ
    def read(self, treeview):
        cursor = self.conn.cursor()
        # Limpando a treeview
        for item in treeview.get_children():
            treeview.delete(item)

        query = cursor.execute("SELECT * FROM estoque")
        for row in query:
            treeview.insert("", "end", text=f"p{id}", values=row)




    # UPDATE
    def update(self, treeview, submit_btn, update_btn, del_btn, cancel_edit_btn, nome_entry, preco_entry, quant_entry, name_stringvar, preco_stringvar, quant_stringvar):
         # Validando se todos os campos estão preenchidos
        if not nome_entry.get() or not preco_entry.get() or not quant_entry.get():
            messagebox.showinfo("Informação", "Preencha todos os campos")
            return
        
        # Capturando valores das entries para edição
        try:
            nome = nome_entry.get().strip()
            preco = float(preco_entry.get())
            quantidade = float(quant_entry.get())
        except ValueError:
            messagebox.showerror("ERRO", "Você só poderá incluir número nos campos 'preço' e 'quantidade'")
            return
        except Exception as er:
            print(er)
        cursor = self.conn.cursor()
        item_selection = treeview.focus() 
        # retorna um array com os valores da linha: [id, nome, preco, quantidade]
        [id, nome_antigo, *rest] = treeview.item(item_selection)["values"]
        
        try:
            cursor.execute(self.update_sql, (nome, preco, quantidade, id))
            self.conn.commit()
            myFunctions.update_log(nome_antigo, nome, preco, quantidade)
            # Atualizando a treeview
            self.read(treeview)
        except sqlite3.Error as er:
            messagebox.showerror("ALGO DEU ERRADO", er)
        finally:
            cursor.close()
            # removendo botão de editar e cancelar
            myFunctions.cancel(submit_btn, update_btn, del_btn, cancel_edit_btn, name_stringvar, preco_stringvar, quant_stringvar)




    # Delete
    def delete(self, treeview):
        # Pegando a seleção
        item_selection = treeview.focus() 
        if not item_selection:
            return

        # retorna um array com os valores da linha: [id, nome, preco, quantidade]
        [id, nome, *rest] = treeview.item(item_selection)["values"] 


        answer = messagebox.askokcancel("Confirmação", f"Você tem certeza que deseja apagar o item {nome} permanentemente?")

        if answer == 1:
            cursor = self.conn.cursor()

            try:
                cursor.execute("DELETE FROM estoque WHERE id = ?", (id,))
                self.conn.commit()
                myFunctions.delete_log(nome)
                # Atualizando a treeview
                self.read(treeview)
            except sqlite3.Error as er:
                messagebox.showerror("ALGO DEU ERRADO", er)      
            finally:
                cursor.close()
        else:
            return
            









class Widgets:
    # Meus widgets personalizados
    @staticmethod
    def my_input(master, label_text, input_color):
        container = tk.Frame(master, bg=colors["bg"]) # Abriga a label e a entry
        
        string_var = tk.StringVar()
        label = tk.Label(container, text=label_text, font=fonte_padrao_menor, bg=colors["bg"])
        entry = tk.Entry(container, bg=input_color, relief="flat", width=100, textvariable=string_var)
        label.pack()
        entry.pack()
        return (container, entry, string_var)
    
    @staticmethod
    def my_btn(master, btn_text, bg_color, func = None):
        text_color = colors["darkred"] if bg_color == colors["red"] else colors["darkgray"] # Se fundo do btn for vermelho o texto será vermelho escuro
        btn = tk.Button(master, text=btn_text, bg=bg_color, font=fonte_padrao_menor, fg=text_color, activebackground=text_color, relief="ridge", command=func)
        return btn    










class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VINÍCIUS ROD - GESTÃO DE ESTOQUE")
        self.resizable(False, False)
        self.config(bg=colors["bg"])
        # Centralizando janela
        self.screen_w = self.winfo_screenwidth() # largura da tela
        self.screen_h = self.winfo_screenheight() # altura da tela
        x = (self.screen_w / 2) - (400)
        y = (self.screen_h  / 2) - (300) 
        self.geometry(f"800x600+{int(x)}+{int(y)}")
        # GRID
        self.grid_columnconfigure((0,1,2), weight=1, uniform="A")
        self.grid_rowconfigure((0,1), weight=1, uniform="A")

        # INICIALIZANDO BANCO DE DADOS
        self.db = myDatabase("estoque_produtos.db")
        self.db.create_table()

        # WIDGETS
            # Frame de Inputs
        self.frame = tk.Frame(self, bg=colors["bg"])
        self.frame.grid(column=1, row=0, sticky="NSEW")

        self.frame_title = tk.Label(self.frame, text="Produto",bg=colors["bg"] , font=fonte_padrao)
        self.frame_title.pack(pady=20)

            # Inputs
        self.name_entry_container, self.name_entry, self.name_SV = Widgets.my_input(self.frame, "nome", input_color=colors["input_bg"])
        self.name_entry_container.pack(fill="both", expand=True)        
        
        self.preco_entry_container, self.preco_entry, self.preco_SV = Widgets.my_input(self.frame, "preço (R$)", input_color=colors["input_bg"])
        self.preco_entry_container.pack(fill="both", expand=True)        
        
        self.quant_entry_container, self.quant_entry, self.quant_SV = Widgets.my_input(self.frame, "quantidade", input_color=colors["input_bg"])
        self.quant_entry_container.pack(fill="both", expand=True)

            # Buttons
        self.del_btn = Widgets.my_btn(self, "excluir", colors["red"], func=lambda: self.db.delete(self.tree))
        self.del_btn.grid(column=0, row=0, sticky="s", pady=(0, 20))        
        
        self.submit_btn = Widgets.my_btn(
            self, "salvar", colors["gray"], 
            func=lambda: self.db.insert(
                self.name_entry, 
                self.preco_entry, 
                self.quant_entry, 
                self.tree,
                self.name_SV, 
                self.preco_SV, 
                self.quant_SV,
              
                )
        )
        self.submit_btn.grid(column=2, row=0, sticky="s", pady=(0, 20))

        self.update_btn = Widgets.my_btn(
            self, "Atualizar", colors["yellow"],
            func=lambda: self.db.update(
                self.tree, 
                self.submit_btn, 
                self.update_btn, 
                self.del_btn, 
                self.cancel_edit_btn, 
                self.name_entry, 
                self.preco_entry, 
                self.quant_entry, 
                self.name_SV, 
                self.preco_SV, 
                self.quant_SV
            )
        )

        self.cancel_edit_btn = Widgets.my_btn(
            self, "Cancelar", colors["red"],
            func=lambda: myFunctions.cancel(self.submit_btn, self.update_btn, self.del_btn, self.cancel_edit_btn, self.name_SV, self.preco_SV, self.quant_SV)
        )


        # TREEVIEW
        self.style = ttk.Style() # para estilizar
        self.style.theme_use("clam")
        self.style.configure("Treeview",
            background=colors["input_bg"],
            rowheight=40, # altura da linha
            fieldbackground=colors["input_bg"],
            font=fonte_padrao_menor
        )

        self.tree = ttk.Treeview(self, columns=("id", "nome", "preco", "quantidade"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.column("id", anchor="center", width=20)

        self.tree.heading("nome", text="Produto")
        self.tree.column("nome", anchor="center")

        self.tree.heading("preco", text="Preço (R$)")
        self.tree.column("preco", anchor="center")

        self.tree.heading("quantidade", text="Quantidade (Un)")
        self.tree.column("quantidade", anchor="center")

        self.tree.grid(column=0, columnspan=3, row=1, sticky="nsew")
            # Leitura inicial do bancco para exibir na treeview
        self.db.read(self.tree)
            # Adicionando eventos de duplo clique
        self.tree.bind("<Double-Button-1>", lambda x: myFunctions.onDoubleClick(
            x, 
            self.name_SV, 
            self.preco_SV, 
            self.quant_SV, 
            self.tree, 
            self.submit_btn, 
            self.update_btn, 
            self.del_btn,
            self.cancel_edit_btn)
        )
        







if __name__ == "__main__":
    app = App()
    app.mainloop()