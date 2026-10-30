#include <stdio.h>

#define MAX_NOME 100
#define MAX_CARGO 31
#define MAX_CPF 12

typedef struct {
    char nome[MAX_NOME];
    int idade;
    char sexo;
    char cpf[MAX_CPF];
    char data_nascimento[11];
    int codigo_setor;
    char cargo[MAX_CARGO];
    float salario;
} Funcionario;

int main() {
    Funcionario funcionario;

    printf("Digite o nome do funcionário: ");
    fgets(funcionario.nome, sizeof(funcionario.nome), stdin);
    funcionario.nome[strcspn(funcionario.nome, "\n")] = '\0';

    printf("Digite a idade do funcionário: ");
    scanf("%d", &funcionario.idade);
    getchar();

    printf("Digite o sexo do funcionário (M/F): ");
    scanf("%c", &funcionario.sexo);
    getchar();

    printf("Digite o CPF do funcionário (apenas números): ");
    fgets(funcionario.cpf, sizeof(funcionario.cpf), stdin);
    funcionario.cpf[strcspn(funcionario.cpf, "\n")] = '\0';

    printf("Digite a data de nascimento do funcionário (DD/MM/AAAA): ");
    fgets(funcionario.data_nascimento, sizeof(funcionario.data_nascimento), stdin);
    funcionario.data_nascimento[strcspn(funcionario.data_nascimento, "\n")] = '\0';

    printf("Digite o código do setor onde o funcionário trabalha (0-99): ");
    scanf("%d", &funcionario.codigo_setor);
    getchar();

    printf("Digite o cargo do funcionário (até 30 caracteres): ");
    fgets(funcionario.cargo, sizeof(funcionario.cargo), stdin);
    funcionario.cargo[strcspn(funcionario.cargo, "\n")] = '\0';

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