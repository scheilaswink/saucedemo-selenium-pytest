"""Gera prints (PNG) e gravações (GIF) dos bugs encontrados no SauceDemo."""
import io, time
from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"
OUT = Path(__file__).resolve().parent.parent / "evidencias"
OUT.mkdir(exist_ok=True)
def T(d, t):
    return WebDriverWait(d, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-test="{t}"]')))

def drv():
    o = webdriver.ChromeOptions(); o.add_argument("--headless=new"); o.add_argument("--window-size=1280,1100")
    o.add_argument("--force-device-scale-factor=1")
    o.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})
    return webdriver.Chrome(options=o)

def login(d, u):
    d.get(URL); T(d,"username").send_keys(u); T(d,"password").send_keys("secret_sauce"); T(d,"login-button").click()
    WebDriverWait(d,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-test="inventory-list"]')))

def note(d, title, step, color="#c62828", highlight=None):
    """Faixa de anotação no topo + contorno vermelho no elemento com problema."""
    d.execute_script("""
      document.querySelectorAll('.qa-note,.qa-hl').forEach(e=>{ if(e.classList.contains('qa-note')) e.remove(); else {e.style.outline=''; e.classList.remove('qa-hl');}});
      const n=document.createElement('div'); n.className='qa-note';
      n.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:99999;background:'+arguments[2]+';color:#fff;font:600 17px Helvetica;padding:10px 16px;line-height:1.35;box-shadow:0 -2px 8px rgba(0,0,0,.3);pointer-events:none';
      n.innerHTML='<div style="font-size:19px">'+arguments[0]+'</div><div style="font-weight:400">'+arguments[1]+' &nbsp;|&nbsp; URL: '+location.href+'</div>';
      document.body.appendChild(n);
      (arguments[3]||[]).forEach(sel=>document.querySelectorAll(sel).forEach(e=>{e.classList.add('qa-hl'); e.style.outline='4px solid #e53935'; e.style.outlineOffset='3px';}));
    """, title, step, color, highlight or [])
    time.sleep(0.3)

def shot(d):
    return Image.open(io.BytesIO(d.get_screenshot_as_png())).convert("RGB")

def save_png(img, name): img.save(OUT / f"{name}.png"); print("PNG", name)
def save_gif(frames, name, ms=2200):
    frames[0].save(OUT / f"{name}.gif", save_all=True, append_images=frames[1:], duration=ms, loop=0, optimize=True)
    frames[-1].save(OUT / f"{name}_final.png"); print("GIF", name, len(frames), "quadros")

# BUG-01 problem_user: imagens dos produtos quebradas
d=drv(); login(d,"problem_user")
note(d,"BUG-01 · Imagens dos produtos incorretas (todas iguais)","Usuário: problem_user · Esperado: cada produto com sua imagem", highlight=["img.inventory_item_img"])
save_png(shot(d),"BUG-01_problem-user_imagens-dos-produtos-todas-iguais"); d.quit()

# BUG-02 problem_user: ordenação não funciona
d=drv(); login(d,"problem_user"); f=[]
note(d,"BUG-02 · Ordenação por preço não funciona","Passo 1/2: lista original", highlight=['[data-test="inventory-item-price"]']); f.append(shot(d))
Select(T(d,"product-sort-container")).select_by_value("lohi"); time.sleep(0.5)
note(d,"BUG-02 · Ordenação por preço não funciona","Passo 2/2: selecionado 'Price (low to high)' → preços continuam fora de ordem", highlight=['[data-test="inventory-item-price"]','[data-test="product-sort-container"]']); f.append(shot(d))
save_gif(f,"BUG-02_problem-user_ordenacao-por-preco-nao-funciona"); d.quit()

# BUG-03 problem_user: Add to cart não funciona
d=drv(); login(d,"problem_user"); f=[]
note(d,"BUG-03 · Botão 'Add to cart' não funciona (Sauce Labs Bolt T-Shirt)","Passo 1/2: carrinho vazio, antes do clique", highlight=['[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]','[data-test="shopping-cart-link"]']); f.append(shot(d))
T(d,"add-to-cart-sauce-labs-bolt-t-shirt").click(); time.sleep(0.5)
note(d,"BUG-03 · Botão 'Add to cart' não funciona (Sauce Labs Bolt T-Shirt)","Passo 2/2: após o clique, botão não muda para 'Remove' e carrinho continua vazio", highlight=['[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]','[data-test="shopping-cart-link"]']); f.append(shot(d))
save_gif(f,"BUG-03_problem-user_botao-add-to-cart-nao-adiciona-item"); d.quit()

# BUG-04 problem_user: Remove não funciona
d=drv(); login(d,"problem_user"); f=[]
T(d,"add-to-cart-sauce-labs-backpack").click(); time.sleep(0.4)
note(d,"BUG-04 · Botão 'Remove' não remove o item (Sauce Labs Backpack)","Passo 1/2: item no carrinho (contador = 1)", highlight=['[data-test="remove-sauce-labs-backpack"]','[data-test="shopping-cart-badge"]']); f.append(shot(d))
T(d,"remove-sauce-labs-backpack").click(); time.sleep(0.5)
note(d,"BUG-04 · Botão 'Remove' não remove o item (Sauce Labs Backpack)","Passo 2/2: após clicar em Remove, item continua no carrinho (contador = 1)", highlight=['[data-test="remove-sauce-labs-backpack"]','[data-test="shopping-cart-badge"]']); f.append(shot(d))
save_gif(f,"BUG-04_problem-user_botao-remove-nao-remove-item"); d.quit()

# BUG-05 problem_user: sobrenome substitui o nome no checkout
d=drv(); login(d,"problem_user"); f=[]
T(d,"add-to-cart-sauce-labs-backpack").click(); T(d,"shopping-cart-link").click(); T(d,"checkout").click()
T(d,"firstName").send_keys("Scheila")
note(d,"BUG-05 · Sobrenome digitado substitui o campo Nome no checkout","Passo 1/3: Nome preenchido com 'Scheila'", highlight=['[data-test="firstName"]','[data-test="lastName"]']); f.append(shot(d))
T(d,"lastName").send_keys("Wink"); time.sleep(0.3)
note(d,"BUG-05 · Sobrenome digitado substitui o campo Nome no checkout","Passo 2/3: digitado 'Wink' no Sobrenome → Nome vira 'k' e Sobrenome fica vazio", highlight=['[data-test="firstName"]','[data-test="lastName"]']); f.append(shot(d))
T(d,"postalCode").send_keys("13330"); T(d,"continue").click(); time.sleep(0.5)
note(d,"BUG-05 · Sobrenome digitado substitui o campo Nome no checkout","Passo 3/3: ao continuar, erro 'Last Name is required' impede a compra", highlight=['[data-test="error"]','[data-test="lastName"]']); f.append(shot(d))
save_gif(f,"BUG-05_problem-user_checkout-sobrenome-substitui-nome"); d.quit()

# BUG-06 error_user: alerta de erro na ordenação
d=drv(); login(d,"error_user")
Select(T(d,"product-sort-container")).select_by_value("za"); time.sleep(0.4)
a=d.switch_to.alert; atxt=a.text; a.accept()
note(d,"BUG-06 · Ordenação exibe alerta de erro e não ordena","Usuário: error_user · Selecionado 'Name (Z to A)' → alerta: \"" + atxt + "\"", highlight=['[data-test="product-sort-container"]','[data-test="inventory-item-name"]'])
save_png(shot(d),"BUG-06_error-user_ordenacao-exibe-alerta-de-erro"); d.quit()

# BUG-07 error_user: sobrenome não aceita texto e checkout avança sem validar
d=drv(); login(d,"error_user"); f=[]
T(d,"add-to-cart-sauce-labs-backpack").click(); T(d,"shopping-cart-link").click(); T(d,"checkout").click()
T(d,"firstName").send_keys("Scheila"); T(d,"lastName").send_keys("Wink"); T(d,"postalCode").send_keys("13330"); time.sleep(0.3)
note(d,"BUG-07 · Campo Sobrenome não aceita texto e o checkout avança sem validação","Passo 1/2: digitado 'Wink' no Sobrenome → campo continua vazio", highlight=['[data-test="lastName"]']); f.append(shot(d))
T(d,"continue").click(); time.sleep(0.6)
note(d,"BUG-07 · Campo Sobrenome não aceita texto e o checkout avança sem validação","Passo 2/2: sistema avança para a revisão do pedido mesmo sem sobrenome (campo obrigatório)"); f.append(shot(d))
save_gif(f,"BUG-07_error-user_sobrenome-nao-aceita-texto-e-checkout-avanca"); d.quit()

# BUG-08 error_user: Finish não conclui o pedido
d=drv(); login(d,"error_user"); f=[]
T(d,"add-to-cart-sauce-labs-backpack").click(); T(d,"shopping-cart-link").click(); T(d,"checkout").click()
T(d,"firstName").send_keys("Scheila"); T(d,"postalCode").send_keys("13330"); T(d,"continue").click(); time.sleep(0.5)
note(d,"BUG-08 · Botão 'Finish' não conclui o pedido","Passo 1/2: tela de revisão do pedido, antes de clicar em Finish", highlight=['[data-test="finish"]']); f.append(shot(d))
T(d,"finish").click(); time.sleep(1)
note(d,"BUG-08 · Botão 'Finish' não conclui o pedido","Passo 2/2: após clicar em Finish, continua na mesma tela (esperado: 'Thank you for your order!')", highlight=['[data-test="finish"]']); f.append(shot(d))
save_gif(f,"BUG-08_error-user_botao-finish-nao-conclui-pedido"); d.quit()

# BUG-09 visual_user: preços incorretos e mudam a cada carregamento
f=[]
d=drv(); login(d,"standard_user")
note(d,"BUG-09 · Preços incorretos e diferentes a cada carregamento","Referência: standard_user mostra os preços corretos", color="#2e7d32", highlight=['[data-test="inventory-item-price"]']); f.append(shot(d)); d.quit()
d=drv(); login(d,"visual_user")
note(d,"BUG-09 · Preços incorretos e diferentes a cada carregamento","visual_user · 1º carregamento: preços diferentes da referência", highlight=['[data-test="inventory-item-price"]']); f.append(shot(d))
d.refresh(); WebDriverWait(d,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-test="inventory-list"]'))); time.sleep(0.5)
note(d,"BUG-09 · Preços incorretos e diferentes a cada carregamento","visual_user · 2º carregamento (F5): os preços mudam de novo", highlight=['[data-test="inventory-item-price"]']); f.append(shot(d))
save_gif(f,"BUG-09_visual-user_precos-incorretos-mudam-a-cada-carregamento"); d.quit()

# BUG-10 visual_user: imagem da mochila incorreta
d=drv(); login(d,"visual_user")
note(d,"BUG-10 · Imagem da 'Sauce Labs Backpack' incorreta","Usuário: visual_user · Esperado: foto da mochila", highlight=['img[alt="Sauce Labs Backpack"]'])
save_png(shot(d),"BUG-10_visual-user_imagem-da-mochila-incorreta"); d.quit()
