# -*- coding: utf-8 -*-
import os

from remotesystem import RemoteSystem

from squape.internal.exceptions import SquishserverError
from squape.report import log


class SquishServer:
    """Class to represent a local or remote squishserver"""

    def __init__(self, location=None, host="127.0.0.1", port=4322):
        """Open an RemoteSystem connection to a machine with a running squishserver

        Args:
            location (_type_, optional):    location of the Squish package.
                                            Defaults to the "SQUISH_PREFIX".
            host (str, optional): host of the squishserver. Defaults to "127.0.0.1".
            port (int, optional): port of the squishserver. Defaults to 4322.
        """
        if location is None:
            self.location = os.environ["SQUISH_PREFIX"]

        self.host = host
        self.port = port
        try:
            self.remotesys = RemoteSystem(host, port)
        except Exception:
            raise SquishserverError(
                f"Unable to connect to squishserver ({host}:{port})"
            )

    def _config_squishserver(self, config_option: str, params=None, cwd=None):
        """A helper function that contains general code for the squishserver congifuration

        Args:
            config_option (str): the config option to be used during configuration
            params (list, optional): the configuration parameters. Defaults to [].
        """
        if params is None:
            params = []
        cmd = ["squishserver", "--config", config_option, *params]
        if cwd is None:
            cwd = self.location

        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError(
                "Squishserver was not able to perform "
                f"{config_option} configuration operation"
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
        log(f"Registering AUT {aut} with location: {path}")
        self._config_squishserver("addAUT", [aut, path])

    def removeAUT(self, aut: str, path: str) -> None:
        """Remove an registered AUT

        Args:
            aut (str): the name of the executable
            path (str): path to the executable folder
        """
        log(f"Removing registered AUT {aut} with location: {path}")
        self._config_squishserver("removeAUT", [aut, path])

    def addAppPath(self, path: str) -> None:
        """Register an AUT path

        Args:
            path (str): the AUT path to register
        """
        log(f"Registering AUT path: {path}")
        self._config_squishserver("addAppPath", [path])

    def removeAppPath(self, path: str) -> None:
        """Remove an registered AUT path

        Args:
            path (str): the path to the AUT
        """
        log(f"Removing registered AUT path: {path}")
        self._config_squishserver("removeAppPath", [path])

    def addAttachableAut(self, aut: str, port: int, host="127.0.0.1") -> None:
        """Register an attachable AUT

        Args:
            aut (str): the name of the attachable AUT
            port (int): port of the machine where the attachable AUT
                        is supposed to be running.
            host (str, optional):   host of the machine where the attachable AUT
                                    is supposed to be running.
                                    Defaults to "127.0.0.1".
        """
        log(f"Registering an attachable AUT {aut} on port: {port}")
        self._config_squishserver("addAttachableAUT", [aut, f"{host}:{port}"])

    def removeAttachableAut(self, aut: str, port: int, host="127.0.0.1") -> None:
        """Register an attachable AUT

        Args:
            aut (str): the name of the attachable AUT
            port (int): port of the machine where the attachable AUT
                        is supposed to be running.
            host (str, optional):   host of the machine where the attachable AUT
                                    is supposed to be running.
                                    Defaults to "127.0.0.1".
        """
        log(f"Removing registered attachable AUT {aut} on port: {port}")
        self._config_squishserver("removeAttachableAUT", [aut, f"{host}:{port}"])
