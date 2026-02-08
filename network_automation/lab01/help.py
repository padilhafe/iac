#!/usr/bin/env python3
"""
Script de ajuda e documentação do NetDevOps Framework
"""

import sys
from datetime import datetime


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}{Colors.ENDC}")


def show_overview():
    """Mostra visão geral do framework"""
    print_header("🚀 NETDEVOPS FRAMEWORK - VISÃO GERAL")

    print(f"""
{Colors.BOLD}O que é:{Colors.ENDC}
Framework Python para automação de dispositivos de rede usando Netmiko.
Suporta múltiplos vendors com drivers específicos e templates Jinja2.

{Colors.BOLD}Principais funcionalidades:{Colors.ENDC}
• ✅ Teste de conectividade SSH
• 🔧 Aplicação de configurações via templates
• 📊 Estatísticas e validação do inventário
• 🎯 Execução em dispositivos específicos ou todos
• 🧪 Modo dry-run para teste seguro
• 🎨 Interface CLI colorida e informativa
• 📋 Multiple templates por vendor
• ⚠️  Proteção contra mudanças de hostname

{Colors.BOLD}Arquitetura:{Colors.ENDC}
• {Colors.OKCYAN}main.py{Colors.ENDC} - Interface principal
• {Colors.OKCYAN}drivers/{Colors.ENDC} - Drivers específicos por vendor
• {Colors.OKCYAN}templates/{Colors.ENDC} - Templates Jinja2 de configuração
• {Colors.OKCYAN}inventory/{Colors.ENDC} - Inventário de dispositivos
• {Colors.OKCYAN}stats.py{Colors.ENDC} - Estatísticas e validação
• {Colors.OKCYAN}help.py{Colors.ENDC} - Este arquivo de ajuda
""")


def show_quick_start():
    """Mostra guia de início rápido"""
    print_header("🏃‍♂️ GUIA DE INÍCIO RÁPIDO")

    print(f"""
{Colors.BOLD}1. Listar dispositivos disponíveis:{Colors.ENDC}
   {Colors.OKCYAN}python main.py list{Colors.ENDC}

{Colors.BOLD}2. Testar conectividade SSH:{Colors.ENDC}
   {Colors.OKCYAN}python main.py check{Colors.ENDC}                    # Todos os dispositivos
   {Colors.OKCYAN}python main.py check huawei-ne40{Colors.ENDC}        # Dispositivo específico

{Colors.BOLD}3. Aplicar configurações (modo seguro):{Colors.ENDC}
   {Colors.OKCYAN}python main.py config --dry-run{Colors.ENDC}         # Teste sem aplicar
   {Colors.OKCYAN}python main.py config{Colors.ENDC}                   # Usa fallback default.j2 (seguro)
   {Colors.OKCYAN}python main.py config --template router_no_hostname.j2{Colors.ENDC}  # Template específico

{Colors.BOLD}4. Ver estatísticas do inventário:{Colors.ENDC}
   {Colors.OKCYAN}python stats.py{Colors.ENDC}                        # Estatísticas básicas
   {Colors.OKCYAN}python stats.py --validate{Colors.ENDC}              # Validar inventário
   {Colors.OKCYAN}python stats.py --all{Colors.ENDC}                   # Todas as informações
""")


def show_commands():
    """Mostra todos os comandos disponíveis"""
    print_header("📝 COMANDOS DISPONÍVEIS")

    print(f"""
{Colors.BOLD}main.py - Interface principal:{Colors.ENDC}

{Colors.OKCYAN}Comandos básicos:{Colors.ENDC}
  list                                    Lista todos os dispositivos
  check [dispositivo]                     Testa conectividade SSH
  config [dispositivo]                    Aplica configurações

{Colors.OKCYAN}Opções avançadas:{Colors.ENDC}
  --template <nome>                       Template específico a usar
  --dry-run                               Apenas mostra config, não aplica

{Colors.OKCYAN}Exemplos:{Colors.ENDC}
  python main.py check
  python main.py config                              # Usa default.j2 (fallback)
  python main.py config huawei-ne40 --dry-run       # Usa template do inventário
  python main.py config --template router.j2        # Força template específico
  python main.py templates                          # Lista todos os templates

{Colors.BOLD}stats.py - Estatísticas e validação:{Colors.ENDC}

{Colors.OKCYAN}Comandos:{Colors.ENDC}
  (sem argumentos)                        Estatísticas básicas
  --all                                   Todas as informações
  --details                               Detalhes de cada dispositivo
  --validate                              Valida consistência do inventário
  --network                               Informações de rede

{Colors.OKCYAN}Exemplos:{Colors.ENDC}
  python stats.py
  python stats.py --validate
  python stats.py --details
""")


def show_drivers():
    """Mostra informações sobre drivers"""
    print_header("🔌 DRIVERS DISPONÍVEIS")

    print(f"""
{Colors.BOLD}huawei_vrp5 (drivers/huawei_vrp5.py):{Colors.ENDC}
• Para dispositivos Huawei VRP 5.x (ex: AR1000V)
• Não executa comando 'commit'
• Lida com mudanças de prompt automaticamente

{Colors.BOLD}huawei_vrp8 (drivers/huawei_vrp8.py):{Colors.ENDC}
• Para dispositivos Huawei VRP 8.x (ex: NE40)
• Executa comando 'commit' após aplicar configurações
• Lida com mudanças de prompt automaticamente

{Colors.BOLD}routeros7 (drivers/routeros7.py):{Colors.ENDC}
• Para dispositivos MikroTik RouterOS 7.x
• Implementação padrão

{Colors.OKCYAN}Como criar novos drivers:{Colors.ENDC}
1. Crie arquivo em drivers/<vendor>.py
2. Implemente função send_config(conn, config_set)
3. Adicione import em drivers/__init__.py
4. Adicione entrada no dicionário DRIVERS em main.py
5. Crie pasta de templates em templates/<vendor>/
""")


def show_templates():
    """Mostra informações sobre templates"""
    print_header("📋 SISTEMA DE TEMPLATES")

    print(f"""
{Colors.BOLD}Estrutura:{Colors.ENDC}
templates/
├── huawei_vrp5/
│   ├── default.j2                      # Template fallback (usado automaticamente)
│   ├── router.j2                       # Template completo com hostname
│   └── router_no_hostname.j2           # Template sem mudança de hostname
├── huawei_vrp8/
│   ├── default.j2                      # Template fallback (usado automaticamente)
│   ├── router.j2                       # Template completo com hostname
│   └── router_no_hostname.j2           # Template sem mudança de hostname
└── routeros7/
    ├── default.j2                      # Template fallback (usado automaticamente)
    └── router.j2                       # Template completo com hostname

{Colors.BOLD}Sistema de Fallback Automático:{Colors.ENDC}
O sistema usa esta ordem de prioridade para selecionar templates:
1. {Colors.OKCYAN}--template <nome>{Colors.ENDC} - Template especificado na linha de comando
2. {Colors.OKCYAN}template no YAML{Colors.ENDC} - Template no inventário do dispositivo
3. {Colors.OKGREEN}default.j2{Colors.ENDC} - Fallback automático (sempre disponível)

{Colors.BOLD}Templates recomendados:{Colors.ENDC}
• {Colors.OKGREEN}default.j2{Colors.ENDC} - Fallback seguro, sem mudança de hostname
• {Colors.OKGREEN}router_no_hostname.j2{Colors.ENDC} - Mais seguro, não muda prompt
• {Colors.WARNING}router.j2{Colors.ENDC} - Completo, mas pode causar problemas com Netmiko

{Colors.BOLD}Variáveis disponíveis nos templates:{Colors.ENDC}
• {Colors.OKCYAN}hostname{Colors.ENDC} - Nome do dispositivo
• {Colors.OKCYAN}interfaces{Colors.ENDC} - Lista de interfaces com name, ip, mask

{Colors.BOLD}Exemplo - Template com hostname (router.j2):{Colors.ENDC}
{Colors.OKBLUE}sysname {{{{ hostname }}}}

{{% for iface in interfaces %}}
interface {{{{ iface.name }}}}
 ip address {{{{ iface.ip }}}} {{{{ iface.mask }}}}
 undo shutdown
 quit
{{% endfor %}}{Colors.ENDC}

{Colors.BOLD}Exemplo - Template seguro (default.j2):{Colors.ENDC}
{Colors.OKBLUE}{{% for iface in interfaces %}}
interface {{{{ iface.name }}}}
 ip address {{{{ iface.ip }}}} {{{{ iface.mask }}}}
 undo shutdown
 quit
{{% endfor %}}{Colors.ENDC}
""")


def show_inventory():
    """Mostra informações sobre inventário"""
    print_header("📁 CONFIGURAÇÃO DO INVENTÁRIO")

    print(f"""
{Colors.BOLD}Arquivo: inventory/devices.yml{Colors.ENDC}

{Colors.BOLD}Campos obrigatórios:{Colors.ENDC}
• name - Nome único do dispositivo
• host - IP ou hostname
• vendor - Driver a usar (huawei_vrp5, huawei_vrp8, routeros7)
• device_type - Tipo para Netmiko
• username - Usuário SSH
• password - Senha SSH

{Colors.BOLD}Campos opcionais:{Colors.ENDC}
• template - Template específico (padrão: router.j2)
• session_log - Arquivo de log da sessão
• ssh_config_file - Arquivo de configuração SSH
• interfaces - Lista de interfaces para configurar

{Colors.BOLD}Exemplo:{Colors.ENDC}
{Colors.OKBLUE}devices:
  - name: huawei-ne40
    host: 192.168.10.238
    vendor: huawei_vrp8
    device_type: huawei_vrpv8
    template: router_no_hostname.j2
    username: automacao
    password: Password@123
    interfaces:
      - name: Ethernet 1/0/1
        ip: 10.0.1.10
        mask: 255.255.255.0{Colors.ENDC}

{Colors.BOLD}Validação:{Colors.ENDC}
Use {Colors.OKCYAN}python stats.py --validate{Colors.ENDC} para verificar erros no inventário.
""")


def show_troubleshooting():
    """Mostra guia de solução de problemas"""
    print_header("🔧 SOLUÇÃO DE PROBLEMAS")

    print(f"""
{Colors.BOLD}Problema: SSH timeout ou falha de conexão{Colors.ENDC}
{Colors.OKGREEN}Solução:{Colors.ENDC}
• Verifique IP/hostname no inventário
• Teste conectividade: ping <ip>
• Verifique credenciais SSH
• Use arquivo de configuração SSH se necessário

{Colors.BOLD}Problema: Netmiko se perde após mudança de hostname{Colors.ENDC}
{Colors.OKGREEN}Solução:{Colors.ENDC}
• Use template router_no_hostname.j2
• Exemplo: python main.py config --template router_no_hostname.j2

{Colors.BOLD}Problema: Template não encontrado{Colors.ENDC}
{Colors.OKGREEN}Solução:{Colors.ENDC}
• Verifique se existe pasta templates/<vendor>/
• Verifique se arquivo .j2 existe na pasta
• Use python stats.py --validate para verificar

{Colors.BOLD}Problema: Driver não encontrado{Colors.ENDC}
{Colors.OKGREEN}Solução:{Colors.ENDC}
• Verifique se vendor no inventário está correto
• Drivers disponíveis: huawei_vrp5, huawei_vrp8, routeros7
• Use python main.py list para ver vendors configurados

{Colors.BOLD}Problema: Configuração demora muito{Colors.ENDC}
{Colors.OKGREEN}Solução:{Colors.ENDC}
• Use --dry-run primeiro para testar
• Configure timeout maior no código se necessário
• Verifique se não há comandos interativos no template

{Colors.BOLD}Depuração avançada:{Colors.ENDC}
• Logs são salvos em arquivos .log (configurável por dispositivo)
• Use modo dry-run para testar templates
• Valide inventário antes de executar configurações
""")


def show_best_practices():
    """Mostra melhores práticas"""
    print_header("✨ MELHORES PRÁTICAS")

    print(f"""
{Colors.BOLD}🔒 Segurança:{Colors.ENDC}
• Sempre use --dry-run antes de aplicar configurações
• O sistema usa default.j2 como fallback seguro automaticamente
• Use templates sem mudança de hostname para evitar problemas
• Teste conectividade antes de aplicar configurações
• Valide templates com 'python main.py templates'

{Colors.BOLD}📋 Organização:{Colors.ENDC}
• Valide inventário regularmente: python stats.py --validate
• Use nomes descritivos para dispositivos
• Organize templates por funcionalidade e segurança
• Configure templates no inventário quando necessário
• Deixe sem template para usar fallback automático
• Mantenha logs de sessão para auditoria

{Colors.BOLD}🚀 Performance:{Colors.ENDC}
• Execute em dispositivos específicos quando possível
• Use paralelização para múltiplos dispositivos (futuro)
• Monitore logs para identificar lentidão

{Colors.BOLD}🔍 Monitoramento:{Colors.ENDC}
• Use python stats.py para ver visão geral
• Monitore arquivos de log para erros
• Valide configurações após aplicação

{Colors.BOLD}📚 Documentação:{Colors.ENDC}
• Documente mudanças no inventário
• Mantenha templates comentados
• Use git para versionamento (recomendado)
""")


def main():
    if len(sys.argv) > 1:
        topic = sys.argv[1].lower()

        topics = {
            "overview": show_overview,
            "quick": show_quick_start,
            "start": show_quick_start,
            "commands": show_commands,
            "drivers": show_drivers,
            "templates": show_templates,
            "inventory": show_inventory,
            "troubleshoot": show_troubleshooting,
            "trouble": show_troubleshooting,
            "best": show_best_practices,
            "practices": show_best_practices,
        }

        if topic in topics:
            topics[topic]()
        else:
            print(f"{Colors.FAIL}❌ Tópico '{topic}' não encontrado!{Colors.ENDC}")
            print(
                f"{Colors.WARNING}Tópicos disponíveis: {', '.join(topics.keys())}{Colors.ENDC}"
            )
    else:
        # Mostra menu principal
        print(f"{Colors.BOLD}{Colors.HEADER}")
        print("🚀 NETDEVOPS FRAMEWORK - SISTEMA DE AJUDA")
        print("=" * 60)
        print(f"📅 Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 60}{Colors.ENDC}")

        show_overview()

        print(f"\n{Colors.BOLD}📚 Tópicos de ajuda disponíveis:{Colors.ENDC}")
        print(
            f"  {Colors.OKCYAN}python help.py overview{Colors.ENDC}        # Visão geral do framework"
        )
        print(
            f"  {Colors.OKCYAN}python help.py quick{Colors.ENDC}           # Guia de início rápido"
        )
        print(
            f"  {Colors.OKCYAN}python help.py commands{Colors.ENDC}        # Todos os comandos"
        )
        print(
            f"  {Colors.OKCYAN}python help.py drivers{Colors.ENDC}         # Informações sobre drivers"
        )
        print(
            f"  {Colors.OKCYAN}python help.py templates{Colors.ENDC}       # Sistema de templates"
        )
        print(
            f"  {Colors.OKCYAN}python help.py inventory{Colors.ENDC}       # Configuração do inventário"
        )
        print(
            f"  {Colors.OKCYAN}python help.py troubleshoot{Colors.ENDC}    # Solução de problemas"
        )
        print(
            f"  {Colors.OKCYAN}python help.py best{Colors.ENDC}            # Melhores práticas"
        )

        print(f"\n{Colors.BOLD}🏃‍♂️ Para começar rapidamente:{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}python help.py quick{Colors.ENDC}")


if __name__ == "__main__":
    main()
