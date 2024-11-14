from typing import List, Optional

from xagent import XAgentClient, XAgentModel  # Hypothetical XAgent imports
from agents.agent_simulations.agent.dialogue_agent import DialogueAgent
from agents.conversational.output_parser import ConvoOutputParser
from config import Config
from memory.zep.zep_memory import ZepMemory
from services.run_log import RunLogsManager
from typings.agent import AgentWithConfigsOutput


class DialogueAgentWithTools(DialogueAgent):
    def __init__(
        self,
        name: str,
        agent_with_configs: AgentWithConfigsOutput,
        system_message: str,  # Updated to string as XAgent likely does not use SystemMessage directly
        model: XAgentModel,  # Hypothetical XAgent model class
        tools: List[any],
        session_id: str,
        sender_name: str,
        is_memory: bool = False,
        run_logs_manager: Optional[RunLogsManager] = None,
        **tool_kwargs,
    ) -> None:
        super().__init__(name, agent_with_configs, system_message, model)
        self.tools = tools
        self.session_id = session_id
        self.sender_name = sender_name
        self.is_memory = is_memory
        self.run_logs_manager = run_logs_manager

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """

        memory: ZepMemory

        # FIXME: This is a hack to get the memory working
        # if self.is_memory:
        memory = ZepMemory(
            session_id=self.session_id,
            url=Config.ZEP_API_URL,
            api_key=Config.ZEP_API_KEY,
            memory_key="chat_history",
            return_messages=True,
        )

        memory.human_name = self.sender_name
        memory.ai_name = self.agent_with_configs.agent.name
        memory.auto_save = False
        # else:
        #     memory = ConversationBufferMemory(
        #         memory_key="chat_history", return_messages=True
        #     )

        callbacks = []

        if self.run_logs_manager:
            self.model.callbacks = [self.run_logs_manager.get_agent_callback_handler()]
            callbacks.append(self.run_logs_manager.get_agent_callback_handler())

        # Initialize XAgent client and set up the agent with tools and model
        agent = XAgentClient(
            model=self.model,
            tools=self.tools,
            config={
                "system_message": self.system_message,  # Assume system_message is now a string
                "output_parser": ConvoOutputParser(),  # Hypothetical parser for XAgent
            },
            max_iterations=5,
        )

        # Construct the input prompt
        prompt = "\n".join(self.message_history + [self.prefix])

        # Execute the agent with the prompt
        res = agent.run(input=prompt)

        # FIXME: is memory
        # memory.save_ai_message(res)

        message = AIMessage(content=res)

        return message.content
