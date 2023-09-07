# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------

import os
import nest_asyncio
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from langsmith import Client
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.smith import RunEvalConfig, run_on_dataset

nest_asyncio.apply()

# --------------------------------------------------------------
# Load API Keys From the .env File
# --------------------------------------------------------------

load_dotenv(find_dotenv())
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "langsmith-tutorial"


# --------------------------------------------------------------
# LangSmith Quick Start
# Load the LangSmith Client and Test Run
# --------------------------------------------------------------

client = Client()

llm = ChatOpenAI()
llm.predict("What can you do?")

# --------------------------------------------------------------
# Evaluation Quick Start
# 1. Create a Dataset (Only Inputs, No Output)
# --------------------------------------------------------------

example_inputs = [
    "a rap battle between Atticus Finch and Cicero",
    "a rap battle between Barbie and Oppenheimer",
    "a Pythonic rap battle between two swallows: one European and one African",
    "a rap battle between Aubrey Plaza and Stephen Colbert",
]

dataset_name = "Rap Battle Dataset"

# Storing inputs in a dataset lets us
# run chains and LLMs over a shared set of examples.
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Rap battle prompts.",
)

for input_prompt in example_inputs:
    # Each example must be unique and have inputs defined.
    # Outputs are optional
    client.create_example(
        inputs={"question": input_prompt},
        outputs=None,
        dataset_id=dataset.id,
    )

# --------------------------------------------------------------
# 2. Evaluate Datasets with LLM
# --------------------------------------------------------------

eval_config = RunEvalConfig(
    evaluators=[
        # You can specify an evaluator by name/enum.
        # In this case, the default criterion is "helpfulness"
        "criteria",
        # Or you can configure the evaluator
        RunEvalConfig.Criteria("harmfulness"),
        RunEvalConfig.Criteria("misogyny"),
        RunEvalConfig.Criteria(
            {
                "cliche": "Are the lyrics cliche? "
                "Respond Y if they are, N if they're entirely unique."
            }
        ),
    ]
)

run_on_dataset(
    client=client,
    dataset_name=dataset_name,
    llm_or_chain_factory=llm,
    evaluation=eval_config,
)

# --------------------------------------------------------------
# Different Ways of Creating Datasets in LangSmith
# 1. Create a Dataset From a List of Examples (Key-Value Pairs)
# --------------------------------------------------------------

example_inputs = [
    ("What is the largest mammal?", "The blue whale"),
    ("What do mammals and birds have in common?", "They are both warm-blooded"),
    ("What are reptiles known for?", "Having scales"),
    (
        "What's the main characteristic of amphibians?",
        "They live both in water and on land",
    ),
]

dataset_name = "Elementary Animal Questions"

dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Questions and answers about animal phylogenetics.",
)

for input_prompt, output_answer in example_inputs:
    client.create_example(
        inputs={"question": input_prompt},
        outputs={"answer": output_answer},
        dataset_id=dataset.id,
    )

# --------------------------------------------------------------
# 2. Create a Dataset From Existing Runs
# --------------------------------------------------------------

dataset_name = "Example Dataset"

dataset = client.create_dataset(dataset_name, description="An example dataset")

# Filter runs to add to the dataset
runs = client.list_runs(
    project_name="langsmith-tutorial",
    execution_order=1,
    error=False,
)

for run in runs:
    client.create_example(
        inputs=run.inputs,
        outputs=run.outputs,
        dataset_id=dataset.id,
    )

# --------------------------------------------------------------
# 3. Create a Dataset From a Dataframe
# --------------------------------------------------------------

# Create a Dataframe
example_inputs = [
    ("What is the largest mammal?", "The blue whale"),
    ("What do mammals and birds have in common?", "They are both warm-blooded"),
    ("What are reptiles known for?", "Having scales"),
    (
        "What's the main characteristic of amphibians?",
        "They live both in water and on land",
    ),
]

df_dataset = pd.DataFrame(example_inputs, columns=["Question", "Answer"])
df_dataset.head()

input_keys = ["Question"]
output_keys = ["Answer"]

# Create Dataset
dataset = client.upload_dataframe(
    df=df_dataset,
    input_keys=input_keys,
    output_keys=output_keys,
    name="My Dataframe Dataset",
    description="Dataset created from a dataframe",
    data_type="kv",  # The default
)

# --------------------------------------------------------------
# 4. Create a Dataset From a CSV File
# --------------------------------------------------------------

# Save the Dataframe as a CSV File
csv_path = "../data/dataset.csv"
df_dataset.to_csv(csv_path, index=False)

# Create Dataset
dataset = client.upload_csv(
    csv_file=csv_path,
    input_keys=input_keys,
    output_keys=output_keys,
    name="My CSV Dataset",
    description="Dataset created from a CSV file",
    data_type="kv",
)

# --------------------------------------------------------------
# Correctness: LangSmith Question-Answer Evaluation
# 1. Evaluate Datasets That Contain Labels
# --------------------------------------------------------------

evaluation_config = RunEvalConfig(
    evaluators=[
        "qa",  # correctness: right or wrong
        "context_qa",  # refer to example outputs
        "cot_qa",  # context_qa + reasoning
    ]
)

run_on_dataset(
    client=client,
    dataset_name="Elementary Animal Questions",
    llm_or_chain_factory=llm,
    evaluation=evaluation_config,
)

# --------------------------------------------------------------
# 2. Evaluate Datasets With Customized Criterias
# --------------------------------------------------------------

evaluation_config = RunEvalConfig(
    evaluators=[
        # You can define an arbitrary criterion as a key: value pair in the criteria dict
        RunEvalConfig.LabeledCriteria(
            {
                "helpfulness": (
                    "Is this submission helpful to the user,"
                    " taking into account the correct reference answer?"
                )
            }
        ),
    ]
)

run_on_dataset(
    client=client,
    dataset_name="Elementary Animal Questions",
    llm_or_chain_factory=llm,
    evaluation=evaluation_config,
)

# --------------------------------------------------------------
# 3. Evaluate Datasets Without Labels
# --------------------------------------------------------------

evaluation_config = RunEvalConfig(
    evaluators=[
        # You can define an arbitrary criterion as a key: value pair in the criteria dict
        RunEvalConfig.Criteria(
            {"creativity": "Is this submission creative, imaginative, or novel?"}
        ),
        # We provide some simple default criteria like "conciseness" you can use as well
        RunEvalConfig.Criteria("conciseness"),
    ]
)

run_on_dataset(
    client=client,
    dataset_name="Rap Battle Dataset",
    llm_or_chain_factory=llm,
    evaluation=evaluation_config,
)

# --------------------------------------------------------------
# 4. Evaluate Datasets Based on Cosine Distance Criteria
# Cosine Distance: Ranged Between 0 to 1. 0 = More Similar
# --------------------------------------------------------------

evaluation_config = RunEvalConfig(
    evaluators=[
        # You can define an arbitrary criterion as a key: value pair in the criteria dict
        "embedding_distance",
        # Or to customize the embeddings:
        # Requires 'pip install sentence_transformers'
        # RunEvalConfig.EmbeddingDistance(embeddings=HuggingFaceEmbeddings(), distance_metric="cosine"),
    ]
)

run_on_dataset(
    client=client,
    dataset_name="Elementary Animal Questions",
    llm_or_chain_factory=llm,
    evaluation=evaluation_config,
)

# --------------------------------------------------------------
# 5. Evaluate Datasets Based on String Distance Criteria
# Jaro-Winkler Similarity Distance: 0 = Exact Match, 1 = No Similarity
# --------------------------------------------------------------

evaluation_config = RunEvalConfig(
    evaluators=[
        # You can define an arbitrary criterion as a key: value pair in the criteria dict
        "string_distance",
        # Or to customize the distance metric:
        # RunEvalConfig.StringDistance(distance="levenshtein", normalize_score=True),
    ]
)

run_on_dataset(
    client=client,
    dataset_name="Elementary Animal Questions",
    llm_or_chain_factory=llm,
    evaluation=evaluation_config,
)
