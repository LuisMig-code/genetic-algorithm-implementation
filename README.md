# Algoritmo Genético para Alocação de Clientes em Access Points

## Descrição do Problema
Uma casa de eventos com capacidade máxima para 350 pessoas instalou 4 access points (AP) para prover conectividade aos clientes. O objetivo é alocar cada cliente ao AP mais próximo, respeitando a capacidade máxima de conexões de cada AP.

## Access Points e suas Configurações
| AP | Localização (x, y) | Capacidade |
|----|----------------|------------|
| A  | (0, 0)        | 64         |
| B  | (80, 0)       | 64         |
| C  | (0, 80)       | 128        |
| D  | (80, 80)      | 128        |

## Entrada
O programa recebe como entrada um arquivo CSV contendo a lista de clientes e suas respectivas posições (x, y). O arquivo deve ter o seguinte formato:

```
x,y
10,20
30,40
50,60
... (continua)
```

## Saída
O programa gera um arquivo `alocacao_clientes.csv` contendo a lista de clientes e o AP ao qual estão conectados e uma imagem mostrando como ficou distribuídos. O formato da saída é:

```
Cliente,AP Conectado,x,y
Cliente 1,A,10,20
Cliente 2,C,30,40
Cliente 3,D,40,50
... (continua)
```

## Como Executar o Algoritmo
### 1. Instalar Dependências
Certifique-se de ter o Python instalado. O script usa a biblioteca `numpy`, que pode ser instalada com:
```bash
pip install numpy
```

### 2. Executar o Script
Salve o código em um arquivo Python (por exemplo, `algoritmo_genetico.py`) e execute:
```bash
python algoritmo_genetico.py
```

Se o comando acima não funcionar, tente:
```bash
python3 algoritmo_genetico.py
```

### 3. Verificar a Saída
Após a execução, o arquivo `alocacao_clientes.csv` será gerado no diretório do script.

## Personalização
- **Parâmetros do Algoritmo Genético**:
  - Tamanho da população: 100
  - Número de gerações: 200
  - Taxa de mutação: 0.1
- Esses parâmetros podem ser ajustados dentro da função `genetic_algorithm()` para otimização dos resultados.

## Contato
Se precisar de mais informações ou ajustes, entre em contato!

