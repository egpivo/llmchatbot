# Chatbot
[![Tests](https://github.com/egpivo/chatbot/workflows/CI/badge.svg)](https://github.com/egpivo/chatbot/actions)
[![Code Coverage](https://codecov.io/gh/egpivo/chatbot/branch/main/graph/badge.svg)](https://codecov.io/gh/egpivo/chatbot)


## Installation

To get the Chatbot Python package from this GitHub repository, use the following command:

```bash
pip install git+https://github.com/egpivo/chatbot.git
```
## Serving Automation
This repository automates the process of checking and fine-tuning pre-trained models for the Chatbot application. The automation script allows you to customize SpeechT5 and SWhisper models and enables retraining if needed.

### Serving Process Flow

```mermaid
graph TD
  A[Check if Model Exists]
  B[Fine-Tune Model]
  C[Serve the App]
  D[Check SSL Certificates]
  E[Generate Dummy SSL Certificates]

  A -- No --> B
  A -- Yes --> C
  B --> C
  C --> D
  D -- No --> E
  D -- Yes --> C

```

### Artifact Folder
During the model serving process, the `artifact` folder is dynamically created to store the BentoML artifacts, essential for serving the Chatbot application.
## Usage
### I. Server Side
#### 1. Default Model Values
 Run the Chatbot service with default model values:
```shell
make serve
```
#### 2. Customizing the Serving Process
Customize the Chatbot serving process using the automation script. Specify your desired models and options:
```shell
bash scripts/run_app_service.sh \
  --t5_pretrained_model {t5_model} \
  --t5_pretrained_vocoder {t5_vocoder} \
  --whisper_pretrained_model {whisper_model} \
  --is_retraining \
  --port {port}
```
- **Note**: Replace `{t5_model}`, `{t5_vocoder}`, `{whisper_model}, and `{port}` with your preferred values. Adding the `--is_retraining` flag forces model retraining.

### II. Client Side
Access the demo chatbot at `https://{ip}:{port}/chatbot`, with the default values being `0.0.0.0` for the `ip` and `3389` for the `port`.

- Note: Dummy SSL certificates and keys are created by default for secure communication. You can replace them manually.

## Demo
- [Demo site]()
## Reference
- [BentoChain Repository](https://github.com/ssheng/BentoChain)
