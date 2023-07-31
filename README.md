# ADCommonPass
Extracts hashes from ndts.dit and checks if same passwords is used by different accounts. 

## Requirements
- linux
- python (with impacket library | default in kali)
- ndts.dit file and system file

## Steps to Run
- Place your ndts file and system file in the ndts folder
- Then, type this in your linux terminal and hit enter.
```
./ad-password-test
```
## References
- [secretsdump.py](https://github.com/fortra/impacket)
- [checkHash.py](https://gist.github.com/bandrel/3dd47c93cd430606865ec84d281913dc)
