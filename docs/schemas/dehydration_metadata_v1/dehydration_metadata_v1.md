



# Dehydration Metadata V1

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[metadata](#metadata)|[metadata](metadata.md)|:white_check_mark:||Metadata|
|[assets](#assets)|[distribution_system_assets](distribution_system_assets.md)|:white_check_mark:||Distribution System Assets|
|[voltage_metrics](#voltage_metrics)|[voltage_metrics](voltage_metrics.md)|:white_check_mark:||Voltage Metrics|

## metadata

Contains information about location, creation date and model year.


- is required
- Type: [metadata](metadata.md)

## assets

Object capturing high level asset information.


- is required
- Type: [distribution_system_assets](distribution_system_assets.md)

## voltage_metrics

High level information about voltage metrics.


- is required
- Type: [voltage_metrics](voltage_metrics.md)
