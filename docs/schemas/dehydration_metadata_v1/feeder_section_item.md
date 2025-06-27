



[dehydration_metadata_v1](dehydration_metadata_v1.md) / [distribution_system_assets](distribution_system_assets.md) / [distribution_feeder_sections](distribution_feeder_sections.md)
# Feeder Section Item

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[kv](#kv)|`number`|:white_check_mark:||Feeder Section Voltage|
|[num_phase](#num_phase)|`number`|:white_check_mark:||Feeder section number of phase.|
|[count](#count)|`number`|:white_check_mark:||Feeder Section Count|
|[avg_feeder_miles](#avg_feeder_miles)|`number`|:white_check_mark:||Average Feeder Miles|
|[min_feeder_miles](#min_feeder_miles)|`number`|:white_check_mark:||Minimum Feeder Miles|
|[max_feeder_miles](#max_feeder_miles)|`number`|:white_check_mark:||Maximum Feeder Miles|
|[std_feeder_miles](#std_feeder_miles)|`number \| string`|:white_check_mark:||Standard Deviation Feeder Miles|
|[min_ampacity](#min_ampacity)|`number`|:white_check_mark:||Minimum Feeder Ampacity|
|[avg_ampacity](#avg_ampacity)|`number`|:white_check_mark:||Average Feeder Ampacity|
|[max_ampacity](#max_ampacity)|`number`|:white_check_mark:||Maximum Feeder Ampacity|
|[std_ampacity](#std_ampacity)|`number \| string`|:white_check_mark:||Standard Deviation Feeder Ampacity|
|[avg_per_unit_resistance_ohm_per_mile](#avg_per_unit_resistance_ohm_per_mile)|`number`|:white_check_mark:||Average Per Unit Resistance|
|[min_per_unit_resistance_ohm_per_mile](#min_per_unit_resistance_ohm_per_mile)|`number`|:white_check_mark:||Minimum Per Unit Resistance|
|[max_per_unit_resistance_ohm_per_mile](#max_per_unit_resistance_ohm_per_mile)|`number`|:white_check_mark:||Maximum Per Unit Resistance|
|[std_per_unit_resistance_ohm_per_mile](#std_per_unit_resistance_ohm_per_mile)|`number \| string`|:white_check_mark:||Standard Deviation Per Unit Resistance|
|[avg_per_unit_reactance_ohm_per_mile](#avg_per_unit_reactance_ohm_per_mile)|`number`|:white_check_mark:||Average Per Unit Reactance|
|[min_per_unit_reactance_ohm_per_mile](#min_per_unit_reactance_ohm_per_mile)|`number`|:white_check_mark:||Minimum Per Unit Reactance|
|[max_per_unit_reactance_ohm_per_mile](#max_per_unit_reactance_ohm_per_mile)|`number`|:white_check_mark:||Maximum Per Unit Reactance|
|[std_per_unit_reactance_ohm_per_mile](#std_per_unit_reactance_ohm_per_mile)|`number \| string`|:white_check_mark:||Standard Deviation Per Unit Reactance|
|[min_customers_served](#min_customers_served)|`number`|:white_check_mark:||Minimum number of customers served.|
|[avg_customers_served](#avg_customers_served)|`number`|:white_check_mark:||Average number of customers served.|
|[max_customers_served](#max_customers_served)|`number`|:white_check_mark:||Maximum number of customers served.|
|[std_customers_served](#std_customers_served)|`number \| string`|:white_check_mark:||Standard Deviation number of customers served.|
|[min_pct_peak_loading](#min_pct_peak_loading)|`number`|:white_check_mark:||Minimum Percentage Peak Loading|
|[avg_pct_peak_loading](#avg_pct_peak_loading)|`number`|:white_check_mark:||Average Percentage Peak Loading|
|[max_pct_peak_loading](#max_pct_peak_loading)|`number`|:white_check_mark:||Maximum Percentage Peak Loading|
|[std_pct_peak_loading](#std_pct_peak_loading)|`number \| string`|:white_check_mark:||Standard Deviation Percentage Peak Loading|

## kv

Kilo volt rating of feeder section. Line to line for multi phase and line to ground for single phase.


- is required
- Type: `number`

Minimum Number: `0.01`
## num_phase

Number of phase for feeder section.


- is required
- Type: `number`

Minimum Number: `1`
Maximum Number: `3`
## count

Number of feeder section for given voltage rating, num of phase and construction type.


- is required
- Type: `number`

Minimum Number: `1`
## avg_feeder_miles

Average feeder section length in miles.


- is required
- Type: `number`

Minimum Number: `0`
## min_feeder_miles

Minimum feeder section length in miles.


- is required
- Type: `number`

Minimum Number: `0`
## max_feeder_miles

Maximum feeder section length in miles.


- is required
- Type: `number`

Minimum Number: `0`
## std_feeder_miles

Standard deviation feeder section length in miles.


- is required
- Type: `number | string`

#### One Of



## min_ampacity

 feeder section ampere capacity.


- is required
- Type: `number`

Minimum Number: `0`
## avg_ampacity

Average feeder section ampere capacity.


- is required
- Type: `number`

Minimum Number: `0`
## max_ampacity

Maximum feeder section ampere capacity.


- is required
- Type: `number`

Minimum Number: `0`
## std_ampacity

Standard deviation feeder section ampere capacity.


- is required
- Type: `number | string`

#### One Of



## avg_per_unit_resistance_ohm_per_mile

Average per unit resistance for feeder sections.


- is required
- Type: `number`

## min_per_unit_resistance_ohm_per_mile

Minimum per unit resistance for feeder sections.


- is required
- Type: `number`

## max_per_unit_resistance_ohm_per_mile

Maximum per unit resistance for feeder sections.


- is required
- Type: `number`

## std_per_unit_resistance_ohm_per_mile

Standard Deviation of per unit resistance for feeder sections.


- is required
- Type: `number | string`

#### One Of



## avg_per_unit_reactance_ohm_per_mile

Average per unit reactance for feeder sections.


- is required
- Type: `number`

## min_per_unit_reactance_ohm_per_mile

Minimum per unit reactance for feeder sections.


- is required
- Type: `number`

## max_per_unit_reactance_ohm_per_mile

Maximum per unit reactance for feeder sections.


- is required
- Type: `number`

## std_per_unit_reactance_ohm_per_mile

Standard Deviation of per unit reactance for feeder sections.


- is required
- Type: `number | string`

#### One Of



## min_customers_served

Minimum number of customers served directly or downward from this feeder section.


- is required
- Type: `number`

Minimum Number: `0`
## avg_customers_served

Average number of customers served directly or downward from this feeder section.


- is required
- Type: `number`

Minimum Number: `0`
## max_customers_served

Maximum number of customers served directly or downward from this feeder section.


- is required
- Type: `number`

Minimum Number: `0`
## std_customers_served

Standard deviation number of customers served directly or downward from this feeder section.


- is required
- Type: `number | string`

#### One Of



## min_pct_peak_loading

Minimum percentage loading of these type of feeder sections during peak load.


- is required
- Type: `number`

Minimum Number: `0`
## avg_pct_peak_loading

Average percentage loading of these type of feeder sections during peak load.


- is required
- Type: `number`

Minimum Number: `0`
## max_pct_peak_loading

Maximum percentage loading of these type of feeder sections during peak load.


- is required
- Type: `number`

Minimum Number: `0`
## std_pct_peak_loading

Standard deviation percentage loading of these type of feeder sections during peak load.


- is required
- Type: `number | string`

#### One Of


