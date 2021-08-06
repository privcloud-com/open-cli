#!/usr/bin/python3
"""Open-CLI."""
import os
import logging
import warnings
import requests
import yaml

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pyfiglet import print_figlet

from . import help
from . import parser
from . import completer
from . import formatter
from .openapi_extension import OpenAPIExt

# Suppress bravado warnings
warnings.filterwarnings("ignore")


class OpenCLI:
    """CLI processor."""

    def __init__(
        self, source, history_path, output_format=formatter.JSON, headers=None, print_request_time=False
    ):
        """Initialize the CLI processor."""
        self.history_path = history_path
        self.output_format = output_format
        self.print_request_time = print_request_time

        self.logger = logging.getLogger("open-cli3")
        self.logger.debug(
            "Creating a python client based on %s, headers: %s", source, headers
        )

        headers = self._parse_headers(headers)

        # Handle non-url sources
        spec = None
        if os.path.exists(source):
            with open(source) as f:
                spec = yaml.safe_load(f.read())

        if not spec:
            spec = requests.get(source).json()
        self.client = OpenAPIExt(spec)

        # Get the CLI prompt name from the spec title
        self.name = self.client.info.title

        # Initialize a command parser based on the client
        self.command_parser = parser.CommandParser(client=self.client)

    def run_loop(self):
        """Run the CLI loop."""
        history = FileHistory(self.history_path)
        command_completer = completer.CommandCompleter(client=self.client)
        print_figlet("PrivCloud", font="starwars", width=100)

        while True:

            try:
                input_text = prompt(
                    u"%s $ " % self.name,
                    history=history,
                    completer=command_completer,
                    auto_suggest=AutoSuggestFromHistory(),
                )
                self.execute(command=input_text)

            except KeyboardInterrupt:
                exit("User Exited")

            except Exception as exc:
                self.logger.error(exc)

    def execute(self, command):
        """Parse and execute the given command."""
        self.logger.debug("Invoke authentication")
        try:
            with open("current_auth_token.txt") as f:
                access_token = f.read()
                if access_token:
                    for k in self.client.components.securitySchemes.keys():
                        self.client.authenticate(k, access_token)
        except FileNotFoundError as e:
            self.logger.debug(str(e))
        self.logger.debug("Parsing the input text %s", command)
        operation, arguments = self.command_parser.parse(text=command)

        if help.is_requested(arguments):
            self.logger.debug("Help requested for operation %s", operation)
            return help.show(operation)

        self.logger.debug("Invoke operation %s with arguments %s", operation, arguments)
        response = operation(**arguments)

        if not isinstance(response, list):
            if hasattr(response, "_raw_data"):
                access_token = response._raw_data.get("access_token")
                expires_at = response._raw_data.get("expires_at")
                if access_token and expires_at:
                    with open("current_auth_token.txt", "w") as f:
                        f.seek(0)
                        f.write(access_token)
                        f.truncate()

        if isinstance(response, list):
            response = [r._raw_data for r in response]
        else:
            if hasattr(response, "_raw_data"):
                response = response._raw_data
        self.logger.debug("Formatting response %s", response)
        print(formatter.format_response(response, output_format=self.output_format))
        if self.print_request_time:
            print(f"Request time: {self.client.request_time_sec} seconds")

    @staticmethod
    def _parse_headers(headers):
        """Parse headers list into a dictionary."""
        try:
            return dict(header.split(":") for header in headers)
        except:
            raise ValueError("Invalid headers %s" % headers)


if __name__ == "__main__":
    OpenCLI("http://petstore.swagger.io/v2/swagger.json").run_loop()
