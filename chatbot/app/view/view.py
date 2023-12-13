import gradio as gr

from chatbot.app.model.chatter import Chatter
from chatbot.app.utils import set_openai_api_key
from chatbot.app.view.utils import (
    create_chatbot,
    create_chatbot_audio,
    create_head,
    create_openai_api_key_textbox,
    create_theme,
    create_user_audio_message,
    create_user_text_message,
)


def create_view(chatter: Chatter) -> gr.Blocks:
    block = gr.Blocks(theme=create_theme())

    with block:
        with gr.Row():
            create_head()
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
