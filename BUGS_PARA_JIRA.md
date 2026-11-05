# Relatórios de bugs para o Jira — SauceDemo

Ambiente (vale para todos): https://www.saucedemo.com · Chrome (macOS) · senha `secret_sauce`
Anexos: pasta `evidencias/`. Quando houver GIF, anexe o GIF (gravação) e o PNG `_final`.

---

## BUG-01 — Imagens dos produtos são todas iguais (problem_user)
**Prioridade:** Baixa
**Pré-condição:** Login com `problem_user`
**Passos:**
1. Acessar https://www.saucedemo.com
2. Fazer login com `problem_user` / `secret_sauce`
3. Observar as imagens na página de produtos
**Resultado esperado:** Cada produto exibe sua própria imagem.
**Resultado obtido:** Todos os produtos exibem a mesma imagem (um cachorro, arquivo `sl-404`).
**Anexo:** `BUG-01_problem-user_imagens-dos-produtos-todas-iguais.png`

---

## BUG-02 — Ordenação por preço não funciona (problem_user)
**Prioridade:** Média
**Pré-condição:** Login com `problem_user`
**Passos:**
1. Fazer login com `problem_user`
2. No filtro de ordenação, selecionar "Price (low to high)"
**Resultado esperado:** Produtos ordenados do menor para o maior preço.
**Resultado obtido:** A ordem dos produtos não muda (o filtro volta para "Name (A to Z)").
**Anexos:** `BUG-02_..._nao-funciona.gif` e `BUG-02_..._final.png`

---

## BUG-03 — Botão "Add to cart" não adiciona alguns itens (problem_user)
**Prioridade:** Alta
**Pré-condição:** Login com `problem_user`, carrinho vazio
**Passos:**
1. Fazer login com `problem_user`
2. Clicar em "Add to cart" em "Sauce Labs Bolt T-Shirt"
3. Repetir em "Sauce Labs Fleece Jacket" e "Test.allTheThings() T-Shirt (Red)"
**Resultado esperado:** O botão muda para "Remove" e o contador do carrinho aumenta.
**Resultado obtido:** Nada acontece; o item não é adicionado e o contador não muda.
**Observação:** O mesmo ocorre com `error_user`.
**Anexos:** `BUG-03_..._nao-adiciona-item.gif` e `BUG-03_..._final.png`

---

## BUG-04 — Botão "Remove" não remove o item (problem_user)
**Prioridade:** Alta
**Pré-condição:** Login com `problem_user`
**Passos:**
1. Fazer login com `problem_user`
2. Adicionar "Sauce Labs Backpack" ao carrinho
3. Clicar em "Remove" no mesmo produto
**Resultado esperado:** O item sai do carrinho, o botão volta para "Add to cart" e o contador diminui.
**Resultado obtido:** O botão continua "Remove" e o item permanece no carrinho. Também acontece com "Bike Light" e "Onesie".
**Observação:** O mesmo ocorre com `error_user`.
**Anexos:** `BUG-04_..._nao-remove-item.gif` e `BUG-04_..._final.png`

---

## BUG-05 — No checkout, digitar o sobrenome substitui o nome (problem_user)
**Prioridade:** Alta (impede concluir a compra)
**Pré-condição:** Login com `problem_user` e 1 item no carrinho
**Passos:**
1. Ir ao carrinho e clicar em "Checkout"
2. Preencher First Name "Scheila"
3. Preencher Last Name "Wink" e Zip "13330-000"
4. Clicar em "Continue"
**Resultado esperado:** Os campos mantêm os valores digitados e o checkout avança para o resumo do pedido.
**Resultado obtido:** O texto do sobrenome vai para o campo First Name (fica só "k"), o Last Name fica vazio e aparece "Error: Last Name is required".
**Anexos:** `BUG-05_..._substitui-nome.gif` e `BUG-05_..._final.png`

---

## BUG-06 — Ordenação exibe alerta de erro e não ordena (error_user)
**Prioridade:** Média
**Pré-condição:** Login com `error_user`
**Passos:**
1. Fazer login com `error_user`
2. No filtro, selecionar "Name (Z to A)"
**Resultado esperado:** Produtos ordenados de Z para A.
**Resultado obtido:** Aparece o alerta "Sorting is broken! This error has been reported to Backtrace." e a lista não muda.
**Anexo:** `BUG-06_error-user_ordenacao-exibe-alerta-de-erro.png`

---

## BUG-07 — Sobrenome não aceita texto e o checkout avança sem validação (error_user)
**Prioridade:** Alta
**Pré-condição:** Login com `error_user` e 1 item no carrinho
**Passos:**
1. Ir ao carrinho e clicar em "Checkout"
2. Preencher First Name, Last Name "Wink" e Zip
3. Clicar em "Continue"
**Resultado esperado:** O campo Last Name aceita o texto. Se estiver vazio, aparece "Last Name is required".
**Resultado obtido:** O campo Last Name continua vazio e, mesmo assim, o checkout avança para o resumo.
**Anexos:** `BUG-07_..._checkout-avanca.gif` e `BUG-07_..._final.png`

---

## BUG-08 — Botão "Finish" não conclui o pedido (error_user)
**Prioridade:** Crítica (bloqueia a compra)
**Pré-condição:** Login com `error_user`, item no carrinho, dados do checkout preenchidos
**Passos:**
1. Na tela "Checkout: Overview", clicar em "Finish"
**Resultado esperado:** Abre a página "Thank you for your order!".
**Resultado obtido:** Nada acontece; o usuário continua em `/checkout-step-two.html`.
**Anexos:** `BUG-08_..._nao-conclui-pedido.gif` e `BUG-08_..._final.png`

---

## BUG-09 — Preços incorretos que mudam a cada carregamento (visual_user)
**Prioridade:** Alta
**Pré-condição:** Login com `visual_user`
**Passos:**
1. Fazer login com `standard_user` e anotar os preços (referência)
2. Fazer logout e entrar com `visual_user`
3. Comparar os preços e recarregar a página (F5)
**Resultado esperado:** Mesmos preços do `standard_user`, sem mudar ao recarregar.
**Resultado obtido:** Os preços são diferentes e mudam a cada carregamento da página.
**Anexos:** `BUG-09_..._a-cada-carregamento.gif` e `BUG-09_..._final.png`

---

## BUG-10 — Imagem da mochila incorreta (visual_user)
**Prioridade:** Baixa
**Pré-condição:** Login com `visual_user`
**Passos:**
1. Fazer login com `visual_user`
2. Observar o produto "Sauce Labs Backpack"
**Resultado esperado:** A imagem mostra a mochila.
**Resultado obtido:** A imagem mostra outro produto (um cachorro).
**Anexo:** `BUG-10_visual-user_imagem-da-mochila-incorreta.png`
