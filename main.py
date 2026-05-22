import sys
import os
from clima_api import buscar_clima
from gerenciador_arquivos import salvar_historico, registrar_erro, carregar_historico
from n8n_integration import enviar_para_ia_n8n

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print("\n" + "="*40)
    print("      ASSISTENTE DE CLIMA INTELIGENTE")
    print("="*40)
    print("1. Consultar Clima de uma Cidade")
    print("2. Ver Histórico de Consultas")
    print("3. Sair")
    print("="*40)

def main():
    """
    Função principal que coordena o fluxo do programa.
    Requisito: Entrada de dados, Loops, Condicionais e Funções.
    """
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cidade = input("\nDigite o nome da cidade: ").strip()
            
            # Validação simples de entrada
            if not cidade:
                print("Erro: O nome da cidade não pode estar vazio.")
                continue

            print(f"\nBuscando informações para {cidade}...")
            dados = buscar_clima(cidade)

            if dados:
                # Passo 2: Enviar para n8n/IA
                print("Consultando Inteligência Artificial...")
                recomendacao = enviar_para_ia_n8n(dados)
                
                # Exibir resultados
                print("\n" + "-"*30)
                print(f"CIDADE: {dados['cidade']}")
                print(f"TEMPERATURA: {dados['temperatura']}°C")
                print(f"CONDIÇÃO: {dados['descricao'].capitalize()}")
                print(f"UMIDADE: {dados['umidade']}%")
                print("-"*30)
                print(f"{recomendacao}")
                print("-"*30)

                # Passo 3: Salvar no histórico
                dados["recomendacao_ia"] = recomendacao
                salvar_historico(dados)
            else:
                registrar_erro(f"Falha na consulta da cidade: {cidade}")

        elif opcao == "2":
            historico = carregar_historico()
            if not historico:
                print("\nNenhuma consulta encontrada no histórico.")
            else:
                print("\n--- ÚLTIMAS CONSULTAS ---")
                # Requisito: Estrutura de repetição (for)
                for item in historico[-5:]: # Mostra as últimas 5
                    print(f"[{item['data_hora']}] {item['cidade']}: {item['temperatura']}°C - {item['descricao']}")
        
        elif opcao == "3":
            print("\nObrigado por usar o Assistente de Clima! Até logo.")
            sys.exit()
        
        else:
            print("\nOpção inválida. Tente novamente.")

        input("\nPressione Enter para continuar...")
        limpar_terminal()

if __name__ == "__main__":
    main()
