import gradio as gr

from chatbot.app.model.chatter import Chatter
from chatbot.app.utils import set_openai_api_key


def create_openai_api_key_textbox() -> gr.Textbox:
    return gr.Textbox(
        placeholder="Paste your OpenAI API key here (e.g., sk-...)",
        show_label=False,
        lines=1,
        type="password",
    )


def create_chatbot() -> gr.Chatbot:
    return gr.Chatbot(
        [],
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


def create_view(chatter: Chatter) -> gr.Blocks:
    block = gr.Blocks(theme=create_theme())

    with block:
        with gr.Row():
            gr.Markdown("<h2><center>Chatbot Playground</center></h2>")
            openai_api_key_textbox = create_openai_api_key_textbox()

        chatbot = create_chatbot()

        with gr.Row():
            audio = create_chatbot_audio()
            with gr.Column(scale=1, min_width=600):
                audio_message = create_user_audio_message()
                text_message = create_user_text_message()

        state = gr.State()
        agent_state = gr.State()

        inputs = [
            openai_api_key_textbox,
            audio_message,
            text_message,
            state,
            agent_state,
        ]
        outputs = [chatbot, state, audio, audio_message, text_message]

        audio_message.change(
            chatter, inputs=inputs, outputs=outputs, show_progress=True
        )
        text_message.submit(chatter, inputs=inputs, outputs=outputs, show_progress=True)
        openai_api_key_textbox.change(
            set_openai_api_key,
            inputs=[openai_api_key_textbox],
            outputs=[agent_state],
            show_progress=True,
        )
    return block
