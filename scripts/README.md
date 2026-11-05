# Scripts de apoio

Scripts usados nos testes exploratórios. Eles não fazem parte da suíte do Pytest.

| Script | O que faz |
|---|---|
| `explorar_bugs.py` | Compara o comportamento de `problem_user`, `error_user` e `visual_user` com o `standard_user` |
| `explorar_checkout.py` | Investiga em detalhe o fluxo de checkout e os alertas do `error_user` |
| `gerar_evidencias.py` | Gera os prints (PNG) e as gravações (GIF) da pasta `evidencias/` |

Para executar, a partir da raiz do projeto:

```
python scripts/gerar_evidencias.py
```
