import os.path
import sys

from fastapi.middleware.cors import CORSMiddleware

import colorama

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from openai_tf_idf.controller.openai_tf_idf_controller import openAITfIdfRouter
from user_defined_initializer.init import UserDefinedInitializer
from tf_idf_bow.controller.tf_idf_bow_controller import tfIdfBowRouter

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))

from template.deep_learning.controller.deep_learning_controller import deepLearningRouter
from template.dice.controller.dice_controller import diceResultRouter
from template.include.socket_server.initializer.init_domain import DomainInitializer
from template.system_initializer.init import SystemInitializer
from template.task_manager.manager import TaskManager

DomainInitializer.initEachDomain()
SystemInitializer.initSystemDomain()
UserDefinedInitializer.initUserDefinedDomain()

app = FastAPI()

load_dotenv()

origins = os.getenv('ALLOWED_ORIGINS', '').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(deepLearningRouter)
app.include_router(diceResultRouter)

app.include_router(tfIdfBowRouter)
app.include_router(openAITfIdfRouter)

if __name__ == "__main__":
    colorama.init(autoreset=True)

    TaskManager.createSocketServer()
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))