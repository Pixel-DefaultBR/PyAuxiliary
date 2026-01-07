#!/usr/bin/env python3

import re
import hashlib
from typing import Dict, Optional, Callable
from pathlib import Path


class SOCLogSanitizer:

    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'ipv4': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
        'ipv6': r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:\b|\b(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}\b',
        'domain': r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b',
        'username': r'\b(?:user|username|usuario|login|account)[\s:=]+([A-Za-z0-9_\-\.]+)\b',
        'client_name': r'\b(?:client|cliente|customer|company|empresa)[\s:=]+([A-Za-z0-9_\-\.\s]+?)(?:\s|$|,|\|)',
    }

    def __init__(self,
                 use_hash: bool = False,
                 preserve_structure: bool = True,
                 custom_replacements: Optional[Dict[str, str]] = None):
        self.use_hash = use_hash
        self.preserve_structure = preserve_structure
        self.custom_replacements = custom_replacements or {}
        self.replacement_cache: Dict[str, str] = {}
        self.counters: Dict[str, int] = {key: 0 for key in self.PATTERNS.keys()}

    def _generate_replacement(self, value: str, data_type: str) -> str:
        cache_key = f"{data_type}:{value}"
        if cache_key in self.replacement_cache:
            return self.replacement_cache[cache_key]

        if data_type in self.custom_replacements:
            replacement = self.custom_replacements[data_type]
        elif self.use_hash:
            hash_value = hashlib.sha256(value.encode()).hexdigest()[:8]
            replacement = f"[{data_type.upper()}_{hash_value}]"
        else:
            self.counters[data_type] += 1
            counter = self.counters[data_type]

            if self.preserve_structure:
                replacement = self._get_structured_replacement(value, data_type, counter)
            else:
                replacement = f"[{data_type.upper()}_{counter}]"

        self.replacement_cache[cache_key] = replacement
        return replacement

    def _get_structured_replacement(self, value: str, data_type: str, counter: int) -> str:
        if data_type == 'email':
            return f"user{counter}@redacted-domain.com"
        elif data_type == 'ipv4':
            return f"10.0.{counter // 256}.{counter % 256}"
        elif data_type == 'ipv6':
            return f"fe80::{counter:x}"
        elif data_type == 'domain':
            return f"redacted-domain-{counter}.com"
        elif data_type in ('username', 'client_name'):
            return f"REDACTED_{data_type.upper()}_{counter}"
        else:
            return f"[{data_type.upper()}_{counter}]"

    def sanitize_email(self, text: str) -> str:
        pattern = re.compile(self.PATTERNS['email'])
        return pattern.sub(
            lambda m: self._generate_replacement(m.group(0), 'email'),
            text
        )

    def sanitize_ipv4(self, text: str) -> str:
        pattern = re.compile(self.PATTERNS['ipv4'])
        return pattern.sub(
            lambda m: self._generate_replacement(m.group(0), 'ipv4'),
            text
        )

    def sanitize_ipv6(self, text: str) -> str:
        pattern = re.compile(self.PATTERNS['ipv6'])
        return pattern.sub(
            lambda m: self._generate_replacement(m.group(0), 'ipv6'),
            text
        )

    def sanitize_domain(self, text: str) -> str:
        pattern = re.compile(self.PATTERNS['domain'])

        def replace_domain(match):
            domain = match.group(0)
            common_domains = ['localhost', 'example.com', 'redacted-domain.com']
            if domain.lower() in common_domains or 'redacted' in domain.lower():
                return domain
            return self._generate_replacement(domain, 'domain')

        return pattern.sub(replace_domain, text)

    def sanitize_username(self, text: str) -> str:
        pattern = re.compile(self.PATTERNS['username'], re.IGNORECASE)

        def replace_username(match):
            prefix = match.group(0).split(match.group(1))[0]
            username = match.group(1)
            replacement = self._generate_replacement(username, 'username')
            return f"{prefix}{replacement}"

        return pattern.sub(replace_username, text)

    def sanitize_client_name(self, text: str) -> str:
        pattern = re.compile(self.PATTERNS['client_name'], re.IGNORECASE)

        def replace_client(match):
            prefix = match.group(0).split(match.group(1))[0]
            client = match.group(1).strip()
            suffix = match.group(0)[len(prefix) + len(match.group(1)):]
            replacement = self._generate_replacement(client, 'client_name')
            return f"{prefix}{replacement}{suffix}"

        return pattern.sub(replace_client, text)

    def sanitize_all(self, text: str) -> str:
        text = self.sanitize_email(text)
        text = self.sanitize_ipv4(text)
        text = self.sanitize_ipv6(text)
        text = self.sanitize_username(text)
        text = self.sanitize_client_name(text)
        text = self.sanitize_domain(text)
        return text

    def sanitize_file(self, input_path: str, output_path: Optional[str] = None) -> None:
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

        if output_path is None:
            output_path = str(input_file.with_suffix(input_file.suffix + '.sanitized'))

        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            with open(output_path, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    sanitized_line = self.sanitize_all(line)
                    f_out.write(sanitized_line)

        print(f"Arquivo sanitizado salvo em: {output_path}")

    def get_statistics(self) -> Dict[str, int]:
        return self.counters.copy()


def sanitize_text(text: str, use_hash: bool = False) -> str:
    sanitizer = SOCLogSanitizer(use_hash=use_hash)
    return sanitizer.sanitize_all(text)


def sanitize_log_file(input_path: str, output_path: Optional[str] = None, use_hash: bool = False) -> None:
    sanitizer = SOCLogSanitizer(use_hash=use_hash)
    sanitizer.sanitize_file(input_path, output_path)


if __name__ == "__main__":
    print("=" * 70)
    print("SOC Log Sanitizer - Exemplo de Uso")
    print("=" * 70)

    sample_log = """
    [2024-01-15 10:30:45] INFO: Login attempt from IP 192.168.1.100
    [2024-01-15 10:30:46] INFO: User: john.doe@example.com authenticated successfully
    [2024-01-15 10:31:00] WARNING: Suspicious activity from 203.0.113.42
    [2024-01-15 10:31:05] ERROR: Failed connection to database.company-corp.com
    [2024-01-15 10:31:10] INFO: Client: Acme Corporation requested access
    [2024-01-15 10:31:15] INFO: Username: admin_user logged in from fe80::1
    [2024-01-15 10:31:20] ALERT: Malware detected from email spam@malicious-domain.net
    [2024-01-15 10:31:25] INFO: Account alice.smith@corporate.com accessed sensitive data
    """

    print("\nLOG ORIGINAL:")
    print("-" * 70)
    print(sample_log)

    print("\nLOG SANITIZADO (com contadores):")
    print("-" * 70)
    sanitizer1 = SOCLogSanitizer(use_hash=False, preserve_structure=True)
    sanitized_log1 = sanitizer1.sanitize_all(sample_log)
    print(sanitized_log1)

    print("\nEstatisticas:")
    for data_type, count in sanitizer1.get_statistics().items():
        if count > 0:
            print(f"  - {data_type}: {count} itens sanitizados")

    print("\n" + "=" * 70)
    print("\nLOG SANITIZADO (com hash):")
    print("-" * 70)
    sanitizer2 = SOCLogSanitizer(use_hash=True, preserve_structure=False)
    sanitized_log2 = sanitizer2.sanitize_all(sample_log)
    print(sanitized_log2)

    print("\n" + "=" * 70)
    print("\nLOG SANITIZADO (substituicoes customizadas):")
    print("-" * 70)
    custom = {
        'email': '[EMAIL_REDACTED]',
        'ipv4': '[IP_REDACTED]',
        'domain': '[DOMAIN_REDACTED]',
    }
    sanitizer3 = SOCLogSanitizer(custom_replacements=custom)
    sanitized_log3 = sanitizer3.sanitize_all(sample_log)
    print(sanitized_log3)

    print("\n" + "=" * 70)
    print("Exemplos concluidos!")
    print("=" * 70)
