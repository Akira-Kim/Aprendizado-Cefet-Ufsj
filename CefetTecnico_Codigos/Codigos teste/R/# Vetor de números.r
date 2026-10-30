# Vetor de números
numeros <- c(5, 10, 15, 20, 25)

# Função para calcular a média
calcular_media <- function(vetor) {
  soma <- sum(vetor)
  media <- soma / length(vetor)
  return(media)
}

# Chamando a função para calcular a média do vetor
media_resultado <- calcular_media(numeros)

# Imprimindo o resultado
print(media_resultado)