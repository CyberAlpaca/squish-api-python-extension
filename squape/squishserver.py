# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List

try:
    import squish
except ImportError:
    import squishtest as squish

from remotesystem import RemoteSystem

from squape.internal.exceptions import EnvironmentError
from squape.internal.exceptions import SquishserverError
from squape.report import debug, log


class SquishServer:
    """Class to configure a running local or remote squishserver"""

    def __init__(self, location=None, host=None, port=None):
        """Open an RemoteSystem connection to a running squishserver

        Args:
            location (str, optional): The location of the Squish package.
                If provided, this value will be used.
                If not provided, it will be taken from the squishserver process.
            host (str, optional): The host of the squishserver.
                If provided, this value will be used.
                If not provided, the value of the squishrunner's "--host"
                will be used if set.
                If "--host" was not set, the default value "127.0.0.1" will be used.
            port (int, optional): The port of the squishserver.
                If provided, this value will be used.
                If not provided, the value of the squishrunner's "--port"
                will be used if set.
                If "--port" was not set, the default value "4322" will be used.
        """

        if host is None:
            self._host = os.environ.get("SQUISHRUNNER_HOST", "127.0.0.1")
        else:
            self._host = host

        if port is None:
            if "SQUISHRUNNER_PORT" in os.environ:
                self._port = int(os.environ["SQUISHRUNNER_PORT"])
            else:
                self._port = 4322
        else:
            self._port = port

        try:
            self._remotesys = RemoteSystem(self.host, self.port)
        except Exception:
            raise SquishserverError(
                f"Unable to connect to squishserver ({self.host}:{self.port})"
            )

        if location is None:
            try:
                self._location = self.remotesys.getEnvironmentVariable("SQUISH_PREFIX")
            except KeyError:
                raise EnvironmentError(
                    "The SQUISH_PREFIX environment variable is not set, "
                    "and location of the squishserver "
                    f"({self.host}:{self.port}) is not specified!"
                )
        else:
            self._location = location

    @property
    def host(self) -> str:
        """The host of the squishserver."""
        return self._host

    @property
    def port(self) -> int:
        """The port of the squishserver."""
        return self._port

    @property
    def location(self) -> str:
        """The location of the Squish package."""
        return self._location

    @property
    def remotesys(self) -> RemoteSystem:
        """RemoteSystem of the squishserver."""
        return self._remotesys

    @property
    def os_name(self) -> str:
        """Name of the Operating System where the squishserver is running."""
        return self.remotesys.getOSName()

    def _config_squishserver(self, config_option: str, params=None, cwd=None):
        """Configures the squishserver by calling 'squishserver --config ...' command


        Args:
            config_option (str): the config option to be used during configuration.
            params (list, optional): the configuration parameters. Defaults to [].
            cwd (str):  the path to the current working directory.
                        Defaults to the "SQUISH_PREFIX" environment vairable.
        """
        if params is None:
            params = []
        cmd = ["squishserver", "--config", config_option, *params]
        if cwd is None:
            cwd = self.location

        debug(
            f"[Squishserver {self.host}:{self.port}] "
            f"Executing command: {' '.join(cmd)}",
            f"cwd: {cwd}",
        )
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError(
                f"[Squishserver {self.host}:{self.port}] "
                "was not able to perform "
                f"{config_option} configuration operation"
                f"\nParameters: {' '.join(params)}"
                f"\nexit code: {exitcode}"
                f"\nstdout: {stdout}"
                f"\nstderr: {stderr}"
            )

    def addAUT(self, aut: str, path: str) -> None:
        """Register an AUT

        Args:
            aut (str): the name of the executable
            path (str): path to the executable folder
        """
        log(
            f"[Squishserver {self.host}:{self.port}] "
            f"Registering {Path(path)/aut} AUT"
        )
        self._config_squishserver("addAUT", [aut, path])

    def removeAUT(self, aut: str, path: str) -> None:
        """Remove registered AUT

        Args:
            aut (str): the name of the executable
            path (str): path to the executable folder
        """
        log(
            f"[Squishserver {self.host}:{self.port}] "
            f"Removing registered {Path(path)/aut} AUT"
        )
        self._config_squishserver("removeAUT", [aut, path])

    def addAppPath(self, path: str) -> None:
        """Register an AUT path

        Args:
            path (str): the AUT path to register
        """
        log(f"[Squishserver {self.host}:{self.port}] " f"Registering AUT path: {path}")
        self._config_squishserver("addAppPath", [path])

    def removeAppPath(self, path: str) -> None:
        """Remove a registered AUT path

        Args:
            path (str): the path to the AUT
        """
        log(
            f"[Squishserver {self.host}:{self.port}] "
            f"Removing registered AUT path: {path}"
        )
        self._config_squishserver("removeAppPath", [path])

    def addAttachableAut(self, aut: str, port: int, host: str = "127.0.0.1") -> None:
        """Register an attachable AUT

        Args:
            aut (str): the name of the attachable AUT
            port (int): port of the machine where the attachable AUT
                        is supposed to be running.
            host (str, optional):   host of the machine where the attachable AUT
                                    is supposed to be running.
                                    Defaults to "127.0.0.1".
        """
        log(
            f"[Squishserver {self.host}:{self.port}] "
            f"Registering an attachable AUT {aut}"
        )
        self._config_squishserver("addAttachableAUT", [aut, f"{host}:{port}"])

    def removeAttachableAut(self, aut: str, port: int, host: str = "127.0.0.1") -> None:
        """Remove registered attachable AUT

        Args:
            aut (str): the name of the attachable AUT
            port (int): port of the machine where the attachable AUT
                        is supposed to be running.
            host (str, optional):   host of the machine where the attachable AUT
                                    is supposed to be running.
                                    Defaults to "127.0.0.1".
        """
        log(
            f"[Squishserver {self.host}:{self.port}] "
            f"Removing registered attachable AUT {aut}"
        )
        self._config_squishserver("removeAttachableAUT", [aut, f"{host}:{port}"])

    def attachToApplication(self, aut: str):
        """
        Attaches to an application with given name.

        Args:
            aut (str): the name of the attachable AUT

        Returns:
            (ApplicationContext): application context
        """
        log(f"[Squishserver {self.host}:{self.port}] " f"Attach to application {aut}")
        ctx = squish.attachToApplication(aut, self.host, self.port)
        return ctx

    def startApplication(self, aut: str):
        """
        Starts to an application with given name.

        Args:
            aut (str): the name of the mapped AUT

        Returns:
            (ApplicationContext): application context
        """
        log(f"[Squishserver {self.host}:{self.port}] " f"Start an application {aut}")
        ctx = squish.startApplication(aut, self.host, self.port)
        return ctx

    def execute_cmd_sync(self, command: str, options: List[str] = None) -> List[str]:
        """Executes the command with optional arguments synchronously.
        This convenience function runs a command as is, leveraging the environment
        settings provided by the squishserver.

        For more advanced use cases, such as specifying a custom current working
        directory (cwd) or environment variables, please use the
        `squishserver.remotesys.execute(...)` method directly.

        Args:
            command (str): The command to execute
            options (List[str]): A list of options for the command

        Returns:
            A list/array with three elements: exitcode, stdout, stderr
        """
        cmd = [command] + (options or [])
        return self.remotesys.execute(cmd)

    def execute_cmd_async(self, command: str, options: List[str] = None) -> None:
        """Executes the command with optional arguments asynchronously.
        This convenience function runs a command as is, leveraging the environment
        settings provided by the squishserver.

        For more advanced use cases, such as specifying a custom current working
        directory (cwd) or environment variables, please use the
        `squishserver.remotesys.execute(...)` method directly.

        Args:
            command (str): The command to execute
            options (List[str]): A list of options for the command

        Returns:
            None
        """
        options = options or []
        if self.os_name == "Windows":
            cmd = ["cmd.exe", "/s", "/c", "start", "", "/min", command, *options]
        else:
            cmd = ["sh", "-c", f"{command} {' '.join(options)} >/dev/null 2>&1 &"]
        self.remotesys.execute(cmd)
