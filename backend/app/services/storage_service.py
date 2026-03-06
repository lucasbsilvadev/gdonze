import cloudinary
import cloudinary.uploader
import os
from config.settings import CLOUDINARY_URL 

cloudinary.config(cloudinary_url=CLOUDINARY_URL)

class StorageService:

  @staticmethod
    def upload_cobranca(file_path, dados):
        try:
            # sanitização
            empresa = str(dados.get('empresa', 'ONZE')).replace(" ", "_")
            ano = str(dados.get('ano', '2026'))
            mes = str(dados.get('mes', 'MES')).upper().replace(" ", "_")
            usina = str(dados.get('usina', 'SEM_USINA')).replace(" ", "_")
            cliente = str(dados.get('nome_cliente', 'CLIENTE')).replace(" ", "_")
            uc = str(dados.get('codigo_uc', 'SEM_UC')).replace(" ", "_")

            # hierarquia de pastas
            folder = f"COBRANCAS_{empresa}/{ano}/{mes}/{usina}/{cliente}/{uc}"
            
            public_id = f"RELATORIO_{cliente}_{uc}_{mes}_{ano}".replace(" ", "_")

            response = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                public_id=public_id,
                resource_type="raw", 
                use_filename=True,
                unique_filename=False 
            )
            
            return response.get("secure_url")

        except Exception as e:

            raise e
            
    @staticmethod
    def upload_cobranca(file_path, dados):
    
        try:
            # hierarquia das pastas
            folder = f"COBRANCAS_{dados.get('empresa')}/{dados.get('ano')}/{dados.get('mes').upper()}"
            
            public_id = f"relatorio_{dados.get('cliente_id')}_{dados.get('mes')}_{dados.get('ano')}".replace(" ", "_")

            # upload
            response = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                public_id=public_id,
                resource_type="raw", 
                use_filename=True,
                unique_filename=False 
            )
            
            return response.get("secure_url")


        except Exception as e:
            
            raise e

    
