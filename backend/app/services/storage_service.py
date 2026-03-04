import cloudinary
import cloudinary.uploader
import os
from config.settings import CLOUDINARY_URL 

cloudinary.config(cloudinary_url=CLOUDINARY_URL)

class StorageService:

    @staticmethod
    def upload_proposta(file_path, dados):

        try:
            # estrutura de pasta e nome do arquivo "Proposta Comercial - Onze/Petro - Cliente - Mês - Ano"
            empresa = dados.get('empresa', 'ONZE')
            cliente = dados.get('nome_cliente', 'Cliente').replace(" ", "_")
            ano = dados.get('ano', '2026')
            mes = dados.get('mes', 'MES').upper() 
            
            folder = f"PROPOSTAS_{empresa}/{cliente}/{ano}_{mes}"
            
            public_id = f"proposta_{dados.get('cliente_id')}_{ano}_{mes}".replace(" ", "_")

            print(f"DEBUG STORAGE: Iniciando upload para: {folder}/{public_id}") # remover em prod

            response = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                public_id=public_id,
                resource_type="raw", 
                use_filename=True,
                unique_filename=False
            )
            
            print(f"Sucesso! Resposta: {response}")
            return response.get("secure_url")

        except Exception as e:
            print(f"debug storage: erro no upload da proposta: {str(e)}")
            raise e
    @staticmethod
    def upload_cobranca(file_path, dados):
    
        try:
            # hierarquia das pastas
            folder = f"COBRANCAS_{dados.get('empresa')}/{dados.get('ano')}/{dados.get('mes').upper()}"
            
            public_id = f"relatorio_{dados.get('cliente_id')}_{dados.get('mes')}_{dados.get('ano')}".replace(" ", "_")

            print(f"DEBUG: Tentando upload para pasta: {folder}") # remover em prod

            # upload
            response = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                public_id=public_id,
                resource_type="raw", 
                use_filename=True,
                unique_filename=False 
            )
            
            print(f"DEBUG: Resposta Cloudinary: {response}") # remover em prod 
            
            # retorna a URL segura
            return response.get("secure_url")


        except Exception as e:
            
            raise e

    