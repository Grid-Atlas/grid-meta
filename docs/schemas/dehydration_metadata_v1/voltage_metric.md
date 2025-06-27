



[dehydration_metadata_v1](dehydration_metadata_v1.md) / [voltage_metrics](voltage_metrics.md)
# Voltage Metric

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[snapshot_category](#snapshot_category)|`enum`|:white_check_mark:||Snapshot Category|
|[kv](#kv)|`number`|:white_check_mark:||Voltage Level|
|[num_phase](#num_phase)|`number`|:white_check_mark:||Number of Phase|
|[avg_voltage_pu](#avg_voltage_pu)|`number`|:white_check_mark:||Average PU Voltage|
|[min_voltage_pu](#min_voltage_pu)|`number`|:white_check_mark:||Minimum PU Voltage|
|[max_voltage_pu](#max_voltage_pu)|`number`|:white_check_mark:||Maximum PU Voltage|
|[std_voltage_pu](#std_voltage_pu)|`number \| string`|:white_check_mark:||Standard Deviation PU Voltage|

## snapshot_category

Snapshot category from which these metrics are generated.


- is required
- Type: `enum`


|Value|
| :--- |
|`NetPeakLoad`|
|`NetMinLoad`|
|`BasePeakLoad`|
|`BaseMinLoad`|

## kv

Voltage level in kV.


- is required
- Type: `number`

Minimum Number: `0.01`
## num_phase

Number of phase.


- is required
- Type: `number`

Minimum Number: `1`
Maximum Number: `3`
## avg_voltage_pu

Average per unit voltage.


- is required
- Type: `number`

Maximum Number: `2.0`
## min_voltage_pu

Minimum per unit voltage.


- is required
- Type: `number`

Maximum Number: `2.0`
## max_voltage_pu

Maximum per unit voltage.


- is required
- Type: `number`

Maximum Number: `2.0`
## std_voltage_pu

Standard deviation per unit voltage.


- is required
- Type: `number | string`

#### One Of

Maximum Number: `2.0`

