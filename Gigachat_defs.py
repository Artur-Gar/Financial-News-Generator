from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import yaml

config_path = r"configs\config.yml"
with open(config_path) as fh:
    read_config = yaml.load(fh, Loader=yaml.FullLoader)
creds = read_config['creds']
model = read_config['model']

# specifically for GigaChat it's necessary to run it at least once at the beginning of generating - this class is for this point
class gigachat_stub():
    def __init__(self, creds = creds, model = model):
        self.creds = creds
        self.model = model

    def __call__(self):
        try:
            chat = GigaChat(credentials=self.creds, verify_ssl_certs=False, model = self.model, scope="GIGACHAT_API_CORP", profanity_check = 'false', temperature=0.5, max_tokens = 10)
            messages = [
                SystemMessage(content="""You are the editor of a business magazine focused on investments and finance.""")
            ]
            message_prompt = f"""Tell me about the company Rosbank."""
            messages.append(HumanMessage(content=message_prompt))
            res = chat(messages)
            print(res.content)
        except:
            chat = GigaChat(credentials=creds, verify_ssl_certs=False, model = 'GigaChat-Pro', scope="GIGACHAT_API_CORP", profanity_check = 'false', temperature=0.5, max_tokens = 10)
            messages = [
                SystemMessage(content="""You are the editor of a business magazine focused on investments and finance.""")
            ]
            message_prompt = f"""Tell me about the company Rosbank."""
            messages.append(HumanMessage(content=message_prompt))
            res = chat(messages)
            print(res.content)
        return res.content


# our output generating function
def llm_output(text_news: str, system_prompt_template: str, prompt_template: str, temperature: float) -> int: 
    # Create a chat with a system prompt for context input + add few-shot examples
    global messages;    
    messages = [
        SystemMessage(
            content=system_prompt_template
        )
    ]
    
    # Format the news message template
    message_prompt = prompt_template.format(text_news)
    
    # Add the request to the message list
    messages.append(HumanMessage(content=message_prompt))
    
    # Initialize the chat based on the message list
    chat = GigaChat(credentials=creds, verify_ssl_certs=False, model = model, scope="GIGACHAT_API_CORP", profanity_check = 'false', temperature=temperature, max_tokens = 1024, top_p = 0.1, update_interval = 2)

    res = chat(messages)
    return res.content 