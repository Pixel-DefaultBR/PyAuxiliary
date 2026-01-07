# SOC Log Sanitizer 🔒

Script Python para remover e substituir informações sensíveis de logs de SOC (Security Operations Center).

## 📋 Funcionalidades

O sanitizador detecta e substitui automaticamente:

- ✉️ **Endereços de email** - `user@domain.com` → `user1@redacted-domain.com`
- 🌐 **Endereços IPv4** - `192.168.1.100` → `10.0.0.1`
- 🌐 **Endereços IPv6** - `fe80::1` → `fe80::1`
- 🔗 **Domínios** - `api.company.com` → `redacted-domain-1.com`
- 👤 **Nomes de usuários** - `username: john.doe` → `username: REDACTED_USERNAME_1`
- 🏢 **Nomes de clientes** - `Client: ACME Corp` → `Client: REDACTED_CLIENT_NAME_1`

## 🚀 Instalação

Não requer instalação de dependências externas, apenas Python 3.6+:

```bash
# Clone ou baixe o arquivo
wget https://raw.githubusercontent.com/seu-repo/sanitize_soc_logs.py

# Torne executável (opcional)
chmod +x sanitize_soc_logs.py
```

## 💡 Uso Rápido

### Sanitizar texto diretamente

```python
from sanitize_soc_logs import sanitize_text

log = "[INFO] User admin@company.com logged from 192.168.1.50"
sanitized = sanitize_text(log)
print(sanitized)
# [INFO] User user1@redacted-domain.com logged from 10.0.0.1
```

### Sanitizar arquivo de log

```python
from sanitize_soc_logs import sanitize_log_file

sanitize_log_file("input.log", "output_sanitized.log")
```

### Interface Gráfica (Recomendado) 🖥️

**Forma mais fácil de usar!** Execute a interface gráfica para sanitizar textos de forma visual:

```bash
python3 sanitizer_gui.py
```

**Recursos da Interface Gráfica:**
- 📝 Áreas de texto para entrada e saída
- ✅ Checkboxes para selecionar o que sanitizar
- 🏢 **Campo para adicionar nomes de clientes personalizados**
- 📋 **Botão para copiar resultado para área de transferência**
- 💾 Carregar e salvar arquivos
- 📊 Estatísticas em tempo real
- ⚙️ Opções avançadas (hash, preservar estrutura)

![GUI Features](https://via.placeholder.com/800x600.png?text=Interface+Gr%C3%A1fica+do+Sanitizador)

**Como usar a GUI:**
1. Cole ou carregue o texto que deseja sanitizar
2. Marque os checkboxes do que deseja remover
3. Adicione nomes específicos de clientes na lista personalizada
4. Clique em "Sanitizar Texto"
5. Copie o resultado ou salve em arquivo

### Linha de comando

```bash
# Executar interface gráfica (recomendado)
python3 sanitizer_gui.py

# Executar exemplos demonstrativos
python3 sanitize_soc_logs.py

# Executar suite completa de testes
python3 test_sanitizer.py
```

## 🔧 Uso Avançado (Programático)

### Modo com Hash (para consistência)

Use hash SHA256 para garantir que o mesmo valor sempre seja substituído pela mesma string:

```python
from sanitize_soc_logs import SOCLogSanitizer

sanitizer = SOCLogSanitizer(use_hash=True)
log = """
Email 1: user@domain.com sent message
Email 2: user@domain.com received reply (mesmo email!)
"""
print(sanitizer.sanitize_all(log))
# Ambos "user@domain.com" terão o mesmo hash
```

### Preservação de Estrutura

Mantenha a estrutura dos dados (recomendado para análise):

```python
sanitizer = SOCLogSanitizer(preserve_structure=True)
# IPs mantêm formato: 192.168.1.1 → 10.0.0.1
# Emails mantêm @: user@domain.com → user1@redacted-domain.com

sanitizer = SOCLogSanitizer(preserve_structure=False)
# Formato genérico: 192.168.1.1 → [IPV4_1]
```

### Substituições Customizadas

Defina seus próprios padrões de substituição:

```python
custom = {
    'email': '[EMAIL_REMOVIDO]',
    'ipv4': '[IP_REMOVIDO]',
    'domain': '[DOMINIO_REMOVIDO]',
    'username': '[USUARIO_REMOVIDO]',
    'client_name': '[CLIENTE_REMOVIDO]'
}

sanitizer = SOCLogSanitizer(custom_replacements=custom)
sanitized = sanitizer.sanitize_all(log_text)
```

### Obter Estatísticas

```python
sanitizer = SOCLogSanitizer()
sanitized = sanitizer.sanitize_all(log_text)

stats = sanitizer.get_statistics()
for data_type, count in stats.items():
    if count > 0:
        print(f"{data_type}: {count} itens sanitizados")
```

## 📖 Exemplos Completos

### Exemplo 1: Sanitização Básica

```python
from sanitize_soc_logs import SOCLogSanitizer

log = """
[2024-01-15 10:30:45] INFO: Login from user@company.com (192.168.1.100)
[2024-01-15 10:31:00] WARNING: Client: ACME Corp accessed api.server.com
[2024-01-15 10:31:15] ERROR: Username: admin failed authentication
"""

sanitizer = SOCLogSanitizer()
print(sanitizer.sanitize_all(log))
```

**Saída:**
```
[2024-01-15 10:30:45] INFO: Login from user1@redacted-domain.com (10.0.0.1)
[2024-01-15 10:31:00] WARNING: Client: REDACTED_CLIENT_NAME_1 accessed redacted-domain-1.com
[2024-01-15 10:31:15] ERROR: Username: REDACTED_USERNAME_1 failed authentication
```

### Exemplo 2: Processar Arquivo Grande

```python
from sanitize_soc_logs import SOCLogSanitizer

sanitizer = SOCLogSanitizer(use_hash=True, preserve_structure=True)

# Processar arquivo linha por linha (eficiente para arquivos grandes)
sanitizer.sanitize_file("large_log.txt", "large_log_sanitized.txt")

# Ver estatísticas
print(sanitizer.get_statistics())
# {'email': 150, 'ipv4': 300, 'domain': 75, ...}
```

### Exemplo 3: Integração com Pipeline

```python
import sys
from sanitize_soc_logs import SOCLogSanitizer

sanitizer = SOCLogSanitizer(preserve_structure=True)

# Ler de stdin, sanitizar, escrever em stdout
for line in sys.stdin:
    sanitized_line = sanitizer.sanitize_all(line)
    sys.stdout.write(sanitized_line)
```

Uso:
```bash
cat original.log | python3 sanitizer_pipeline.py > sanitized.log
```

## 🧪 Testes

Execute a suite completa de testes:

```bash
python3 test_sanitizer.py
```

Testes incluídos:
- ✅ Sanitização básica
- ✅ Modo hash com consistência
- ✅ Preservação de estrutura
- ✅ Substituições customizadas
- ✅ Estatísticas
- ✅ Processamento de arquivos
- ✅ IPv6
- ✅ Casos extremos

## 📝 API Reference

### Classe `SOCLogSanitizer`

#### Construtor

```python
SOCLogSanitizer(
    use_hash: bool = False,
    preserve_structure: bool = True,
    custom_replacements: Optional[Dict[str, str]] = None
)
```

**Parâmetros:**
- `use_hash`: Se True, usa hash SHA256 para substituições consistentes
- `preserve_structure`: Se True, preserva estrutura dos dados (IPs, emails, etc)
- `custom_replacements`: Dicionário com substituições customizadas por tipo

#### Métodos

##### `sanitize_all(text: str) -> str`
Aplica todas as sanitizações no texto.

##### `sanitize_email(text: str) -> str`
Sanitiza apenas endereços de email.

##### `sanitize_ipv4(text: str) -> str`
Sanitiza apenas endereços IPv4.

##### `sanitize_ipv6(text: str) -> str`
Sanitiza apenas endereços IPv6.

##### `sanitize_domain(text: str) -> str`
Sanitiza apenas domínios.

##### `sanitize_username(text: str) -> str`
Sanitiza apenas nomes de usuários.

##### `sanitize_client_name(text: str) -> str`
Sanitiza apenas nomes de clientes.

##### `sanitize_file(input_path: str, output_path: Optional[str] = None) -> None`
Sanitiza um arquivo completo.

##### `get_statistics() -> Dict[str, int]`
Retorna estatísticas de sanitização.

### Funções Auxiliares

#### `sanitize_text(text: str, use_hash: bool = False) -> str`
Função rápida para sanitizar texto.

#### `sanitize_log_file(input_path: str, output_path: Optional[str] = None, use_hash: bool = False) -> None`
Função rápida para sanitizar arquivo.

## 🔍 Padrões Regex Utilizados

O sanitizador usa os seguintes padrões regex:

| Tipo | Padrão Regex |
|------|--------------|
| Email | `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z\|a-z]{2,}\b` |
| IPv4 | `\b(?:(?:25[0-5]\|2[0-4][0-9]\|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]\|2[0-4][0-9]\|[01]?[0-9][0-9]?)\b` |
| IPv6 | `\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b\|...` |
| Domínio | `\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b` |
| Username | `\b(?:user\|username\|usuario\|login\|account)[\s:=]+([A-Za-z0-9_\-\.]+)\b` |
| Cliente | `\b(?:client\|cliente\|customer\|company\|empresa)[\s:=]+([A-Za-z0-9_\-\.\s]+?)(?:\s\|$\|,\|\|)` |

## ⚙️ Características Técnicas

- ✅ **Sem dependências externas**: Usa apenas biblioteca padrão Python
- ✅ **Eficiente**: Processa logs linha por linha
- ✅ **Consistente**: Cache interno garante mesma substituição para mesmo valor
- ✅ **Flexível**: Múltiplos modos e opções de customização
- ✅ **Seguro**: Não altera dados originais, cria novos arquivos
- ✅ **Python 3.6+**: Compatível com versões modernas do Python

## 🎯 Casos de Uso

### 1. Compartilhamento de Logs com Terceiros
```python
# Sanitizar logs antes de enviar para análise externa
sanitizer = SOCLogSanitizer(use_hash=True)
sanitizer.sanitize_file("production.log", "production_safe.log")
```

### 2. Demonstrações e Treinamentos
```python
# Criar logs de exemplo sem dados reais
sanitizer = SOCLogSanitizer(preserve_structure=True)
sanitized = sanitizer.sanitize_all(real_log)
```

### 3. Conformidade com LGPD/GDPR
```python
# Remover dados pessoais de logs arquivados
custom = {
    'email': '[DADOS_PESSOAIS_REMOVIDOS]',
    'username': '[DADOS_PESSOAIS_REMOVIDOS]'
}
sanitizer = SOCLogSanitizer(custom_replacements=custom)
sanitizer.sanitize_file("old_logs.txt", "gdpr_compliant.txt")
```

### 4. Testes Automatizados
```python
# Criar fixtures de teste a partir de logs reais
sanitizer = SOCLogSanitizer(use_hash=False, preserve_structure=True)
sanitizer.sanitize_file("real_incidents.log", "test_fixtures.log")
```

## 🖥️ Interface Gráfica - Guia Completo

### Características da GUI

A interface gráfica (`sanitizer_gui.py`) oferece uma experiência completa e intuitiva:

#### 1. **Área de Texto**
- Entrada: Cole ou carregue qualquer texto (logs, emails, documentos)
- Saída: Visualize o resultado sanitizado em tempo real
- Suporte para arquivos grandes

#### 2. **Opções de Sanitização (Checkboxes)**
Selecione exatamente o que deseja sanitizar:
- ✉️ Endereços de Email
- 🌐 Endereços IPv4
- 🌐 Endereços IPv6
- 🔗 Domínios
- 👤 Nomes de Usuários
- 🏢 Nomes de Clientes (padrão)
- 📝 Nomes de Clientes (customizados)

Atalhos: Botões "✓ Todos" e "✗ Nenhum" para facilitar seleção

#### 3. **Clientes/Termos Personalizados** ⭐
Campo especial para adicionar nomes específicos:
- Adicione nome de clientes reais da sua empresa
- Adicione termos específicos que deseja remover
- Lista editável (adicionar/remover itens)
- Case-insensitive (maiúsculas/minúsculas)

**Exemplo de uso:**
```
Adicione à lista:
- "Empresa XYZ Ltda"
- "Cliente ABC"
- "Projeto Confidencial"

O sanitizador removerá todas as ocorrências desses termos!
```

#### 4. **Opções Avançadas**
- 🔐 **Usar Hash**: Garante consistência nas substituições
- 📐 **Preservar Estrutura**: Mantém formato dos dados (IPs, emails)

#### 5. **Ações Rápidas**
- 🔒 **Sanitizar Texto**: Processa o texto com as opções selecionadas
- 📋 **Copiar para Área de Transferência**: Copia resultado instantaneamente
- 💾 **Salvar em Arquivo**: Exporta resultado para arquivo
- 📂 **Carregar Arquivo**: Importa arquivo para sanitizar
- 🗑️ **Limpar Tudo**: Reset completo

#### 6. **Estatísticas**
Visualize em tempo real:
- Quantos itens de cada tipo foram sanitizados
- Total de substituições realizadas
- Contadores por categoria

### Casos de Uso da GUI

#### Caso 1: Sanitizar Email para Cliente
```
Situação: Precisa enviar logs para cliente externo
Ação:
1. Carregue o arquivo de log
2. Adicione nome da sua empresa na lista personalizada
3. Marque todos os checkboxes
4. Clique "Sanitizar"
5. Clique "Copiar para Área de Transferência"
6. Cole no email
```

#### Caso 2: Preparar Dados para Treinamento
```
Situação: Criar material de treinamento sem dados reais
Ação:
1. Cole o conteúdo no campo de entrada
2. Adicione nomes de clientes reais na lista
3. Mantenha "Preservar Estrutura" marcado
4. Sanitize e salve o arquivo
```

#### Caso 3: Conformidade LGPD
```
Situação: Remover dados pessoais de logs antigos
Ação:
1. Carregue arquivo antigo
2. Marque apenas: Emails, Usernames, Custom Clients
3. Adicione nomes de pessoas na lista personalizada
4. Sanitize e salve
```

### Dicas de Uso da GUI

💡 **Dica 1**: Use a lista personalizada para termos específicos da sua organização
💡 **Dica 2**: Ative "Usar Hash" para manter consistência em análises
💡 **Dica 3**: Sempre revise o resultado antes de compartilhar
💡 **Dica 4**: Salve configurações frequentes como templates
💡 **Dica 5**: A GUI funciona com QUALQUER texto, não apenas logs

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas para melhoria:

- Adicionar mais padrões (números de telefone, CPF/CNPJ, etc)
- Suporte para formatos de log específicos (syslog, JSON, etc)
- Performance para arquivos muito grandes
- Salvar/carregar configurações da GUI
- Testes unitários com pytest
- Modo batch para múltiplos arquivos

## 📄 Licença

Este script é fornecido como está, sem garantias. Use por sua conta e risco.

## ⚠️ Avisos Importantes

- **Sempre revise os logs sanitizados** antes de compartilhar
- **Mantenha backups dos logs originais**
- **Teste em ambiente controlado** antes de usar em produção
- **Ajuste os padrões regex** conforme necessário para seu caso de uso
- **Alguns falsos positivos podem ocorrer** - revise manualmente logs críticos

## 🔗 Recursos Relacionados

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [LGPD - Lei Geral de Proteção de Dados](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [GDPR - General Data Protection Regulation](https://gdpr.eu/)

---

**Desenvolvido para facilitar a sanitização de logs de SOC mantendo a utilidade dos dados para análise de segurança.**
