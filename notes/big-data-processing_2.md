# 大規模データ処理法

### 20190415

## シェルについて

- sh系 (sh, bash...): Loaded on first UNIX made by AT&T Bell Lab
- csh系 (csh, tcsh...): Loaded on BSD by UC Berkeley. 
- The difference is more historical and is just preference

## An Input and Outputs

- stdin (Standard input): keyboard is assinged in default.
- stdout (Standard output): console display is assinged in default.
- stderr (Standard error output): Error / notification will be delivered here. Console display is assinged in default.
- However, the connection is modifiable. 
    - >: set an input file
    - く: set an output file
    - |: pass the return value of first function to the second function
- sed: 正規表現での修正
- awk: パターンベースの酒精
- wgetとcurlの違い: wgetはディレクトリに, curlはstdoutに.
-

