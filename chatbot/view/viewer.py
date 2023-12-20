import gradio as gr

from chatbot.controller.chatter import Chatter
from chatbot.view.component import (
    create_chatbot,
    create_chatbot_audio,
    create_head,
    create_openai_api_key_textbox,
    create_theme,
    create_user_audio_message,
    create_user_text_message,
)
from chatbot.view.utils import set_openai_api_key


class ChatbotViewer:
    def __init__(self, chatter: Chatter) -> None:
        self.chatter = chatter
        self.block = gr.Blocks(theme=create_theme())
        self.create_view()

    @staticmethod
    def _create_layout() -> tuple[gr.components.Component]:
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

        return (openai_api_key_textbox, audio_message, text_message, chatbot, audio)

    def create_view(self) -> None:
        with self.block:
            (
                openai_api_key_textbox,
                audio_message,
                text_message,
                chatbot,
                audio,
            ) = self._create_layout()

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
                self.chatter, inputs=inputs, outputs=outputs, show_progress=True
            )
            text_message.submit(
                self.chatter, inputs=inputs, outputs=outputs, show_progress=True
            )
            openai_api_key_textbox.change(
                set_openai_api_key,
                inputs=[openai_api_key_textbox],
                outputs=[agent_state],
                show_progress=True,
            )

    def get_view(self) -> gr.Blocks:
        return self.block
