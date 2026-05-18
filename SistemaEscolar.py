import tkinter as tk

import sqlite3

import os

# existe só pra rodar em qlqr maquina
BASE_DIR = os.path.dirname(__file__)

CAMINHO_DB = os.path.join(BASE_DIR, "SQLite.db")

# puxa e le o sqlite e as turmas txt
def ValidarMatriculaBD(matricula):
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Matricula WHERE NumMatric = ?", (matricula,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None

def LerAturma(nome_arquivo):
    alunos = []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                nome, nota = linha.strip().split(",")
                alunos.append({"nome": nome, "nota": float(nota)})
        return alunos
    except FileNotFoundError:
        return None

# interface do tkinter
root = tk.Tk()
root.title("Sistema Escolar")
root.state("zoomed")
root.configure(bg="#d9d9d9")

canvas = tk.Canvas(root, bg="#d9d9d9", highlightthickness=0)
canvas.pack(fill="both", expand=True)

titulo = canvas.create_text(
    0, 80,
    text="ESCOLA DOHKO",
    font=("Arial Black", 40),
    fill="#7ED321"
)

lbl_professor = canvas.create_text(
    0, 100,
    text="PROFESSOR/ALUNO",
    font=("Arial", 20),
    fill="black"
)

lbl_matricula = canvas.create_text(
    0, 200,
    text="MATRICULA",
    font=("Arial", 20),
    fill="black"
)

lbl_turma = canvas.create_text(
    0, 300,
    text="TURMA",
    font=("Arial", 20),
    fill="black"
)

# input das turmas e matricula
def ValidarInputMatricula(P):
    return (P.isdigit() and len(P) <= 12) or P == ""

def ValidarInputTurma(P):
    return (P.isdigit() and len(P) <= 4) or P == ""

vcmd_matricula = root.register(ValidarInputMatricula)
vcmd_turma = root.register(ValidarInputTurma)

entry1 = tk.Entry(
    root,
    font=("Arial", 18),
    bd=0,
    justify="center",
    validate="key",
    validatecommand=(vcmd_matricula, "%P")
)

entry2 = tk.Entry(
    root,
    font=("Arial", 18),
    bd=0,
    justify="center",
    validate="key",
    validatecommand=(vcmd_turma, "%P")
)

box1 = canvas.create_rectangle(
    0, 0, 0, 0,
    outline="#555555",
    width=3
)

box2 = canvas.create_rectangle(
    0, 0, 0, 0,
    outline="#555555",
    width=3
)

resultado_label = tk.Label(
    root,
    text="",
    font=("Arial", 16),
    bg="#d9d9d9",
    justify="left"
)

def ListaTurma():
    matricula = entry1.get()
    turma = entry2.get()

    if not ValidarMatriculaBD(matricula):
        resultado_label.config(text="Essa matricula não existe")
        return

    caminho_txt = os.path.join(BASE_DIR, f"turma{turma}.txt")

    alunos = LerAturma(caminho_txt)

    if alunos is None:
        resultado_label.config(text="Essa turma não existe")
        return

    texto = "ALUNOS:\n\n"

    for aluno in alunos:
        texto += f"{aluno['nome']} - Nota: {aluno['nota']}\n"

    resultado_label.config(text=texto)

# botão mostrar notas
btn = tk.Button(
    root,
    text="IMPRIMIR NOTAS",
    font=("Arial", 20),
    bg="#2183D3",
    fg="black",
    bd=3,
    relief="solid",
    command=ListaTurma
)

# botão sair
btn_sair = tk.Button(
    root,
    text="SAIR",
    font=("Arial", 18),
    bg="#D9534F",
    fg="black",
    bd=3,
    relief="solid",
    command=root.destroy
)

def resize(event):
    w = event.width

    canvas.coords(titulo, w/2, 70)
    canvas.coords(lbl_professor, w/2, 135)
    canvas.coords(lbl_matricula, w/4, 200)
    canvas.coords(lbl_turma, w/4, 300)

    canvas.coords(box1, w/3, 180, w/1.5, 230)
    canvas.coords(box2, w/3, 280, w/1.5, 330)

    entry1.place(
        x=w/3+10,
        y=185,
        width=(w/1.5 - w/3 - 20),
        height=40
    )

    entry2.place(
        x=w/3+10,
        y=285,
        width=(w/1.5 - w/3 - 20),
        height=40
    )

    btn.place(
        x=w/2-125,
        y=400,
        width=250,
        height=70
    )

    btn_sair.place(
        x=w/2-75,
        y=490,
        width=150,
        height=50
    )

    resultado_label.place(x=w/3, y=560)

canvas.bind("<Configure>", resize)

root.mainloop()
