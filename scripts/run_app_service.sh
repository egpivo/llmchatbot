#!/bin/bash
#
# Chatbot Serving
#
# - Parameters
#   - Optional
#     - --t5_pretrained_model: Specifies the Hugging Face SpeechT5 model. Default: microsoft/speecht5_tts
#     - --t5_pretrained_vocoder: Specifies the Hugging Face SpeechT5 HiFi-GAN Vocoder. Default: microsoft/speecht5_hifigan
#     - --whisper_pretrained_model: Specifies the Hugging Face SWhisper model. Default: openai/whisper-tiny
#     - --is_retraining: Forces retraining of models.
#     - --is_production: Turn on the production mode.
#
# This script automates the process of checking and fine-tuning pre-trained models for the Chatbot application.
# It supports customizing the SpeechT5 and SWhisper models, as well as enabling retraining if needed.
# If the specified models do not exist, or if retraining is forced, the script initiates the fine-tuning process.
# After model preparation, it serves the Chatbot application using BentoML.
#

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_BASE_PATH="${CURRENT_DIR}/../"
source "${PACKAGE_BASE_PATH}/envs/.env"
source "${CURRENT_DIR}/exit_code.sh"

# Parse command line options
while [[ $# -gt 0 ]]; do
  case "$1" in
    --t5_pretrained_model) T5_PRETRAINED_MODEL="$2"; shift 2 ;;
    --t5_pretrained_vocoder) T5_PRETRAINED_VOCODER="$2"; shift 2 ;;
    --whisper_pretrained_model) WHISPER_PRETRAINED_MODEL="$2"; shift 2 ;;
    --is_retraining) IS_RETRAINING="TRUE"; shift ;;
    --is_production) IS_PRODUCTION="TRUE"; shift ;;
    *) shift ;;
  esac
done

# Set default values if not provided
T5_PRETRAINED_MODEL=${T5_PRETRAINED_MODEL:-"microsoft/speecht5_tts"}
T5_PRETRAINED_VOCODER=${T5_PRETRAINED_VOCODER:-"microsoft/speecht5_hifigan"}
WHISPER_PRETRAINED_MODEL=${WHISPER_PRETRAINED_MODEL:-"openai/whisper-tiny"}

# Set job commands
JOB_COMMANDS=(
  "${CURRENT_DIR}/run_model_training.py"
  "--t5_pretrained_model" "${T5_PRETRAINED_MODEL}"
  "--t5_pretrained_vocoder" "${T5_PRETRAINED_VOCODER}"
  "--whisper_pretrained_model" "${WHISPER_PRETRAINED_MODEL}"
)
[[ "x${IS_RETRAINING}x" == "xTRUEx" ]] && JOB_COMMANDS+=("--is_retraining")

# Check and fine-tune models
echo -e "$(tput setaf 6)Check and fine-tune models$(tput sgr0)"
python "${JOB_COMMANDS[@]}"
if [[ $? != "${SUCCESS_EXITCODE}" ]]; then
  exit "${ERROR_EXITCODE}"
fi

# Serve BentoML App
echo -e "$(tput setaf 2)Serve BentoML App$(tput sgr0)"
KEY_PERM="${CURRENT_DIR}/key.pem"
CERTIFICATE_PERM="${CURRENT_DIR}/cert.pem"

if [[ ! -f "${KEY_PERM}" || ! -f "${CERTIFICATE_PERM}" ]]; then
  echo -e "$(tput setaf 3)Create a dummy SSL files$(tput sgr0)"
  SUBJ="/C=DK/ST=Test/O=Company Name"
  openssl req -x509 \
   -newkey rsa:4096 \
   -keyout "${KEY_PERM}" \
   -out "${CERTIFICATE_PERM}" \
   -sha256 -days 365 \
   -nodes -subj "$SUBJ"
fi

if [[ "x${IS_PRODUCTION}x" == "xTRUEx" ]]; then
  echo -e "$(tput setaf 2)Production Mode$(tput sgr0)"
  bentoml serve chatbot/app.py:svc \
  --production
else
  echo -e "$(tput setaf 2)Development Mode$(tput sgr0)"
  bentoml serve chatbot/app.py:svc \
  --reload
fi
