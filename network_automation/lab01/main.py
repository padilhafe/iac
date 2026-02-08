import argparse
import yaml
from netmiko import ConnectHandler
from drivers import huawei, routeros7
from render import render_template
from utils import get_connection_params

DRIVERS = {
    "huawei": huawei,
    "routeros7": routeros7,
}


def load_inventory(path="inventory/devices.yml"):
    with open(path) as f:
        return yaml.safe_load(f)["devices"]


def check_ssh(device):
    try:
        conn_params = get_connection_params(device)
        with ConnectHandler(**conn_params) as conn:
            conn.find_prompt()
        return True, "SSH OK"
    except Exception as e:
        return False, str(e)


def apply_config(device):
    config_text = render_template(
        vendor=device["vendor"],
        template_name=device.get("template", "router.j2"),
        dados={
            "hostname": device["name"],
            "interfaces": device.get("interfaces", [])
        }
    )

    config_set = [
        line.strip()
        for line in config_text.splitlines()
        if line.strip()
    ]

    conn_params = get_connection_params(device)

    with ConnectHandler(**conn_params) as conn:
        return DRIVERS[device["vendor"]].send_config(conn, config_set)


def main():
    parser = argparse.ArgumentParser(
        description="NetDevOps mini framework"
    )
    parser.add_argument(
        "action",
        choices=["check", "config"],
        help="check = testa SSH | config = aplica configuração"
    )

    args = parser.parse_args()
    devices = load_inventory()

    for device in devices:
        print(f"\n➡️ {device['name']}")

        if args.action == "check":
            ok, msg = check_ssh(device)
            status = "✅" if ok else "❌"
            print(f"{status} {msg}")

        elif args.action == "config":
            ok, msg = check_ssh(device)
            if not ok:
                print(f"❌ SSH falhou: {msg}")
                continue

            output = apply_config(device)
            print(output)


if __name__ == "__main__":
    main()