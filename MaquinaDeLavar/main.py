from maquina_de_lavar import MaquinaDeLavar

if __name__ == "__main__":
    maquina = MaquinaDeLavar()
    
    nivel_sujeira = float(input("Informe o nível de sujeira (0 a 100): "))
    peso_roupa = float(input("Informe o peso da roupa (0 a 10 kg): "))
    
    maquina.input_valores(nivel_sujeira, peso_roupa)
    maquina.calcular_tempo()
    maquina.mostrar_tempo()
    maquina.mostrar_graficos()
