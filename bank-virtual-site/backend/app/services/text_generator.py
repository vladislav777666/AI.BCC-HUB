from jinja2 import Template, Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

def generate_push_text(template_id: str, variables: dict) -> str:
    template = env.get_template(f"{template_id}.jinja")
    text = template.render(**variables)
    if len(text) < 180:
        text += " Это поможет сэкономить на повседневных расходах."
    if len(text) > 220:
        text = text[:217] + '...'
    return text