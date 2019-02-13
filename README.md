## Implementing Dining Cryptographers and Crowds Anonymity Protocols ##

#### Requirements
* Python >= 3.6

#### Usage

- Use simulate.py for simulating Dining Cryptographers and Crowds anonymity protocols.<br />
 ```
 python3 simulate.py <dc|crowds> <graph_file> <c> <users_file> 
 ```
- Use attack.py for predicting the user that initiated a message.<br />
```
python3 attack.py <dc|crowds> <graph_file> <c> <prior_file> <output>  
```

- Vulnerability.py simulates and attacks for <runs> times and then prints accuracy result on predictions.<br />
```
python3 vulnerability.py <dc|crowds> <graph_file> <c> <prior_file> <runs>
```
