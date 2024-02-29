from jjcli import* 

from bs4 import BeautifulSoup as bs 


ats = glob("1139-1146/Article.aspx*3302") #Função glob para obter uma lista de arquivos que têm nomes começando com "Article.aspx" no diretório "ext"
print(ats)

fo = open("saida1.txt", "w", encoding = "utf-8")  #Abre um arquivo chamado "saida.txt" no modo de escrita ("w") 


def proc_data(html):
    a = bs(html, features="html.parser")
    dt = ""
    for span in a.find_all("span", id="ctl00_ContentPlaceHolder1_LabelInfo"):
        data = span.get_text(strip=True)  # Obtém o texto dentro da tag <span>
        if not data:  # Se não houver texto, continue para a próxima iteração
            continue
        dt += f"{data}\n"  # Adiciona a data à variável dt
    print("===========\n", dt, a.get_text(), file=datas_ext)


def proc_article(html): #Define uma função chamada proc_article que recebe uma string HTML como argumento.
    # Processa um ficheiro Article.aspx@id=\d\d\d\d do jornal NOSuminho
    #print(len(html))  #está a contar os caracteres de cada artigo
    a = bs(html, features="html.parser")  #cria uma árvore
    cabecalho = "" 
    for meta in a.find_all("meta"):
        p = meta.get("property") #Itera sobre todas as tags "meta" no HTML, extrai o atributo "property"
        if p is None:
            continue
        p = p.replace("og:", "") #se existir, remove o prefixo "og:"
        cabecalho += f"{p}: {meta.get('content')}\n" #constrói uma string chamada cabecalho com o nome da propriedade e seu conteúdo.
        divisao = "==================="
        #print(p, ":" , meta.get("content"))
    art = a.find("div", id="artigo")
    corpo = proc_art_contents(art)
    print("==========\n", cabecalho, divisao, corpo, file = fo)

datas_ext = open("datas.txt", "w", encoding="UTF-8")


def proc_art_contents(art):
    for tag in art.find_all("div", class_="voltar"): tag.extract()
    for tag in art.find_all("div", id="slidesjs-log"): tag.decompose() 
    for tag in art.find_all("ul", class_="socialcount"): tag.decompose() 
    for tag in art.find_all("div", id="slides"):
        slides= tag.extract() 
    #FIXME processar slides
    for tag in art.find_all("table"): 
        tag.insert(0, "\n##Tabela")
    for strong_tag in art.find_all("strong"):
        strong_tag.replace_with(bs(str(strong_tag).replace('<strong>', '<b>').replace('</strong>', '</b>'), 'html.parser'))
    finalt = art.get_text()
    finalt = re.sub(r"\n{3,}",r"\n\n",finalt)
    return art


for file in ats: #Itera sobre a lista de arquivos obtida anteriormente. Para cada arquivo, lê o conteúdo HTML, chama a função proc_article para processar o HTML e extrair informações relevantes, e imprime os resultados no arquivo de saída.
    with open (file, encoding="utf-8") as f:
        html = f.read()
    proc_data(html)


for file in ats: #Itera sobre a lista de arquivos obtida anteriormente. Para cada arquivo, lê o conteúdo HTML, chama a função proc_article para processar o HTML e extrair informações relevantes, e imprime os resultados no arquivo de saída.
    with open (file, encoding="utf-8") as f:
        html = f.read()
    proc_article(html)







"""<meta property='og:title' content='A nova bengala robótica'/><meta property='og:url' content='http://www.nos.uminho.pt/Article.aspx?id=3686'/><meta property='og:image' content='http://www.nos.uminho.pt/Images/destaques/20231222192503_Bengala1a.jpg'/><meta property='og:site_name' content='Jornal Online UMINHO A nova bengala robótica'/><meta property='og:description' content='

'/><meta property='og:type' content='blog'/>

<div id="artigo">
                    <div class="title">
                        
                        <div class="voltar">


<h1>
                        <span id="ctl00_ContentPlaceHolder1_LabelTitle">A nova bengala robótica</span></h1>
                    <span class="creditos">
                        <span id="ctl00_ContentPlaceHolder1_LabelInfo">22-12-2023 | Beatriz Mendes | Fotos: BirdLab</span>
                    </span>


"""


