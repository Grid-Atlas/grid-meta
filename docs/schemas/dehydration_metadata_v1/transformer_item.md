



[dehydration_metadata_v1](dehydration_metadata_v1.md) / [distribution_system_assets](distribution_system_assets.md) / [distribution_transformers](distribution_transformers.md)
# Transformer Item

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[kva](#kva)|`integer`|:white_check_mark:||Capacity in kVA|
|[count](#count)|`integer`|:white_check_mark:||Transformer Count|
|[is_regulator](#is_regulator)|`boolean`|:white_check_mark:||Is Regulator|
|[is_substation_transformer](#is_substation_transformer)|`boolean`|:white_check_mark:||Is Substation Transformer|
|[num_phase](#num_phase)|`integer`|:white_check_mark:||Number of Phase|
|[high_kv](#high_kv)|`number`|:white_check_mark:||High Voltage kV|
|[low_kv](#low_kv)|`number`|:white_check_mark:||Low Voltage kV|
|[avg_customers_served](#avg_customers_served)|`number`|:white_check_mark:||Average Customers Served|
|[min_customers_served](#min_customers_served)|`number`|:white_check_mark:||Minimum Customers Served|
|[max_customers_served](#max_customers_served)|`number`|:white_check_mark:||Maximum Customers Served|
|[std_customers_served](#std_customers_served)|`number \| string`|:white_check_mark:||Standard Deviation Customers Served|
|[min_pct_peak_loading](#min_pct_peak_loading)|`number`|:white_check_mark:||Minimum Percentage Peak Loading|
|[avg_pct_peak_loading](#avg_pct_peak_loading)|`number`|:white_check_mark:||Average Percentage Peak Loading|
|[max_pct_peak_loading](#max_pct_peak_loading)|`number`|:white_check_mark:||Maximum Percentage Peak Loading|
|[std_pct_peak_loading](#std_pct_peak_loading)|`number \| string`|:white_check_mark:||Standard Deviation Percentage Peak Loading|

## kva

Transformer capacity on kVA.


- is required
- Type: `integer`

Minimum Number: `1`
## count

Number of transformers.


- is required
- Type: `integer`

Minimum Number: `1`
## is_regulator

True if regulator.


- is required
- Type: `boolean`

## is_substation_transformer

Set to true if these are substation transformers.


- is required
- Type: `boolean`

## num_phase

Transformer number of phase.


- is required
- Type: `integer`

Minimum Number: `1`
Maximum Number: `3`
## high_kv

Kilovolt rating for high voltage side.


- is required
- Type: `number`

Minimum Number: `0.01`
## low_kv

Kilovolt rating for low voltage side.


- is required
- Type: `number`

Minimum Number: `0.01`
## avg_customers_served

Average number of customer served downward from these type of transformers.


- is required
- Type: `number`

Minimum Number: `0`
## min_customers_served

Minimum number of customer served downward from these type of transformers.


- is required
- Type: `number`

Minimum Number: `0`
## max_customers_served

Maximum number of customer served downward from these type of transformers.


- is required
- Type: `number`

Minimum Number: `0`
## std_customers_served

Standard deviation number of customer served downward from these type of transformers.


- is required
- Type: `number | string`

#### One Of



## min_pct_peak_loading

Minimum percenatge loading of these type of transformers during peak load.


- is required
- Type: `number`

Minimum Number: `0`
## avg_pct_peak_loading

Average percenatge loading of these type of transformers during peak load.


- is required
- Type: `number`

Minimum Number: `0`
## max_pct_peak_loading

Maximum percenatge loading of these type of transformers during peak load.


- is required
- Type: `number`

Minimum Number: `0`
## std_pct_peak_loading

Standard deviation percenatge loading of these type of transformers during peak load.


- is required
- Type: `number | string`

#### One Of


