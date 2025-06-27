



[dehydration_metadata_v1](dehydration_metadata_v1.md)
# Distribution System Assets

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[transformers](#transformers)|[distribution_transformers](distribution_transformers.md)|||Distribution Transformers|
|[feeder_sections](#feeder_sections)|[distribution_feeder_sections](distribution_feeder_sections.md)|||Distribution Feeder Sections|
|[capacitors](#capacitors)|[capacitors](capacitors.md)|||Capacitors|
|[switches](#switches)|[switches](switches.md)|||Switches|
|[loads](#loads)|[loads](loads.md)|||Loads|

## transformers

Object capturing high level information about distribution transformers.


- is not required
- Type: [distribution_transformers](distribution_transformers.md)

## feeder_sections

High level information about feeder sections.


- is not required
- Type: [distribution_feeder_sections](distribution_feeder_sections.md)

## capacitors

Object representing high level information about capacitors.


- is not required
- Type: [capacitors](capacitors.md)

## switches

High level information about switches present in the model.


- is not required
- Type: [switches](switches.md)

## loads

Represents high level load information.


- is not required
- Type: [loads](loads.md)
