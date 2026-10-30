```markdown
# Simulador Interativo de Bilhares Simpléticos

Simulador em Python para bilhares **elásticos** e **simpléticos**, com visualização em tempo real no espaço de configuração e no espaço de fase (mapa de calor).

Versão do artigo: fronteiras **Círculo** e **Elipse** (suaves).  
No modo Simplético **não** há fallback para reflexão elástica.

Referência: Albers & Tabachnikov, *Introducing symplectic billiards* (2018).

---

## Como rodar o projeto

### 1. Requisitos

- Python 3.9 ou superior
- `numpy`
- `matplotlib`

### 2. Instalação

```bash
# (opcional) ambiente virtual
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# dependências
pip install numpy matplotlib
```

Ou, se houver `requirements.txt` na pasta:

```bash
pip install -r requirements.txt
```

### 3. Executar

Na pasta do arquivo do simulador:

```bash
python simulador_bilhares.py
```

(Substitua pelo nome real do arquivo, se for outro.)

Deve abrir uma janela com:

- **esquerda:** espaço de configuração (mesa + trajetória)
- **direita:** espaço de fase + mapa de calor
- **embaixo:** controles

### 4. Uso rápido da interface

1. Escolha a fronteira (**Círculo** ou **Elipse**).
2. Ajuste `a` e `b` (na elipse).
3. Escolha o modo de colisão (**Elástico** ou **Simplético**).
4. Ajuste `t`, ângulo e velocidade da condição inicial.
5. Use um dos modos de execução:
   - **Iniciar** — animação contínua
   - **Passo a passo** — avança 1 colisão e pausa
   - **Prever N** — desenha N ricochetes futuros (verde) sem alterar o estado
6. **Limpar prev.** apaga só a previsão verde.
7. **Reset** volta à condição inicial.

Recomendação: comece com velocidade baixa e poucas colisões no modo Simplético para ver a linha auxiliar ciano (construção geométrica).

### 5. Problemas comuns

| Problema | O que tentar |
|----------|----------------|
| `ModuleNotFoundError: numpy/matplotlib` | `pip install numpy matplotlib` |
| Janela não abre | rode no terminal (não só no editor) |
| Slider não muda a bolinha | só vale **antes** do primeiro Iniciar; use Reset |
| Prever N não desenha | confira se N é inteiro (ex.: 10) |

---

## O que o programa faz

- Simula uma partícula em linha reta dentro de uma mesa (círculo ou elipse).
- Em cada colisão aplica:
  - **Elástico:** ângulo de incidência = ângulo de reflexão;
  - **Simplético:** construção de Albers–Tabachnikov (sem trocar para elástico se a construção falhar).
- Mostra:
  - trajetória na mesa;
  - linha auxiliar da construção simplética (ciano);
  - previsão de N ricochetes (verde);
  - espaço de fase e mapa de calor das colisões.

---

## Documentação das funções

### Geometria — `CurvaParametrica`

| Função | O que faz | Quando usa |
|--------|-----------|------------|
| `__init__` | Inicializa no círculo unitário | Criação do estado / reset |
| `__call__(t)` | Devolve `[t, x(t), y(t)]` | Sempre que precisa de um ponto da fronteira |
| `circulo(t)` / `elipse(t)` | Parametrizações da fronteira | Conforme a curva escolhida |
| `intersect_line(point, direction)` | Interseção reta–curva (lista de λ) | Próxima colisão e construção do a₃ |
| `get_tangente(t)` | Tangente unitária T(t) | Condição inicial, simplético, cos θ |
| `get_normal(t)` | Normal unitária para **dentro** | Elástico e validação no simplético |
| `get_t_from_pos(pos)` | Recupera t ∈ [0, 2π) | Após obter o ponto de impacto |

### Estado — `EstadoBilhar`

| Função | O que faz | Quando usa |
|--------|-----------|------------|
| `__init__` | Condição inicial padrão | Arranque do programa |
| `reset` | Limpa trajetória, colisões, heatmap e previsão | Clique em Reset |

### Física

| Função | O que faz | Quando usa |
|--------|-----------|------------|
| `refletir_vetor(v, n)` | Reflexão elástica clássica | **Só** modo Elástico |
| `colisao_simpletica_robusta(...)` | Colisão simplética sem fallback elástico | Cada colisão no modo Simplético |
| `aplicar_colisao(...)` | Escolhe elástico ou simplético | Animação, passo a passo e previsão |
| `simular_uma_colisao(...)` | Avança até a próxima colisão (sem desenhar) | Base do passo a passo e da previsão |
| `prever_trajetoria(...)` | Simula N colisões à frente sem mudar o estado | Clique em Prever N |

**Estratégia do simplético**

1. Interseção analítica da reta por \(a_1\) com direção \(T(a_2)\).  
2. Se falhar, raiz de \(f(s)=\langle r(s)-a_1,\,N(a_2)\rangle=0\).  
3. Se ainda falhar, **mantém a velocidade** (não troca para elástico).

### Interface (callbacks)

| Função | O que faz | Quando usa |
|--------|-----------|------------|
| `preparar_simulacao` | Desenho inicial + heatmap | Arranque |
| `atualizar_curva_e_bolinha` | Redesenha mesa e condição inicial | Controles antes de iniciar / Reset |
| `on_curva` / `on_modo` / `on_parametros` | Fronteira, modo, a e b | Radios e caixas de texto |
| `on_t` / `on_angulo` / `on_vel` | Condição inicial e velocidade da animação | Sliders |
| `on_start` | Inicia ou pausa a animação contínua | Botão Iniciar |
| `on_step` | Avança 1 colisão e pausa | Botão Passo a passo |
| `on_prever` | Desenha N ricochetes futuros (verde) | Botão Prever N |
| `on_limpar_prev` | Apaga a previsão verde | Botão Limpar prev. |
| `on_reset` | Reinicia tudo | Botão Reset |
| `on_info` | Texto de ajuda | Botão Info |
| `_atualizar_heatmap` | Atualiza o mapa de calor | Após novas colisões |
| `iniciar_animacao` | Cria o `FuncAnimation` | Iniciar / Continuar |
| `init` | Init exigido pelo Matplotlib | Criação da animação |
| `update` | Núcleo da animação contínua | Cada frame (não pausado) |

---

## Resumo: qual função usar para quê

| Objetivo | Função |
|----------|--------|
| Ponto / tangente / normal da mesa | `CurvaParametrica.*` |
| Próxima colisão (só cálculo) | `simular_uma_colisao` |
| Lei elástica | `refletir_vetor` via `aplicar_colisao` |
| Lei simplética | `colisao_simpletica_robusta` via `aplicar_colisao` |
| 1 colisão na tela | `on_step` |
| N ricochetes futuros na tela | `on_prever` → `prever_trajetoria` |
| Animação contínua | `update` |
| Redesenhar condição inicial | `atualizar_curva_e_bolinha` |

---

## Limitação importante

Esta versão implementa apenas **Círculo** e **Elipse** (fronteiras suaves).  
Em fronteiras com cantos (estádio, polígono), a tangente deixa de estar bem definida e a colisão simplética exige tratamento próprio — isso fica como extensão futura e **não** é resolvido trocando silenciosamente para o modo elástico.

---

