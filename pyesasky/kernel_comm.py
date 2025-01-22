import time
import zmq
import json
import pyesasky.constants as const
from pyesasky.exceptions import CommNotInitializedError
from IPython import get_ipython
import uuid
from ipykernel.comm import Comm
from typing import Callable, Dict, Any
from pyesasky.log_utils import logger
import pyesasky.message_utils as m

ContentType = Dict[str, Any]
CommCallback = Callable[[str, ContentType], None]


class KernelComm:

    def __init__(self, widget_comm: Comm, widget_on_msg: CommCallback = None):
        self.kernel = get_ipython().kernel
        self.shell_streams = self.kernel.shell_streams
        self.widget_comm = widget_comm
        self.widget_on_msg = widget_on_msg
        self.comm_established = False
        self.default_timeout = 5

        if not self._valid_widget_comm(widget_comm):
            raise CommNotInitializedError("The comm is not valid")

        self.widget_comm.on_msg(self._handle_unsolicited_message)

    def send_message(self, content, buffers=None) -> str:
        """
        Sends a message to the frontend if communication is established,
        otherwise attempts to initialize communication before sending the message.

        Args:
            content (str): The message content.
            buffers (Optional[Iterable]): Optional buffers for sending.

        Returns:
            str: The message ID of the request

        Raises:
            CommNotInitializedError: If communication cannot be established.
        """
        if not self.comm_established and not self._initialize_comm(buffers):
            raise CommNotInitializedError("Communication could not be established.")

        return self._send_message(content, buffers)

    def wait_message(self, msg_id: str, max_wait_time: float = 5):
        """
        Waits for a message with the given ID within a timeout period.

        Args:
            msg_id (str): The message ID to wait for.
            max_wait_time (float): Maximum time to wait (in seconds).

        Returns:
            dict: The parsed message.

        Raises:
            CommNotInitializedError: If shell streams are not initialized.
            TimeoutError: If the message is not received within the timeout.
        """
        if not self.shell_streams:
            raise CommNotInitializedError("Shell streams are not initialized.")

        stream = self.shell_streams[0]
        start_time = time.time()

        while time.time() - start_time <= max_wait_time:
            try:
                message = self._poll_for_message(stream)
                if message:
                    parsed_msg = self._parse_message(message)
                    if parsed_msg and m.is_init_message(parsed_msg):
                        logger.debug("Comms established")
                        self.comm_established = True
                        
                    if parsed_msg and m.get_message_id(parsed_msg) == msg_id:
                        logger.debug("Message recieved %s", parsed_msg)
                        return parsed_msg
            except zmq.Again:
                continue  # No message received, continue polling

            time.sleep(0.1)  # Avoid busy waiting

        # If the loop completes without finding the message
        raise TimeoutError(f"Timed out waiting for message with ID '{msg_id}'")

    def _poll_for_message(self, stream):
        # Poll for a message with a short timeout (milliseconds)
        if stream.socket.poll(timeout=100):
            return stream.socket.recv_multipart()
        return None

    def _parse_message(self, msg_parts):
        # Attempt to decode and parse JSON from message parts
        for part in msg_parts:
            try:
                decoded_part = part.decode("utf-8")
                parsed_msg = json.loads(decoded_part)

                if not m.is_response_message(parsed_msg):
                    continue

                return parsed_msg
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue  # Skip non-JSON parts or decoding errors
        return None

    def _send_message(self, content, buffers) -> str:
        message_id = str(uuid.uuid4())
        content[const.MESSAGE_CONTENT_ID] = message_id
        content[const.MESSAGE_ORIGIN] = "pyesasky"

        if self._valid_widget_comm(self.widget_comm):
            logger.debug('Sending message %s', content)
            self.widget_comm.send(
                data={const.MESSAGE_METHOD: "custom", const.MESSAGE_CONTENT: content},
                buffers=buffers,
            )
            return message_id

        return None

    def _initialize_comm(self, buffers):
        try:
            self._send_message({"event": "initTest"}, buffers)
            self.wait_message(const.MESSAGE_INIT_ID_FLAG, self.default_timeout)
            self.comm_established = True
            time.sleep(0.5)
            return True
        except TimeoutError:
            self.comm_established = False
            return False

    def _valid_widget_comm(self, comm: Comm):
        return comm is not None and (
            comm.kernel is not None if hasattr(comm, "kernel") else True
        )

    def _handle_unsolicited_message(self, message):
        if not self.widget_on_msg:
            return
        content = m.get_nested_message_content(message)
        if content and const.MESSAGE_CONTENT_TYPE in content:
            msg_type = content[const.MESSAGE_CONTENT_TYPE]
            self.widget_on_msg(msg_type, content)
