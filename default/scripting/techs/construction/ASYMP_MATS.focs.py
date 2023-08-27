from common.base_prod import TECH_COST_MULTIPLIER
from focs._tech import *

Tech(
    name="CON_ASYMP_MATS",
    description="CON_ASYMP_MATS_DESC",
    short_description="THEORY_SHORT_DESC",
    category="CONSTRUCTION_CATEGORY",
    researchcost=20 * TECH_COST_MULTIPLIER,
    researchturns=2,
    tags=["PEDIA_CONSTRUCTION_CATEGORY", "THEORY"],
    graphic="icons/tech/asymptotic_materials.png",
)
