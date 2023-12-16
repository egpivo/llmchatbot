# ChatBot
[![Tests](https://github.com/egpivo/chatbot/workflows/CI/badge.svg)](https://github.com/egpivo/chatbot/actions)
[![Code Coverage](https://codecov.io/gh/egpivo/chatbot/branch/main/graph/badge.svg)](https://codecov.io/gh/egpivo/chatbot)


## Installation

To install the `chatbot` Python package from this GitHub repository, you can use the following command:

```bash
pip install git+https://github.com/egpivo/chatbot.git
```
## Serving Automation
This repository provides an automated process for checking and fine-tuning pre-trained models for the ChatBot application. The automation script supports customization of SpeechT5 and SWhisper models, as well as enabling retraining if needed.
### Serving Process Flow

```mermaid
graph TD
  A[Check if Model Exists]
  B[Fine-Tune Model]
  C[Serve the App]

  A -- No --> B
  A -- Yes --> C
  B --> C
```
## Usage
### 1. Default Model Values
Run the ChatBot service with default model values:
```shell
make serve
```

### 2. Customizing the Serving Process
To customize the ChatBot serving process, use the automation script. Specify your desired models and options as follows:
```shell
bash cli/scripts/run_app_service.sh \
  --t5_pretrained_model {t5_model} \
  --t5_pretrained_vocoder {t5_vocoder} \
  --whisper_pretrained_model {whisper_model} \
  --is_retraining
```
- **Note**: Replace `{t5_model}`, `{t5_vocoder}`, and `{whisper_model}` with actual values or placeholders for users to fill in. Adding the `--is_retraining` flag forces retraining of models.

## Reference
- [BentoChain Repository](https://github.com/ssheng/BentoChain)
