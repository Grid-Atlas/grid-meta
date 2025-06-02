from pathlib import Path
import uuid
import math
from typing import Literal

import pandas as pd
import opendssdirect as odd
import numpy as np

from gridmeta.models import (
    Metadata,
    DistributionSystemDehydratedDataset,
    Assets,
    VoltageMetric,
    Load,
    Transformer,
    FeederSection,
    Capacitor,
    Switch,
    SnapshotCategory,
)
from gridmeta.json_utils import write_to_json_file, validate_json_data_from_schema_file
from gridmeta.privacy import apply_differential_privacy

UNIT_MAPPER = {
    0: 1,
    1: 1.60934,
    2: 0.3048,
    3: 1,
    4: 0.001,
    5: 0.0003048,
    6: 0.0000254,
    7: 0.00001,
    8: 0.000001,
}


def get_load_assets_from_opendss_dataframe(load_df: pd.DataFrame) -> list[Load]:
    """Function to return load objects from opendss load data frame."""

    load_group = load_df.groupby(["Phases", "kV"])[["NumCust", "kW", "kvar"]].agg(
        ["mean", "min", "max", "std", "count", "sum"]
    )
    load_objects: list[Load] = []
    for (phases, kv), row in load_group.iterrows():
        load_obj = Load(
            kv=kv,
            count=row[("NumCust", "count")],
            num_phase=phases,
            total_customer=row[("NumCust", "sum")],
            avg_customers_per_load=row[("NumCust", "mean")],
            min_customers_per_load=row[("NumCust", "min")],
            max_customers_per_load=row[("NumCust", "max")],
            std_customers_per_load="NaN"
            if np.isnan(row[("NumCust", "std")])
            else row[("NumCust", "std")],
            avg_peak_kw=row[("kW", "mean")],
            avg_peak_kvar=row[("kvar", "mean")],
            min_peak_kw=row[("kW", "min")],
            min_peak_kvar=row[("kvar", "min")],
            max_peak_kw=row[("kW", "max")],
            max_peak_kvar=row[("kvar", "max")],
            std_peak_kw="NaN" if np.isnan(row[("kW", "std")]) else row[("kW", "std")],
            std_peak_kvar="NaN" if np.isnan(row[("kvar", "std")]) else row[("kvar", "std")],
        )
        load_objects.append(load_obj)
    return load_objects


def get_transformer_assets_from_dataframe(
    transformer_df: pd.DataFrame,
) -> list[Transformer]:
    """Function to return transformer objects from transformer data frame."""

    transformer_group = transformer_df.groupby(
        ["kva", "is_substation", "high_kv", "low_kv", "num_phases", "is_regulator"]
    )[["num_customers_served", "pct_peak_loading"]].agg(
        ["mean", "min", "max", "std", "count", "sum"]
    )
    transformer_objects: list[Transformer] = []
    for (
        kva,
        is_substation,
        high_kv,
        low_kv,
        num_phase,
        is_regulator,
    ), row in transformer_group.iterrows():
        transformer_obj = Transformer(
            kva=int(kva),
            count=row[("num_customers_served", "count")],
            num_phase=num_phase,
            is_substation_transformer=is_substation,
            high_kv=high_kv,
            low_kv=low_kv,
            is_regulator=is_regulator,
            avg_customers_served=row[("num_customers_served", "mean")],
            min_customers_served=row[("num_customers_served", "min")],
            max_customers_served=row[("num_customers_served", "max")],
            std_customers_served="NaN"
            if np.isnan(row[("num_customers_served", "std")])
            else row[("num_customers_served", "std")],
            avg_pct_peak_loading=row[("pct_peak_loading", "mean")],
            min_pct_peak_loading=row[("pct_peak_loading", "min")],
            max_pct_peak_loading=row[("pct_peak_loading", "max")],
            std_pct_peak_loading="NaN"
            if np.isnan(row[("pct_peak_loading", "std")])
            else row[("pct_peak_loading", "std")],
        )
        transformer_objects.append(transformer_obj)
    return transformer_objects


def get_feeder_sections_from_dataframe(
    lines_df: pd.DataFrame,
) -> list[FeederSection]:
    """Function to return feeder section objects from lines data frame."""

    feeder_group = lines_df.groupby(["voltage_lg_kv", "num_phases"])[
        [
            "num_customers_served",
            "pct_peak_loading",
            "resistance_ohm_per_mile",
            "reactance_ohm_per_mile",
            "ampacity",
            "line_length_miles",
        ]
    ].agg(["mean", "min", "max", "std", "count", "sum"])
    feeder_objects: list[FeederSection] = []
    for (
        kv,
        num_phase,
    ), row in feeder_group.iterrows():
        feeder_obj = FeederSection(
            kv=kv,
            count=row[("num_customers_served", "count")],
            num_phase=num_phase,
            avg_customers_served=row[("num_customers_served", "mean")],
            min_customers_served=row[("num_customers_served", "min")],
            max_customers_served=row[("num_customers_served", "max")],
            std_customers_served="NaN"
            if np.isnan(row[("num_customers_served", "std")])
            else row[("num_customers_served", "std")],
            avg_pct_peak_loading=row[("pct_peak_loading", "mean")],
            min_pct_peak_loading=row[("pct_peak_loading", "min")],
            max_pct_peak_loading=row[("pct_peak_loading", "max")],
            std_pct_peak_loading="NaN"
            if np.isnan(row[("pct_peak_loading", "std")])
            else row[("pct_peak_loading", "std")],
            avg_ampacity=row[("ampacity", "mean")],
            min_ampacity=row[("ampacity", "min")],
            max_ampacity=row[("ampacity", "max")],
            std_ampacity="NaN" if np.isnan(row[("ampacity", "std")]) else row[("ampacity", "std")],
            avg_per_unit_reactance_ohm_per_mile=row[("reactance_ohm_per_mile", "mean")],
            min_per_unit_reactance_ohm_per_mile=row[("reactance_ohm_per_mile", "min")],
            max_per_unit_reactance_ohm_per_mile=row[("reactance_ohm_per_mile", "max")],
            std_per_unit_reactance_ohm_per_mile="NaN"
            if np.isnan(row[("reactance_ohm_per_mile", "std")])
            else row[("reactance_ohm_per_mile", "std")],
            avg_per_unit_resistance_ohm_per_mile=row[("resistance_ohm_per_mile", "mean")],
            min_per_unit_resistance_ohm_per_mile=row[("resistance_ohm_per_mile", "min")],
            max_per_unit_resistance_ohm_per_mile=row[("resistance_ohm_per_mile", "max")],
            std_per_unit_resistance_ohm_per_mile="NaN"
            if np.isnan(row[("resistance_ohm_per_mile", "std")])
            else row[("resistance_ohm_per_mile", "std")],
            avg_feeder_miles=row[("line_length_miles", "mean")],
            min_feeder_miles=row[("line_length_miles", "min")],
            max_feeder_miles=row[("line_length_miles", "max")],
            std_feeder_miles="NaN"
            if np.isnan(row[("line_length_miles", "std")])
            else row[("line_length_miles", "std")],
        )
        feeder_objects.append(feeder_obj)
    return feeder_objects


def get_switch_sections_from_dataframe(
    switches_df: pd.DataFrame,
) -> list[Switch]:
    """Function to return switch section objects from switches data frame."""

    switch_group = switches_df.groupby(["voltage_lg_kv", "num_phases", "is_open"])[
        [
            "ampacity",
        ]
    ].agg(["mean", "min", "max", "std", "count", "sum"])
    switch_objects: list[Switch] = []
    for (kv, num_phase, is_open), row in switch_group.iterrows():
        switch_obj = Switch(
            kv=kv,
            count=row[("ampacity", "count")],
            num_phase=num_phase,
            is_normally_open=is_open,
            avg_ampacity=row[("ampacity", "mean")],
            min_ampacity=row[("ampacity", "min")],
            max_ampacity=row[("ampacity", "max")],
            std_ampacity="NaN" if np.isnan(row[("ampacity", "std")]) else row[("ampacity", "std")],
        )
        switch_objects.append(switch_obj)
    return switch_objects


def get_capacitors_from_dataframe(cap_df: pd.DataFrame) -> list[Capacitor]:
    """Get capacitor objects from capacitor dataframe."""
    cap_group = cap_df.groupby(["kv", "num_phases", "kvar"])
    cap_objects: list[Capacitor] = []
    for (kv, num_phase, kvar), group in cap_group:
        cap_obj = Capacitor(kv=kv, count=len(group), num_phase=num_phase, kvar=kvar)
        cap_objects.append(cap_obj)
    return cap_objects


def get_voltage_metrics_from_dataframe(
    voltage_df: pd.DataFrame, snapshot: SnapshotCategory = SnapshotCategory.NetPeakLoad
) -> list[VoltageMetric]:
    volt_metrics = []
    volt_group = voltage_df.groupby(["kv", "num_phase"])[["vmag_pu"]].agg(
        ["mean", "min", "max", "std", "count"]
    )
    for (kv, num_phase), row in volt_group.iterrows():
        volt_metric = VoltageMetric(
            snapshot_category=snapshot,
            kv=kv,
            num_phase=num_phase,
            avg_voltage_pu=row[("vmag_pu", "mean")],
            min_voltage_pu=row[("vmag_pu", "min")],
            max_voltage_pu=row[("vmag_pu", "max")],
            std_voltage_pu="NaN" if np.isnan(row[("vmag_pu", "std")]) else row[("vmag_pu", "std")],
        )
        volt_metrics.append(volt_metric)
    return volt_metrics


class OpenDSS:
    def __init__(self, master_file_path: Path):
        self.master_file_path = master_file_path
        odd.Command(f'Redirect "{str(master_file_path)}"')
        self._add_source_energy_meter()
        self.pct_norm_mapping = self.get_pct_norm_loadings()

    def get_load_dataframe(self) -> pd.DataFrame:
        return odd.utils.loads_to_dataframe()

    def get_capacitor_dataframe(self) -> pd.DataFrame:
        caps = []
        flag = odd.Capacitors.First()
        while flag:
            caps.append(
                {
                    "kv": odd.Capacitors.kV(),
                    "kvar": odd.Capacitors.kvar(),
                    "num_phases": odd.CktElement.NumPhases(),
                }
            )
            flag = odd.Capacitors.Next()
        return pd.DataFrame(caps)

    def get_regulator_dataframe(self) -> pd.DataFrame:
        return odd.utils.regcontrols_to_dataframe()

    def get_pct_norm_loadings(self) -> dict[str, float]:
        return dict(zip(odd.PDElements.AllNames(), odd.PDElements.AllPctNorm(), strict=True))

    def get_source_voltage(self) -> float:
        odd.Circuit.SetActiveBus(self._get_source_bus_name())
        factor = math.sqrt(3) if odd.CktElement.NumPhases() > 1 else 1
        return round(odd.Bus.kVBase() * factor, 5)

    def get_bus_voltages_mapping(self) -> dict[str, float]:
        bus_voltage_mapping = {}
        for bus in odd.Circuit.AllBusNames():
            odd.Circuit.SetActiveBus(bus)
            bus_voltage_mapping[bus] = round(odd.Bus.kVBase(), 5)
        return bus_voltage_mapping

    def get_bus_num_phase_mapping(self) -> dict[str, int]:
        bus_phase_mapping = {}
        for bus in odd.Circuit.AllBusNames():
            odd.Circuit.SetActiveBus(bus)
            bus_phase_mapping[bus] = odd.Bus.NumNodes()
        return bus_phase_mapping

    def _get_source_bus_name(self) -> str:
        # Activate the source
        odd.Vsources.Name("source")

        # Set the source bus name as active bus
        bus_name = odd.CktElement.BusNames()[0]
        return bus_name

    def _add_source_energy_meter(self) -> str:
        odd.Circuit.SetActiveBus(self._get_source_bus_name())
        # get the first pd element
        pd_element = odd.Bus.AllPDEatBus()[0]
        # odd.PDElements.Name(pd_element)

        # for idx in range(odd.CktElement.NumTerminals()):
        meter = f"new energymeter.{str(uuid.uuid4()).replace('-', '')} {pd_element}"
        odd.Command(meter)
        print(f"Added new energy meter: {meter}")
        odd.Solution.Solve()

    def get_powerflow_voltages(self) -> pd.DataFrame:
        bus_voltage_data = []
        odd.Solution.Solve()
        node_names = odd.Circuit.AllNodeNames()
        vmags = odd.Circuit.AllBusMagPu()
        bus_num_phase_mapping = self.get_bus_num_phase_mapping()
        bus_voltage_mapping = self.get_bus_voltages_mapping()
        for node, vmag in zip(node_names, vmags, strict=True):
            bus_name = node.split(".")[0]
            bus_voltage_data.append(
                {
                    "vmag_pu": vmag,
                    "num_phase": bus_num_phase_mapping[bus_name],
                    "kv": bus_voltage_mapping[bus_name],
                }
            )
        return pd.DataFrame(bus_voltage_data)

    def get_line_sections_dataframe(self) -> pd.DataFrame:
        line_sections = []
        bus_voltage_mapping = self.get_bus_voltages_mapping()
        flag = odd.Lines.First()

        while flag:
            if not odd.Lines.IsSwitch():
                mile_converter = UNIT_MAPPER[odd.Lines.Units()] * 0.621371
                line_length_miles = mile_converter * odd.Lines.Length()
                line_sections.append(
                    {
                        "voltage_lg_kv": bus_voltage_mapping[odd.Lines.Bus1().split(".")[0]],
                        "num_phases": odd.Lines.Phases(),
                        "line_length_miles": line_length_miles,
                        "ampacity": odd.Lines.NormAmps(),
                        "num_customers_served": odd.PDElements.TotalCustomers(),
                        "pct_peak_loading": self.pct_norm_mapping[odd.PDElements.Name()],
                        "resistance_ohm_per_mile": odd.Lines.RMatrix()[0] / mile_converter,
                        "reactance_ohm_per_mile": odd.Lines.XMatrix()[0] / mile_converter,
                    }
                )
            flag = odd.Lines.Next()
        return pd.DataFrame(line_sections)

    def get_switch_sections_dataframe(self) -> pd.DataFrame:
        switch_sections = []
        bus_voltage_mapping = self.get_bus_voltages_mapping()
        flag = odd.Lines.First()

        while flag:
            if odd.Lines.IsSwitch():
                switch_sections.append(
                    {
                        "voltage_lg_kv": bus_voltage_mapping[odd.Lines.Bus1().split(".")[0]],
                        "num_phases": odd.Lines.Phases(),
                        "ampacity": odd.Lines.NormAmps(),
                        "is_open": any(
                            [
                                odd.CktElement.IsOpen(term + 1, ph + 1)
                                for term in range(odd.CktElement.NumTerminals())
                                for ph in range(odd.CktElement.NumPhases())
                            ]
                        ),
                    }
                )
            flag = odd.Lines.Next()
        return pd.DataFrame(switch_sections)

    def get_transformer_dataframe(self) -> pd.DataFrame:
        transformer_objects = []
        reg_transformers = list(self.get_regulator_dataframe()["Transformer"])
        source_voltage = self.get_source_voltage()
        flag = odd.Transformers.First()
        while flag:
            kvs = []
            for wdg in range(odd.Transformers.NumWindings()):
                odd.Transformers.Wdg(wdg + 1)
                kvs.append(odd.Transformers.kV())

            # Note for three winding transformers (e.g. split phase transformers)
            # We have not checked if there capacities are different in each
            # windings

            # There is a bug I think in a way that TotalCustomers are
            # computed downward of PD Elements. For example in IEEE13 test case
            # if you try to compute TotalCustomers() for reg1, reg2 and reg3 you will get
            # 0 for Reg1 and Reg2 however for Reg3 we get all 15. Not sure if this is intentional.
            # Ideally you would create your own graph and solve this the way you like
            # for now I am going OpenDSSDirect's TotalCustomer implementation.
            # Revist this in the future if causing too much trouble.

            # Assumption: All transformers connected to highest voltage will be considered substation
            # transformers. Obvisouly a substation might contain transformers with different voltage levels
            # Will need to refine this logic.

            transformer_objects.append(
                {
                    "kva": odd.Transformers.kVA(),
                    "name": odd.Transformers.Name(),
                    "high_kv": max(kvs),
                    "low_kv": min(kvs),
                    "num_phases": odd.CktElement.NumPhases(),
                    "num_customers_served": odd.PDElements.TotalCustomers(),
                    "pct_peak_loading": self.pct_norm_mapping[odd.PDElements.Name()],
                    "is_substation": max(kvs) == source_voltage,
                    "is_regulator": odd.Transformers.Name() in reg_transformers,
                }
            )
            flag = odd.Transformers.Next()
        return pd.DataFrame(transformer_objects)


class OpenDSSMetdataExtractorV1:
    schema_file_path = Path(__file__).parent / "schemas" / "dehydration-metadata.v1.schema.json"

    def __init__(self, master_dss_file: Path, metadata: Metadata):
        self.master_dss_file = master_dss_file
        self.metadata = metadata
        self.opendss = OpenDSS(master_dss_file)

    def get_dehydration_dataset(self) -> DistributionSystemDehydratedDataset:
        asset_data = self.get_asset_data_object()
        voltage_metrics_data = self.get_voltage_metrics_object()
        return DistributionSystemDehydratedDataset(
            metadata=self.metadata,
            voltage_metrics=voltage_metrics_data,
            assets=asset_data,
        )

    def validate_dehydrated_data(self, dehydrated_data: DistributionSystemDehydratedDataset):
        validate_json_data_from_schema_file(
            dehydrated_data.model_dump(mode="json"), self.schema_file_path
        )

    def export(
        self, out_json_file: Path, privacy_mode: Literal["low", "moderate", "high"] | None = None
    ):
        metadata = self.get_dehydration_dataset()
        self.validate_dehydrated_data(metadata)
        metadata_dict = metadata.model_dump(mode="json")
        privacy_metadata = (
            apply_differential_privacy(metadata_dict, privacy_mode)
            if privacy_mode
            else metadata_dict
        )
        write_to_json_file(privacy_metadata, out_json_file)

    def get_asset_data_object(self) -> Assets:
        return Assets(
            transformers=get_transformer_assets_from_dataframe(
                self.opendss.get_transformer_dataframe()
            ),
            feeder_sections=get_feeder_sections_from_dataframe(
                self.opendss.get_line_sections_dataframe()
            ),
            capacitors=get_capacitors_from_dataframe(self.opendss.get_capacitor_dataframe()),
            switches=get_switch_sections_from_dataframe(
                self.opendss.get_switch_sections_dataframe()
            ),
            loads=get_load_assets_from_opendss_dataframe(self.opendss.get_load_dataframe()),
        )

    def get_voltage_metrics_object(self) -> list[VoltageMetric]:
        return get_voltage_metrics_from_dataframe(self.opendss.get_powerflow_voltages())
