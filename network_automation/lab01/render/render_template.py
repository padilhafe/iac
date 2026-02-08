from jinja2 import Environment, FileSystemLoader

def render_template(vendor, template_name, dados):
    env = Environment(
        loader=FileSystemLoader("templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(f"{vendor}/{template_name}")
    return template.render(dados)
