#!/bin/bash
#
# Chatbot Serving
#
# - Parameters
#    - Optional
#       - -m/--t5_pretrained_model: Hugging Face SpeechT5 model
#       - -v/--t5_pretrained_vocoder: Hugging Face SpeechT5 HiFi-GAN Vocoder
#       - -w/--whisper_pretrained_model: Hugging Face SWhisper model
#

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_BASE_PATH="${CURRENT_DIR}/../../"
source "${PACKAGE_BASE_PATH}/.env"

for ARG in "$@"; do
  shift
  case "${ARG}" in
  "--t5_pretrained_model") set -- "$@" "-m" ;;
  "--t5_pretrained_vocoder") set -- "$@" "-v" ;;
  "--whisper_pretrained_model") set -- "$@" "-w" ;;
  *) set -- "$@" "${ARG}" ;;
  esac
done

while getopts "m:v:w:*" OPT; do
  case "${OPT}" in
  m)
    T5_PRETRAINED_MODEL="${OPTARG}"
    ;;
  v)
    T5_PRETRAINED_VOCODER="${OPTARG}"
    ;;
  w)
    WHISPER_PRETRAINED_MODEL="${OPTARG}"
    ;;
  *) ;;
  esac
done


# Python job setting - Update the optional parameters
if [ "x${T5_PRETRAINED_MODEL}x" == "xx" ]; then
  T5_PRETRAINED_MODEL="microsoft/speecht5_tts"
fi
if [ "x${T5_PRETRAINED_VOCODER}x" == "xx" ]; then
  T5_PRETRAINED_VOCODER="microsoft/speecht5_hifigan"
fi
if [ "x${WHISPER_PRETRAINED_MODEL}x" == "xx" ]; then
  WHISPER_PRETRAINED_MODEL="openai/whisper-tiny"
fi


if [ ! -d "${BENTOML_HOME}" ]; then
   python ${CURRENT_DIR}/run_model_training.py \
      --t5_pretrained_model ${T5_PRETRAINED_MODEL} \
      --t5_pretrained_vocoder ${T5_PRETRAINED_VOCODER} \
      --whisper_pretrained_model ${WHISPER_PRETRAINED_MODEL}
fi

bentoml serve chatbot/app.py
