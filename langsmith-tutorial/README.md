# Monitor and Evaluate LLM-Powered Applications with LangSmith

This repository is a practical tutorial on using LangSmith to monitor and evaluate LLM-powered applications. It contains a quick setup and execution of LangSmith, followed by an example of creating an example dataset to evaluate an LLM. We also explore in detail different ways of creating datasets in LangSmith as well as different methods of evaluating LLM outputs. 

This project will guide and equip you with the necessary information to get started on utilizing LangSmith to test your LLM applications.

If you would like to learn more about LangSmith, please refer to the `langsmith-first-look` repository.

The code of this tutorial is referred from LangChain's official documentation [^1] [^2] [^3] [^4], adapted to a presentation flow catered for beginners.

## LangSmith: Setup and Example Evaluation

LangSmith is a platform for building production-grade LLM applications. It lets you debug, test, evaluate, and monitor chains and intelligent agents built on any LLM framework and seamlessly integrates with LangChain, the go-to open source framework for building with LLMs. It is developed by LangChain, the company behind the open source LangChain framework [^1].

Please refer to the first section of the script `langchain-tutorial.py` at the `src` folder to set up the logging function at LangSmith for an example application. 

Feel free to execute the next section of the script, which is an example execution of evaluating a dataset and LLM outputs using LangSmith. More details follow in the next section.

## Different Ways of Creating Datasets on LangSmith

Datasets are collections of examples that can be used to evaluate or otherwise improve a chain, agent, or model. Examples are rows in the dataset, containing the inputs and (optionally) expected outputs for a given interaction [^3]. 

### Types of Datasets [^3]:
- `kv` datasets: The default type, where inputs and outputs can be any dictionary (key-value pairs). 

- `llm` datasets: They have an "inputs" dictionary which contains a single "input" key mapped to a single prompt string. Similarly, the "outputs" dictionary contains a single "output" key mapped to a single response string (inputs=prompts, outputs=responses).

- `chat` datasets: They have an "inputs" dictionary containing a single "input" key mapped to a single list of serialized chat messages. The "outputs" dictionary contains a single "output" key mapped to a single list of serialized chat messages (inputs=keys of chat messages dict, outputs=keys of chat messages dict).

### Different Dataset Creation:

We can create datasets in two ways: 
- 1) via the LangSmith web app, and 
- 2) via the LangSmith client using code.

Please refer to the script `langchain-tutorial.py` in the `src` folder to explore these different ways of creating datasets on LangSmith:
1. Create a Dataset From a List of Examples (Key-Value Pairs)
2. Create a Dataset From Existing Runs
3. Create a Dataset From a Dataframe
4. Create a Dataset From a CSV File

## Determining the Correctness of LLM outputs: Question-Answer Evaluation

LangChain's evaluation module provides evaluators you can use as-is for common evaluation scenarios. QA evaluators help to measure the correctness of a response to a user query or question [^4].

Three QA evaluators you can load are: "context_qa", "qa", and "cot_qa". Based on our meta-evals, we recommend using "cot_qa" or a similar prompt for best results [^4].

The evaluators [^4]:
1. "context_qa" evaluator: Instructs the LLM chain to use reference "context" (provided through the example outputs) in determining correctness. This is useful if you have a larger corpus of grounding docs but don't have ground truth answers to a query.
2. "qa" evaluator: Instructs an LLMChain to directly grade a response as "correct" or "incorrect" based on the reference answer. 
3. "cot_qa" evaluator: Similar to the "context_qa" evaluator, expect it instructs the LLMChain to use a chain of thought "reasoning" before determining a final verdict. This tends to lead to responses that better correlate with human labels, for a slightly higher token and runtime cost.

Please refer to the script `langchain-tutorial.py` in the `src` folder to explore these different ways of evaluating datasets and LLM outputs on LangSmith:
1. Evaluate Datasets That Contain Labels
    - "qa": correctness: right or wrong
    - "context_qa": refer to example outputs
    - "cot_qa": context_qa + reasoning
2. Evaluate Datasets With Customized Criterias
3. Evaluate Datasets Without Labels
4. Evaluate Datasets Based on Cosine Distance Criteria
    - Cosine Distance: Ranged Between 0 to 1. 0 = More Similar
5. Evaluate Datasets Based on String Distance Criteria
    - Jaro-Winkler Similarity Distance: 0 = Exact Match, 1 = No Similarity

## Setting Up the Experiment

You can find the code for setting up and running the experiment in the `langchain-tutorial.py` script in the `src` folder. 

To check out the LLM outputs, refer to the `langchain-tutorial.ipynb` notebook.

Note: Make sure your device has Python 3.9 or higher and an up-to-date version of the LangChain module to execute the scripts successfully.

Refer to `requirements.txt` for all required libraries to execute the script.

## Observation From the Use Case

- The logging function of LangSmith provides a transparent and structured way to examine the outputs of LLMs.
- Creating datasets allows different evaluations to be made independently on different runs.
- It is very useful to evaluate and compare LLM outputs with ground truths and use both the existing and customized evaluation criteria.  
- Customized evaluations use LLMs to examine the case, input-by-input. It can use up a lot of tokens.


[^1]: https://docs.smith.langchain.com/
[^2]: https://docs.smith.langchain.com/evaluation/quickstart
[^3]: https://docs.smith.langchain.com/evaluation/datasets
[^4]: https://docs.smith.langchain.com/evaluation/evaluator-implementations#correctness-qa-evaluation