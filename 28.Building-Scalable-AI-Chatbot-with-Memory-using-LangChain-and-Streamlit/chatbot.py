import streamlit as st
import os
from dotenv import load_dotenv
from ollama import Client
from streamlit.errors import StreamlitSecretNotFoundError
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI  # Import for OpenAI models
from langchain_core.runnables import RunnableLambda  # Import RunnableLambda for explicit formatting

load_dotenv()


def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Read configuration from Streamlit secrets first, then fall back to environment variables.
    This keeps local Streamlit runs aligned with `.streamlit/secrets.toml` while still
    allowing `.env` as a fallback source.
    """

    try:
        secret_value = st.secrets[name]
        if secret_value:
            return secret_value
    except (KeyError, StreamlitSecretNotFoundError):
        pass

    return os.getenv(name, default)


def get_ollama_base_url() -> str:
    return get_secret("OLLAMA_BASE_URL", "http://localhost:11434")


def get_available_ollama_models() -> tuple[list[str], str | None]:
    """
    Return locally available Ollama models from the configured Ollama server.
    The second return value is an optional error message for the UI.
    """

    try:
        client = Client(host=get_ollama_base_url())
        response = client.list()
        models = sorted(
            {
                model.model
                for model in response.models
                if getattr(model, "model", None)
            }
        )

        if models:
            return models, None

        return [], "No Ollama models were found. Pull one with `ollama pull <model_name>`."
    except Exception as exc:
        return [], (
            "Could not connect to Ollama at "
            f"`{get_ollama_base_url()}`. Start Ollama locally or update `OLLAMA_BASE_URL` "
            f"in `.env`. Details: {exc}"
        )


# ---- Model Abstraction and Initialization ----
def get_llm(model_type: str, model_name: str, temperature: float, max_tokens: int):
    """
    Initializes and returns a chat model based on the provided type and name.
    Supports local (Ollama) and cloud-based (OpenAI) models.
    """

    if model_type == "Ollama":
        # Ollama models run locally. Base URL can be configured via st.secrets or default.
        ollama_base_url = get_ollama_base_url()

        return ChatOllama(
            base_url=ollama_base_url,
            model=model_name,
            temperature=temperature,
            num_predict=max_tokens,  # Use num_predict for max_tokens in Ollama
        )

    elif model_type == "OpenAI":
        # OpenAI models require an API key.
        openai_api_key = get_secret("OPENAI_API_KEY")

        if not openai_api_key:
            st.error(
                "OpenAI API key not found. Add `OPENAI_API_KEY` to `.env` "
                "for local runs or `.streamlit/secrets.toml` for Streamlit deployment."
            )
            st.stop()  # Stop the app if key is missing

        return ChatOpenAI(
            model=model_name,
            api_key=openai_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    else:
        st.error(f"Unsupported model type: {model_type}")
        st.stop()


# ---- Get or create SQL-based chat history ----
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # Ensure the database file is created if it doesn't exist
    db_path = "chat_history.db"

    if not os.path.exists(db_path):
        open(db_path, "a").close()  # Simple way to ensure file exists

    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string=f"sqlite:///{db_path}",
    )


# ---- Streamlit UI Setup ----
st.set_page_config(page_title="🤖 Scalable AI Chatbot (with Memory)")
st.title("🤖 Scalable AI Chatbot (with Memory)")


# ---- Sidebar for Configuration ----
with st.sidebar:
    st.header("Model Configuration")

    model_type = st.selectbox(
        "Select LLM Provider:",
        options=["Ollama", "OpenAI"],
        help="Choose between local Ollama models or cloud-based OpenAI models.",
    )

    # Dynamically show model options based on provider
    if model_type == "Ollama":
        ollama_models, ollama_error = get_available_ollama_models()

        st.caption(f"Using Ollama server: `{get_ollama_base_url()}`")

        if ollama_error:
            st.warning(ollama_error)
            st.stop()

        selected_model_name = st.selectbox("Select Ollama Model:", options=ollama_models)

    elif model_type == "OpenAI":
        openai_models = ["gpt-4o", "gpt-3.5-turbo"]  # Add more as needed
        selected_model_name = st.selectbox(
            "Select OpenAI Model:",
            options=openai_models,
        )

    temperature = st.slider(
        "Temperature (Creativity):",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help=(
            "Higher values (e.g., 0.7-1.0) make the output more random and creative. "
            "Lower values (e.g., 0.0-0.3) make it more focused and deterministic."
        ),
    )

    max_tokens = st.slider(
        "Max Output Tokens:",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
        help=(
            "Maximum number of tokens (words/pieces of words) the model will generate "
            "in its response."
        ),
    )

    st.markdown("---")
    st.subheader("Chat History Settings")

    default_user = "Ankit"

    session_id_input = st.text_input(
        "Enter your name (for chat history):",
        value=default_user,
    )
    session_id = session_id_input.strip() or default_user

    if st.button("Clear Chat History"):
        get_session_history(session_id).clear()
        st.session_state.messages = []
        st.session_state.active_session_id = session_id
        st.success("Chat history cleared!")
        st.rerun()  # Rerun to reflect changes immediately


# Initialize the selected LLM based on sidebar choices
llm = get_llm(model_type, selected_model_name, temperature, max_tokens)


# ---- Prompt template setup (system + memory + human prompt) ----
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="chat_history_placeholder"),
        ("human", "{input}"),
    ]
)


# ---- Chain: Explicitly format input for the prompt ----
# This RunnableLambda will take the list of messages from RunnableWithMessageHistory
# and convert it into the dictionary format expected by ChatPromptTemplate.
def format_messages_for_prompt(messages: list):
    # The last message in the list is the current human input
    current_input_message = messages[-1]

    # The rest are historical messages
    chat_history = messages[:-1]

    return {
        "input": current_input_message.content,
        "chat_history_placeholder": chat_history,
    }


chain = (
    RunnableLambda(format_messages_for_prompt)
    | prompt_template
    | llm
    | StrOutputParser()
)


# ---- Wrap chain with message history ----
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)


# ---- Load chat history from database ----
if st.session_state.get("active_session_id") != session_id:
    st.session_state.active_session_id = session_id
    st.session_state.messages = get_session_history(session_id).messages
elif "messages" not in st.session_state:
    st.session_state.messages = get_session_history(session_id).messages


# ---- Display chat history ----
for message in st.session_state.messages:
    if message.type == "human":
        with st.chat_message("user"):
            st.markdown(message.content)

    elif message.type == "ai":
        with st.chat_message("assistant"):
            st.markdown(message.content)


# ---- Chat input ----
if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    config = {
        "configurable": {
            "session_id": session_id,
        }
    }

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in chain_with_history.stream(
                prompt,
                config=config,
            ):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        # Refresh session state messages from database
        st.session_state.messages = get_session_history(session_id).messages

    except Exception as e:
        st.error(f"An error occurred: {e}")
