import time
import threading
import uuid
from typing import Callable, Dict, Any, Optional

from ipykernel.comm import Comm

import pyesasky.constants as const
import pyesasky.message_utils as m
from pyesasky.exceptions import CommNotInitializedError
from pyesasky.log_utils import logger

ContentType = Dict[str, Any]
CommCallback = Callable[[str, ContentType], None]


class KernelComm:

    def __init__(self, widget_comm: Comm, widget_on_msg: Optional[CommCallback] = None):
        self.widget_comm = widget_comm
        self.widget_on_msg = widget_on_msg
        self.comm_established = False
        self.default_timeout = 5

        self._pending = {}  # msg_id -> {"event": Event, "response": dict}
        self._lock = threading.Lock()

        if not self._valid_widget_comm(widget_comm):
            raise CommNotInitializedError("The comm is not valid")

        self.widget_comm.on_msg(self._on_message)

    def send_message(self, content, buffers=None) -> Optional[str]:
        """
        Sends a message to the frontend. Initializes comm first if needed.
        For request/response, use send_and_wait() instead.
        """
        if not self.comm_established and not self._initialize_comm(buffers):
            raise CommNotInitializedError("Communication could not be established.")

        return self._send_message(content, buffers)

    def send_and_wait(self, content, buffers=None, timeout: float = 5):
        """
        Sends a message and waits for response. Registers listener before
        sending to avoid missing fast responses.
        """
        if not self.comm_established and not self._initialize_comm(buffers):
            raise CommNotInitializedError("Communication could not be established.")

        msg_id = str(uuid.uuid4())
        event = threading.Event()

        with self._lock:
            self._pending[msg_id] = {"event": event, "response": None}

        content[const.MESSAGE_CONTENT_ID] = msg_id
        content[const.MESSAGE_ORIGIN] = "pyesasky"

        if not self._valid_widget_comm(self.widget_comm):
            with self._lock:
                self._pending.pop(msg_id, None)
            raise CommNotInitializedError("Widget comm is not valid.")

        logger.debug('Sending message %s', content)
        self.widget_comm.send(
            data={const.MESSAGE_METHOD: "custom", const.MESSAGE_CONTENT: content},
            buffers=buffers,
        )

        if not event.wait(timeout=timeout):
            with self._lock:
                self._pending.pop(msg_id, None)
            raise TimeoutError(f"Timed out waiting for message with ID '{msg_id}'")

        with self._lock:
            data = self._pending.pop(msg_id, None)

        if data and data["response"]:
            logger.debug("Message received %s", data["response"])
            return data["response"]

        raise TimeoutError(f"No response received for message ID '{msg_id}'")

    def _on_message(self, message):
        """Routes incoming messages to pending waiters or the widget callback."""
        content = m.get_nested_message_content(message)

        # Check for init message
        raw_content = message.get(const.MESSAGE_CONTENT, {})
        data = raw_content.get(const.MESSAGE_DATA, {}) if raw_content else {}
        inner = data.get(const.MESSAGE_CONTENT, {}) if data else {}

        if inner.get(const.MESSAGE_INIT):
            logger.debug("Comms established")
            self.comm_established = True
            with self._lock:
                pending = self._pending.get(const.MESSAGE_INIT_ID_FLAG)
                if pending:
                    pending["response"] = raw_content
                    pending["event"].set()
            return

        # Check for response to pending request
        msg_id = m.get_message_id(raw_content)
        if msg_id:
            with self._lock:
                pending = self._pending.get(msg_id)
                if pending:
                    pending["response"] = raw_content
                    pending["event"].set()
                    return

        # Unsolicited message (e.g. download request)
        if content and const.MESSAGE_CONTENT_TYPE in content and self.widget_on_msg:
            self.widget_on_msg(content[const.MESSAGE_CONTENT_TYPE], content)

    def _send_message(self, content, buffers) -> Optional[str]:
        msg_id = str(uuid.uuid4())
        content[const.MESSAGE_CONTENT_ID] = msg_id
        content[const.MESSAGE_ORIGIN] = "pyesasky"

        if self._valid_widget_comm(self.widget_comm):
            logger.debug('Sending message %s', content)
            self.widget_comm.send(
                data={const.MESSAGE_METHOD: "custom", const.MESSAGE_CONTENT: content},
                buffers=buffers,
            )
            return msg_id

        return None

    def _initialize_comm(self, buffers):
        event = threading.Event()
        with self._lock:
            self._pending[const.MESSAGE_INIT_ID_FLAG] = {"event": event, "response": None}

        self._send_message({"event": "initTest"}, buffers)

        if not event.wait(timeout=self.default_timeout):
            with self._lock:
                self._pending.pop(const.MESSAGE_INIT_ID_FLAG, None)
            self.comm_established = False
            return False

        with self._lock:
            self._pending.pop(const.MESSAGE_INIT_ID_FLAG, None)

        self.comm_established = True
        time.sleep(0.5)
        return True

    def _valid_widget_comm(self, comm: Comm):
        return comm is not None and (
            comm.kernel is not None if hasattr(comm, "kernel") else True
        )
