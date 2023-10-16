from controller.ctrl_principal import CtrlPrincipal
import sys,os

sys.path.insert(0,os.path.abspath(os.curdir))

if __name__ == "__main__":
    ctrl_principal = CtrlPrincipal()
    ctrl_principal.inicia()