#!/usr/bin/env python3
"""
Script de teste para o SOC Log Sanitizer.
Demonstra diferentes modos de uso e opções.
"""

from sanitize_soc_logs import SOCLogSanitizer, sanitize_text, sanitize_log_file


def test_basic_usage():
    """Teste de uso básico."""
    print("\n" + "=" * 80)
    print("TEST 1: Uso Básico - Sanitização Rápida")
    print("=" * 80)

    test_text = """
    User: alice@example.com logged in from 192.168.1.100
    Accessing server at database.corporate.net
    Client: ACME Corporation requested data
    """

    print("\nTexto Original:")
    print(test_text)

    sanitized = sanitize_text(test_text)
    print("\nTexto Sanitizado:")
    print(sanitized)


def test_hash_mode():
    """Teste com modo hash."""
    print("\n" + "=" * 80)
    print("TEST 2: Modo Hash - Consistência de Substituições")
    print("=" * 80)

    test_text = """
    Email 1: user@domain.com sent message
    Email 2: admin@domain.com received message
    Email 3: user@domain.com sent another message (mesmo email!)
    """

    print("\nTexto Original:")
    print(test_text)

    sanitizer = SOCLogSanitizer(use_hash=True)
    sanitized = sanitizer.sanitize_all(test_text)

    print("\nTexto Sanitizado (note que user@domain.com tem sempre o mesmo hash):")
    print(sanitized)


def test_preserve_structure():
    """Teste de preservação de estrutura."""
    print("\n" + "=" * 80)
    print("TEST 3: Preservação de Estrutura vs Sem Preservação")
    print("=" * 80)

    test_text = """
    IPs: 192.168.1.1, 10.0.0.50, 172.16.0.100
    Emails: alice@company.com, bob@partner.net
    """

    print("\nTexto Original:")
    print(test_text)

    print("\n--- COM preservação de estrutura ---")
    sanitizer1 = SOCLogSanitizer(preserve_structure=True)
    print(sanitizer1.sanitize_all(test_text))

    print("\n--- SEM preservação de estrutura ---")
    sanitizer2 = SOCLogSanitizer(preserve_structure=False)
    print(sanitizer2.sanitize_all(test_text))


def test_custom_replacements():
    """Teste com substituições customizadas."""
    print("\n" + "=" * 80)
    print("TEST 4: Substituições Customizadas")
    print("=" * 80)

    test_text = """
    Contact: support@company.com
    Server IP: 192.168.10.50
    Domain: private-server.company.net
    """

    print("\nTexto Original:")
    print(test_text)

    custom = {
        'email': '***EMAIL-REMOVED***',
        'ipv4': '***IP-REMOVED***',
        'domain': '***DOMAIN-REMOVED***',
    }

    sanitizer = SOCLogSanitizer(custom_replacements=custom)
    sanitized = sanitizer.sanitize_all(test_text)

    print("\nTexto Sanitizado:")
    print(sanitized)


def test_statistics():
    """Teste de estatísticas."""
    print("\n" + "=" * 80)
    print("TEST 5: Estatísticas de Sanitização")
    print("=" * 80)

    test_text = """
    [LOG] User john@example.com from 192.168.1.50
    [LOG] User mary@example.com from 192.168.1.51
    [LOG] User admin@system.local from 10.0.0.1
    [LOG] Client: ABC Corp accessed api.service.com
    [LOG] Client: XYZ Ltd accessed api.service.com
    [LOG] Username: user123 login from fe80::1
    """

    print("\nProcessando log...")
    sanitizer = SOCLogSanitizer()
    sanitized = sanitizer.sanitize_all(test_text)

    print("\nEstatísticas:")
    stats = sanitizer.get_statistics()
    for data_type, count in stats.items():
        if count > 0:
            print(f"  ✓ {data_type:15s}: {count:3d} itens sanitizados")


def test_file_sanitization():
    """Teste de sanitização de arquivo."""
    print("\n" + "=" * 80)
    print("TEST 6: Sanitização de Arquivo")
    print("=" * 80)

    input_file = "example_soc_log.txt"
    output_file = "example_soc_log_sanitized.txt"

    try:
        print(f"\nSanitizando arquivo: {input_file}")
        sanitize_log_file(input_file, output_file)
        print(f"✓ Arquivo sanitizado salvo em: {output_file}")

        # Mostrar primeiras linhas do resultado
        print("\nPrimeiras 10 linhas do arquivo sanitizado:")
        print("-" * 80)
        with open(output_file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                print(line.rstrip())
        print("-" * 80)

    except FileNotFoundError:
        print(f"⚠ Arquivo {input_file} não encontrado. Pulando teste.")


def test_ipv6():
    """Teste específico para IPv6."""
    print("\n" + "=" * 80)
    print("TEST 7: Sanitização de IPv6")
    print("=" * 80)

    test_text = """
    Connection from 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    Local address fe80::1
    Remote address ::1
    Full address 2001:db8:85a3::8a2e:370:7334
    """

    print("\nTexto Original:")
    print(test_text)

    sanitizer = SOCLogSanitizer()
    sanitized = sanitizer.sanitize_all(test_text)

    print("\nTexto Sanitizado:")
    print(sanitized)


def test_edge_cases():
    """Teste de casos extremos."""
    print("\n" + "=" * 80)
    print("TEST 8: Casos Extremos e Especiais")
    print("=" * 80)

    test_text = """
    1. Email em meio a texto: The user alice123@very-long-domain-name.co.uk sent...
    2. Múltiplos IPs na mesma linha: 192.168.1.1, 10.0.0.1, 172.16.0.1
    3. Username com underscore: username: admin_user_2024
    4. Cliente com espaços: Client: Big Corporation Name Inc
    5. Domínio com hífens: api-gateway.multi-level-domain.com
    6. Email + IP juntos: user@domain.com (192.168.1.1)
    """

    print("\nTexto Original:")
    print(test_text)

    sanitizer = SOCLogSanitizer(preserve_structure=True)
    sanitized = sanitizer.sanitize_all(test_text)

    print("\nTexto Sanitizado:")
    print(sanitized)


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SOC LOG SANITIZER - SUITE DE TESTES" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")

    try:
        test_basic_usage()
        test_hash_mode()
        test_preserve_structure()
        test_custom_replacements()
        test_statistics()
        test_file_sanitization()
        test_ipv6()
        test_edge_cases()

        print("\n" + "=" * 80)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ ERRO durante os testes: {e}")
        import traceback
        traceback.print_exc()
