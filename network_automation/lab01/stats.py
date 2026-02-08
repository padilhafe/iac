#!/usr/bin/env python3
"""
Script de utilitários para estatísticas do inventário NetDevOps
"""

from collections import Counter
from datetime import datetime

import yaml


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


def load_inventory(path="inventory/devices.yml"):
    """Carrega o inventário de dispositivos"""
    try:
        with open(path) as f:
            return yaml.safe_load(f)["devices"]
    except FileNotFoundError:
        print(
            f"{Colors.FAIL}❌ Arquivo de inventário não encontrado: {path}{Colors.ENDC}"
        )
        return []
    except Exception as e:
        print(f"{Colors.FAIL}❌ Erro ao carregar inventário: {e}{Colors.ENDC}")
        return []


def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}{Colors.ENDC}")


def show_basic_stats(devices):
    """Mostra estatísticas básicas"""
    print_header("📊 ESTATÍSTICAS BÁSICAS")

    print(f"{Colors.BOLD}Total de dispositivos:{Colors.ENDC} {len(devices)}")

    # Contagem por vendor
    vendors = Counter(d["vendor"] for d in devices)
    print(f"\n{Colors.OKCYAN}📈 Por Vendor:{Colors.ENDC}")
    for vendor, count in vendors.most_common():
        percentage = (count / len(devices)) * 100
        print(f"  • {vendor:<15} {count:>2} dispositivos ({percentage:4.1f}%)")

    # Contagem por device_type
    device_types = Counter(d["device_type"] for d in devices)
    print(f"\n{Colors.OKCYAN}📈 Por Device Type:{Colors.ENDC}")
    for dev_type, count in device_types.most_common():
        percentage = (count / len(devices)) * 100
        print(f"  • {dev_type:<20} {count:>2} dispositivos ({percentage:4.1f}%)")


def show_network_info(devices):
    """Mostra informações de rede"""
    print_header("🌐 INFORMAÇÕES DE REDE")

    # Análise de subnets
    subnets = set()
    total_interfaces = 0

    for device in devices:
        interfaces = device.get("interfaces", [])
        total_interfaces += len(interfaces)

        for interface in interfaces:
            if "ip" in interface and "mask" in interface:
                # Tenta extrair subnet básica
                ip_parts = interface["ip"].split(".")
                if len(ip_parts) >= 3:
                    subnet = f"{'.'.join(ip_parts[:3])}.0"
                    subnets.add(subnet)

    print(f"{Colors.BOLD}Total de interfaces:{Colors.ENDC} {total_interfaces}")
    print(f"{Colors.BOLD}Subnets identificadas:{Colors.ENDC} {len(subnets)}")

    if subnets:
        print(f"\n{Colors.OKCYAN}🔗 Subnets encontradas:{Colors.ENDC}")
        for subnet in sorted(subnets):
            print(f"  • {subnet}/24")


def show_device_details(devices):
    """Mostra detalhes completos dos dispositivos"""
    print_header("🔍 DETALHES DOS DISPOSITIVOS")

    for i, device in enumerate(devices, 1):
        print(f"\n{Colors.BOLD}{i}. {device['name']}{Colors.ENDC}")
        print(f"   {Colors.OKBLUE}Host:{Colors.ENDC} {device['host']}")
        print(f"   {Colors.OKBLUE}Vendor:{Colors.ENDC} {device['vendor']}")
        print(f"   {Colors.OKBLUE}Device Type:{Colors.ENDC} {device['device_type']}")
        print(
            f"   {Colors.OKBLUE}Template:{Colors.ENDC} {device.get('template', 'N/A')}"
        )

        interfaces = device.get("interfaces", [])
        if interfaces:
            print(f"   {Colors.OKCYAN}Interfaces ({len(interfaces)}):{Colors.ENDC}")
            for iface in interfaces:
                ip_info = f"{iface.get('ip', 'N/A')}/{iface.get('mask', 'N/A')}"
                print(f"     • {iface['name']:<20} {ip_info}")
        else:
            print(f"   {Colors.WARNING}⚠️  Nenhuma interface configurada{Colors.ENDC}")


def validate_inventory(devices):
    """Valida a consistência do inventário"""
    print_header("✅ VALIDAÇÃO DO INVENTÁRIO")

    errors = []
    warnings = []

    required_fields = ["name", "host", "vendor", "device_type", "username", "password"]
    device_names = set()
    device_hosts = set()

    for i, device in enumerate(devices, 1):
        device_id = f"Dispositivo #{i} ({device.get('name', 'SEM_NOME')})"

        # Verifica campos obrigatórios
        for field in required_fields:
            if field not in device or not device[field]:
                errors.append(
                    f"{device_id}: Campo obrigatório '{field}' ausente ou vazio"
                )

        # Verifica duplicação de nomes
        name = device.get("name")
        if name:
            if name in device_names:
                errors.append(f"{device_id}: Nome duplicado '{name}'")
            device_names.add(name)

        # Verifica duplicação de hosts
        host = device.get("host")
        if host:
            if host in device_hosts:
                warnings.append(
                    f"{device_id}: Host duplicado '{host}' (pode ser intencional)"
                )
            device_hosts.add(host)

        # Verifica se vendor existe nos drivers conhecidos
        vendor = device.get("vendor")
        known_vendors = ["huawei_vrp5", "huawei_vrp8", "routeros7"]
        if vendor and vendor not in known_vendors:
            warnings.append(
                f"{device_id}: Vendor '{vendor}' não reconhecido. Vendors conhecidos: {', '.join(known_vendors)}"
            )

        # Verifica interfaces
        interfaces = device.get("interfaces", [])
        interface_names = set()
        for iface in interfaces:
            iface_name = iface.get("name")
            if not iface_name:
                warnings.append(f"{device_id}: Interface sem nome")
            elif iface_name in interface_names:
                errors.append(
                    f"{device_id}: Nome de interface duplicado '{iface_name}'"
                )
            else:
                interface_names.add(iface_name)

            # Verifica IP e máscara
            if "ip" not in iface or not iface["ip"]:
                warnings.append(f"{device_id}: Interface '{iface_name}' sem IP")
            if "mask" not in iface or not iface["mask"]:
                warnings.append(f"{device_id}: Interface '{iface_name}' sem máscara")

    # Mostra resultados da validação
    print(f"{Colors.BOLD}Resumo da validação:{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}✅ Dispositivos analisados: {len(devices)}{Colors.ENDC}")
    print(f"  {Colors.FAIL}❌ Erros encontrados: {len(errors)}{Colors.ENDC}")
    print(f"  {Colors.WARNING}⚠️  Avisos: {len(warnings)}{Colors.ENDC}")

    if errors:
        print(f"\n{Colors.FAIL}❌ ERROS CRÍTICOS:{Colors.ENDC}")
        for error in errors:
            print(f"  • {error}")

    if warnings:
        print(f"\n{Colors.WARNING}⚠️  AVISOS:{Colors.ENDC}")
        for warning in warnings:
            print(f"  • {warning}")

    if not errors and not warnings:
        print(
            f"\n{Colors.OKGREEN}🎉 Inventário válido! Nenhum problema encontrado.{Colors.ENDC}"
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="📊 Utilitários de Estatísticas do Inventário NetDevOps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📚 Exemplos de uso:
  python stats.py                    # Mostra estatísticas básicas
  python stats.py --all              # Mostra todas as informações
  python stats.py --details          # Mostra detalhes dos dispositivos
  python stats.py --validate         # Valida consistência do inventário
  python stats.py --network          # Mostra informações de rede
        """,
    )

    parser.add_argument(
        "--all", action="store_true", help="Mostra todas as informações disponíveis"
    )

    parser.add_argument(
        "--details",
        action="store_true",
        help="Mostra detalhes completos de cada dispositivo",
    )

    parser.add_argument(
        "--validate", action="store_true", help="Valida a consistência do inventário"
    )

    parser.add_argument(
        "--network", action="store_true", help="Mostra informações de rede"
    )

    parser.add_argument(
        "--inventory",
        default="inventory/devices.yml",
        help="Caminho para o arquivo de inventário (padrão: inventory/devices.yml)",
    )

    args = parser.parse_args()

    # Banner inicial
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("📊 NETDEVOPS - ESTATÍSTICAS DO INVENTÁRIO")
    print("=" * 60)
    print(f"⏰ Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Inventário: {args.inventory}")
    print(f"{'=' * 60}{Colors.ENDC}")

    # Carrega inventário
    devices = load_inventory(args.inventory)
    if not devices:
        return

    # Determina o que mostrar
    if args.all:
        show_basic_stats(devices)
        show_network_info(devices)
        validate_inventory(devices)
        show_device_details(devices)
    elif args.details:
        show_device_details(devices)
    elif args.validate:
        validate_inventory(devices)
    elif args.network:
        show_network_info(devices)
    else:
        # Padrão: mostra estatísticas básicas
        show_basic_stats(devices)

    print(f"\n{Colors.BOLD}🏁 Análise concluída!{Colors.ENDC}")


if __name__ == "__main__":
    main()
