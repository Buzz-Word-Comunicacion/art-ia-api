from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from openai import OpenAI
import json
import configparser

from models.validations import StatementInput, Questionnaire, QuestionnaireResultsList

from .db import save_questions, save_user_rank, get_questions

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

config = configparser.ConfigParser()
config.read("config.ini")

model = "gpt-3.5-turbo"

client = OpenAI(
    api_key=config["misc-keys"]["openai_key"]
)

prompt_statatements = '''
Genera XXXNUMEROPREGUNTASXXX preguntas de educación financiera en la siguiente estructura JSON (todas las preguntas ponlas dentro de un solo JSON):

{
  "questions": [
    {
      "statement": "¿Pregunta sobre educación financiera?",
      "answer1": "Opción de respuesta 1",
      "answer2": "Opción de respuesta 2",
      "answer3": "Opción de respuesta 3",
      "correct": "Número de la respuesta correcta (1, 2, o 3)",
      "category": "Identificador de la categoría de la pregunta",
      "lection": "texto largo, de almenos 100 palabras sobre el que se esta haciendo la pregunta"
    }
  ]
}


las categorías validas son:

- Tarjetas de credito
- Seguros
- Ahorro
- Inversiones
- Hipotecas

Las respuestas correctas ("correct") tiene que ir variando del 1 al 3
'''

async def generate_questions_openai(num_of_questions: StatementInput = Depends(oauth2_scheme)):
    prompt_statatements_replaced = prompt_statatements.replace("XXXNUMEROPREGUNTASXXX", str(num_of_questions.number_of_questions))
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_statatements_replaced}]
    )

    response_message = response.choices[0].message.content

    # Save questions into database
    try:
      xx = save_questions(json.loads(response_message))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error saving questions into database: %s" % e
        )

    return json.loads(response_message)

async def get_questions_from_db(num_of_questions: StatementInput = Depends(oauth2_scheme)):
    try:
      results = get_questions(num_of_questions.number_of_questions)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error getting questions from database: %s" % e
        )
    questions = {"questions": json.loads(results)}
    return questions

async def user_rank(user_rank: QuestionnaireResultsList = Depends(oauth2_scheme)):
    # Save user rank into database
    for i in user_rank.results:
      print(i)
    # try:
    #   xx = save_questions(user_rank)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Error saving user rank into database: %s" % e
    #     )

    return 1