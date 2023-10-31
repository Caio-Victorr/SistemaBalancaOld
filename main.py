import decimal

class Produto:
    def __init__(self, codigo, tipo, descricao, preco_venda):
        self.codigo = codigo
        self.tipo = tipo
        self.descricao = descricao
        self.preco_venda = preco_venda

class FilizolaSmartExporter:
    def export(self, produtos, arquivo):
        with open(arquivo, 'w') as f:
            for produto in produtos:
                linha = f"{produto.codigo.zfill(6)}{produto.tipo}{produto.descricao.ljust(22)}" \
                        f"{int(produto.preco_venda * 100):07}\n"
                f.write(linha)

class ToledoMGV6Exporter:
    def export(self, produtos, arquivo):
        with open(arquivo, 'w') as f:
            for produto in produtos:
                linha = f"01{produto.tipo}{produto.codigo.zfill(6)}" \
                        f"{int(produto.preco_venda * 100):06}{produto.descricao.ljust(50)}" \
                        "0000000000000000000000|01|000000000000|0000|0||\n"
                f.write(linha)

class UranoIntegraExporter:
    def export(self, produtos, arquivo):
        with open(arquivo, 'w') as f:
            for produto in produtos:
                validade = "00000D"
                linha = f"{produto.codigo.zfill(6)}*{produto.tipo}{produto.descricao.ljust(20)}" \
                        f"{produto.preco_venda:.2f}".replace(".", "").zfill(9) + validade + "\n"
                f.write(linha)

class GerenciadorProdutos:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, codigo, tipo, descricao, preco_venda):
        produto = Produto(codigo, tipo, descricao, preco_venda)
        self.produtos.append(produto)

    def limpar_produtos(self):
        self.produtos = []

    def listar_produtos(self):
        for i, produto in enumerate(self.produtos):
            print(f"Produto {i + 1}:")
            print(f"Código: {produto.codigo}")
            print(f"Tipo: {produto.tipo}")
            print(f"Descrição: {produto.descricao}")
            print(f"Preço de Venda: {produto.preco_venda:.2f}")
            print()

def criar_produto():
    codigo = input("Digite o código do produto (6 dígitos): ")
    tipo = input("Digite o tipo do produto (P para peso, U para unidade): ")
    descricao = input("Digite a descrição do produto (até 22 caracteres): ")
    preco_venda = input("Digite o preço de venda do produto: ")

    if codigo.isdigit() and len(codigo) == 6 and (tipo.upper() == 'P' or tipo.upper() == 'U') and len(descricao) <= 22 and preco_venda.replace(".", "", 1).replace(",", "", 1).isdigit():
        return codigo, tipo, descricao, decimal.Decimal(preco_venda.replace(",", "."))
    else:
        print("Entrada inválida. Verifique os dados e tente novamente.")
        return None

def exportar_para_balanca(produtos, arquivo, exporter):
    exporter.export(produtos, arquivo)
    print(f"Exportação para {arquivo} concluída com sucesso.")

if __name__ == "__main__":
    gerenciador_produtos = GerenciadorProdutos()

    while True:
        print("\nMenu:")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Exportar para FilizolaSmart (CADTXT.TXT)")
        print("4. Exportar para ToledoMGV6 (ITENSMGV.TXT)")
        print("5. Exportar para UranoIntegra (PRODUTOS.TXT)")
        print("6. Limpar Lista de Produtos")
        print("7. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            produto = criar_produto()
            if produto is not None:
                codigo, tipo, descricao, preco_venda = produto
                gerenciador_produtos.adicionar_produto(codigo, tipo, descricao, preco_venda)
        elif escolha == "2":
            gerenciador_produtos.listar_produtos()
        elif escolha == "3":
            filizola_exporter = FilizolaSmartExporter()
            produtos = gerenciador_produtos.produtos
            exportar_para_balanca(produtos, "CADTXT.TXT", filizola_exporter)
        elif escolha == "4":
            toledo_exporter = ToledoMGV6Exporter()
            produtos = gerenciador_produtos.produtos
            exportar_para_balanca(produtos, "ITENSMGV.TXT", toledo_exporter)
        elif escolha == "5":
            urano_exporter = UranoIntegraExporter()
            produtos = gerenciador_produtos.produtos
            exportar_para_balanca(produtos, "PRODUTOS.TXT", urano_exporter)
        elif escolha == "6":
            gerenciador_produtos.limpar_produtos()
            print("Lista de produtos foi limpa.")
        elif escolha == "7":
            break
        else:
            print("Opção inválida. Escolha uma opção válida do menu.")
