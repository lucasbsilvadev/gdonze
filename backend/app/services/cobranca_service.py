import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from config.settings import TEMPLATE_RELATORIO_DIR, OUTPUT_DIR 

env = Environment(loader=FileSystemLoader(TEMPLATE_RELATORIO_DIR), autoescape=True)

def formatar_moeda(valor):
    """Auxiliar para formatação padrão brasileira de moeda."""
    if valor is None: valor = 0.0
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_valores_cobranca(dados: dict) -> dict:

    consumo = float(dados.get("consumo", 0))
    compensado = float(dados.get("compensado", 0))
    tarifa = float(dados.get("tarifa", 0))
    desconto = float(dados.get("desconto", 0))
    fio_b = float(dados.get("fio_b", 0))

    bruto = compensado * tarifa
    economia = bruto * (desconto / 100)
    total = (bruto - economia) - fio_b

    return {
        "consumo_fmt": f"{consumo:,.0f}".replace(",", "."),
        "compensado_fmt": f"{compensado:,.0f}".replace(",", "."),
        "bruto": bruto,
        "economia": economia,
        "total": total,
        "desconto_label": f"{desconto}%"
    }

def gerar_pdf_relatorio(dados: dict):
    """
    Responsabilidade única: Orquestrar a montagem do PDF.
    Não sabe nada sobre Cloudinary ou Supabase.
    """
    # cálculos
    valores = calcular_valores_cobranca(dados)

    # contexto para o Jinja2
    context = {
        'base_path': TEMPLATE_RELATORIO_DIR, 
        'CLIENTE': dados.get("nome_cliente"),
        'MES': dados.get("mes", "").upper(),
        'ANO': dados.get("ano"),
        'consumo': valores["consumo_fmt"],
        'compensado': valores["compensado_fmt"],
        'tarifa': formatar_moeda(float(dados.get("tarifa", 0))),
        'valor_bruto': formatar_moeda(valores["bruto"]),
        'economia': formatar_moeda(valores["economia"]),
        'fio_b': formatar_moeda(float(dados.get("fio_b", 0))),
        'valor_total': formatar_moeda(valores["total"]),
        'desconto_label': valores["desconto_label"]
    }

    # seleção do tempalte
    template_nome = "modelo_onze.html" if dados.get("empresa") == "ONZE" else "modelo_petro.html"
    
    # renderização
    html_renderizado = env.get_template(template_nome).render(context)
    
    # persistência local
    nome_arquivo = f"relatorio_{dados.get('cliente_id')}_{dados.get('mes')}_{dados.get('ano')}.pdf".replace(" ", "_")
    pdf_path = os.path.join(OUTPUT_DIR, nome_arquivo)

    # geração do pdf - weasyprint
    HTML(string=html_renderizado, base_url=TEMPLATE_RELATORIO_DIR).write_pdf(
        pdf_path, 
        presentational_hints=True
    )
    
    return pdf_path, valores["total"]