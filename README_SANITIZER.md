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

### Linha de comando

```bash
# Executar exemplos demonstrativos
python3 sanitize_soc_logs.py

# Executar suite completa de testes
python3 test_sanitizer.py
```

## 🔧 Uso Avançado

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

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas para melhoria:

- Adicionar mais padrões (números de telefone, CPF/CNPJ, etc)
- Suporte para formatos de log específicos (syslog, JSON, etc)
- Performance para arquivos muito grandes
- Interface CLI mais robusta
- Testes unitários com pytest

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
