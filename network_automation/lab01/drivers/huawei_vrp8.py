def send_config(conn, config_set):
    """
    Envia configurações para dispositivos Huawei que requerem commit
    (como VRPv8)
    """
    # Captura o prompt original antes das mudanças
    original_prompt = conn.find_prompt()

    # Envia as configurações
    output = conn.send_config_set(config_set)

    # Se o hostname foi alterado, o prompt mudou, então refaz a detecção
    if any("sysname" in cmd for cmd in config_set):
        # Aguarda um pouco para o sistema atualizar o prompt
        import time

        time.sleep(2)

        # Força nova detecção do prompt antes do commit
        try:
            new_prompt = conn.find_prompt()
            output += f"\n[INFO] Prompt alterado de '{original_prompt.strip()}' para '{new_prompt.strip()}'"
        except Exception as e:
            output += f"\n[WARNING] Erro na detecção do novo prompt: {str(e)}"

    # Executa o comando commit para salvar as configurações
    commit_output = conn.send_command("commit")

    # Combina as saídas para retorno completo
    return output + "\n" + commit_output
