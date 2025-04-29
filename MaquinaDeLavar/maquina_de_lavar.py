import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class MaquinaDeLavar:
    def __init__(self):
        self._criar_variaveis()
        self._criar_regras()
        self.simulador = ctrl.ControlSystemSimulation(self.tempo_ctrl)

    def _criar_variaveis(self):
        # Definindo os universos fuzzy
        self.sujeira = ctrl.Antecedent(np.arange(0, 101, 1), 'sujeira')
        self.peso = ctrl.Antecedent(np.arange(0, 11, 1), 'peso')
        self.tempo = ctrl.Consequent(np.arange(0, 61, 1), 'tempo')

        # Funções de pertinência
        self.sujeira['baixo'] = fuzz.trimf(self.sujeira.universe, [0, 0, 40])
        self.sujeira['medio'] = fuzz.trimf(self.sujeira.universe, [30, 50, 70])
        self.sujeira['alto'] = fuzz.trimf(self.sujeira.universe, [60, 100, 100])

        self.peso['leve'] = fuzz.trimf(self.peso.universe, [0, 0, 4])
        self.peso['medio'] = fuzz.trimf(self.peso.universe, [3, 5, 7])
        self.peso['pesado'] = fuzz.trimf(self.peso.universe, [6, 10, 10])

        self.tempo['curto'] = fuzz.trimf(self.tempo.universe, [0, 0, 20])
        self.tempo['medio'] = fuzz.trimf(self.tempo.universe, [15, 30, 45])
        self.tempo['longo'] = fuzz.trimf(self.tempo.universe, [40, 60, 60])

    def _criar_regras(self):
        # Definindo as regras fuzzy
        regra1 = ctrl.Rule(self.sujeira['baixo'] & self.peso['leve'], self.tempo['curto'])
        regra2 = ctrl.Rule(self.sujeira['baixo'] & self.peso['pesado'], self.tempo['curto'])
        regra3 = ctrl.Rule(self.sujeira['medio'] & self.peso['medio'], self.tempo['medio'])
        regra4 = ctrl.Rule(self.sujeira['alto'] & self.peso['leve'], self.tempo['medio'])
        regra5 = ctrl.Rule(self.sujeira['alto'] & self.peso['pesado'], self.tempo['longo'])
        regra6 = ctrl.Rule(self.sujeira['medio'] & self.peso['pesado'], self.tempo['longo'])
        regra7 = ctrl.Rule(self.sujeira['medio'] & self.peso['leve'], self.tempo['curto'])

        self.tempo_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7])

    def input_valores(self, nivel_sujeira, peso_roupa):
        self.simulador.input['sujeira'] = nivel_sujeira
        self.simulador.input['peso'] = peso_roupa
        self.nivel_sujeira = nivel_sujeira
        self.peso_roupa = peso_roupa

    def calcular_tempo(self):
        self.simulador.compute()

    def mostrar_tempo(self):
        tempo_calculado = self.simulador.output['tempo']
        print(f"Tempo de lavagem sugerido: {tempo_calculado:.2f} minutos")
        return tempo_calculado

    def mostrar_graficos(self):
        # Gráficos personalizados
        fig, axes = plt.subplots(3, 1, figsize=(10, 15))

        # Sujeira
        axes[0].plot(self.sujeira.universe, self.sujeira['baixo'].mf, 'b', label='Baixo')
        axes[0].plot(self.sujeira.universe, self.sujeira['medio'].mf, 'g', label='Médio')
        axes[0].plot(self.sujeira.universe, self.sujeira['alto'].mf, 'r', label='Alto')
        axes[0].axvline(self.nivel_sujeira, color='k', linestyle='--', label=f'Entrada: {self.nivel_sujeira}')
        axes[0].set_title('Nível de Sujeira')
        axes[0].legend()

        # Peso
        axes[1].plot(self.peso.universe, self.peso['leve'].mf, 'b', label='Leve')
        axes[1].plot(self.peso.universe, self.peso['medio'].mf, 'g', label='Médio')
        axes[1].plot(self.peso.universe, self.peso['pesado'].mf, 'r', label='Pesado')
        axes[1].axvline(self.peso_roupa, color='k', linestyle='--', label=f'Entrada: {self.peso_roupa}')
        axes[1].set_title('Peso da Roupa')
        axes[1].legend()

        # Tempo
        tempo_saida = self.simulador.output['tempo']
        axes[2].plot(self.tempo.universe, self.tempo['curto'].mf, 'b', label='Curto')
        axes[2].plot(self.tempo.universe, self.tempo['medio'].mf, 'g', label='Médio')
        axes[2].plot(self.tempo.universe, self.tempo['longo'].mf, 'r', label='Longo')
        axes[2].axvline(tempo_saida, color='k', linestyle='--', label=f'Saída: {tempo_saida:.2f}')
        axes[2].set_title('Tempo de Lavagem')
        axes[2].legend()

        plt.tight_layout()
        plt.show()
