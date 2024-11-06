import google.generativeai as genai
import json
import os

from pinecone import Pinecone
from util import create_log, get_secret

PINECONE_DEV_KEY = get_secret("PINECONE_DEV_KEY")
GEMINI_DEV_KEY = get_secret("GEMINI_DEV_KEY")
LOG_LEVEL = os.environ.get("LOG_LEVEL")

logger = create_log('inference_handler', LOG_LEVEL)

def create_context(question):
    """
    Create a context for a question by finding the most similar context from the pinecone index
    """
    logger.info(f"Creating context for question: {question}")

    pc = Pinecone(api_key=PINECONE_DEV_KEY)
    logger.debug("Initialized Pinecone client")

    index = pc.Index('semantic-search-gemini')
    logger.debug("Connected to 'semantic-search-gemini' index")
    
    # Get the embeddings for the question
    logger.debug("Generating embeddings for question")
    q_embeddings  = genai.embed_content(
        model="models/text-embedding-004",
        content=question)
    logger.debug("Successfully generated embeddings")
    
    # Get the distances from the embeddings
    logger.debug("Querying Pinecone index for similar contexts")
    res = index.query(vector=[q_embeddings['embedding']], top_k=5, include_metadata=True)
    logger.debug(f"Found {len(res.matches)} matching contexts")
    
    results = []
    for m in res.matches:
        text = m['metadata']['text']
        results.append(text)
 
    context = r"\n\n###\n\n".join(results)
    logger.info(f"Created context with {len(results)} text segments")
    logger.debug(f"Total context length: {len(context)} characters")

    return context

def answer_question(
    question,
    model="gemini-1.5-flash-8b",
):
    """
    Answer a question based on the most similar context from pinecone
    """
    logger.info(f"Starting to process question: {question}")
    logger.debug(f"Parameters - model: {model}")
    
    genai.configure(api_key=GEMINI_DEV_KEY)
    logger.debug("Configured Gemini API")

    context = create_context(question)
    logger.debug(f"Retrieved context length: {len(context)}")

    model = genai.GenerativeModel(model)
    logger.debug(f"Initialized Gemini model: {model}")

    try:
        # Create a completions using the question and context
        message =  f"You are a yoda chatbot for padawans. Strictly answer the question based on the context below, and if the question can't be answered based on the context, say \"I'm sorry I cannot answer the question\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:"
        logger.debug("Sending request to Gemini")

        response = model.generate_content(message)
        logger.info("Successfully generated response from Gemini")
        logger.debug(f"Response text length: {len(response.text)}")

        return response.text
    
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}", exc_info=True)
        return ""
        

def lambda_handler(event, context):
    """The central handler function called when the Lambda function is invoked.

    Arguments:
        event {dict} -- Dictionary containing contents of the event that
        invoked the function, primarily the payload of data to be processed.
        context {LambdaContext} -- An object containing metadata describing
        the event source and client details.

    Returns:
        [string|dict] -- An output object that does not impact the effect of
        the function but which is reflected in CloudWatch
    """
    logger.info('Starting Lambda Execution')

    logger.debug(event)

    try:
        logger.info("Received new request")
        logger.debug(f"Event: {json.dumps(event)}")
        
        # Get the request body
        body = json.loads(event.get('body', '{}'))
        logger.debug(f"Parsed request body: {json.dumps(body)}")
        
        # Extract the question from the request
        question = body.get('question')
        
        # Validate input
        if not question:
            logger.warning("Request received with missing question")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Question is required'
                })
            }
        
        logger.info(f"Processing question request: {question}")
        
        # Process the question
        answer = answer_question(question)
        
        logger.info("Successfully processed question")
        logger.debug(f"Generated answer: {answer}")
        
        # Return the response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'question': question,
                'answer': answer
            })
        }
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request body: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Invalid JSON in request body'
            })
        }
    
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}'
            })
        }