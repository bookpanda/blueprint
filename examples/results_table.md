| App + Spec           | no cached | cached   | change   | % change |
|----------------------|-----------|----------|----------|----------|
| dsb_hotel - original   | 1.841s    | 1.070s   | -771.308ms | -41.89%  |
| dsb_sn - docker        | 80.647ms  | 64.865ms | -15.782ms | -19.57%  |
| leaf - docker          | 203.896ms | 246.413ms | +42.517ms | +20.85%  |
| leaf - govector        | 25.263ms  | 14.500ms | -10.763ms | -42.60%  |
| leaf - http            | 15.044ms  | 14.644ms | -0.399ms | -2.66%   |
| leaf - ot_logger       | 21.298ms  | 13.968ms | -7.330ms | -34.41%  |
| leaf - thrift          | 64.663ms  | 57.644ms | -7.019ms | -10.85%  |
| leaf - timeout_demo    | 15.113ms  | 15.465ms | +0.352ms | +2.33%   |
| leaf - timeout_retries_demo | 14.168ms  | 16.429ms | +2.261ms | +15.96%  |
| leaf - xtrace_logger   | 14.316ms  | 15.826ms | +1.510ms | +10.55%  |
| sockshop - basic       | 24.115ms  | 27.217ms | +3.101ms | +12.86%  |
| sockshop - docker      | 8.602s    | 5.293s   | -3309.203ms | -38.47%  |
| sockshop - grpc        | 5.400s    | 1.268s   | -4131.543ms | -76.51%  |
| sockshop - rabbit      | 6.708s    | 1.595s   | -5112.352ms | -76.21%  |
| train_ticket - docker  | 23.367ms  | 25.471ms | +2.104ms | +9.01%   |
|----------------------|-----------|----------|----------|----------|
| TOTAL                | 23.053s   | 9.739s   | -13313.855ms | -57.75%  |

