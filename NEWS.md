# NEWS
## Chatbot 1.0.2 (Release date: 2023-12-31)
### Enhancement
- Reduce the image size from 8GB to 2GB

## Chatbot 1.0.1 (Release date: 2023-12-31)
### Bugfix
- Incorrect entrypoint in Dockerfile; polish the Dockerfile by reducing multi-stage installation


## Chatbot 1.0.0 (Release date: 2023-12-30)
#### Overview
Explore the LLM Chatbot, a powerful Python application for advanced conversational experiences. The chatbot integrates ChatGPT with LangChain Agent, along with Hugging Face's advanced text-to-speech and speech-to-text models.

## Highlighted Features
### AI Service
   - **Speech-to-Text and Text-to-Speech Models**: Incorporates advanced Hugging Face models for more dynamic conversations.
   - **LangChain Chat Agent**: Features a chat agent powered by LangChain for enhanced conversational capabilities.
### Infrastructure
- **BentoML service Support**
- **Docker Support**: Run the chatbot service using Docker for easy deployment.
- **Automation**:
  - Provide Makefile
  - Setup Docker CI process.
