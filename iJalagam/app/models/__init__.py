# Master Tables
from iJalagam.app.models.states import State
from iJalagam.app.models.districts import District
from iJalagam.app.models.blocks import Block
from iJalagam.app.models.villages import Village

from iJalagam.app.models.territory import TerritoryJoin

# Census Masters
from iJalagam.app.models.population import Population
from iJalagam.app.models.livestocks import Livestock
from iJalagam.app.models.lulc import LULC
from iJalagam.app.models.crops import Crop
from iJalagam.app.models.waterbody import WaterbodyType
from iJalagam.app.models.industries import Industry

# Census Data Tables
from iJalagam.app.models.livestocks_census import LivestockCensus
from iJalagam.app.models.crop_census import CropCensus
from iJalagam.app.models.population_census import PopulationCensus
from iJalagam.app.models.waterbody_census import WaterbodyCensus
from iJalagam.app.models.lulc_census import LULCCensus
from iJalagam.app.models.groundwater_extraction import GroundwaterExtraction
from iJalagam.app.models.rainfall import Rainfall
from iJalagam.app.models.strange_table import StrangeTable


# Block Data Tables
from iJalagam.app.models.desktop.block_crops import BlockCrop
from iJalagam.app.models.desktop.block_groundwater import BlockGroundwater
from iJalagam.app.models.desktop.block_industries import BlockIndustry
from iJalagam.app.models.desktop.block_livestocks import BlockLivestock
from iJalagam.app.models.desktop.block_lulc import BlockLulc
from iJalagam.app.models.desktop.block_populations import BlockPopulation
from iJalagam.app.models.desktop.block_rainfall import BlockRainfall
from iJalagam.app.models.desktop.block_territory import BlockTerritory
from iJalagam.app.models.desktop.block_waterbodies import BlockWaterbody


# Auth Tables
from iJalagam.app.models.users import User