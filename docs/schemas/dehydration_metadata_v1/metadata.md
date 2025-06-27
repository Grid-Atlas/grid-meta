



[dehydration_metadata_v1](dehydration_metadata_v1.md)
# Metadata

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[state](#state)|`unknown`|:white_check_mark:||List U.S state to which model belongs to.|
|[created_at](#created_at)|`string`|:white_check_mark:|`date-time`|Created Datetime|
|[model_year](#model_year)|`integer`|:white_check_mark:||Model Year|
|[info](#info)|`string`|:white_check_mark:||Metadata Info|
|[region_type](#region_type)|`enum`|:white_check_mark:||Feeder Category|

## state

U.S State to which model belongs to.


- is required
- Type: `unknown`

#### Any Of


Minimum number of items: `1`

## created_at

Data obfuscation date-time.


- is required
- Type: `string`

## model_year

Model year from which data is extracted.


- is required
- Type: `integer`

Regex Pattern: `^(19|20|21)\d{2}$`
## info

Any description you would like to add.


- is required
- Type: `string`

## region_type

An enumeration of feeder categories representing it's area type.


- is required
- Type: `enum`


|Value|
| :--- |
|`Urban`|
|`Suburban`|
|`Rural`|
