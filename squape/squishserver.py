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

    def addAUT(self, aut: str, path: str) -> None:
        """Register an AUT

        Args:
            aut (str): the name of the executable
            path (str): path to the executable folder
        """
        cmd = ["squishserver", "--config", "addAUT", aut, path]
        cwd = self.location
        log(f"Registering AUT {aut} with location: {path}")
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError(
                "Squishserver was not able to register the AUT"
                f"exit code: {exitcode}"
                f"stdout: {stdout}"
                f"stderr: {stderr}"
            )

    def addAppPath(self, path: str) -> None:
        """Register an AUT path

        Args:
            path (str): the AUT path to register
        """
        cmd = ["squishserver", "--config", "addAppPath", path]
        cwd = self.location
        log(f"Registering AUT path: {path}")
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError(
                "Squishserver was not able to register the AUT path"
                f"exit code: {exitcode}"
                f"stdout: {stdout}"
                f"stderr: {stderr}"
            )

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
        cmd = [
            "squishserver",
            "--config",
            "addAttachableAUT",
            aut,
            host + ":" + str(port),
        ]
        cwd = self.location
        log(f"Registering an attachable AUT {aut} on port: {port}")
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError(
                "Squishserver was not able to register an attachable AUT"
                f"exitcode: {exitcode}"
                f"stdout: {stdout}"
                f"stderr: {stderr}"
            )
