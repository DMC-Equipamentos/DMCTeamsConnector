import logging
import logging.config

# Sua configuração de logging (adaptada para teste standalone)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'teams_html': {
            'class': 'DMCTeamsConnector.DMCTeamsConnector.DMCTeamsAdaptiveCardFormatter',
        }
    },
    'handlers': {
        'hof_complete': {
            'level': 'DEBUG',
            'class': 'DMCTeamsConnector.DMCTeamsConnector.DMCTeamsLogHandler',
            'formatter': 'teams_html',
            'webhook_url': 'https://default1e94beec1b5d469ebb48646c49fe6c.e8.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/fb6a209f071d4663bcf9eb72d22ec770/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=E2hfsQuiAPOPhuWck1hWwVo6v9CFDFh2dQrdhn9pg-s',
        }
    },
    'loggers': {
        'hof': {
            'handlers': ['hof_complete'],
            'level': 'DEBUG',
        }
    }
}

# Aplica a configuração
logging.config.dictConfig(LOGGING)

# Pega o logger
logger = logging.getLogger("hof")

# Testa logs
logger.warning("", extra={'html': True, 'html_title': 'Uso de fibra em equipamento em produção', 
                        'html_list': [
                            ('Equipamento','{}'.format(123)),
                            ('Modelo', '{}'.format(123)),
                            ('Fibra','{}'.format(123)),
                        ]
                    }
                )

logger.warning("Teste")

print("✅ Teste de logger concluído")