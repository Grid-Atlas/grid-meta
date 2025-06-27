



[dehydration_metadata_v1](dehydration_metadata_v1.md) / [distribution_system_assets](distribution_system_assets.md) / [loads](loads.md)
# Load Item

Type: `object`
Additional Properties Allowed: `True`


|Property|Type|Required|Format|Title|
| :---: | :---: | :---: | :---: | :---: |
|[kv](#kv)|`number`|:white_check_mark:||Load Voltage Rating|
|[count](#count)|`number`|:white_check_mark:||Load Count|
|[num_phase](#num_phase)|`number`|:white_check_mark:||Number of Phase|
|[total_customer](#total_customer)|`number`|:white_check_mark:||Total Customer Count|
|[avg_customers_per_load](#avg_customers_per_load)|`number`|:white_check_mark:||Average Customers Per Load|
|[min_customers_per_load](#min_customers_per_load)|`number`|:white_check_mark:||Minimum Customers Per Load|
|[max_customers_per_load](#max_customers_per_load)|`number`|:white_check_mark:||Maximum Customers Per Load|
|[std_customers_per_load](#std_customers_per_load)|`number \| string`|:white_check_mark:||Standard Deviation Customers Per Load|
|[avg_peak_kw](#avg_peak_kw)|`number`|:white_check_mark:||Average Peak kW|
|[avg_peak_kvar](#avg_peak_kvar)|`number`|:white_check_mark:||Average Peak kVAR|
|[min_peak_kw](#min_peak_kw)|`number`|:white_check_mark:||Minimum Peak kW|
|[min_peak_kvar](#min_peak_kvar)|`number`|:white_check_mark:||Minimum Peak kVAR|
|[max_peak_kw](#max_peak_kw)|`number`|:white_check_mark:||Maximum Peak kW|
|[max_peak_kvar](#max_peak_kvar)|`number`|:white_check_mark:||Maximum Peak kVAR|
|[std_peak_kw](#std_peak_kw)|`number \| string`|:white_check_mark:||Standard Deviation Peak kW|
|[std_peak_kvar](#std_peak_kvar)|`number \| string`|:white_check_mark:||Standard Deviation Peak kVAR|

## kv

Load voltage rating in kilovolt.


- is required
- Type: `number`

Minimum Number: `0`
## count

Count of loads.


- is required
- Type: `number`

Minimum Number: `1`
## num_phase

Loads number of phase.


- is required
- Type: `number`

Minimum Number: `1`
Maximum Number: `3`
## total_customer

Count of total customers.


- is required
- Type: `number`

Minimum Number: `1`
## avg_customers_per_load

Average count of customers per load.


- is required
- Type: `number`

Minimum Number: `1`
## min_customers_per_load

Minimum count of customers per load.


- is required
- Type: `number`

Minimum Number: `1`
## max_customers_per_load

Maximum count of customers per load.


- is required
- Type: `number`

Minimum Number: `1`
## std_customers_per_load

Standard deviation count of customers per load.


- is required
- Type: `number | string`

#### One Of



## avg_peak_kw

Average peak active power consumption in kW.


- is required
- Type: `number`

Minimum Number: `0`
## avg_peak_kvar

Average peak reactive power consumption in kVAR.


- is required
- Type: `number`

Minimum Number: `0`
## min_peak_kw

Minimum peak active power consumption in kW.


- is required
- Type: `number`

Minimum Number: `0`
## min_peak_kvar

Minimum peak reactive power consumption in kVAR.


- is required
- Type: `number`

Minimum Number: `0`
## max_peak_kw

Maximum peak active power consumption in kW.


- is required
- Type: `number`

Minimum Number: `0`
## max_peak_kvar

Maximum peak reactive power consumption in kVAR.


- is required
- Type: `number`

Minimum Number: `0`
## std_peak_kw

Standard deviation peak active power consumption in kW.


- is required
- Type: `number | string`

#### One Of



## std_peak_kvar

Standard deviation peak reactive power consumption in kVAR.


- is required
- Type: `number | string`

#### One Of


