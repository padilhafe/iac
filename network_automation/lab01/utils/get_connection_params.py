NETMIKO_KEYS = {
    "host",
    "username",
    "password",
    "secret",
    "device_type",
    "port",
    "ssh_config_file",
    "use_keys",
    "key_file",
    "allow_agent",
    "timeout",
    "conn_timeout",
    "auth_timeout",
    "session_log",
}

def get_connection_params(device: dict) -> dict:
    return {
        k: v
        for k, v in device.items()
        if k in NETMIKO_KEYS
    }
