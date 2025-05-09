import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からトークンを取得
hf_token = os.getenv("HUGGING_FACE_TOKEN")

# トークンを使用してモデルをロード
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    token=hf_token
)