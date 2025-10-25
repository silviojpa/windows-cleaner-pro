import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import send2trash

# --- 1. Configuração de Localização (Multi-idiomas) ---
LANG_DATA = {
    "pt": {
        "title": "Limpeza do Windows - Cleaner Pro",
        "app_title": "Windows Cleaner Pro",
        "lang_label": "Idioma:",
        "options_group": "Opções de Limpeza",
        "select_all": "Selecionar Tudo",
        "cleanup_button": "Executar Limpeza",
        "status_ready": "Pronto para limpar",
        "status_cleaning": "Limpando: {0}...",
        "status_success": "Limpeza Concluída! {0} tarefas executadas.",
        "status_error": "ERRO em {0}. Tente executar como Administrador.",
        "result_header": "Resultados:",
        "opt_temp_files": "Arquivos Temporários (Geral do Windows)",
        "opt_user_temp": "Temp do Usuário (%TEMP%)",
        "opt_prefetch": "Cache Prefetch (Otimização)",
        "opt_dns_cache": "Cache DNS (ipconfig /flushdns)",
        "opt_recycle_bin": "Esvaziar Lixeira",
        "opt_thumbnails": "Cache de Miniaturas (Ícones de Imagem)",
        "opt_windows_temp": "Temp do Windows (C:\\Windows\\Temp)",
        "opt_log_files": "Arquivos de Log do Sistema",
    },
    "en": {
        "title": "Windows Cleanup - Cleaner Pro",
        "app_title": "Windows Cleaner Pro",
        "lang_label": "Language:",
        "options_group": "Cleanup Options",
        "select_all": "Select All",
        "cleanup_button": "Execute Cleanup",
        "status_ready": "Ready to clean",
        "status_cleaning": "Cleaning: {0}...",
        "status_success": "Cleanup Complete! {0} tasks executed.",
        "status_error": "ERROR in {0}. Try running as Administrator.",
        "result_header": "Results:",
        "opt_temp_files": "Temporary Files (Windows General)",
        "opt_user_temp": "User Temp (%TEMP%)",
        "opt_prefetch": "Prefetch Cache (Optimization)",
        "opt_dns_cache": "DNS Cache (ipconfig /flushdns)",
        "opt_recycle_bin": "Empty Recycle Bin",
        "opt_thumbnails": "Thumbnail Cache (Image Icons)",
        "opt_windows_temp": "Windows Temp (C:\\Windows\\Temp)",
        "opt_log_files": "System Log Files",
    },
}

class CleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_lang = "pt"
        self.lang_keys = list(LANG_DATA.keys())
        
        # Configuração da Janela
        self.title("Windows Cleaner Pro")
        self.geometry("450x700")
        
        # --- ALTERAÇÃO 1: HABILITAR REDIMENSIONAMENTO ---
        self.resizable(True, True) 
        
        ctk.set_appearance_mode("Dark")
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

        # Frame principal (Onde o conteúdo está)
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10) 

        # Configura as colunas e linhas dentro do main_frame
        main_frame.grid_columnconfigure(0, weight=1) 
        # Linha 6 (campo de resultados) deve receber todo o espaço vertical extra
        main_frame.grid_rowconfigure(6, weight=1) 
        
        row_counter = 0

        # Título Principal
        self.lbl_title = ctk.CTkLabel(main_frame, text="Windows Cleaner Pro", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_title.grid(row=row_counter, column=0, pady=20)
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

        # Frame das Opções de Limpeza
        self.options_frame = ctk.CTkFrame(main_frame)
        self.options_frame.grid(row=row_counter, column=0, sticky="ew", pady=10)
        
        self.lbl_options_title = ctk.CTkLabel(self.options_frame, text="Opções de Limpeza", font=ctk.CTkFont(weight="bold"))
        self.lbl_options_title.pack(pady=(10, 5))

        self.checkbox_configs = [
            "opt_temp_files", "opt_user_temp", "opt_prefetch", "opt_dns_cache",
            "opt_recycle_bin", "opt_thumbnails", "opt_windows_temp", "opt_log_files"
        ]
        
        self.select_all_var = ctk.BooleanVar(value=True)
        self.cb_select_all = ctk.CTkCheckBox(self.options_frame, text="Selecionar Tudo", 
                                            variable=self.select_all_var, command=self._toggle_select_all)
        self.cb_select_all.pack(anchor="w", padx=20, pady=(10, 5))
        
        # Frame para as Checkboxes (duas colunas)
        cb_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        cb_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        # Configuração para evitar texto cortado
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

        # Botão de Limpeza
        self.btn_cleanup = ctk.CTkButton(main_frame, text="Executar Limpeza", command=self._execute_cleanup)
        self.btn_cleanup.grid(row=row_counter, column=0, sticky="ew", pady=20)
        row_counter += 1
        
        # Rótulo de Status
        self.lbl_status = ctk.CTkLabel(main_frame, text="Pronto para limpar", text_color="yellow")
        self.lbl_status.grid(row=row_counter, column=0, pady=(5, 10))
        row_counter += 1

        # Resultados (TextBox)
        self.lbl_results_title = ctk.CTkLabel(main_frame, text="Resultados:", font=ctk.CTkFont(weight="bold"))
        self.lbl_results_title.grid(row=row_counter, column=0, sticky="w", pady=(5, 5))
        row_counter += 1
        
        # --- CAMPO DE TEXTO QUE SE EXPANDE ---
        self.txt_results = ctk.CTkTextbox(main_frame) 
        self.txt_results.grid(row=row_counter, column=0, sticky="nsew") # nsew garante expansão
        # -------------------------------------
        
        self.txt_results.insert("end", "Inicie a limpeza...")
        self.txt_results.configure(state="disabled")

    # --- Funções de Tradução e Interação (Não alteradas) ---
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

    # --- 3. Lógica de Limpeza de Sistema (Aprimorada) ---
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


if __name__ == "__main__":
    try:
        app = CleanerApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror(
            "ERRO CRÍTICO DE INICIALIZAÇÃO", 
            f"O aplicativo não pôde ser iniciado.\n\nDetalhes do Erro:\n{e}"
        )