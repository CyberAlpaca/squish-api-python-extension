import squish
import test
from remotesystem import RemoteSystem
import os
import pathlib
from squape.report import log
from squape.internal.exceptions import SquishserverError

class SquishServer:
    def __init__(self, location=None, host='127.0.0.1', port=4322):
        if location is None:
            self.location = os.environ['SQUISH_PREFIX']

        self.host = host
        self.port = port
        self.remotesys = RemoteSystem(host, port)
            

    def addAUT(self, aut: str, path: str) -> None:
        cmd = [
            "squishserver", '--config', 'addAUT', aut, path
        ]
        cwd = self.location
        log(f"Registering AUT {aut} with location: {path}")
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError("Squishserver was not able to register the AUT")
        
    def addAppPath(self, path: str) -> None:
        cmd = [
            "squishserver", '--config', 'addAppPath', path
        ]
        cwd = self.location
        log(f"Registering AUT path: {path}")
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError("Squishserver was not able to register the AUT path."
                                    f"{stdout}"
                                    )
        
    def addAttachableAut(self, aut: str, port: int, host='127.0.0.1') -> None:
        cmd = [
            "squishserver", '--config', 'addAttachableAUT', aut, host + ':' + str(port)
        ]
        cwd = self.location
        log(f"Registering an attachable AUT {aut} on port: {port}")
        (exitcode, stdout, stderr) = self.remotesys.execute(cmd, cwd)
        if exitcode != "0":
            raise SquishserverError("Squishserver was not able to register an attachable AUT.\n"
                                    f"{stdout}"
                                    )
        