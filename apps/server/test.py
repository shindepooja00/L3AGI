# Importing XAgent components (hypothetical imports based on typical agent frameworks)
from xagent import XAgentClient, XAgentEvalConfig, XAgentModel

# TODO: refactor test to use new auth

# res = requests.post(
#     f"{Config.L3_AUTH_API_URL}/auth/login",
#     json={"email": Config.TEST_USER_EMAIL, "password": Config.TEST_USER_PASSWORD},
#     timeout=30,
# )

# auth_data = res.json()

# headers = {
#     "authorization": auth_data["access_token"],
#     "x-refresh-token": auth_data["refresh_token"],
# }

def agent_factory():
    # Set up XAgent’s language model
    llm = XAgentModel(temperature=0.5, model_name="xagent-model-v1")

    # Initialize XAgent with necessary configuration
    # Assuming XAgent has a similar conversational agent setup
    return XAgentClient(
        model=llm,
        tools=["GoogleSearchTool"],  # Replace with XAgent's toolset if available
        config={
            "system_message": "Provide conversational responses in a helpful manner.",
            "output_parser": "simple_parser",  # Example parser based on XAgent’s expected parsers
        },
        max_iterations=5,
    )

# Instantiate agent
agent = agent_factory()

# Instantiate client - using XAgent’s client instead of Langchain's Client
client = XAgentClient()

# Set up XAgent evaluation configuration
eval_config = XAgentEvalConfig(
    evaluators=[
        "qa",
        XAgentEvalConfig.Criteria("helpfulness"),
        XAgentEvalConfig.Criteria("conciseness"),
    ],
    input_key="input",
    eval_model=XAgentModel(temperature=0.5, model_name="xagent-eval-model"),
)

# Run evaluation on the dataset
chain_results
