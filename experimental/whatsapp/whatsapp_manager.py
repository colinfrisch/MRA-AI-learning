# whatsapp_inference.py
import json
import logging
import requests
from typing import List
from dotenv import load_dotenv
import sys
import os



class WhatsappManager:
    """
    Stand-alone helper around the WhatsApp Cloud API.
    Keeps every inbound / outbound message for one user in memory.
    """

    GRAPH_URL_TMPL = "https://graph.facebook.com/{version}/{phone_number_id}/messages"

    def __init__(
        self,
        wa_id: str,
        *,
        access_token: str,
        phone_number_id: str,
        api_version: str = "v22.0",
    ):
        """
        Parameters
        ----------
        wa_id : str
            The WhatsApp ID of the user (comes from webhook payload).
        access_token : str
            Permanent token from Meta.
        phone_number_id : str
            Your business phoneNumberId (also in the webhook payload URL).
        api_version : str, optional
            Graph version to call. Defaults to 'v19.0'.
        """
        self.wa_id = wa_id
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.api_version = api_version

        # message log, newest last
        self.messages: List[dict] = []  # each item: {"direction": "in"/"out", "text": str}

    # ---------- internal helpers ----------

    def _build_payload(self, text: str) -> str:
        """Return the JSON body required by the Cloud API."""
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "to": self.wa_id,
                "type": "text",
                "text": {"preview_url": False, "body": text},
            }
        )

    def _graph_url(self) -> str:
        return self.GRAPH_URL_TMPL.format(
            version=self.api_version, phone_number_id=self.phone_number_id
        )

    # ---------- public API ----------

    def record_incoming(self, text: str) -> None:
        """Call this from your webhook handler when a message arrives."""
        self.messages.append({"direction": "in", "text": text})

    def send_message(self, text: str, timeout: int = 10) -> requests.Response:
        """
        Send `text` to the user and append it to the local history.
        Returns the `requests.Response` so the caller can inspect status / JSON.
        """
        body = self._build_payload(text)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        resp = requests.post(self._graph_url(), headers=headers, data=body, timeout=timeout)
        resp.raise_for_status()

        # keep a record of what we sent
        self.messages.append({"direction": "out", "text": text})

        logging.info("Sent message to %s: %s", self.wa_id, text)
        logging.debug("Graph API response: %s", resp.text)
        return resp
