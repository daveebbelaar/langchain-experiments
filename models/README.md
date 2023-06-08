# Text Summarization with Falcon-7B and text-davinci-003

This repository contains an experiment comparing the Falcon-7B language model, accessed through the Hugging Face Model Hub, and OpenAI's text-davinci-003 model. The experiment is set up using the LangChain framework and involves a series of basic question tests followed by a text summarization task.

## Falcon-7B Model

The Falcon-7B model, created by the Technology Innovation Institute in Abu Dhabi, is a state-of-the-art language model that rivals many current closed-source models. It is part of the Falcon family of models, which also includes the Falcon-40B model. The Falcon-7B model requires ~15GB of GPU memory, making it accessible for inference and fine-tuning even on consumer hardware. It has been trained on a massive web dataset called RefinedWeb, which comprises over 80% of its training data. The model uses a technique called multiquery attention, which improves the scalability of inference by reducing memory costs and enabling novel optimizations such as statefulness​[^1].


## Setting Up the Experiment
We first test the Falcon-7B model with basic questions using LangChain. We then compare its capabilities to OpenAI's text-davinci-003 model in a text summarization task, which we set up with the help of LangChain. The experiment involves loading a YouTube video transcript, splitting it into smaller chunks, and running a summarization task on each chunk. The final output is a summarized version of the entire transcript.

You can find the code for setting up and running the experiment in the `falcon_model.py` file in this repository. Below is a brief description of the key steps in the code:

1. Load the HuggingFaceHub API token from the .env file.
2. Load the Falcon-7B LLM model from the HuggingFaceHub[^4].
3. Create a PromptTemplate and LLMChain for the Falcon-7B model.
4. Run the LLMChain with a test question.
5. Load a video transcript from YouTube and split it into smaller chunks.
7. Run the text summarization task on the Falcon-7B model[^5].
8. Load the OpenAI text-davinci-003 model and run the text summarization task.


[^1]: https://huggingface.co/blog/falcon
[^2]: https://platform.openai.com/docs/models/gpt-3-5
[^3]: https://python.langchain.com
[^4]: https://python.langchain.com/en/latest/modules/models/llms/integrations/huggingface_hub.html
[^5]: https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html
