import cloudinary
import cloudinary.uploader
import logging
from config.settings import CLOUDINARY_URL

cloudinary.config(cloudinary_url=CLOUDINARY_URL)
logger = logging.getLogger(__name__)

class StorageService:

    @staticmethod
    def _sanitizar(texto):
        return str(texto).replace(" ", "_").replace("/", "-")

    @staticmethod
    def upload_cobranca(file_path, dados):
        try:
            empresa = StorageService._sanitizar(dados.get('empresa', 'ONZE'))
            ano = StorageService._sanitizar(dados.get('ano', '2026'))
            mes = StorageService._sanitizar(dados.get('mes', 'MES')).upper()
            usina = StorageService._sanitizar(dados.get('usina', 'SEM_USINA'))
            cliente = StorageService._sanitizar(dados.get('nome_cliente', 'CLIENTE'))
            uc = StorageService._sanitizar(dados.get('codigo_uc', 'SEM_UC'))

            folder = f"COBRANCAS_{empresa}/{ano}/{mes}/{usina}/{cliente}/{uc}"
            public_id = f"RELATORIO_{cliente}_{uc}_{mes}_{ano}"

            response = cloudinary.uploader.upload(
                file_path, folder=folder, public_id=public_id,
                resource_type="raw", use_filename=True, unique_filename=False
            )
            return response.get("secure_url")
        except Exception as e:
            logger.error(f"Erro no upload de cobrança: {e}")
            raise e

    @staticmethod
    def upload_proposta(file_path, dados):
        try:
            empresa = StorageService._sanitizar(dados.get('empresa', 'ONZE'))
            cliente = StorageService._sanitizar(dados.get('nome_cliente', 'CLIENTE'))

            folder = f"PROPOSTAS_{empresa}/{cliente}"
            public_id = f"PROPOSTA_{cliente}_{empresa}"

            response = cloudinary.uploader.upload(
                file_path, folder=folder, public_id=public_id,
                resource_type="raw", use_filename=True, unique_filename=False
            )
            return response.get("secure_url")
        except Exception as e:
            logger.error(f"Erro no upload de proposta: {e}")
            raise e
