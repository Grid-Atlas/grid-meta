



[dehydration_metadata_v1](dehydration_metadata_v1.md) / [distribution_system_assets](distribution_system_assets.md) / [capacitors](capacitors.md)
# Capacitor Item

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[kvar](#kvar)|`number`|:white_check_mark:||Capacitor Capacity|
|[num_phase](#num_phase)|`number`|:white_check_mark:||Capacitor Number of Phase|
|[kv](#kv)|`number`|:white_check_mark:||Capacitor kV|
|[count](#count)|`number`|:white_check_mark:||Capacitor Count|

## kvar

Nameplate rating of capacitor in kvar.


- is required
- Type: `number`

Minimum Number: `0.01`
## num_phase

Number of phase for capacitor


- is required
- Type: `number`

Minimum Number: `1`
Maximum Number: `3`
## kv

Kilo volt rating for the capacitor.


- is required
- Type: `number`

Minimum Number: `0.01`
## count

Count of capacitors.


- is required
- Type: `number`

Minimum Number: `1`