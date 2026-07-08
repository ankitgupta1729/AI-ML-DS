from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from colorama import Fore

load_dotenv()
llm = OpenAI()

prompt_template = PromptTemplate.from_template("Tell me a joke about a {topic}")
output_parser = StrOutputParser()

def generate(text):
    
    """ generate text based on the input """
    
    chain = prompt_template | llm | output_parser 
    
    # Here prompt_template and llm are components of our chain and they are separated by pipe 
    # operator and each component is input to the next component. So, here prompt_template
    # becomes input for the llm component  
    
    return chain.invoke(text)



def start():
    instructions = (
        "Type your question and press ENTER. Type 'x' to go back to the MAIN menu.\n"
    )
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)

    print("MENU")
    print("====")
    print("[1]- Ask a question")
    print("[2]- Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        ask()
    elif choice == "2":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice")
        start()


def ask():
    while True:
        user_input = input("Q: ")
        # Exit
        if user_input == "x":
            start()
        else:
            response = generate(user_input)
            print(Fore.BLUE + f"A: " + response + Fore.RESET)
            print(Fore.WHITE + "\n-------------------------------------------------")


if __name__ == "__main__":
    start()