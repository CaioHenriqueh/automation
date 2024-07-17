import tkinter as tk
import time
import threading
import pyautogui

id_zoom = "933 490 2569"
pass_zoom = "085076"

class Cronometro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronômetro")
        self.root.geometry("400x200")  # Define o tamanho da janela
        self.root.attributes("-topmost", True)  # Mantém a janela sempre no topo
        
        self.tempo_total = 240  # Tempo total em segundos (4 minutos)
        self.tempo_inicio = 60  # Tempo de início da automação em segundos (1 minuto)
        self.tempo_restante_inicio = self.tempo_inicio  # Tempo restante para início
        self.tempo_restante_automacao = self.tempo_total  # Tempo restante para a automação
        self.automacao_ativa = False  # Flag para verificar se a automação está ativa
        self.processo_automacao = None  # Referência ao processo de automação

        self.label_inicio = tk.Label(root, text="Automação começa em:", font=("Helvetica", 12))
        self.label_inicio.pack(pady=5)
        
        self.display_inicio = tk.Label(root, text=self.format_time(self.tempo_restante_inicio), font=("Helvetica", 24))
        self.display_inicio.pack(pady=5)
        
        self.label_termino = tk.Label(root, text="", font=("Helvetica", 12))
        self.label_termino.pack(pady=5)
        
        self.display_termino = tk.Label(root, text="", font=("Helvetica", 24))
        self.display_termino.pack(pady=5)
        
        self.start_countdown()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer_inicio(self):
        if self.tempo_restante_inicio > 0 and not self.automacao_ativa:
            self.display_inicio.config(text=self.format_time(self.tempo_restante_inicio))
            self.tempo_restante_inicio -= 1
            self.root.after(1000, self.update_timer_inicio)

    def update_timer_automacao(self):
        if self.tempo_restante_automacao > 0 and self.automacao_ativa:
            self.display_termino.config(text=self.format_time(self.tempo_restante_automacao))
            self.tempo_restante_automacao -= 1
            self.root.after(1000, self.update_timer_automacao)
        elif self.automacao_ativa:
            self.stop_automation()

    def start_countdown(self):
        self.update_timer_inicio()
        if self.tempo_restante_inicio == 0:
            self.start_automation()

    def start_automation(self):
        self.automacao_ativa = True
        self.label_inicio.config(text="Automação termina em:")
        self.label_termino.config(text=self.format_time(self.tempo_total))
        self.update_timer_automacao()
        self.processo_automacao = threading.Thread(target=self.automation_process)
        self.processo_automacao.start()

    def stop_automation(self):
        self.automacao_ativa = False
        if self.processo_automacao and self.processo_automacao.is_alive():
            self.processo_automacao.join()  # Aguarda o término do processo de automação
        self.root.destroy()  # Fecha a janela quando a automação é concluída ou interrompida

    def automation_process(self):
        try:
            # Simulação de inicialização da automação
            time.sleep(self.tempo_inicio)
            
            pyautogui.press("win")
            time.sleep(1)

            pyautogui.write("zoom", interval=0.3)
            time.sleep(1)

            pyautogui.press("enter")
            time.sleep(2)

            pyautogui.hotkey('win', 'up')
            time.sleep(2)

            img = pyautogui.locateCenterOnScreen('Capturar.png', confidence=0.7)
            time.sleep(2)

            if img:
                pyautogui.click(img.x, img.y)
                time.sleep(2)

                pyautogui.write(id_zoom, interval=0.2)
                pyautogui.press("enter")
                time.sleep(1)

                pyautogui.write(pass_zoom, interval=0.2)
                pyautogui.press("enter")
                
                # Verifica se você foi admitido na sala
                admitted = False
                while not admitted and self.tempo_restante_automacao > 0 and self.automacao_ativa:
                    img_admitted = pyautogui.locateCenterOnScreen('admitted.png', confidence=0.7)
                    if img_admitted:
                        admitted = True
                        pyautogui.hotkey('win', 'up')  # Maximiza a tela
                    else:
                        time.sleep(5)  # Espera 5 segundos antes de verificar novamente

        except Exception as e:
            print(f"Erro na automação: {e}")
        finally:
            self.stop_automation()

if __name__ == "__main__":
    root = tk.Tk()
    cronometro = Cronometro(root)
    root.mainloop()
