from bs4 import BeautifulSoup as bs
from jjcli import *
import yaml
import re

ats = glob("1139-1146/Article.aspx*3302")  # Função glob para obter uma lista de arquivos que têm nomes começando com "Article.aspx" no diretório "ext"
print(ats)

output_data = []

for at in ats:
    with open(at, 'r', encoding="utf-8") as f:
        html = f.read()
        a = bs(html, features="html.parser")

        title = a.find("span", id="ctl00_ContentPlaceHolder1_LabelTitle").get_text(strip=True)
        url = f"http://www.nos.uminho.pt/Article.aspx?id=3302"  # Substitua a URL conforme necessário
        image = a.find("meta", property="og:image").get("content")
        site_name = a.find("meta", property="og:site_name").get("content")
        description = a.find("meta", property="og:description").get("content")

        # Extrair data e autor
        info_span = a.find("span", id="ctl00_ContentPlaceHolder1_LabelInfo")
        date = ""
        author = ""
        if info_span:
            match = re.search(r'(\d{2}-\d{2}-\d{4}) \| (.+)', info_span.text)
            if match:
                date = match.group(1).strip()
                author = match.group(2).strip()

        # Construir o dicionário de dados para este artigo
        article_data = {
            "-Título": title,
            "URL": url,
            "Site": site_name,
            "Imagem": image,
            "Data": date,
            "Autor": author,
            "Sobre": description
            
        }

        output_data.append(article_data)

# Escrever os dados em formato YAML
with open("dados_artigos.yaml", "w", encoding="utf-8") as file:
    yaml.dump(output_data, file, default_flow_style=False, allow_unicode=True)  # Habilita o suporte a caracteres unicode

fo = open("nomes_arquivos.txt", "w", encoding="utf-8")


def processa_slides(art):
    slide_files = []
    for div_slide in art.find_all("div", class_="slide"):
        img_tag = div_slide.find("img")
        if img_tag and img_tag.get("src").endswith(".jpg"):  # Verifica se o src termina com .jpg
            slide_files.append(img_tag.get("src"))
    return slide_files


for at in ats:
    with open(at, 'r', encoding="utf-8") as f:
        content = f.read()
        art = bs(content, 'html.parser')
        slide_files = processa_slides(art)
        with open("nomes_arquivos.txt", "a", encoding="utf-8") as file:
            for filename in slide_files:
                file.write(filename + "\n")