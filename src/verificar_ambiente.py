"""Verifica se as bibliotecas do projeto estão instaladas."""
import sys

import duckdb
import numpy as np
import pandas as pd

print(f"Python: {sys.version.split()[0]}")
print(f"pandas: {pd.__version__}")
print(f"numpy: {np.__version__}")
print(f"duckdb: {duckdb.__version__}")

pedidos = pd.DataFrame({"pedido": [1, 2, 3], "valor": [42.0, 55.5, 30.0]})
total = duckdb.sql("SELECT SUM(valor) AS total FROM pedidos").fetchall()[0][0]
print(f"Teste rápido: o total dos 3 pedidos é R$ {total:.2f}")
print("Ambiente pronto!")