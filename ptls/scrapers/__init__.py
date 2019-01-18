from typing import Set

from ._Athletico import Athletico
from ._ATI import ATI
from ._CORA import CORA
from ._Pivot import Pivot
from ._Professional import Professional
from ._Select import Select
from ._URPT import URPT
from ._USPh import USPh

SCRAPERS: dict = dict({
    Athletico.company_name: Athletico,
    ATI.company_name: ATI,
    CORA.company_name: CORA,
    Pivot.company_name: Pivot,
    Professional.company_name: Professional,
    Select.company_name: Select,
    URPT.company_name: URPT,
    USPh.company_name: USPh
})