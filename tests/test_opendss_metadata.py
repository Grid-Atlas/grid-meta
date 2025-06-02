from pathlib import Path
import datetime

import pytest
import pandas as pd

from gridmeta.opendss import (
    OpenDSS,
    get_load_assets_from_opendss_dataframe,
    get_transformer_assets_from_dataframe,
    get_feeder_sections_from_dataframe,
    get_capacitors_from_dataframe,
    get_switch_sections_from_dataframe,
    OpenDSSMetdataExtractorV1,
)
from gridmeta.models import (
    Load,
    Transformer,
    FeederSection,
    Capacitor,
    Switch,
    Metadata,
    RegionType,
)

opendss_root_folder = Path(__file__).parent / "data/opendss"
OPENDSS_MODELS = list(opendss_root_folder.rglob("master.dss"))


@pytest.fixture(params=OPENDSS_MODELS)
def opendss_model(request):
    return request.param


@pytest.fixture
def dss_instance(opendss_model):
    return OpenDSS(opendss_model)


def test_load_dataframe(dss_instance):
    load_df = dss_instance.get_load_dataframe()
    assert isinstance(load_df, pd.DataFrame)


def test_capacitor_dataframe(dss_instance):
    cap_df = dss_instance.get_capacitor_dataframe()
    assert isinstance(cap_df, pd.DataFrame)


def test_regcontrols_dataframe(dss_instance):
    reg_df = dss_instance.get_regulator_dataframe()
    assert isinstance(reg_df, pd.DataFrame)


def test_switches_dataframe(dss_instance):
    switch_df = dss_instance.get_switch_sections_dataframe()
    assert isinstance(switch_df, pd.DataFrame)


def test_powerflow_voltage_dataframe(dss_instance):
    voltage_df = dss_instance.get_powerflow_voltages()
    assert isinstance(voltage_df, pd.DataFrame)


def test_load_asset_creation(dss_instance):
    load_df = dss_instance.get_load_dataframe()
    load_assets = get_load_assets_from_opendss_dataframe(load_df)
    assert isinstance(load_assets, list)
    assert len(load_assets) >= 1
    assert all([isinstance(item, Load) for item in load_assets])


def test_transformer_dataframe_creation(dss_instance):
    transformer_df = dss_instance.get_transformer_dataframe()
    assert isinstance(transformer_df, pd.DataFrame)


def test_transformer_asset_creation(dss_instance):
    transformer_df = dss_instance.get_transformer_dataframe()
    transformer_assets = get_transformer_assets_from_dataframe(transformer_df)
    assert isinstance(transformer_assets, list)
    assert len(transformer_assets) >= 1
    assert all([isinstance(item, Transformer) for item in transformer_assets])


def test_feeder_sections_creation(dss_instance):
    lines_df = dss_instance.get_line_sections_dataframe()
    feeder_assets = get_feeder_sections_from_dataframe(lines_df)
    assert isinstance(feeder_assets, list)
    assert len(feeder_assets) >= 1
    assert all([isinstance(item, FeederSection) for item in feeder_assets])


def test_switch_sections_creation(dss_instance):
    switches_df = dss_instance.get_switch_sections_dataframe()
    switch_assets = get_switch_sections_from_dataframe(switches_df)
    assert isinstance(switch_assets, list)
    assert len(switch_assets) >= 1
    assert all([isinstance(item, Switch) for item in switch_assets])


def test_capacitors_creation(dss_instance):
    capacitor_df = dss_instance.get_capacitor_dataframe()
    capacitor_assets = get_capacitors_from_dataframe(capacitor_df)
    assert isinstance(capacitor_assets, list)
    assert len(capacitor_assets) >= 1
    assert all([isinstance(item, Capacitor) for item in capacitor_assets])


def test_metadata_extraction(opendss_model, tmp_path):
    extractor = OpenDSSMetdataExtractorV1(
        opendss_model,
        metadata=Metadata(
            state="WA",
            created_at=datetime.datetime.now(),
            model_year=2018,
            region_type=RegionType.Suburban,
            info="Test IEEE feeder",
        ),
    )
    extractor.export(tmp_path / "test.json")
