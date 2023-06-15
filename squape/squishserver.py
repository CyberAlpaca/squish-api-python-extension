# -*- coding: utf-8 -*-
import os
from pathlib import Path

from remotesystem import RemoteSystem

import squish
from squape.internal.exceptions import EnvironmentError
from squape.internal.exceptions import SquishserverError
from squape.report import debug
from squape.report import log


class SquishServer:
    """Class to represent a local or remote squishserver"""

    def __init__(self, location=None, host=None, port=None):
        """Open an RemoteSystem connection to a machine with a running squishserver

        Args:
            location (_type_, optional):    location of the Squish package.
                                            Defaults to the "SQUISH_PREFIX".
            host (str, optional): host of the squishserver.
                                  Defaults to SQUISHRUNNER_HOST if it is defined,
                                  else "127.0.0.1".
            port (int, optional): port of the squishserver.
                                  Defaults to SQUISHRUNNER_PORT if it is defined,
                                  else 4322.
        """
        if location is None:
            try:
                self.location = os.environ["SQUISH_PREFIX"]
            except KeyError:
                raise EnvironmentError(
                    "The SQUISH_PREFIX variable is not set, "
                    "and location of the squishserver "
                    f"({self.host}:{self.port}) is not specified!"
                )
        else:
            self.location = location

        if host is None:
            self.host = os.environ.get("SQUISHRUNNER_HOST", "127.0.0.1")

        if port is None:
            if "SQUISHRUNNER_PORT" in os.environ:
                self.port = int(os.environ["SQUISHRUNNER_PORT"])
            else:
                self.port = 4322

        try:
            self.remotesys = RemoteSystem(host, port)
        except Exception:
            raise SquishserverError(
                f"Unable to connect to squishserver ({host}:{port})"
            )

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
            "Executing command: squishserver --config "
            f"{' '.join(params)}",
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
            ctx : Application Context
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
            ctx : Application Context
        """
        log(f"[Squishserver {self.host}:{self.port}] " f"Start an application {aut}")
        ctx = squish.startApplication(aut, self.host, self.port)
        return ctx
