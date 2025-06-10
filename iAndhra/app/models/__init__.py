# Master Tables
from iAndhra.app.models.states import State
from iAndhra.app.models.districts import District
from iAndhra.app.models.blocks import Block
from iAndhra.app.models.villages import Village
from iAndhra.app.models.panchayats import Panchayat

from iAndhra.app.models.territory import TerritoryJoin

# # Census Masters
from iAndhra.app.models.population import Population
from iAndhra.app.models.livestocks import Livestock
from iAndhra.app.models.lulc import LULC
from iAndhra.app.models.crops import Crop
from iAndhra.app.models.waterbody import WaterbodyType
from iAndhra.app.models.industries import Industry

# Census Data Tables
from iAndhra.app.models.livestocks_census import LivestockCensus
from iAndhra.app.models.crop_census import CropCensus
from iAndhra.app.models.population_census import PopulationCensus
from iAndhra.app.models.waterbody_census import WaterbodyCensus
from iAndhra.app.models.lulc_census import LULCCensus
from iAndhra.app.models.groundwater_extraction import GroundwaterExtraction
from iAndhra.app.models.rainfall import Rainfall
from iAndhra.app.models.strange_table import StrangeTable


# Block Data Tables
from iAndhra.app.models.block_territory import BlockTerritory
from iAndhra.app.models.block_livestocks import BlockLivestock
from iAndhra.app.models.block_pop import BlockPop
from iAndhra.app.models.block_crops import BlockCrop
from iAndhra.app.models.block_industries import BlockIndustry
from iAndhra.app.models.block_ground import BlockGround
from iAndhra.app.models.block_lulc import BlockLULC
from iAndhra.app.models.budget_entities import BudgetEntity


from iAndhra.app.models.block_rainfall import BlockRainfall
from iAndhra.app.models.block_transfer_type import BlockTransferType
from iAndhra.app.models.block_transfer_sector import BlockTransferSector
from iAndhra.app.models.block_transfer import BlockWaterTransfer
from iAndhra.app.models.block_progress import BlockProgress
from iAndhra.app.models.block_category import BlockCategory


# Auth Tables
from iAndhra.app.models.users import User