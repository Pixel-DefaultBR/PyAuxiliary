#!/usr/bin/env python3
"""
SOC Log Sanitizer - Interface Gráfica
======================================
Interface gráfica para sanitização de informações sensíveis em textos e logs.

Recursos:
- Checkboxes para selecionar quais dados sanitizar
- Campo para adicionar nomes de clientes personalizados
- Suporte para qualquer tipo de texto
- Botão para copiar resultado para área de transferência
- Opções avançadas (hash, preservar estrutura, etc)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import re
from typing import List, Set
from sanitize_soc_logs import SOCLogSanitizer


class SanitizerGUI:
    """Interface gráfica para o sanitizador de logs."""

    def __init__(self, root):
        self.root = root
        self.root.title("SOC Log Sanitizer - Interface Gráfica 🔒")
        self.root.geometry("1200x800")

        # Variáveis de controle
        self.sanitize_email = tk.BooleanVar(value=True)
        self.sanitize_ipv4 = tk.BooleanVar(value=True)
        self.sanitize_ipv6 = tk.BooleanVar(value=True)
        self.sanitize_domain = tk.BooleanVar(value=True)
        self.sanitize_username = tk.BooleanVar(value=True)
        self.sanitize_client = tk.BooleanVar(value=True)
        self.sanitize_custom_clients = tk.BooleanVar(value=True)

        self.use_hash = tk.BooleanVar(value=False)
        self.preserve_structure = tk.BooleanVar(value=True)

        self.custom_clients_list: List[str] = []

        self.setup_ui()

    def setup_ui(self):
        """Configura a interface gráfica."""
        # Configurar grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ===== FRAME SUPERIOR: Título e Instruções =====
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        title_label = ttk.Label(
            header_frame,
            text="🔒 SOC Log Sanitizer - Remova Informações Sensíveis",
            font=("Arial", 16, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Sanitize emails, IPs, domínios, nomes de usuários e clientes em qualquer texto",
            font=("Arial", 10)
        )
        subtitle_label.pack()

        # ===== FRAME PRINCIPAL: Dividido em esquerda e direita =====
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)

        # ===== LADO ESQUERDO: Texto de entrada/saída =====
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_rowconfigure(2, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Texto de entrada
        input_label = ttk.Label(text_frame, text="📝 Texto Original:", font=("Arial", 11, "bold"))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.input_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=("Courier New", 10)
        )
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Botões entre entrada e saída
        buttons_frame = ttk.Frame(text_frame)
        buttons_frame.grid(row=2, column=0, pady=10)

        sanitize_btn = ttk.Button(
            buttons_frame,
            text="🔒 Sanitizar Texto",
            command=self.sanitize_text,
            style="Accent.TButton"
        )
        sanitize_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(
            buttons_frame,
            text="🗑️ Limpar Tudo",
            command=self.clear_all
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        load_file_btn = ttk.Button(
            buttons_frame,
            text="📂 Carregar Arquivo",
            command=self.load_file
        )
        load_file_btn.pack(side=tk.LEFT, padx=5)

        # Texto de saída
        output_label = ttk.Label(text_frame, text="✅ Texto Sanitizado:", font=("Arial", 11, "bold"))
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 5))

        self.output_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=("Courier New", 10),
            bg="#f0f0f0"
        )
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Botões de ação na saída
        output_buttons_frame = ttk.Frame(text_frame)
        output_buttons_frame.grid(row=5, column=0, pady=10)

        copy_btn = ttk.Button(
            output_buttons_frame,
            text="📋 Copiar para Área de Transferência",
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side=tk.LEFT, padx=5)

        save_btn = ttk.Button(
            output_buttons_frame,
            text="💾 Salvar em Arquivo",
            command=self.save_to_file
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        # ===== LADO DIREITO: Opções e Configurações =====
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Frame de checkboxes
        checkbox_frame = ttk.LabelFrame(options_frame, text="🎯 Selecione o que Sanitizar", padding="10")
        checkbox_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(
            checkbox_frame,
            text="✉️ Endereços de Email",
            variable=self.sanitize_email
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            checkbox_frame,
            text="🌐 Endereços IPv4",
            variable=self.sanitize_ipv4
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            checkbox_frame,
            text="🌐 Endereços IPv6",
            variable=self.sanitize_ipv6
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            checkbox_frame,
            text="🔗 Domínios",
            variable=self.sanitize_domain
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            checkbox_frame,
            text="👤 Nomes de Usuários",
            variable=self.sanitize_username
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            checkbox_frame,
            text="🏢 Nomes de Clientes (padrão)",
            variable=self.sanitize_client
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            checkbox_frame,
            text="📝 Nomes de Clientes (customizados)",
            variable=self.sanitize_custom_clients
        ).pack(anchor=tk.W, pady=2)

        # Atalhos para selecionar/desmarcar todos
        select_buttons_frame = ttk.Frame(checkbox_frame)
        select_buttons_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            select_buttons_frame,
            text="✓ Todos",
            command=self.select_all,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            select_buttons_frame,
            text="✗ Nenhum",
            command=self.deselect_all,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        # Frame de clientes customizados
        custom_clients_frame = ttk.LabelFrame(
            options_frame,
            text="📋 Clientes/Termos Personalizados",
            padding="10"
        )
        custom_clients_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Label(
            custom_clients_frame,
            text="Adicione nomes específicos para remover:",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))

        # Campo de entrada para novo cliente
        entry_frame = ttk.Frame(custom_clients_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        self.client_entry = ttk.Entry(entry_frame)
        self.client_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.client_entry.bind('<Return>', lambda e: self.add_custom_client())

        ttk.Button(
            entry_frame,
            text="➕ Adicionar",
            command=self.add_custom_client,
            width=10
        ).pack(side=tk.LEFT)

        # Lista de clientes customizados
        ttk.Label(
            custom_clients_frame,
            text="Nomes na lista:",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(10, 5))

        list_frame = ttk.Frame(custom_clients_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.clients_listbox = tk.Listbox(
            list_frame,
            height=8,
            yscrollcommand=scrollbar.set,
            font=("Arial", 9)
        )
        self.clients_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.clients_listbox.yview)

        ttk.Button(
            custom_clients_frame,
            text="🗑️ Remover Selecionado",
            command=self.remove_custom_client
        ).pack(pady=(5, 0))

        # Frame de opções avançadas
        advanced_frame = ttk.LabelFrame(options_frame, text="⚙️ Opções Avançadas", padding="10")
        advanced_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(
            advanced_frame,
            text="🔐 Usar Hash (consistência)",
            variable=self.use_hash
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            advanced_frame,
            text="📐 Preservar Estrutura",
            variable=self.preserve_structure
        ).pack(anchor=tk.W, pady=2)

        # Frame de estatísticas
        stats_frame = ttk.LabelFrame(options_frame, text="📊 Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)

        self.stats_label = ttk.Label(
            stats_frame,
            text="Nenhuma sanitização realizada ainda.",
            font=("Arial", 9),
            wraplength=250,
            justify=tk.LEFT
        )
        self.stats_label.pack(anchor=tk.W)

        # Texto de exemplo na entrada
        self.input_text.insert("1.0", """Cole aqui o texto que deseja sanitizar...

Exemplo:
[2024-01-15 10:30] User: john.doe@company.com from 192.168.1.100
[2024-01-15 10:31] Client: ACME Corporation accessed api.server.com
[2024-01-15 10:32] Username: admin logged in
[2024-01-15 10:33] Email sent to support@example.com from fe80::1
""")

    def select_all(self):
        """Seleciona todos os checkboxes."""
        self.sanitize_email.set(True)
        self.sanitize_ipv4.set(True)
        self.sanitize_ipv6.set(True)
        self.sanitize_domain.set(True)
        self.sanitize_username.set(True)
        self.sanitize_client.set(True)
        self.sanitize_custom_clients.set(True)

    def deselect_all(self):
        """Desmarca todos os checkboxes."""
        self.sanitize_email.set(False)
        self.sanitize_ipv4.set(False)
        self.sanitize_ipv6.set(False)
        self.sanitize_domain.set(False)
        self.sanitize_username.set(False)
        self.sanitize_client.set(False)
        self.sanitize_custom_clients.set(False)

    def add_custom_client(self):
        """Adiciona um cliente customizado à lista."""
        client_name = self.client_entry.get().strip()
        if client_name and client_name not in self.custom_clients_list:
            self.custom_clients_list.append(client_name)
            self.clients_listbox.insert(tk.END, client_name)
            self.client_entry.delete(0, tk.END)
        elif client_name in self.custom_clients_list:
            messagebox.showinfo("Info", "Este nome já está na lista!")

    def remove_custom_client(self):
        """Remove o cliente selecionado da lista."""
        selection = self.clients_listbox.curselection()
        if selection:
            index = selection[0]
            client_name = self.clients_listbox.get(index)
            self.clients_listbox.delete(index)
            self.custom_clients_list.remove(client_name)

    def sanitize_custom_clients_in_text(self, text: str) -> str:
        """Sanitiza nomes de clientes customizados."""
        if not self.custom_clients_list:
            return text

        sanitized_text = text
        for i, client_name in enumerate(self.custom_clients_list, 1):
            # Escape caracteres especiais de regex
            escaped_name = re.escape(client_name)
            # Substituir de forma case-insensitive
            pattern = re.compile(escaped_name, re.IGNORECASE)
            replacement = f"[CUSTOM_CLIENT_{i}]"
            sanitized_text = pattern.sub(replacement, sanitized_text)

        return sanitized_text

    def sanitize_text(self):
        """Sanitiza o texto de acordo com as opções selecionadas."""
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Aviso", "Por favor, insira algum texto para sanitizar!")
            return

        # Verificar se pelo menos uma opção está selecionada
        if not any([
            self.sanitize_email.get(),
            self.sanitize_ipv4.get(),
            self.sanitize_ipv6.get(),
            self.sanitize_domain.get(),
            self.sanitize_username.get(),
            self.sanitize_client.get(),
            self.sanitize_custom_clients.get()
        ]):
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecione pelo menos uma opção de sanitização!"
            )
            return

        # Criar sanitizador
        sanitizer = SOCLogSanitizer(
            use_hash=self.use_hash.get(),
            preserve_structure=self.preserve_structure.get()
        )

        sanitized_text = input_text

        # Aplicar sanitizações selecionadas
        if self.sanitize_email.get():
            sanitized_text = sanitizer.sanitize_email(sanitized_text)

        if self.sanitize_ipv4.get():
            sanitized_text = sanitizer.sanitize_ipv4(sanitized_text)

        if self.sanitize_ipv6.get():
            sanitized_text = sanitizer.sanitize_ipv6(sanitized_text)

        if self.sanitize_username.get():
            sanitized_text = sanitizer.sanitize_username(sanitized_text)

        if self.sanitize_client.get():
            sanitized_text = sanitizer.sanitize_client_name(sanitized_text)

        if self.sanitize_domain.get():
            sanitized_text = sanitizer.sanitize_domain(sanitized_text)

        # Sanitizar clientes customizados por último
        if self.sanitize_custom_clients.get():
            sanitized_text = self.sanitize_custom_clients_in_text(sanitized_text)

        # Exibir resultado
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", sanitized_text)

        # Atualizar estatísticas
        stats = sanitizer.get_statistics()
        stats_text = "Itens sanitizados:\n"
        total = 0
        for data_type, count in stats.items():
            if count > 0:
                stats_text += f"• {data_type}: {count}\n"
                total += count

        if self.sanitize_custom_clients.get() and self.custom_clients_list:
            custom_count = len(re.findall(
                r'\[CUSTOM_CLIENT_\d+\]',
                sanitized_text
            ))
            if custom_count > 0:
                stats_text += f"• custom_clients: {custom_count}\n"
                total += custom_count

        stats_text += f"\nTotal: {total} itens"

        self.stats_label.config(text=stats_text)

        messagebox.showinfo("Sucesso", "Texto sanitizado com sucesso!")

    def copy_to_clipboard(self):
        """Copia o texto sanitizado para a área de transferência."""
        output_text = self.output_text.get("1.0", tk.END).strip()

        if not output_text:
            messagebox.showwarning("Aviso", "Não há texto sanitizado para copiar!")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        self.root.update()

        messagebox.showinfo("Sucesso", "Texto copiado para a área de transferência!")

    def clear_all(self):
        """Limpa todos os campos."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.stats_label.config(text="Nenhuma sanitização realizada ainda.")

    def load_file(self):
        """Carrega um arquivo para sanitização."""
        filename = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[
                ("Arquivos de Texto", "*.txt"),
                ("Arquivos de Log", "*.log"),
                ("Todos os Arquivos", "*.*")
            ]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                messagebox.showinfo("Sucesso", f"Arquivo carregado: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}")

    def save_to_file(self):
        """Salva o texto sanitizado em um arquivo."""
        output_text = self.output_text.get("1.0", tk.END).strip()

        if not output_text:
            messagebox.showwarning("Aviso", "Não há texto sanitizado para salvar!")
            return

        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo sanitizado",
            defaultextension=".txt",
            filetypes=[
                ("Arquivos de Texto", "*.txt"),
                ("Arquivos de Log", "*.log"),
                ("Todos os Arquivos", "*.*")
            ]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                messagebox.showinfo("Sucesso", f"Arquivo salvo: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")


def main():
    """Função principal."""
    root = tk.Tk()

    # Tentar aplicar estilo moderno (se disponível)
    try:
        style = ttk.Style()
        style.theme_use('clam')  # Pode usar 'vista', 'xpnative', 'clam', etc
    except:
        pass

    app = SanitizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
