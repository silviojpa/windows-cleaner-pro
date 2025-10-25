# 🧹 Windows Cleaner Pro

Uma ferramenta de limpeza e otimização do Windows com Interface Gráfica (GUI) moderna e multi-idiomas, desenvolvida em Python utilizando a biblioteca **CustomTkinter**.

O aplicativo é capaz de limpar caches de sistema, arquivos temporários, logs e o cache DNS, ajudando a manter a performance do Windows 10/11.

## ✨ Funcionalidades

* **Interface Gráfica Minimalista:** Desenvolvida em CustomTkinter com Dark Mode.
* **Limpeza Abrangente:** Inclui arquivos temporários de usuário (`%TEMP%`), Prefetch, logs, cache de miniaturas e esvaziamento da Lixeira.
* **Otimização de Performance:** Limpeza do Cache DNS (`ipconfig /flushdns`).
* **Janela Ajustável:** A interface pode ser redimensionada, expandindo o campo de logs e resultados para melhor visualização.
* **Multi-idiomas:** Suporte inicial para Português (pt) e Inglês (en).

## 🖼️ Prévia

| Interface Principal | Resultados da Limpeza |
| :---: | :---: |
| <img width="451" height="726" alt="image" src="https://github.com/user-attachments/assets/f19d97b4-d468-47ed-a223-dd071ba28289" /> | <img width="449" height="721" alt="image" src="https://github.com/user-attachments/assets/5cf8cf2e-df76-4501-a512-5b8bcee2ccf6" />
 |

*(Nota: Substitua `assets/preview_main.png` e `assets/preview_results.png` por capturas de tela do seu próprio projeto, como as que foram geradas.)*

## 🚀 Como Usar (Recomendado)

A melhor forma de usar e distribuir a ferramenta é através da versão executável (`.exe`).

1.  Baixe o arquivo `WindowsCleanerPro.exe` da pasta [`dist/`](dist/) ou da página de *Releases* do projeto.
2.  **IMPORTANTE:** Para que o programa consiga apagar todos os logs e arquivos de sistema protegidos (evitando erros de **Permissão Negada** e avisos de falha), **sempre execute o EXE como Administrador** (clique com o botão direito -> Executar como Administrador).
3.  Selecione as opções e clique em "Executar Limpeza".

---

## ⚙️ Configuração para Desenvolvimento (Clonar e Rodar)

Se você deseja modificar o código-fonte (`cleaner_pro.py`), siga os passos abaixo.

### Pré-requisitos

* Python 3.8+
* Git

### Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/windows-cleaner-pro.git](https://github.com/SEU_USUARIO/windows-cleaner-pro.git)
    cd windows-cleaner-pro
    ```

2.  **Crie e Ative o Ambiente Virtual (`venv`):**
    É altamente recomendado usar um ambiente virtual para isolar as dependências.
    ```bash
    python -m venv venv
    # No Windows PowerShell:
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instale as Dependências:**
    Instale as bibliotecas necessárias listadas no `requirements.txt`:
    ```bash
    (venv) pip install -r requirements.txt
    ```

### Execução do Código-Fonte

Com o ambiente virtual ativo, execute o script:

```bash
(venv) python cleaner_pro.py
```
------------------------------

### Compilando para EXE (PyInstaller)
Para gerar o executável de arquivo único (.exe), utilize o PyInstaller. Certifique-se de que o caminho absoluto no comando abaixo está correto para o seu sistema!

```bash
(venv) pyinstaller --onefile --windowed --name "WindowsCleanerPro" --add-data "C:/Users/SEU_USUARIO/Documents/cleaner_pro/venv/Lib/site-packages/customtkinter/assets;customtkinter/assets" cleaner_pro.py
```
