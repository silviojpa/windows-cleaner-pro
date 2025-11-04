import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import send2trash

# --- Configurações Globais ---
DEVELOPER_NAME = "Silvio Luiz" # <-- MEU NOME AQUI
APP_VERSION = "1.5" 

# --- 1. Configuração de Localização (Multi-idiomas) ---
LANG_DATA = {
    "pt": {
        "title": f"Limpeza e Utilitários - Cleaner Pro v{APP_VERSION}",
        "app_title": "Windows Cleaner Pro",
        "developer_label": f"Developer by : {DEVELOPER_NAME}",
        "lang_label": "Idioma:",
        
        # Abas
        "tab_cleaner": "Limpeza",
        "tab_utilities": "Utilitários",
        
        # Limpeza
        "options_group": "Opções de Limpeza",
        "select_all": "Selecionar Tudo",
        "cleanup_button": "Executar Limpeza",
        
        # Status e Log
        "status_ready": "Pronto para iniciar",
        "status_cleaning": "Limpando: {0}...",
        "status_success": "Limpeza Concluída! {0} tarefas executadas.",
        "status_error": "ERRO em {0}. Tente executar como Administrador.",
        "result_header": "Resultados/Logs:",
        
        # Opções de Limpeza
        "opt_temp_files": "Arquivos Temporários (Geral do Windows)",
        "opt_user_temp": "Temp do Usuário (%TEMP%)",
        "opt_prefetch": "Cache Prefetch (Otimização)",
        "opt_dns_cache": "Cache DNS (ipconfig /flushdns)",
        "opt_recycle_bin": "Esvaziar Lixeira",
        "opt_thumbnails": "Cache de Miniaturas (Ícones de Imagem)",
        "opt_windows_temp": "Temp do Windows (C:\\Windows\\Temp)",
        "opt_log_files": "Arquivos de Log do Sistema",
        
        # Utilitários
        "util_appearance": "Aparência",
        "util_mode_label": "Modo de Cor:",
        "util_mode_dark": "Escuro (Dark)",
        "util_mode_light": "Claro (Light)",
        "util_mode_system": "Sistema",
        "util_integrity": "Integridade do Sistema",
        "util_sfc_desc": "Verifica e repara arquivos essenciais do Windows (sfc /scannow).",
        "util_sfc_button": "Executar SFC /SCANNOW",
    },
    "en": {
        "title": f"Cleanup and Utilities - Cleaner Pro v{APP_VERSION}",
        "app_title": "Windows Cleaner Pro",
        "developer_label": f"Developed by: {DEVELOPER_NAME}",
        "lang_label": "Language:",
        
        # Tabs
        "tab_cleaner": "Cleaner",
        "tab_utilities": "Utilities",

        # Cleaner
        "options_group": "Cleanup Options",
        "select_all": "Select All",
        "cleanup_button": "Execute Cleanup",
        
        # Status and Log
        "status_ready": "Ready to start",
        "status_cleaning": "Cleaning: {0}...",
        "status_success": "Cleanup Complete! {0} tasks executed.",
        "status_error": "ERROR in {0}. Try running as Administrator.",
        "result_header": "Results/Logs:",

        # Cleanup Options
        "opt_temp_files": "Temporary Files (Windows General)",
        "opt_user_temp": "User Temp (%TEMP%)",
        "opt_prefetch": "Prefetch Cache (Optimization)",
        "opt_dns_cache": "DNS Cache (ipconfig /flushdns)",
        "opt_recycle_bin": "Empty Recycle Bin",
        "opt_thumbnails": "Thumbnail Cache (Image Icons)",
        "opt_windows_temp": "Windows Temp (C:\\Windows\\Temp)",
        "opt_log_files": "System Log Files",

        # Utilities
        "util_appearance": "Appearance",
        "util_mode_label": "Color Mode:",
        "util_mode_dark": "Dark",
        "util_mode_light": "Light",
        "util_mode_system": "System",
        "util_integrity": "System Integrity",
        "util_sfc_desc": "Checks and repairs essential Windows files (sfc /scannow).",
        "util_sfc_button": "Execute SFC /SCANNOW",
    },
}

class CleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_lang = "pt"
        self.lang_keys = list(LANG_DATA.keys())
        
        # Configuração da Janela
        self.title(self.get_string("title"))
        self.geometry("500x750") # Um pouco maior para acomodar as abas
        self.resizable(True, True) 
        ctk.set_appearance_mode("Dark") # Inicia em Dark
        ctk.set_default_color_theme("blue")

        self.cleanup_vars = {}
        
        self._setup_ui()
        self._update_language()

    def get_string(self, key):
        return LANG_DATA[self.current_lang].get(key, key)

    # --- 2. Criação e Layout da Interface (GUI) ---
    def _setup_ui(self):
        
        # Configura a célula principal da janela para se expandir
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0) # Linha do developer_label

        # Frame principal para as abas
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 0)) 
        main_frame.grid_columnconfigure(0, weight=1) 
        main_frame.grid_rowconfigure(2, weight=1) # Faz o TabView expandir

        row_counter = 0
        
        # Título Principal
        self.lbl_title = ctk.CTkLabel(main_frame, text="Windows Cleaner Pro", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_title.grid(row=row_counter, column=0, pady=(10, 5))
        row_counter += 1

        # Seletor de Idioma
        lang_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        lang_frame.grid(row=row_counter, column=0, sticky="ew", pady=(0, 10))
        
        self.lbl_lang = ctk.CTkLabel(lang_frame, text="Idioma:")
        self.lbl_lang.pack(side="left", padx=(0, 10))

        self.cmb_lang = ctk.CTkComboBox(lang_frame, 
                                        values=[f"{LANG_DATA[k]['lang_label']} ({k})" for k in self.lang_keys],
                                        command=self._language_changed)
        self.cmb_lang.set(f"Português (pt)")
        self.cmb_lang.pack(side="left", fill="x", expand=True)
        row_counter += 1

        # --- TabView para separar Limpeza e Utilitários ---
        # Note: Os nomes das abas ("Limpeza" e "Utilitários") são definidos aqui
        # e não serão traduzidos ao trocar de idioma (pois removemos a função problemática).
        self.tab_view = ctk.CTkTabview(main_frame)
        self.tab_view.grid(row=row_counter, column=0, sticky="nsew", pady=10)
        self.tab_cleaner = self.tab_view.add(self.get_string("tab_cleaner")) # Usa a string traduzida
        self.tab_utilities = self.tab_view.add(self.get_string("tab_utilities")) # Usa a string traduzida
        row_counter += 1
        
        # --- Configurar as abas para que o conteúdo se expanda ---
        self._setup_cleaner_tab()
        self._setup_utilities_tab()
        
        # Rótulo de Status
        self.lbl_status = ctk.CTkLabel(main_frame, text="Pronto para limpar", text_color="yellow")
        self.lbl_status.grid(row=row_counter, column=0, pady=(5, 10))
        row_counter += 1

        # Resultados (TextBox)
        self.lbl_results_title = ctk.CTkLabel(main_frame, text="Resultados:", font=ctk.CTkFont(weight="bold"))
        self.lbl_results_title.grid(row=row_counter, column=0, sticky="w", pady=(5, 5))
        row_counter += 1
        
        self.txt_results = ctk.CTkTextbox(main_frame) 
        self.txt_results.grid(row=row_counter, column=0, sticky="nsew") 
        self.txt_results.insert("end", "Inicie a limpeza...")
        self.txt_results.configure(state="disabled")
        
        # --- NOME DO DESENVOLVEDOR (Fundo) ---
        self.lbl_developer = ctk.CTkLabel(self, text=DEVELOPER_NAME, font=ctk.CTkFont(size=10))
        self.lbl_developer.grid(row=1, column=0, pady=5)


    # --- Aba: Limpeza (CLEANER) ---
    def _setup_cleaner_tab(self):
        tab = self.tab_cleaner
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(4, weight=1) 

        row_counter = 0

        self.lbl_options_title = ctk.CTkLabel(tab, text="Opções de Limpeza", font=ctk.CTkFont(weight="bold"))
        self.lbl_options_title.grid(row=row_counter, column=0, pady=(10, 5))
        row_counter += 1

        self.checkbox_configs = [
            "opt_temp_files", "opt_user_temp", "opt_prefetch", "opt_dns_cache",
            "opt_recycle_bin", "opt_thumbnails", "opt_windows_temp", "opt_log_files"
        ]
        
        self.select_all_var = ctk.BooleanVar(value=True)
        self.cb_select_all = ctk.CTkCheckBox(tab, text="Selecionar Tudo", 
                                            variable=self.select_all_var, command=self._toggle_select_all)
        self.cb_select_all.grid(row=row_counter, column=0, sticky="w", padx=20, pady=(10, 5))
        row_counter += 1
        
        cb_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cb_frame.grid(row=row_counter, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        cb_frame.columnconfigure(0, weight=1, minsize=190)
        cb_frame.columnconfigure(1, weight=1, minsize=190)

        for i, key in enumerate(self.checkbox_configs):
            self.cleanup_vars[key] = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(cb_frame, text="", variable=self.cleanup_vars[key])
            
            row = i // 2
            col = i % 2
            cb.grid(row=row, column=col, sticky="w", padx=(10 if col == 0 else 5), pady=5) 
            self.cleanup_vars[key].widget = cb 
        row_counter += 1

        self.btn_cleanup = ctk.CTkButton(tab, text="Executar Limpeza", command=self._execute_cleanup)
        self.btn_cleanup.grid(row=row_counter, column=0, sticky="ew", pady=20, padx=10)
        row_counter += 1

    # --- Aba: Utilitários (UTILITIES) ---
    def _setup_utilities_tab(self):
        tab = self.tab_utilities
        tab.grid_columnconfigure(0, weight=1)
        
        row_counter = 0
        
        # --- 1. Troca de Aparência ---
        frame_appearance = ctk.CTkFrame(tab)
        frame_appearance.grid(row=row_counter, column=0, sticky="ew", padx=10, pady=(10, 5))
        frame_appearance.grid_columnconfigure(0, weight=1) # Rótulo
        frame_appearance.grid_columnconfigure(1, weight=1) # Seletor
        
        lbl_appearance_title = ctk.CTkLabel(frame_appearance, text="Aparência", font=ctk.CTkFont(weight="bold"))
        lbl_appearance_title.grid(row=0, column=0, columnspan=2, pady=(5, 5))
        
        self.lbl_mode = ctk.CTkLabel(frame_appearance, text="Modo de Cor:")
        self.lbl_mode.grid(row=1, column=0, sticky="w", padx=(10, 0))
        
        # O ComboBox usa os textos traduzidos para os valores
        self.cmb_mode = ctk.CTkComboBox(frame_appearance, 
                                        values=[self.get_string("util_mode_dark"), 
                                                self.get_string("util_mode_light"), 
                                                self.get_string("util_mode_system")],
                                        command=self._change_appearance_mode)
        self.cmb_mode.set(self.get_string("util_mode_dark")) # Valor inicial
        self.cmb_mode.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        row_counter += 1
        
        # --- 2. Verificação de Integridade de Arquivos (SFC) ---
        frame_sfc = ctk.CTkFrame(tab)
        frame_sfc.grid(row=row_counter, column=0, sticky="ew", padx=10, pady=(10, 5))
        frame_sfc.grid_columnconfigure(0, weight=1)

        lbl_sfc_title = ctk.CTkLabel(frame_sfc, text="Integridade do Sistema", font=ctk.CTkFont(weight="bold"))
        lbl_sfc_title.grid(row=0, column=0, pady=(5, 5))

        self.lbl_sfc_desc = ctk.CTkLabel(frame_sfc, text="Verifica e repara arquivos essenciais do Windows (sfc /scannow).", wraplength=450)
        self.lbl_sfc_desc.grid(row=1, column=0, padx=10, sticky="w")
        
        self.btn_sfc = ctk.CTkButton(frame_sfc, text="Executar SFC /SCANNOW", command=self._execute_sfc)
        self.btn_sfc.grid(row=2, column=0, sticky="ew", pady=(10, 10), padx=10)
        row_counter += 1


    # --- 3. Lógica de Funcionalidades (Nova) ---

    def _change_appearance_mode(self, new_mode):
        """Muda o modo de cor do CustomTkinter."""
        
        # Mapeia o texto traduzido de volta para o valor interno do CTk
        mode_map = {
            self.get_string("util_mode_dark"): "Dark",
            self.get_string("util_mode_light"): "Light",
            self.get_string("util_mode_system"): "System"
        }
        
        ctk.set_appearance_mode(mode_map.get(new_mode, "Dark"))
        self._log(f"[Aparência] Modo alterado para: {new_mode}", is_error=False)


    def _execute_sfc(self):
        """Executa o SFC /SCANNOW no Windows (requer Admin)."""
        
        task_name = self.get_string("util_sfc_button")
        
        self._log(f"\n--- Iniciando: {task_name} ---")
        self._log("AVISO: Esta tarefa pode levar tempo e exige privilégios de Administrador.", is_error=False)
        
        self.btn_sfc.configure(state="disabled")
        self.lbl_status.configure(text=self.get_string("status_cleaning").format(task_name), text_color="yellow")
        self.update()
        
        try:
            # Comando SFC /SCANNOW. 
            result = subprocess.run("sfc /scannow", shell=True, capture_output=True, text=True, encoding='cp850')
            
            if result.returncode == 0:
                self._log(f"--- Concluído com sucesso: {task_name} (Verifique o console para detalhes). ---", is_error=False)
                
                # Exibe o resultado da saída no log (pode ser muito longo)
                self._log("\nSaída do SFC (Resumo):\n" + result.stdout[:500] + "...", is_error=False)
            else:
                self._log(f"--- Falha na execução: {task_name}. Código de Retorno: {result.returncode}", is_error=True)
                self._log(f"Erro: {result.stderr}", is_error=True)

        except Exception as e:
            self._log(f"--- ERRO CRÍTICO em {task_name}: {e} ---", is_error=True)
            
        self.lbl_status.configure(text=self.get_string("status_ready"), text_color="yellow")
        self.btn_sfc.configure(state="normal")


    # --- 4. Lógica de Limpeza de Sistema (Manutenção) ---
    
    def _cleanup_dir(self, path_env, task_name):
        path = os.path.expandvars(path_env)
        if not os.path.exists(path):
            self._log(f"[AVISO] Pasta {path_env} não encontrada ou inacessível.") 
            return 0
        
        deleted_count = 0
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.islink(item_path) or os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                    deleted_count += 1
                elif os.path.isfile(item_path):
                    os.remove(item_path)
                    deleted_count += 1
            except PermissionError:
                self._log(f"  > [PERMISSÃO NEGADA] Falha ao excluir {item}.", is_error=True)
            except Exception as e:
                self._log(f"  > [FALHA] Falha ao excluir {item}: {e}", is_error=True)
        return deleted_count

    def _execute_cleanup(self):
        self.btn_cleanup.configure(state="disabled")
        self.lbl_status.configure(text=self.get_string("status_cleaning").format("Geral"), text_color="yellow")
        self.txt_results.configure(state="normal")
        self.txt_results.delete("1.0", "end")
        self.txt_results.configure(state="disabled")
        
        tasks_executed = 0

        tasks = {
            "opt_user_temp": lambda: self._cleanup_dir(os.environ.get('TEMP'), "Temp do Usuário"),
            "opt_windows_temp": lambda: self._cleanup_dir("C:\\Windows\\Temp", "Temp do Windows"),
            "opt_prefetch": lambda: self._cleanup_dir("C:\\Windows\\Prefetch", "Cache Prefetch"),
            "opt_temp_files": lambda: self._cleanup_dir(os.environ.get('LOCALAPPDATA') + "\\Temp", "Arquivos Temporários (Geral)"), 
            
            "opt_dns_cache": lambda: subprocess.run("ipconfig /flushdns", shell=True, capture_output=True, text=True).returncode == 0,
            "opt_recycle_bin": lambda: send2trash.empty_trash() or 1,
            
            "opt_thumbnails": lambda: subprocess.run('cmd /c "del /q /f /s %LocalAppData%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db"', shell=True, capture_output=True, text=True).returncode == 0,
            
            "opt_log_files": lambda: self._cleanup_dir("C:\\Windows\\Logs", "Arquivos de Log do Sistema")
        }

        self._log("\n*** Aviso: Execute o EXE como Administrador para melhores resultados! ***")

        for key, action in tasks.items():
            if self.cleanup_vars[key].get():
                self.update() 
                task_name = self.get_string(key)
                
                self.lbl_status.configure(text=self.get_string("status_cleaning").format(task_name))
                self._log(f"\n--- Iniciando: {task_name} ---")
                
                try:
                    action_result = action()
                    
                    is_successful = False
                    if isinstance(action_result, int) and action_result >= 0:
                        is_successful = True
                    elif action_result is True:
                        is_successful = True

                    if is_successful:
                        self._log(f"--- Concluído: {task_name} ---", is_error=False)
                        tasks_executed += 1
                    else:
                        self._log(f"--- Falha: {task_name} - Retorno inesperado. ---", is_error=True)

                except Exception as e:
                    self._log(f"--- ERRO CRÍTICO em {task_name}: {e} ---", is_error=True)


        # Resultado Final
        self.lbl_status.configure(text=self.get_string("status_success").format(tasks_executed), text_color="green")
        self.btn_cleanup.configure(state="normal")
        self._log("\n*** Limpeza Geral Concluída! ***", is_error=False)


    # --- 5. Funções de Tradução e Log (Manutenção) ---

    def _language_changed(self, choice):
        self.current_lang = choice.split("(")[-1].replace(")", "").strip()
        self._update_language()

    def _update_language(self):
        self.title(self.get_string("title"))
        self.lbl_title.configure(text=self.get_string("app_title"))
        self.lbl_lang.configure(text=self.get_string("lang_label"))
        self.lbl_options_title.configure(text=self.get_string("options_group"))
        self.cb_select_all.configure(text=self.get_string("select_all"))
        self.btn_cleanup.configure(text=self.get_string("cleanup_button"))
        self.lbl_results_title.configure(text=self.get_string("result_header"))
        self.lbl_developer.configure(text=self.get_string("developer_label"))
        
        # Abas
        # Os nomes das abas não serão traduzidos dinamicamente devido à falta do método 'set_tab_text'
        # na sua versão do customtkinter (5.2.2). Elas usam o nome definido na inicialização.
        
        # Utilitários
        self.lbl_mode.configure(text=self.get_string("util_mode_label"))
        self.lbl_sfc_desc.configure(text=self.get_string("util_sfc_desc"))
        self.btn_sfc.configure(text=self.get_string("util_sfc_button"))
        
        # O ComboBox de Aparência precisa ser atualizado, mas isso é feito na inicialização.
        
        for key, var in self.cleanup_vars.items():
            if hasattr(var, 'widget'):
                var.widget.configure(text=self.get_string(key))
        
        self.lbl_status.configure(text=self.get_string("status_ready"))
            
    def _toggle_select_all(self):
        state = self.select_all_var.get()
        for var in self.cleanup_vars.values():
            var.set(state)
            
    def _log(self, message, is_error=False):
        self.txt_results.configure(state="normal")
        self.txt_results.tag_config("error", foreground="red") 
        self.txt_results.tag_config("success", foreground="#00C000") 
        
        tag = "error" if is_error else ""
        self.txt_results.insert("end", f"{message}\n", tag)
        self.txt_results.configure(state="disabled")
        self.txt_results.see("end")
        self.update() 


if __name__ == "__main__":
    try:
        app = CleanerApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror(
            "ERRO CRÍTICO DE INICIALIZAÇÃO", 
            f"O aplicativo não pôde ser iniciado.\n\nDetalhes do Erro:\n{e}"
        )