#include <stdio.h>

#define MAX_CARGO 31  // +1 para o caractere nulo

typedef struct {
    char nome[100];
    int idade;
    char sexo;
    char cpf[12];
    char data_nascimento[11]; // formato dd/mm/aaaa
    int codigo_setor;
    char cargo[MAX_CARGO];
    float salario;
} Funcionario;

int main() {
    Funcionario funcionario;

    printf("Digite o nome do funcionário: ");
    fgets(funcionario.nome, sizeof(funcionario.nome), stdin);
    // Remove o caractere de nova linha, se presente
    funcionario.nome[strcspn(funcionario.nome, "\n")] = '\0';

    printf("Digite a idade do funcionário: ");
    scanf("%d", &funcionario.idade);

    printf("Digite o sexo do funcionário (M/F): ");
    scanf(" %c", &funcionario.sexo);

    printf("Digite o CPF do funcionário (xxx.xxx.xxx-xx): ");
    scanf("%s", funcionario.cpf);

    printf("Digite a data de nascimento do funcionário (dd/mm/aaaa): ");
    scanf("%s", funcionario.data_nascimento);

    printf("Digite o código do setor (0-99): ");
    scanf("%d", &funcionario.codigo_setor);

    printf("Digite o cargo do funcionário: ");
    scanf(" %30[^\n]", funcionario.cargo); // Limita a leitura a 30 caracteres

    printf("Digite o salário do funcionário: ");
    scanf("%f", &funcionario.salario);

    printf("\nDados do Funcionário:\n");
    printf("Nome: %s\n", funcionario.nome);
    printf("Idade: %d\n", funcionario.idade);
    printf("Sexo: %c\n", funcionario.sexo);
    printf("CPF: %s\n", funcionario.cpf);
    printf("Data de Nascimento: %s\n", funcionario.data_nascimento);
    printf("Código do Setor: %d\n", funcionario.codigo_setor);
    printf("Cargo: %s\n", funcionario.cargo);
    printf("Salário: %.2f\n", funcionario.salario);

    return 0;
}