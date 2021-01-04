import numpy as np
from scipy.special import expit


class NeuralNet:
    def __init__(self, input_qty, hidden_dts, output_qty):
        """
        input_qty : Quantidade de entradas que a rede vai receber.
        hidden_dts : Uma tuple contedo os detalhes das camadas escondidas.
                        Primeiro valor quantidade de camadas escondidas.
                        Segundo valor quantidade de 'neurônios' em cada camada.
        saida : Quantidade de saidas da rede.
        """
        self.input_qty = input_qty
        self.hidden_dts = hidden_dts
        self.output_qty = output_qty

    def fitting(self, inputs, weights):
        inputs = np.asarray(inputs)
        bias = -1
        ini = 0

        # INPUT LAYER
        end = self.input_qty * self.hidden_dts[1]
        newshape = (self.input_qty, self.hidden_dts[1])
        new_input = self.neuron(weights[ini:end], inputs, newshape, bias)
        ini = end

        # HIDDENS LAYER
        for _ in range(self.hidden_dts[0] - 1):
            end = self.hidden_dts[1] ** self.hidden_dts[0] + ini
            newshape = (self.hidden_dts[1], self.hidden_dts[1])
            new_input = self.neuron(weights[ini:end], new_input, newshape, bias)
            ini = end

        # OUTPUT LAYER
        end = self.hidden_dts[1] * self.output_qty + ini
        newshape = (self.hidden_dts[1], self.output_qty)
        output = self.neuron(weights[ini:end], new_input, newshape, bias, out=True)

        return output

    def neuron(self, weights, matrix_a, newshape, bias, out=False):
        matrix_weights = np.reshape(weights, newshape)
        output = np.dot(matrix_a, matrix_weights) + bias
        if out:
            output = expit(output)
        else:
            output = np.maximum(output, 0)
        return output

    def generate_weights(self):
        input_qty = self.input_qty * self.hidden_dts[1]
        hidden_qty = self.hidden_dts[1] ** self.hidden_dts[0]
        output_qty = self.hidden_dts[1] * self.output_qty
        total = input_qty + hidden_qty + output_qty
        weights = np.random.uniform(-1, 1, total)
        return weights
