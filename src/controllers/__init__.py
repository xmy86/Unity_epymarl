REGISTRY = {}

from .basic_controller import BasicMAC
from .basic_controller_continue import BasicMACContinue
from .non_shared_controller import NonSharedMAC
from .maddpg_controller import MADDPGMAC

REGISTRY["basic_mac"] = BasicMAC
REGISTRY["non_shared_mac"] = NonSharedMAC
REGISTRY["maddpg_mac"] = MADDPGMAC
REGISTRY["basic_mac_continue"] = BasicMACContinue