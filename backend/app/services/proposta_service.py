import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from config.settings import TEMPLATE_PROPOSTA_DIR, OUTPUT_DIR, PROPOSTA_ONZE, PROPOSTA_PETRO

env = Environment(loader=FileSystemLoader(TEMPLATE_PROPOSTA_DIR), autoescape=True)

def formatar_moeda(valor):
    if valor is None: valor = 0.0
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_numero(valor):
    return f"{valor:,.0f}".replace(",", ".")

def gerar_pdf_proposta(dados):
    # dados brutos de entrada
    consumo = float(dados.get("consumo", 0))
    tarifa = float(dados.get("tarifa", 0))
    desconto_base = float(dados.get("desconto", 0)) / 100
    
    # valores das bandeiras 
    # por enquanto vamos mantê-los fixos
    
    val_b_verde = 0.0
    val_b_amarela = 0.02989 
    val_b_vermelha1 = 0.04463 
    val_b_vermelha2 = 0.07877 

    def calcular_cenario(v_bandeira_kwh):
        #  bandeira = consumo * valor da bandeira
        valor_bandeira = consumo * v_bandeira_kwh
        #  valor mensal = (consumo * tarifa) + bandeira
        valor_mensal = (consumo * tarifa) + valor_bandeira
        #  valor com desconto = valor mensal * (1 - desconto)
        #  como não é renderizado no pdf, não precisamos desse cálculo, mas fica aqui documentado 
        #  como temos: economia mensal = valor mensal - valor com desconto
        #  podemos fazer somente: economia = valor_mensal * desconto /  
        econ_mes = valor_mensal * desconto_base
        #  economia anual
        econ_ano = econ_mes * 12
        
        return {
            "bandeira": formatar_moeda(valor_bandeira),
            "total": formatar_moeda(valor_mensal),
            "econ_mes": formatar_moeda(econ_mes),
            "econ_ano": formatar_moeda(econ_ano)
        }

    # processamento dos 4 cenários
    verde = calcular_cenario(val_b_verde)
    amarela = calcular_cenario(val_b_amarela)
    v1 = calcular_cenario(val_b_vermelha1)
    v2 = calcular_cenario(val_b_vermelha2)

    # tratamento do prazo (anos ou meses)
    prazo_valor = dados.get("prazo_valor", "5")
    prazo_tipo = dados.get("prazo_tipo", "ANOS").upper()
    prazo_texto = f"{prazo_valor} {prazo_tipo}"

    context = {
        'CLIENTE': dados.get("nome_cliente", "").upper(),
        'consumo': formatar_numero(consumo),
        'consumo_amar': formatar_numero(consumo),
        'consumo_ver1': formatar_numero(consumo),
        'consumo_ver2': formatar_numero(consumo),
        
        # bandeira verde
        'tarifa_verde': formatar_moeda(tarifa),
        'bandeira_verde': verde['bandeira'],
        'valor_verde': verde['total'],
        'desconto_verde': f"{dados.get('desconto')}%",
        'economia_mensal': verde['econ_mes'],
        'economia_anual': verde['econ_ano'],

        # bandeira amarela
        'tarifa_amarela': formatar_moeda(tarifa),
        'valor_band_amar': amarela['bandeira'],
        'valor_total_amar': amarela['total'],
        'desconto_amar': f"{dados.get('desconto')}%",
        'econ_mes_amar': amarela['econ_mes'],
        'econ_ano_amar': amarela['econ_ano'],

        # bandeira vermelha 1
        'tarifa_ver1': formatar_moeda(tarifa),
        'bandeira_ver1': v1['bandeira'],
        'valor_ver1': v1['total'],
        'desconto_ver1': f"{dados.get('desconto')}%",
        'economia_mes1': v1['econ_mes'],
        'economia_ano1': v1['econ_ano'],

        # bandeira vermelha 2
        'tarifa_ver2': formatar_moeda(tarifa),
        'bandeira_ver2': v2['bandeira'],
        'valor_ver2': v2['total'],
        'desconto_ver2': f"{dados.get('desconto')}%",
        'economia_mes2': v2['econ_mes'],
        'economia_ano2': v2['econ_ano'],

        # condições e aceite
        'prazo_contrato': prazo_texto,
        'desconto_geral': dados.get("desconto")
    }

    # define template por empresa
    empresa = dados.get("empresa", "ONZE").upper()
    template_nome = PROPOSTA_ONZE if empresa == "ONZE" else PROPOSTA_PETRO
    
    assets_subfolder = "onze" if empresa == "ONZE" else "petro"

    html_renderizado = env.get_template(template_nome).render(context)

    # salvamento
    nome_arquivo = f"proposta_{dados.get('cliente_id')}_{empresa}.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, nome_arquivo)

    HTML(string=html_renderizado, base_url=TEMPLATE_PROPOSTA_DIR).write_pdf(pdf_path, presentational_hints=True)
    
    return pdf_path