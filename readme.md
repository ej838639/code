# Patent Details, Automation Projects, and DevOps Learning Journey

This repository houses details about my two patents, automation code I developed using Python pandas libraries, and my journey learning DevOps tools.

## Patents

I am an inventor: I have two patents for wireless communication applications.

### Dominance

**[Dominance](https://github.com/ej838639/code/tree/main/patents/dominance "Dominance patent folder")**: Patent 10245442: "Dominance-Based Coverage Management for Wireless Communication Network"

**Summary**: Algorithm that ingests geo-located mobile device measurement reports to automatically downtilt or uptilt cellular bast station antennas to improve coverage and reduce interference.

### Automatic RET Label

**[RET Label](https://github.com/ej838639/code/tree/main/patents/auto_ret_label "RET Label patent folder")**: Patent 11296936: "Automatic Antenna Association For Cellular Telecommunication Network (RET Audit)"

**Summary**: Algorithm to methodically and autonomously align the Remote Electrical Tilt (RET) Label of antennas to the proper network cell name. This enables large-scale automatic antenna tilt changes to improve coverage and reduce interference.

Automatically adjust antenna tilts, evaluate the change in distribution of user traffic using Timing Advance counters, determine the correlation between RET and cell name, and then automatically update the RET Label for the antennas. Adjust the antenna tilts during the night (aka the Maintenance Window) when very few people are using the cell site to minimize the number of customers impacted by the temporary network coverage loss.

## Automation Projects

Some of the following Python code uses Pandas libraries to post-process outputs from Nokia's Self-Organizing Network (SON) solution on the EdenNet platform.

A SON platform automates the routine work done by Radio Frequency (RF) Engineers on a wireless communications network. The EdenNet solution has built-in Python libraries and T-Mobile built many custom libraries to create custom modules to meet business requirements.

**[CCO](https://github.com/ej838639/code/blob/main/automation/cco/cco.py "CCO python code")**: Identify the cells that had a significant change in timing advance and find the associated RET. Source data: Outputs from the Coordinated Coverage and Capacity Optimization (C-CCO) SON module. 

**[Before and After Cell](https://github.com/ej838639/code/blob/main/automation/before_after_cell/Before%20After%20Cell%20-%20Nokia.py "Before and After Cell python code")**: Before and After (aka Pre/Post) Analysis: Determine if there is a significant change in KPIs related to a network change (Ex: Downtilt). Source data: Daily KPI results from the performance management tool.

**[Parameter Progression](https://github.com/ej838639/code/blob/main/automation/parameter_progression.py "Parameter Progression python code")**: Calculate the parameters audited and enforced for any number of parameter baselines. Source data: extract from parameter database.

## DevOps Learning journey

Projects to learn DevOps tools.

**[Terraform](https://github.com/ej838639/code/tree/main/terraform "Terraform projects folder")**: Terraform code from projects the Educative's "DevOps for Developers: Terraform: From Beginner to Master with Examples in AWS: Module 9".
