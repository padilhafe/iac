import argparse
import time
from datetime import datetime

import yaml
from netmiko import ConnectHandler

from drivers import huawei_vrp5, huawei_vrp8, routeros7
from render import render_template
from utils import get_connection_params


# Códigos de cor ANSI
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


DRIVERS = {
    "huawei_vrp5": huawei_vrp5,
    "huawei_vrp8": huawei_vrp8,
    "routeros7": routeros7,
}


def load_inventory(path="inventory/devices.yml"):
    with open(path) as f:
        return yaml.safe_load(f)["devices"]


def print_device_header(device):
    """Imprime cabeçalho bonito para cada dispositivo"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}🔧 Dispositivo: {device['name']}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}   📍 Host: {device['host']}")
    print(f"   🏷️  Vendor: {device['vendor']}")
    print(f"   🔌 Device Type: {device['device_type']}")
    print(f"   📋 Template: {device.get('template', 'router.j2')}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'-' * 60}{Colors.ENDC}")


def check_ssh(device):
    """Verifica conectividade SSH com melhor feedback"""
    print(f"{Colors.WARNING}🔍 Testando conectividade SSH...{Colors.ENDC}")
    start_time = time.time()

    try:
        conn_params = get_connection_params(device)
        with ConnectHandler(**conn_params) as conn:
            prompt = conn.find_prompt()

        elapsed = time.time() - start_time
        return True, f"SSH OK - Prompt: {prompt.strip()} (⏱️ {elapsed:.2f}s)"
    except Exception as e:
        elapsed = time.time() - start_time
        return False, f"SSH FALHOU: {str(e)} (⏱️ {elapsed:.2f}s)"


def apply_config(device, template_override=None, dry_run=False):
    """Aplica configuração com feedback detalhado"""
    print(f"{Colors.WARNING}📝 Renderizando template...{Colors.ENDC}")

    # Determina template usando ordem de prioridade:
    # 1. Template especificado via --template
    # 2. Template especificado no inventário do dispositivo
    # 3. Fallback para default.j2
    if template_override:
        template_name = template_override
        print(
            f"   {Colors.OKCYAN}📋 Usando template especificado: {template_name}{Colors.ENDC}"
        )
    elif device.get("template"):
        template_name = device.get("template")
        print(
            f"   {Colors.OKCYAN}📋 Usando template do inventário: {template_name}{Colors.ENDC}"
        )
    else:
        template_name = "default.j2"
        print(
            f"   {Colors.WARNING}📋 Usando template padrão (fallback): {template_name}{Colors.ENDC}"
        )

    config_text = render_template(
        vendor=device["vendor"],
        template_name=template_name,
        dados={"hostname": device["name"], "interfaces": device.get("interfaces", [])},
    )

    config_set = [line.strip() for line in config_text.splitlines() if line.strip()]

    print(f"{Colors.OKCYAN}📋 Configuração a ser aplicada:")
    print(f"   {Colors.BOLD}Template:{Colors.ENDC} {template_name}")
    print(f"   {Colors.BOLD}Linhas de config:{Colors.ENDC} {len(config_set)}")
    print(f"   {Colors.BOLD}Driver:{Colors.ENDC} {device['vendor']}")

    if dry_run:
        print(
            f"   {Colors.WARNING}🧪 Modo DRY-RUN ativo - NÃO será aplicado!{Colors.ENDC}"
        )

    # Mostra preview completo no dry-run, senão apenas as primeiras 3 linhas
    preview_lines = config_set if dry_run else config_set[:3]
    for i, line in enumerate(preview_lines):
        print(f"   {Colors.OKBLUE}  {line}{Colors.ENDC}")

    if not dry_run and len(config_set) > 3:
        print(f"   {Colors.OKBLUE}  ... (+{len(config_set) - 3} linhas){Colors.ENDC}")

    # Verifica se tem comandos que mudam hostname
    has_hostname_change = any("sysname" in cmd for cmd in config_set)
    if has_hostname_change:
        print(
            f"   {Colors.WARNING}⚠️  ATENÇÃO: Configuração altera hostname - pode causar problemas no Netmiko{Colors.ENDC}"
        )
        print(
            f"   {Colors.WARNING}💡 Dica: Use template 'router_no_hostname.j2' para evitar isso{Colors.ENDC}"
        )

    if dry_run:
        print(
            f"{Colors.OKGREEN}✅ Dry-run concluído - configuração NÃO foi aplicada{Colors.ENDC}"
        )
        return "DRY-RUN: Configuração validada mas não aplicada"

    print(f"{Colors.WARNING}🚀 Aplicando configuração...{Colors.ENDC}")
    start_time = time.time()

    conn_params = get_connection_params(device)

    with ConnectHandler(**conn_params) as conn:
        output = DRIVERS[device["vendor"]].send_config(conn, config_set)

    elapsed = time.time() - start_time
    print(
        f"{Colors.OKGREEN}✅ Configuração aplicada com sucesso! (⏱️ {elapsed:.2f}s){Colors.ENDC}"
    )

    return output


def list_available_devices():
    """Lista todos os dispositivos disponíveis"""
    devices = load_inventory()
    print(f"{Colors.BOLD}{Colors.HEADER}📋 Dispositivos Disponíveis:{Colors.ENDC}")
    print(f"{Colors.HEADER}{'-' * 60}{Colors.ENDC}")

    for device in devices:
        print(
            f"{Colors.OKCYAN}• {device['name']:<20}{Colors.ENDC} "
            f"{Colors.OKBLUE}({device['vendor']}) - {device['host']}{Colors.ENDC}"
        )

    print(f"{Colors.HEADER}{'-' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}Total: {len(devices)} dispositivos{Colors.ENDC}")


def list_available_templates():
    """Lista todos os templates disponíveis por vendor"""
    import os

    print(f"{Colors.BOLD}{Colors.HEADER}📋 Templates Disponíveis:{Colors.ENDC}")
    print(f"{Colors.HEADER}{'-' * 60}{Colors.ENDC}")

    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        print(
            f"{Colors.FAIL}❌ Diretório de templates não encontrado: {templates_dir}{Colors.ENDC}"
        )
        return

    for vendor in sorted(os.listdir(templates_dir)):
        vendor_path = os.path.join(templates_dir, vendor)
        if os.path.isdir(vendor_path):
            print(f"\n{Colors.OKCYAN}📁 {vendor}:{Colors.ENDC}")

            templates = [f for f in os.listdir(vendor_path) if f.endswith(".j2")]
            if templates:
                for template in sorted(templates):
                    if template == "default.j2":
                        print(
                            f"  • {Colors.OKGREEN}{template:<25}{Colors.ENDC} (fallback padrão)"
                        )
                    elif "hostname" in template:
                        print(
                            f"  • {Colors.WARNING}{template:<25}{Colors.ENDC} (sem mudança de hostname)"
                        )
                    else:
                        print(f"  • {Colors.OKBLUE}{template:<25}{Colors.ENDC}")
            else:
                print(f"  {Colors.FAIL}❌ Nenhum template encontrado{Colors.ENDC}")

    print(f"\n{Colors.BOLD}💡 Ordem de prioridade:{Colors.ENDC}")
    print(f"  1. {Colors.OKCYAN}--template <nome>{Colors.ENDC} (linha de comando)")
    print(
        f"  2. {Colors.OKCYAN}template no YAML{Colors.ENDC} (inventário do dispositivo)"
    )
    print(f"  3. {Colors.OKGREEN}default.j2{Colors.ENDC} (fallback automático)")


def print_summary(results, action):
    """Imprime resumo final"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}")
    print(f"📊 RESUMO FINAL - {action.upper()}")
    print(f"{'=' * 60}{Colors.ENDC}")

    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)

    print(f"{Colors.BOLD}Total de dispositivos: {total_count}")
    print(f"✅ Sucessos: {Colors.OKGREEN}{success_count}{Colors.ENDC}")
    print(f"❌ Falhas: {Colors.FAIL}{total_count - success_count}{Colors.ENDC}")

    if success_count < total_count:
        print(f"\n{Colors.WARNING}Dispositivos com falha:{Colors.ENDC}")
        for result in results:
            if not result["success"]:
                print(
                    f"  {Colors.FAIL}❌ {result['device']}: {result['error']}{Colors.ENDC}"
                )


def main():
    parser = argparse.ArgumentParser(
        description="🚀 NetDevOps Framework - Automação de Rede",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📚 Exemplos de uso:
  python main.py list                              # Lista todos os dispositivos disponíveis
  python main.py templates                         # Lista todos os templates disponíveis
  python main.py check                             # Testa SSH em todos os dispositivos
  python main.py config                            # Aplica config em todos os dispositivos
  python main.py check huawei-ne40                 # Testa SSH apenas no huawei-ne40
  python main.py config huawei-ar1000v             # Aplica config apenas no huawei-ar1000v
  python main.py config --dry-run                  # Mostra config sem aplicar (todos)
  python main.py config huawei-ne40 --dry-run      # Mostra config sem aplicar (específico)
  python main.py config --template router_no_hostname.j2  # Usa template específico

🔄 Ordem de prioridade para templates:
  1. --template <nome>   # Template especificado na linha de comando
  2. template no YAML    # Template especificado no inventário do dispositivo
  3. default.j2         # Template padrão usado como fallback automático

🏷️  Drivers disponíveis:
  huawei_vrp5    # Huawei VRP 5.x (sem commit)
  huawei_vrp8    # Huawei VRP 8.x (com commit)
  routeros7      # MikroTik RouterOS 7.x

📋 Templates disponíveis:
  default.j2             # Template padrão usado como fallback
  router.j2              # Template completo (inclui mudança de hostname)
  router_no_hostname.j2  # Template sem mudança de hostname (mais seguro)

⚠️  Nota: Certifique-se de que o inventário (inventory/devices.yml) está atualizado!
        """,
    )
    parser.add_argument(
        "action",
        choices=["list", "templates", "check", "config"],
        help="list = lista dispositivos | templates = lista templates | check = testa SSH | config = aplica configuração",
    )
    parser.add_argument(
        "device_name",
        nargs="?",
        help="Nome do dispositivo específico (opcional). Se não fornecido, executa em todos.",
    )
    parser.add_argument(
        "--template",
        help="Template específico a usar (ex: router_no_hostname.j2)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostra a configuração que seria aplicada, sem executar",
    )

    args = parser.parse_args()

    # Se a ação for 'list', apenas lista os dispositivos e sai
    if args.action == "list":
        list_available_devices()
        return

    # Se a ação for 'templates', apenas lista os templates e sai
    if args.action == "templates":
        list_available_templates()
        return

    # Validação: se passou device_name mas não é check nem config
    if args.device_name and args.action not in ["check", "config"]:
        print(
            f"{Colors.FAIL}❌ Nome de dispositivo só pode ser usado com 'check' ou 'config'{Colors.ENDC}"
        )
        return

    all_devices = load_inventory()

    # Filtra dispositivos se um nome específico foi fornecido
    if args.device_name:
        devices = [d for d in all_devices if d["name"] == args.device_name]
        if not devices:
            print(
                f"{Colors.FAIL}❌ Dispositivo '{args.device_name}' não encontrado!{Colors.ENDC}"
            )
            print(
                f"{Colors.WARNING}💡 Dica: Use 'python main.py list' para ver todos os dispositivos{Colors.ENDC}"
            )
            print(f"{Colors.WARNING}Dispositivos disponíveis:{Colors.ENDC}")
            for device in all_devices:
                vendor_info = f"({device['vendor']})"
                print(
                    f"  • {Colors.OKCYAN}{device['name']:<20}{Colors.ENDC} {Colors.OKBLUE}{vendor_info}{Colors.ENDC}"
                )
            return
        print(
            f"{Colors.OKCYAN}🎯 Filtrado para dispositivo: {args.device_name}{Colors.ENDC}"
        )
    else:
        devices = all_devices

    # Banner inicial
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("🚀 NETDEVOPS FRAMEWORK")
    print("=" * 60)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Ação: {args.action.upper()}")
    if args.device_name:
        print(f"🎯 Dispositivo: {args.device_name}")
    print(f"📊 Dispositivos: {len(devices)} de {len(all_devices)} total")
    print(f"{'=' * 60}{Colors.ENDC}")

    results = []
    total_start_time = time.time()

    for i, device in enumerate(devices, 1):
        print_device_header(device)
        print(f"{Colors.BOLD}📍 Progresso: {i}/{len(devices)}{Colors.ENDC}")

        result = {"device": device["name"], "success": False, "error": None}

        if args.action == "check":
            ok, msg = check_ssh(device)
            result["success"] = ok
            if ok:
                print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")
            else:
                result["error"] = msg
                print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")

        elif args.action == "config":
            ok, msg = check_ssh(device)
            if not ok:
                result["error"] = f"SSH: {msg}"
                print(f"{Colors.FAIL}❌ SSH falhou: {msg}{Colors.ENDC}")
            else:
                try:
                    output = apply_config(device, args.template, args.dry_run)
                    result["success"] = True

                    # Mostra saída de forma organizada
                    if output.strip():
                        print(f"\n{Colors.OKCYAN}📄 Saída do dispositivo:{Colors.ENDC}")
                        for line in output.strip().split("\n"):
                            if line.strip():
                                print(f"   {Colors.OKBLUE}{line}{Colors.ENDC}")

                except Exception as e:
                    result["error"] = f"Config: {str(e)}"
                    print(f"{Colors.FAIL}❌ Erro na configuração: {e}{Colors.ENDC}")

        results.append(result)

    # Resumo final
    total_elapsed = time.time() - total_start_time
    print_summary(results, args.action)
    print(f"\n{Colors.BOLD}⏱️  Tempo total: {total_elapsed:.2f}s")
    print(f"🏁 Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")


if __name__ == "__main__":
    main()
