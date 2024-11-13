# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

#IMPORTAÇÕES ASK ALEXA SKILLS
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_model.services.reminder_management import ReminderManagementServiceClient
from ask_sdk_model.services import ServiceException
from ask_sdk_core.utils import is_request_type
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# IMPORTAÇÕES PARA REQUISIÇÃO API
import json
import requests
import os.path
import datetime

#IMPORTANDO CLASSES
from API import Remedio
from Funcoes import Lembrete, Driver


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


#INSTANCIANDO OS OBJETOS
Remedio = Remedio()
Lembrete = Lembrete()
Driver = Driver()



from ask_sdk_model.services.reminder_management import (
    ReminderRequest, Trigger, TriggerType, AlertInfo, SpokenInfo, SpokenText)

import json
import requests



def Credenciais():
    credentials_path = r"token.json"
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes)
    
    return creds

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Mensagem de boas-vindas e opções caso a permissão seja concedida
        speak_output = "Bem-vindo, me chamo JARVIS. você deseja Cadastro Remédio?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class CadastroIntents(AbstractRequestHandler):
    """Handler for Skill Launch."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CadastroIntents")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        

        # Mensagem de boas-vindas e opções caso a permissão seja concedida
        speak_output = "Qual o nome do Remédio para registrar ?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ConsultaIntents(AbstractRequestHandler):
    """Handler for Skill Launch."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ConsultaIntents")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        

        # Mensagem de boas-vindas e opções caso a permissão seja concedida
        speak_output = "Resultado da Consulta"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class registrarRemedioIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RegistroRemedio")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        nomeRemedio = handler_input.request_envelope.request.intent.slots.get('nomeremedio')
        
        remedio = nomeRemedio.value
        Remedio.nome(remedio)
        
        speak_output = "Qual a descrição do remedio "+remedio+" ?"
        return (
        handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class registrarDescricaoIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("descricao_remedio")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        descricaoRemedio = handler_input.request_envelope.request.intent.slots.get('descricao_do_remedio')
        if descricaoRemedio and descricaoRemedio.value:
            
            descricao = descricaoRemedio.value
            Remedio.descricao(descricao)
            speak_output = "Qual a dosagem ?"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )
        else:
            speak_output = "Qual a descrição do remédio ?"
            return(
                handler_input.response.builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
                )
        


class registrarDosagemIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Dosagem")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        doseRemedio = handler_input.request_envelope.request.intent.slots.get('dose')
        dose = doseRemedio.value
        
        if doseRemedio and doseRemedio.value:
            Remedio.dosagem(dose)
            speak_output = "Qual horario eu devo te lembrar ?"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )
        else:
            speak_output = "Qual a dosagem ? "
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )



class registrarHorarioIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Horario_Remedio")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        permissions = handler_input.request_envelope.context.system.user.permissions
        horarioRemedio = handler_input.request_envelope.request.intent.slots.get('horas')
        hora = horarioRemedio.value
        
        token = permissions.consent_token
        Mensagem = "chegou a hora de tomar o "+str(Remedio.infoNome())+" remedio com a descrição: "+ str(Remedio.infoDescricao())
        duracao = Remedio.infohorario()
        
        print("Duração###########")
        print(duracao)
        Remedio.horario(hora)
        print(Remedio.infoRemedio())
        
        lembrete = Lembrete.CriandoLembrete(token,Mensagem , Remedio.infohorario(),recurrence={"freq": "DAILY"})
        if lembrete == 201:
            speak_output = str(Remedio.nomeRemedio)+" cadastrado com sucesso"
            Driver.cadastroRemedio(Remedio.infoRemedio())
        else:
            speak_output = "Ocorreu um erro código - "+lembrete
            print("Errroooo")
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Obrigado por utlizar os serviços Stark!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )





class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Desculpe, não consegui entender o que você quer dizer. "
            "Você pode tentar pedir para cadastrar"
        )

        # Log da entrada para depuração
        print("FallbackIntentHandler acionado.")
        print(f"Entrada do usuário: {handler_input.request_envelope.request.intent}")

        return handler_input.response_builder.speak(speak_output).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Você acabou de acionar " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, tive problemas para fazer o que você pediu. Por favor, tente novamente.",error

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CadastroIntents())
sb.add_request_handler(ConsultaIntents())
sb.add_request_handler(registrarRemedioIntentHandler()) 
sb.add_request_handler(registrarDescricaoIntentHandler())
sb.add_request_handler(registrarHorarioIntentHandler())
sb.add_request_handler(registrarDosagemIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) 
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
