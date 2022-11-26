import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv(".env", verbose=True)

from flask import Flask

from application.core.configurations.app_configurations import AppConfigurations
from application.core.managers.blacklist_manager import BlackList
from application.core.managers.cipher_manager import CaesarCipher
from application.core.managers.language_manager import LanguageManager
from application.core.managers.field_validation_manager import FieldsValidationManager

from infrastructure.repositories.repository_manager import repository
from interface.http.adapter import HttpAdapter
from orchestrator import Orchestrator

app = Flask(import_name=__name__,
            static_folder='interface/gui/FrontEnd/build',
            static_url_path='/',
            template_folder='interface/gui/templates')

__black_list_manager = BlackList()
AppConfigurations(app=app, repository=repository, logger=logger)
logger.debug("App Configurations Initialized Successfully")

__caesar_cipher_manager = CaesarCipher()
language_manager = LanguageManager()
field_validator_manager = FieldsValidationManager()
logger.debug("Managers Initialized Successfully")

orchestrator = Orchestrator(app=app,
                            repository=repository,
                            logger=logger,
                            black_list_manager=__black_list_manager,
                            caesar_cipher=__caesar_cipher_manager,
                            language_manager=language_manager,
                            field_validator_manager=field_validator_manager)
use_cases = orchestrator.generate_use_cases_mapper()
logger.debug("Use Cases Initialized Successfully")

http_adapter = HttpAdapter(app=app, black_list_manager=__black_list_manager)
http_adapter.init_http_adapter(use_cases=use_cases)
logger.debug("Resources Initialized Successfully")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
