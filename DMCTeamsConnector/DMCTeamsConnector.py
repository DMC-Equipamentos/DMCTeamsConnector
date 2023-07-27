from urllib import request as req
import logging
import json

class DMCTeamsWebhookException(Exception):
    pass

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
        
        # envia mensagem HTML
        self.sendHtmlMessage(html_format.format(title = data['title'], list=list))
        

class DMCTeamsLogHandler(logging.Handler):
    """
    Gerente de logs DMC para enviar mensagem para o TEAMS
    """
    
    def __init__(self, webhook_url):
        
        super().__init__()
        # inicia connector com o teams baseado na url recebida
        self.webhook_url = webhook_url
        self.conn = DMCTeamsConnector(self.webhook_url)
    
    def emit(self, record):
        self.conn.sendHtmlMessage(record)