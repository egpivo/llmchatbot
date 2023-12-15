import gradio as gr

from chatbot.app.controller.chatter import Chatter
from chatbot.app.view.component import (
    create_chatbot,
    create_chatbot_audio,
    create_head,
    create_openai_api_key_textbox,
    create_theme,
    create_user_audio_message,
    create_user_text_message,
)
from chatbot.app.view.utils import set_openai_api_key


class ChatbotViewer:
    def __init__(self, chatter: Chatter):
        self.chatter = chatter
        self.block = gr.Blocks(theme=create_theme())
        self.state = gr.State()
        self.agent_state = gr.State()

        self.create_view()

    def create_view(self) -> None:
        with self.block:
            with gr.Row():
                create_head()

            with gr.Row():
                with gr.Column(scale=1, min_width=600):
                    openai_api_key_textbox = create_openai_api_key_textbox()
                    with gr.Row():
                        audio_message = create_user_audio_message()
                        text_message = create_user_text_message()
                with gr.Column(scale=1, min_width=600):
                    chatbot = create_chatbot()
                    audio = create_chatbot_audio()

            inputs = [
                openai_api_key_textbox,
                audio_message,
                text_message,
                self.state,
                self.agent_state,
            ]
            outputs = [chatbot, self.state, audio, audio_message, text_message]

            audio_message.change(
                self.chatter, inputs=inputs, outputs=outputs, show_progress=True
            )
            text_message.submit(
                self.chatter, inputs=inputs, outputs=outputs, show_progress=True
            )
            openai_api_key_textbox.change(
                set_openai_api_key,
                inputs=[openai_api_key_textbox],
                outputs=[self.agent_state],
                show_progress=True,
            )

    def get_view(self) -> gr.Blocks:
        return self.block
