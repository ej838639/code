# Automation Projects

Some of the following Python code uses Pandas libraries to post-process outputs from Nokia's Self-Organizing Network (SON) solution on the EdenNet platform.

A SON platform automates the routine work done by Radio Frequency (RF) Engineers on a wireless communications network. The EdenNet solution has built-in Python libraries and T-Mobile built many custom libraries to create custom modules to meet business requirements.

**[CCO](https://github.com/ej838639/code/blob/main/automation/cco/cco.py "CCO python code")**: Identify the cells that had a significant change in timing advance and find the associated RET. Source data: Outputs from the Coordinated Coverage and Capacity Optimization (C-CCO) SON module.

**[Before and After Cell](https://github.com/ej838639/code/blob/main/automation/before_after_cell/Before%20After%20Cell%20-%20Nokia.py "Before and After Cell python code")**: Before and After (aka Pre/Post) Analysis: Determine if there is a significant change in KPIs related to a network change (Ex: Downtilt). Source data: Daily KPI results from the performance management tool.

**[Parameter Progression](https://github.com/ej838639/code/blob/main/automation/parameter_progression.py "Parameter Progression python code")**: Calculate the parameters audited and enforced for any number of parameter baselines. Source data: extract from parameter database.
