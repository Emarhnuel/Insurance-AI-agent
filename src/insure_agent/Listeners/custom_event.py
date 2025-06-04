from crewai.utilities.events.base_event_listener import BaseEventListener
from crewai.utilities.events import (
    # Crew Events
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    CrewKickoffFailedEvent,
    # Tool Events
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent,
    ToolUsageErrorEvent,
    # Flow Events
    MethodExecutionStartedEvent,
    MethodExecutionFinishedEvent,
    MethodExecutionFailedEvent
)
import datetime # For timestamping logs

class LoggingCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()
        print(f"[{datetime.datetime.now()}] LoggingCustomListener: Initialized.")

    def setup_listeners(self, crewai_event_bus):
        print(f"[{datetime.datetime.now()}] LoggingCustomListener: Setting up listeners...")

        # --- Crew Event Handlers ---
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event: CrewKickoffStartedEvent):
            crew_id = source.id if hasattr(source, 'id') else 'N/A'
            print(f"[{event.timestamp}] CREW STARTED: '{event.crew_name}' (ID: {crew_id})")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event: CrewKickoffCompletedEvent):
            crew_id = source.id if hasattr(source, 'id') else 'N/A'
            print(f"[{event.timestamp}] CREW COMPLETED: '{event.crew_name}' (ID: {crew_id})")
            # Consider logging event.output if it's not too verbose for your needs
            # print(f"  Output: {event.output}")

        @crewai_event_bus.on(CrewKickoffFailedEvent)
        def on_crew_failed(source, event: CrewKickoffFailedEvent):
            crew_id = source.id if hasattr(source, 'id') else 'N/A'
            print(f"[{event.timestamp}] CREW FAILED: '{event.crew_name}' (ID: {crew_id})")
            print(f"  Error Message: {event.error_message}")
            if event.original_exception:
                print(f"  Original Exception: {type(event.original_exception).__name__}: {event.original_exception}")

        # --- Tool Event Handlers ---
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_started(source, event: ToolUsageStartedEvent):
            agent_role = source.role if hasattr(source, 'role') else 'Unknown Agent'
            print(f"[{event.timestamp}] TOOL STARTED: '{event.tool_name}' by Agent '{agent_role}'")
            # print(f"  Input: {event.tool_input}") # Can be verbose

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_finished(source, event: ToolUsageFinishedEvent):
            agent_role = source.role if hasattr(source, 'role') else 'Unknown Agent'
            print(f"[{event.timestamp}] TOOL FINISHED: '{event.tool_name}' by Agent '{agent_role}'")
            # print(f"  Output: {event.output}") # Can be verbose

        @crewai_event_bus.on(ToolUsageErrorEvent)
        def on_tool_error(source, event: ToolUsageErrorEvent):
            agent_role = source.role if hasattr(source, 'role') else 'Unknown Agent'
            print(f"[{event.timestamp}] TOOL ERROR: '{event.tool_name}' by Agent '{agent_role}'")
            print(f"  Error: {event.error}")
            if event.original_exception:
                print(f"  Original Exception: {type(event.original_exception).__name__}: {event.original_exception}")

        # --- Flow Event Handlers ---
        @crewai_event_bus.on(MethodExecutionStartedEvent)
        def on_flow_method_started(source, event: MethodExecutionStartedEvent):
            flow_name = source.__class__.__name__ if hasattr(source, '__class__') else 'Unknown Flow'
            print(f"[{event.timestamp}] FLOW METHOD STARTED: '{event.method_name}' in Flow '{flow_name}'")

        @crewai_event_bus.on(MethodExecutionFinishedEvent)
        def on_flow_method_finished(source, event: MethodExecutionFinishedEvent):
            flow_name = source.__class__.__name__ if hasattr(source, '__class__') else 'Unknown Flow'
            print(f"[{event.timestamp}] FLOW METHOD FINISHED: '{event.method_name}' in Flow '{flow_name}'")
            # print(f"  Result: {event.result}") # Can be verbose

        @crewai_event_bus.on(MethodExecutionFailedEvent)
        def on_flow_method_failed(source, event: MethodExecutionFailedEvent):
            flow_name = source.__class__.__name__ if hasattr(source, '__class__') else 'Unknown Flow'
            print(f"[{event.timestamp}] FLOW METHOD FAILED: '{event.method_name}' in Flow '{flow_name}'")
            print(f"  Error Message: {event.error_message}")
            if event.original_exception:
                print(f"  Original Exception: {type(event.original_exception).__name__}: {event.original_exception}")

        print(f"[{datetime.datetime.now()}] LoggingCustomListener: All listeners set up.")

# Create an instance of your listener.
# This line is crucial: it ensures the listener registers itself with CrewAI's event bus
# when this module (custom_event.py) is imported.
logging_custom_listener = LoggingCustomListener()
print(f"[{datetime.datetime.now()}] LoggingCustomListener instance created and registered globally in custom_event.py.")