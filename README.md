## Implementing Dining Cryptographers and Crowds Anonymity Protocols ##

#### Requirements
* Python >= 3.6

#### Usage

- Depending on the script that you want to use, you need to provide some of the following parameters.
  - [dc|crowds]       The protocol you want to simulate or attack to.
  - \<graph-file\>    Name or path of the file containing graph adjacency matrix.
  - \<c\>             Number of corrupted users (0 for none).
  - \<users-file\>    Name of the file containing senders id (one execution per line)
  - \<prior-file\>    Name or path of the file containing sender's probability distribution (only for non-corrupted users)
  - \<output-file\>   Name or path of output file created by simulate.py (only for attacker.py script)
  - \<runs\>          Number of simulations (only for vulnerability.py script)

- Use simulate.py for simulating Dining Cryptographers and Crowds anonymity protocols.<br />
 ```
 python3 simulate.py <dc|crowds> <graph_file> <c> <users_file> 
 ```
- Use attack.py for predicting the user that initiated a message.<br />
```
python3 attack.py <dc|crowds> <graph_file> <c> <prior_file> <output>  
```

- vulnerability.py simulates and attacks for <runs> times and then prints accuracy result on predictions.<br />
```
python3 vulnerability.py <dc|crowds> <graph_file> <c> <prior_file> <runs>
```
