import logging
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

# logs para monitoramento 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL ou SUPABASE_KEY não configurados no ambiente.")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Conexão com Supabase estabelecida com sucesso.")
except Exception as e:
    logger.error(f"Falha ao inicializar cliente Supabase: {e}")
    supabase = None

def listar_clientes(empresa_filtro: str = None):

    if not supabase: return []
    
    try:
        query = supabase.table("clientes").select("*").eq("status", "ativo")
        
        if empresa_filtro and empresa_filtro.upper() != "AMBAS":
            query = query.eq("empresa", empresa_filtro.upper())
            
        response = query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Erro ao listar clientes no Supabase: {e}")
        return []

def salvar_registro_db(dados_db: dict):
    if not supabase:
        raise ConnectionError("Cliente Supabase não inicializado.")

    try:
        # mapeamento de atributos para garantir correspondência com db
        payload = {
            "cliente_id": dados_db.get("cliente_id"),
            "mes": dados_db.get("mes"),
            "ano": dados_db.get("ano"),
            "consumo": dados_db.get("consumo"),
            "compensado": dados_db.get("compensado"),
            "valor_total": dados_db.get("valor_total"),
            "url_arquivo": dados_db.get("url_arquivo"), 
            "tarifa_aplicada": dados_db.get("tarifa_aplicada"),
            "desconto_aplicado": dados_db.get("desconto_aplicado"),
            "valor_fio_b": dados_db.get("valor_fio_b"),
            "codigo_uc_id": dados_db.get("codigo_uc_id"),
            "empresa": dados_db.get("empresa"),
            "status": "CONCLUIDO"
        }

        response = supabase.table("lancamentos").insert(payload).execute()
        logger.info(f"Lançamento registrado com sucesso para o cliente {dados_db.get('cliente_id')}")
        return response.data
    except Exception as e:
        logger.error(f"Erro ao salvar lançamento: {e}")
        raise e

def salvar_proposta_db(dados_proposta: dict, url_pdf: str):
    if not supabase: return None

    try:
        payload = {
            "cliente_id": dados_proposta.get("cliente_id"),
            "empresa": dados_proposta.get("empresa"),
            "dados_json": dados_proposta,
            "url_pdf": url_pdf
        }
        response = supabase.table("propostas").insert(payload).execute()
        return response.data
    except Exception as e:
        logger.error(f"Erro ao salvar proposta: {e}")
        return None