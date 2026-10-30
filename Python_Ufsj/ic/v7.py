import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry

# Listas para armazenar os dados
angles = []
positions = []

# Função para adicionar um ponto ao gráfico
def add_point():
    try:
        angle = float(angle_entry.get())
        position = float(position_entry.get())
        
        if 0 <= angle <= 180 and 0 <= position <= 100:
            angles.append(angle)
            positions.append(position)
            
            # Atualiza os dados no gráfico
            line.set_xdata(angles)
            line.set_ydata(positions)
            plt.draw()  # Redesenha o gráfico
            plt.pause(0.1)  # Pausa para atualizar o gráfico
        else:
            print("Por favor, insira valores válidos entre 0-180 para ângulo e 0-100 para posição.")
    except ValueError:
        print("Entrada inválida. Por favor, insira números válidos.")

# Função para criar a janela do Tkinter
def create_gui():
    root = Tk()
    root.title("Entrada de Dados para o Gráfico")
    
    # Rótulos e campos de entrada
    Label(root, text="Ângulo de Saída (0 a 180 graus):").pack()
    global angle_entry
    angle_entry = Entry(root)
    angle_entry.pack()
    
    Label(root, text="Posição no Perímetro (0 a 100):").pack()
    global position_entry
    position_entry = Entry(root)
    position_entry.pack()
    
    # Botão para adicionar ponto ao gráfico
    add_button = Button(root, text="Adicionar Ponto", command=add_point)
    add_button.pack()
    
    # Inicia a interface gráfica
    root.mainloop()

# Configuração inicial do gráfico
plt.ion()  # Modo interativo para atualizar o gráfico em tempo real
fig, ax = plt.subplots()
ax.set_xlim(0, 180)  # Eixo X de 0 a 180 graus
ax.set_ylim(0, 100)  # Eixo Y de 0 a 100
ax.set_xlabel('Ângulo de Saída (°)')
ax.set_ylabel('Posição no Perímetro (0-100)')

# Plotando um gráfico inicial vazio
line, = ax.plot([], [], 'bo')  # 'bo' significa pontos azuis

# Chama a função para criar a interface gráfica
create_gui()

# Finaliza o gráfico interativo
plt.ioff()  # Desliga o modo interativo
plt.show()  # Exibe o gráfico final

# implementar isso e implementar a colisao simpletica

# Geometria Diferencial - Keti Tenenblat