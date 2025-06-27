



[dehydration_metadata_v1](dehydration_metadata_v1.md) / [distribution_system_assets](distribution_system_assets.md) / [switches](switches.md)
# Switch Item

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[num_phase](#num_phase)|`number`|:white_check_mark:||Switch Number Of Phase|
|[kv](#kv)|`number`|:white_check_mark:||Switch kV|
|[is_normally_open](#is_normally_open)|`boolean`|:white_check_mark:||Is Normally Open|
|[count](#count)|`number`|:white_check_mark:||Switch Count|
|[avg_ampacity](#avg_ampacity)|`number`|:white_check_mark:||Average Switch Ampacity|
|[min_ampacity](#min_ampacity)|`number`|:white_check_mark:||Minimum Switch Ampacity|
|[max_ampacity](#max_ampacity)|`number`|:white_check_mark:||Maximum Switch Ampacity|
|[std_ampacity](#std_ampacity)|`number \| string`|:white_check_mark:||Standard Deviation Switch Ampacity|

## num_phase

Number of phase for switch item.


- is required
- Type: `number`

Maximum Number: `3`
## kv

Switch voltage rating in kV.


- is required
- Type: `number`

Minimum Number: `0.01`
## is_normally_open

Set to true if this switch is normally open.


- is required
- Type: `boolean`

## count

Count of switches.


- is required
- Type: `number`

Minimum Number: `1`
## avg_ampacity

Average switch rating in ampere.


- is required
- Type: `number`

Minimum Number: `0`
## min_ampacity

Minimum switch rating in ampere.


- is required
- Type: `number`

Minimum Number: `0`
## max_ampacity

Maximum switch rating in ampere.


- is required
- Type: `number`

Minimum Number: `0`
## std_ampacity

Standard deviation switch rating in ampere.


- is required
- Type: `number | string`

#### One Of


