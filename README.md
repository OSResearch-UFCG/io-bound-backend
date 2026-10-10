# io-bound-backend

Escreve um arquivo de `mb` megabytes no disco (com fsync), lê ele de volta e apaga. Todo o tempo da requisição é gasto esperando o disco.

Só usa a biblioteca padrão do Python 3.

```bash
python3 server.py
curl "http://localhost:8080/?mb=50"
```

A porta pode ser trocada com a variável `PORT`.
