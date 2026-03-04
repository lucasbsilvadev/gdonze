import os
from dotenv import load_dotenv

load_dotenv()

# ambiente e credenciais
AMBIENTE = os.getenv("AMBIENTE_ATIVO", "cloud")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# credenciais de armazenamento
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

# config de diretorios base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# caminho de modelos de cobrança
TEMPLATE_RELATORIO_DIR = os.path.join(BASE_DIR, "templates", "html")
TEMPLATE_PROPOSTA_DIR = os.path.join(BASE_DIR, "templates", "propostas")

# caminho de modelos de proposta
PROPOSTA_ONZE = os.getenv("PROPOSTA_ONZE", "modelo_onze.html")
PROPOSTA_PETRO = os.getenv("PROPOSTA_PETRO", "modelo_petro.html")

TEMPLATE_DIR = TEMPLATE_RELATORIO_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)