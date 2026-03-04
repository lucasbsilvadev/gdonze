import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Core e Services
from core.database import listar_clientes, salvar_registro_db
from services.cobranca_service import gerar_pdf_relatorio
from services.proposta_service import gerar_pdf_proposta
from services.storage_service import StorageService  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/clientes/{empresa}")
def api_listar_clientes(empresa: str):
    return listar_clientes(empresa.upper())

@app.post("/gerar-relatorio")
async def api_gerar_relatorio(dados: dict):
    try:
        # geração do pdf local
        pdf_path, valor_total = gerar_pdf_relatorio(dados)

        # upload para o Cloudinary (Acoplamento do Storage)

        url_pdf_cloud = None
        try:
            url_pdf_cloud = StorageService.upload_cobranca(pdf_path, dados)
        except Exception as storage_err:
            logger.error(f"Erro no upload Cloudinary: {storage_err}")

        # estruturação dos dados
        dados_db = {
            "cliente_id": dados.get("cliente_id"),
            "mes": dados.get("mes"),
            "ano": int(dados.get("ano")),
            "consumo": float(dados.get("consumo", 0)),
            "compensado": float(dados.get("compensado", 0)),
            "valor_total": valor_total,
            "tarifa_aplicada": float(dados.get("tarifa", 0)),
            "desconto_aplicado": float(dados.get("desconto", 0)),
            "valor_fio_b": float(dados.get("fio_b", 0)),
            "url_arquivo": url_pdf_cloud 
        }

        # registro no BD agora somente dos inputs
        salvar_registro_db(dados_db)

        # devolve download 
        nome_final = f"Relatorio_{dados.get('nome_cliente')}_{dados.get('mes')}.pdf".replace(" ", "_")
        return FileResponse(path=pdf_path, filename=nome_final, media_type='application/pdf')

    except Exception as e:
        logger.error(f"erro: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gerar-proposta")
async def api_gerar_proposta(dados: dict):
    try:
        # geração
        pdf_path = gerar_pdf_proposta(dados)

        # upload 
        url_proposta = None
        try:
            url_proposta = StorageService.upload_proposta(pdf_path, dados)
        
        except Exception as storage_err:
            logger.error(f"Erro storage proposta: {storage_err}")

        nome_cliente = dados.get('nome_cliente', 'Cliente').replace(" ", "_")
        nome_final = f"Proposta_{nome_cliente}_{dados.get('empresa', 'ONZE')}.pdf"

        return FileResponse(
            path=pdf_path, 
            filename=nome_final, 
            media_type='application/pdf'
        )

    except Exception as e:
        logger.error(f"erro ao gerar proposta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))