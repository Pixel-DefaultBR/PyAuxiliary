#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import re
from typing import List, Set, Dict
from sanitize_soc_logs import SOCLogSanitizer


class ColorTheme:
    THEMES = {
        'Azul': {
            'bg': '#E3F2FD',
            'fg': '#0D47A1',
            'button_bg': '#2196F3',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#1976D2'
        },
        'Verde': {
            'bg': '#E8F5E9',
            'fg': '#1B5E20',
            'button_bg': '#4CAF50',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#388E3C'
        },
        'Roxo': {
            'bg': '#F3E5F5',
            'fg': '#4A148C',
            'button_bg': '#9C27B0',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#7B1FA2'
        },
        'Laranja': {
            'bg': '#FFF3E0',
            'fg': '#E65100',
            'button_bg': '#FF9800',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#F57C00'
        },
        'Vermelho': {
            'bg': '#FFEBEE',
            'fg': '#B71C1C',
            'button_bg': '#F44336',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#D32F2F'
        },
        'Ciano': {
            'bg': '#E0F7FA',
            'fg': '#006064',
            'button_bg': '#00BCD4',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#0097A7'
        },
        'Rosa': {
            'bg': '#FCE4EC',
            'fg': '#880E4F',
            'button_bg': '#E91E63',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#C2185B'
        },
        'Amarelo': {
            'bg': '#FFFDE7',
            'fg': '#F57F17',
            'button_bg': '#FFEB3B',
            'button_fg': '#000000',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#FBC02D'
        },
        'Cinza': {
            'bg': '#F5F5F5',
            'fg': '#212121',
            'button_bg': '#9E9E9E',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#616161'
        },
        'Indigo': {
            'bg': '#E8EAF6',
            'fg': '#1A237E',
            'button_bg': '#3F51B5',
            'button_fg': '#FFFFFF',
            'text_bg': '#FFFFFF',
            'text_fg': '#000000',
            'accent': '#303F9F'
        },
        'Modo Escuro': {
            'bg': '#1E1E1E',
            'fg': '#FFFFFF',
            'button_bg': '#0D47A1',
            'button_fg': '#FFFFFF',
            'text_bg': '#2D2D2D',
            'text_fg': '#E0E0E0',
            'accent': '#1976D2'
        }
    }


class SanitizerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("SOC Log Sanitizer - Interface Grafica")
        self.root.geometry("1200x800")

        self.sanitize_email = tk.BooleanVar(value=True)
        self.sanitize_ipv4 = tk.BooleanVar(value=True)
        self.sanitize_ipv6 = tk.BooleanVar(value=True)
        self.sanitize_domain = tk.BooleanVar(value=True)
        self.sanitize_username = tk.BooleanVar(value=True)
        self.sanitize_client = tk.BooleanVar(value=True)
        self.sanitize_custom_clients = tk.BooleanVar(value=True)

        self.use_hash = tk.BooleanVar(value=False)
        self.preserve_structure = tk.BooleanVar(value=True)

        self.current_theme = tk.StringVar(value='Azul')

        self.custom_clients_list: List[str] = []

        self.setup_ui()
        self.apply_theme('Azul')

    def setup_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        title_label = ttk.Label(
            header_frame,
            text="SOC Log Sanitizer - Remova Informacoes Sensiveis",
            font=("Arial", 16, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Sanitize emails, IPs, dominios, nomes de usuarios e clientes",
            font=("Arial", 10)
        )
        subtitle_label.pack()

        theme_frame = ttk.Frame(header_frame)
        theme_frame.pack(pady=5)

        ttk.Label(theme_frame, text="Tema:").pack(side=tk.LEFT, padx=5)

        self.theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.current_theme,
            values=list(ColorTheme.THEMES.keys()),
            state='readonly',
            width=15
        )
        self.theme_combo.pack(side=tk.LEFT, padx=5)
        self.theme_combo.bind('<<ComboboxSelected>>', self.on_theme_change)

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)

        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_rowconfigure(2, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.input_label = ttk.Label(text_frame, text="Texto Original:", font=("Arial", 11, "bold"))
        self.input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.input_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=("Courier New", 10)
        )
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        buttons_frame = ttk.Frame(text_frame)
        buttons_frame.grid(row=2, column=0, pady=10)

        self.sanitize_btn = ttk.Button(
            buttons_frame,
            text="Sanitizar Texto",
            command=self.sanitize_text
        )
        self.sanitize_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(
            buttons_frame,
            text="Limpar Tudo",
            command=self.clear_all
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.load_file_btn = ttk.Button(
            buttons_frame,
            text="Carregar Arquivo",
            command=self.load_file
        )
        self.load_file_btn.pack(side=tk.LEFT, padx=5)

        self.output_label = ttk.Label(text_frame, text="Texto Sanitizado:", font=("Arial", 11, "bold"))
        self.output_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 5))

        self.output_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=("Courier New", 10)
        )
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        output_buttons_frame = ttk.Frame(text_frame)
        output_buttons_frame.grid(row=5, column=0, pady=10)

        self.copy_btn = ttk.Button(
            output_buttons_frame,
            text="Copiar para Area de Transferencia",
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = ttk.Button(
            output_buttons_frame,
            text="Salvar em Arquivo",
            command=self.save_to_file
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        self.checkbox_frame = ttk.LabelFrame(options_frame, text="Selecione o que Sanitizar", padding="10")
        self.checkbox_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Enderecos de Email",
            variable=self.sanitize_email
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Enderecos IPv4",
            variable=self.sanitize_ipv4
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Enderecos IPv6",
            variable=self.sanitize_ipv6
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Dominios",
            variable=self.sanitize_domain
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Nomes de Usuarios",
            variable=self.sanitize_username
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Nomes de Clientes (padrao)",
            variable=self.sanitize_client
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.checkbox_frame,
            text="Nomes de Clientes (customizados)",
            variable=self.sanitize_custom_clients
        ).pack(anchor=tk.W, pady=2)

        select_buttons_frame = ttk.Frame(self.checkbox_frame)
        select_buttons_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            select_buttons_frame,
            text="Todos",
            command=self.select_all,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            select_buttons_frame,
            text="Nenhum",
            command=self.deselect_all,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        self.custom_clients_frame = ttk.LabelFrame(
            options_frame,
            text="Clientes/Termos Personalizados",
            padding="10"
        )
        self.custom_clients_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Label(
            self.custom_clients_frame,
            text="Adicione nomes especificos para remover:",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))

        entry_frame = ttk.Frame(self.custom_clients_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        self.client_entry = ttk.Entry(entry_frame)
        self.client_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.client_entry.bind('<Return>', lambda e: self.add_custom_client())

        ttk.Button(
            entry_frame,
            text="Adicionar",
            command=self.add_custom_client,
            width=10
        ).pack(side=tk.LEFT)

        ttk.Label(
            self.custom_clients_frame,
            text="Nomes na lista:",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(10, 5))

        list_frame = ttk.Frame(self.custom_clients_frame)
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
            self.custom_clients_frame,
            text="Remover Selecionado",
            command=self.remove_custom_client
        ).pack(pady=(5, 0))

        self.advanced_frame = ttk.LabelFrame(options_frame, text="Opcoes Avancadas", padding="10")
        self.advanced_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(
            self.advanced_frame,
            text="Usar Hash (consistencia)",
            variable=self.use_hash
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            self.advanced_frame,
            text="Preservar Estrutura",
            variable=self.preserve_structure
        ).pack(anchor=tk.W, pady=2)

        self.stats_frame = ttk.LabelFrame(options_frame, text="Estatisticas", padding="10")
        self.stats_frame.pack(fill=tk.X, pady=5)

        self.stats_label = ttk.Label(
            self.stats_frame,
            text="Nenhuma sanitizacao realizada ainda.",
            font=("Arial", 9),
            wraplength=250,
            justify=tk.LEFT
        )
        self.stats_label.pack(anchor=tk.W)

        self.input_text.insert("1.0", """Cole aqui o texto que deseja sanitizar...

Exemplo:
[2024-01-15 10:30] User: john.doe@company.com from 192.168.1.100
[2024-01-15 10:31] Client: ACME Corporation accessed api.server.com
[2024-01-15 10:32] Username: admin logged in
[2024-01-15 10:33] Email sent to support@example.com from fe80::1
""")

    def on_theme_change(self, event=None):
        theme_name = self.current_theme.get()
        self.apply_theme(theme_name)

    def apply_theme(self, theme_name: str):
        theme = ColorTheme.THEMES.get(theme_name, ColorTheme.THEMES['Azul'])

        self.root.configure(bg=theme['bg'])

        style = ttk.Style()
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TLabelframe', background=theme['bg'], foreground=theme['fg'])
        style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
        style.configure('TCheckbutton', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', background=theme['button_bg'], foreground=theme['button_fg'])
        style.configure('TCombobox', fieldbackground=theme['text_bg'], foreground=theme['text_fg'])

        style.map('TButton',
                  background=[('active', theme['accent'])])

        self.input_text.configure(bg=theme['text_bg'], fg=theme['text_fg'], insertbackground=theme['text_fg'])
        self.output_text.configure(bg=theme['text_bg'], fg=theme['text_fg'], insertbackground=theme['text_fg'])
        self.clients_listbox.configure(bg=theme['text_bg'], fg=theme['text_fg'])

    def select_all(self):
        self.sanitize_email.set(True)
        self.sanitize_ipv4.set(True)
        self.sanitize_ipv6.set(True)
        self.sanitize_domain.set(True)
        self.sanitize_username.set(True)
        self.sanitize_client.set(True)
        self.sanitize_custom_clients.set(True)

    def deselect_all(self):
        self.sanitize_email.set(False)
        self.sanitize_ipv4.set(False)
        self.sanitize_ipv6.set(False)
        self.sanitize_domain.set(False)
        self.sanitize_username.set(False)
        self.sanitize_client.set(False)
        self.sanitize_custom_clients.set(False)

    def add_custom_client(self):
        client_name = self.client_entry.get().strip()
        if client_name and client_name not in self.custom_clients_list:
            self.custom_clients_list.append(client_name)
            self.clients_listbox.insert(tk.END, client_name)
            self.client_entry.delete(0, tk.END)
        elif client_name in self.custom_clients_list:
            messagebox.showinfo("Info", "Este nome ja esta na lista!")

    def remove_custom_client(self):
        selection = self.clients_listbox.curselection()
        if selection:
            index = selection[0]
            client_name = self.clients_listbox.get(index)
            self.clients_listbox.delete(index)
            self.custom_clients_list.remove(client_name)

    def sanitize_custom_clients_in_text(self, text: str) -> str:
        if not self.custom_clients_list:
            return text

        sanitized_text = text
        for i, client_name in enumerate(self.custom_clients_list, 1):
            escaped_name = re.escape(client_name)
            pattern = re.compile(escaped_name, re.IGNORECASE)
            replacement = f"[CUSTOM_CLIENT_{i}]"
            sanitized_text = pattern.sub(replacement, sanitized_text)

        return sanitized_text

    def sanitize_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Aviso", "Por favor, insira algum texto para sanitizar!")
            return

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
                "Por favor, selecione pelo menos uma opcao de sanitizacao!"
            )
            return

        sanitizer = SOCLogSanitizer(
            use_hash=self.use_hash.get(),
            preserve_structure=self.preserve_structure.get()
        )

        sanitized_text = input_text

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

        if self.sanitize_custom_clients.get():
            sanitized_text = self.sanitize_custom_clients_in_text(sanitized_text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", sanitized_text)

        stats = sanitizer.get_statistics()
        stats_text = "Itens sanitizados:\n"
        total = 0
        for data_type, count in stats.items():
            if count > 0:
                stats_text += f"- {data_type}: {count}\n"
                total += count

        if self.sanitize_custom_clients.get() and self.custom_clients_list:
            custom_count = len(re.findall(
                r'\[CUSTOM_CLIENT_\d+\]',
                sanitized_text
            ))
            if custom_count > 0:
                stats_text += f"- custom_clients: {custom_count}\n"
                total += custom_count

        stats_text += f"\nTotal: {total} itens"

        self.stats_label.config(text=stats_text)

        messagebox.showinfo("Sucesso", "Texto sanitizado com sucesso!")

    def copy_to_clipboard(self):
        output_text = self.output_text.get("1.0", tk.END).strip()

        if not output_text:
            messagebox.showwarning("Aviso", "Nao ha texto sanitizado para copiar!")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        self.root.update()

        messagebox.showinfo("Sucesso", "Texto copiado para a area de transferencia!")

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.stats_label.config(text="Nenhuma sanitizacao realizada ainda.")

    def load_file(self):
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
        output_text = self.output_text.get("1.0", tk.END).strip()

        if not output_text:
            messagebox.showwarning("Aviso", "Nao ha texto sanitizado para salvar!")
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
    root = tk.Tk()

    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass

    app = SanitizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
