import re
def extract_basic_info(text):
    template_match = re.search(r'{{基礎情報 国(.*?)\n}}', text, re.DOTALL)
    if not template_match:
        return {}