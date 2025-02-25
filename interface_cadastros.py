import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

frame = None  # Variável global para armazenar o frame capturado

def exibir_camera():
    global cap, camera_window, camera_label

    # Cria uma nova janela para exibir a câmera
    camera_window = tk.Toplevel(root)
    camera_window.title("Câmera")
    camera_window.geometry("640x520")
    camera_window.configure(bg="#f0f0f0")

    # Centraliza a janela da câmera
    centralizar_janela(camera_window)

    # Inicia a captura de vídeo
    cap = cv2.VideoCapture(0)

    # Cria um frame para organizar os elementos
    frame_video = tk.Frame(camera_window, bg="#f0f0f0")
    frame_video.pack()

    # Cria um rótulo para exibir o vídeo
    camera_label = tk.Label(frame_video)
    camera_label.pack()

    # Botão para capturar a foto
    btn_capturar = tk.Button(camera_window, text="Capturar Foto", font=btn_font, bg="#4CAF50", fg="white", command=capturar_foto)
    btn_capturar.pack(pady=10, ipadx=10)

    # Atualiza o vídeo na janela
    atualizar_video()

def atualizar_video():
    global cap, camera_label

    ret, frame = cap.read()
    if ret:
        # Converte o frame para RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    camera_label.after(10, atualizar_video)

def capturar_foto():
    global cap, frame

    ret, frame = cap.read()
    if ret:
        messagebox.showinfo("Sucesso", "Foto capturada com sucesso!")
    else:
        messagebox.showerror("Erro", "Não foi possível capturar a foto.")
    cap.release()
    camera_window.destroy()

def visualizar_foto():
    if frame is None:
        messagebox.showerror("Erro", "Nenhuma foto capturada.")
        return

    # Cria uma nova janela para exibir a foto
    foto_window = tk.Toplevel(root)
    foto_window.title("Foto Capturada")
    foto_window.geometry("640x480")
    foto_window.configure(bg="#f0f0f0")

    # Centraliza a janela da foto
    centralizar_janela(foto_window)

    # Converte o frame para RGB e exibe a foto
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    foto_label = tk.Label(foto_window, image=imgtk)
    foto_label.imgtk = imgtk
    foto_label.pack()

def salvar_dados():
    global frame

    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    ie_sexo = entry_rg.get()
    whatsapp = entry_rg.get()
    email = entry_rg.get()
    nm_mae = entry_rg.get()
    whatsapp_mae = entry_rg.get()
    nm_pai = entry_rg.get()
    whatsapp_pai = entry_rg.get()
    cd_pis = entry_rg.get()
    cd_ctps = entry_rg.get()
    cd_eleitor = entry_rg.get()
    cadastro_pessoa_fisica = entry_rg.get()
    registro_geral = entry_rg.get()
    ie_qualificacao = entry_rg.get()
    matrix_face = entry_rg.get()
    matrix_digital = entry_rg.get()
    matrix_retina = entry_rg.get()
    matrix_senha = entry_rg.get()
    data_cadastro_original = entry_rg.get()
    data_contratacao = entry_rg.get()
    data_ult_alteracao = None
    nr_seq_prof_ult_alter = None
    nr_seq_prof_cadastro = None
    nr_seq_prof_contratacao = None


    if frame is None:
        messagebox.showerror("Erro", "Nenhuma foto capturada.")
        return

    # Salva a foto com o nome do CPF
    cv2.imwrite(f"./static/im_nao_registradas/{cadastro_pessoa_fisica}.jpg", frame)

    # Salva os dados em um arquivo com o nome do CPF
    with open(f"./static/im_nao_registradas/{cadastro_pessoa_fisica}.txt", "w") as file:
        json_modelo = [{"nm_pessoa_fisica": nome,
                        "data_nascimento":data_nascimento,
                        "ie_sexo": ie_sexo,
                        "whatsapp":whatsapp,
                        "email":email,
                        "nm_mae":nm_mae,
                        "whatsapp_mae":whatsapp_mae,
                        "nm_pai":nm_pai,
                        "whatsapp_pai":whatsapp_pai,
                        "cd_pis":cd_pis,
                        "cd_ctps":cd_ctps,
                        "cd_eleitor":cd_eleitor,
                        "cadastro_pessoa_fisica":cadastro_pessoa_fisica,
                        "registro_geral":registro_geral,
                        "ie_qualificacao":ie_qualificacao,
                        "matrix_face":matrix_face,
                        "matrix_digital":matrix_digital,
                        "matrix_retina":matrix_retina,
                        "matrix_senha":matrix_senha,
                        "data_cadastro_original":data_cadastro_original,
                        "data_contratacao":data_contratacao,
                        "data_ult_alteracao":data_ult_alteracao,
                        "nr_seq_prof_ult_alter":nr_seq_prof_ult_alter,
                        "nr_seq_prof_cadastro":nr_seq_prof_cadastro,
                        "nr_seq_prof_contratacao":nr_seq_prof_contratacao
                        }]
        json_modelo = str(json_modelo)
        file.write(json_modelo)

    messagebox.showinfo("Dados Salvos", f"Dados e foto salvos com sucesso!\nNome do arquivo: {cadastro_pessoa_fisica}.txt")

def centralizar_janela(janela):
    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f'{largura}x{altura}+{x}+{y}')

# Cria a janela principal
root = tk.Tk()
root.title("Registro de Dados e Foto")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

# Centraliza a janela
centralizar_janela(root)

# Estilos
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)
btn_font = ("Helvetica", 12, "bold")

# Cria os campos de entrada
tk.Label(root, text="Nome:", font=label_font, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_nome = tk.Entry(root, font=entry_font)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Data de Nascimento:", font=label_font, bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_data_nascimento = tk.Entry(root, font=entry_font)
entry_data_nascimento.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="CPF:", font=label_font, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_cpf = tk.Entry(root, font=entry_font)
entry_cpf.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="RG:", font=label_font, bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_rg = tk.Entry(root, font=entry_font)
entry_rg.grid(row=3, column=1, padx=10, pady=10)

# Botão para exibir a câmera
btn_foto = tk.Button(root, text="Registrar Foto", font=btn_font, bg="#4CAF50", fg="white", command=exibir_camera)
btn_foto.grid(row=4, column=0, columnspan=2, pady=10, ipadx=10)

# Botão para tirar nova foto
btn_nova_foto = tk.Button(root, text="Tirar Nova Foto", font=btn_font, bg="#FF5722", fg="white", command=exibir_camera)
btn_nova_foto.grid(row=5, column=0, columnspan=2, pady=10, ipadx=10)

# Botão para visualizar a foto
btn_visualizar = tk.Button(root, text="Visualizar Foto", font=btn_font, bg="#FFC107", fg="white", command=visualizar_foto)
btn_visualizar.grid(row=6, column=0, columnspan=2, pady=10, ipadx=10)

# Botão para salvar os dados
btn_salvar = tk.Button(root, text="Salvar Dados", font=btn_font, bg="#2196F3", fg="white", command=salvar_dados)
btn_salvar.grid(row=7, column=0, columnspan=2, pady=10, ipadx=10)

# Inicia o loop principal da interface
root.mainloop()
