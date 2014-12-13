py_telstra_usage
================

Command line tool for checking your Telstra prepaid data usage.  At $10/GB and 40Mbps you'll want to watch that usage!

#Example output

```
hmacread$ python get_telstra_usage.py 
Data remaining: 9.582 GB
Recharge Credit: $100.0
Expiring on: 11 Mar 2015
Percent used: 4.18%
```
#Usage

1. Check that python is installed `python -V`
2. Ensure you are connected vi a Telstra mobile broadband data connection.
3. Run `python get_telstra_usage.py`

#Notes

This works for the current telstra mobile broadband and requires no authentication as the https://m.telstra.com/ generates content based (presumably) on the source of incoming connection.

The script just simulates and http request to 'https://m.telstra.com/ppdata/viewBalanceAction.html?a=view' and parses out the relevant data.

The percentage meter that the credit remaining is the original amount of credit purchased AND that the data included for that plan have not changed. I.e. you need to update this for your plan.
