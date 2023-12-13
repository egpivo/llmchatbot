import gradio as gr


def create_head() -> gr.Markdown:
    return gr.Markdown("<h2>Chatbot Playground</h2>")


def create_openai_api_key_textbox() -> gr.Textbox:
    return gr.Textbox(
        placeholder="Paste your OpenAI API key here (e.g., sk-...)",
        show_label=False,
        lines=1,
        type="password",
    )


def create_chatbot() -> gr.Chatbot:
    return gr.Chatbot(
        value=[],
        elem_id="chatbot",
    )


def create_chatbot_audio() -> gr.Audio:
    return gr.Audio(label="Chatbot Voice", elem_id="chatbot_voice")


def create_user_audio_message() -> gr.Audio:
    return gr.Audio(label="User Voice Message", source="microphone", type="filepath")


def create_user_text_message() -> gr.Text:
    return gr.Text(label="User Text Message", placeholder="Input text")


def create_theme() -> gr.themes:
    return gr.themes.Glass().set(
        loader_color="#FF0000",
        slider_color="#FF0000",
    )
