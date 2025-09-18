import tkinter as tk
from tkinter import messagebox
import requests
from pythonosc import udp_client

HOLYRICS_API = "http://localhost:8091/api/v1"  # Porta padrão do Holyrics
RESOLUME_IP = "127.0.0.1"
RESOLUME_PORT = 7000

osc_client = udp_client.SimpleUDPClient(RESOLUME_IP, RESOLUME_PORT)

def mostrar_versiculo(ref):
    """Mostra um versiculo no Holyrics usando a API"""
    try:
        r = requests.get(f"{HOLYRICS_API}/bible/show", params={"ref": ref})
        if r.status_code == 200:
            messagebox.showinfo("Holyrics", f"Versículo {ref} enviado!")
        else:
            messagebox.showerror("Erro Holyrics", f"Falha: {r.text}")
    except Exception as e:
        messagebox.showerror("Erro Holyrics", str(e))

def trocar_fundo(layer, clip):
    """Troca o fundo no Resolume via OSC"""
    try:
        osc_client.send_message(f"/layer{layer}/clip{clip}/connect", 1)
        messagebox.showinfo("Resolume", f"Clip {clip} ativado no layer {layer}")
    except Exception as e:
        messagebox.showerror("Erro Resolume", str(e))

def acao_cena():
    """Exemplo de preset: João 3:16 + Fundo Clip 2 Layer 1"""
    mostrar_versiculo("John3:16")
    trocar_fundo(1, 2)

# === INTERFACE GRÁFICA ===
root = tk.Tk()
root.title("Controle projecao")

tk.Label(root, text="Controle Holyrics & Resolume", font=("Arial", 16, "bold")).pack(pady=10)

# Botão para mostrar versículo específico
btn_verso = tk.Button(root, text="Mostrar João 3:16", font=("Arial", 14),
                      command=lambda: mostrar_versiculo("John3:16"))
btn_verso.pack(pady=5, fill="x", padx=20)

# Botão para trocar fundo no Resolume
btn_fundo = tk.Button(root, text="Trocar para Fundo Clip 2 Layer 1", font=("Arial", 14),
                      command=lambda: trocar_fundo(1, 2))
btn_fundo.pack(pady=5, fill="x", padx=20)

# Botão para acionar os dois ao mesmo tempo
btn_cena = tk.Button(root, text="Cena Completa (Verso + Fundo)", font=("Arial", 14, "bold"),
                     bg="#4CAF50", fg="white", command=acao_cena)
btn_cena.pack(pady=10, fill="x", padx=20)

root.mainloop()
