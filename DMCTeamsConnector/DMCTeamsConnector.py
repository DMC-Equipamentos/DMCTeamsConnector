from urllib import request as req
import logging
import json
from threading import Thread

class DMCTeamsWebhookException(Exception):
    pass

def formatHtmlList(data):
    """
    Trata um dicionário e transforma em uma mensagem HTML
    ex.
    data = {
        "title": "Título teste",
        "list": [
            ('Campo 1', 'Valor 1'),
            ('Campo 2', 'Valor 2'),
        ]
    }
    """
    
    # string com formato HTML X
    html_format = """

        <h1> {title} </h1>
        
        <ul> 
            {list}
        </ul>
        
    """.strip() # Não pode ter trailing spaces
    
    # transforma lista em HTML
    list = ["<li> <strong>{}:</strong> {} </li>".format(v, d) for v, d in data['list']]
    list = "".join(list)
    
    html = html_format.format(title = data['title'], list=list)
    
    return html

class DMCTeamsConnector():
    """
    Connector para enviar mensagem para o Teams
    """
    
    def __init__(self, webhook_url):
        self.url = webhook_url
        
    def sendHtmlMessage(self, html):
        """
        Manda um html como uma mensagem JSON para o teams
        """
        
        # cria um request JSON para o webhook do teams
        request = req.Request(url=self.url, method="POST")
        request.add_header("Content-Type", "application/json;charset=UTF-8")
        
        # o request deve ser enviado codificado em um JSON
        post_data = json.dumps({"text": html}).encode()
        
        # envia request
        response = req.urlopen(url=request, data=post_data)
        
        # Levanta um erro caso resposta não seja 200
        if response.status != 200:
            raise DMCTeamsWebhookException(response.reason) # Trata erros
        
    def sendHtmlListMessage(self, data):
        """
        Formata os dados em HTML como uma lista
        """
        
        # envia mensagem HTML
        self.sendHtmlMessage(formatHtmlList(data))
        

class DMCTeamsLogHandler(logging.Handler):
    """
    Gerente de logs DMC para enviar mensagem para o TEAMS
    """
    
    def __init__(self, webhook_url):
        
        super().__init__()
        self.message = "" # mensagem que será enviada
        
        # inicia connector com o teams baseado na url recebida
        self.webhook_url = webhook_url
        self.conn = DMCTeamsConnector(self.webhook_url)
        
    def sendInAnotherThread(self, message):
        """
        Envia mensagem pelo team em outra thread
        """
        thread = Thread(target = self.conn.sendHtmlMessage, args = (message, ))
        thread.start()
    
    def emit(self, record):
        try:
            self.sendInAnotherThread(self.format(record))
        except:
            print("ERROR!!")
            pass
        
class DMCTeamsHtmlFormatter(logging.Formatter):
    
    def format(self, record):
        
        # verifica se foi passado para o logger um argumento para html
        if 'html' in record.__dict__ and record.html: 
            return formatHtmlList({
                'title': "{}: {}".format(logging.getLevelName(record.levelno), record.html_title),
                'list': record.html_list
            })
        else: # senão retorna apenas a mensagem
            return "{}: {}".format(logging.getLevelName(record.levelno), record.msg)
        