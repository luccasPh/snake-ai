# SnakeAI

## Como roda na sua maquina
```sh
    # Clone o repositório
    $ git clone https://github.com/luccasPh/snake-ai.git && cd snake-ai

    # Instale o pipenv
    $ pip install pipenv

    # Instale as dependência
    $ pipenv install --skip-lock

    # Para roda o jogo
    $ pipenv run game
```


## Snake
### Rede neural
Cada cobra contém uma rede neural. A rede neural tem uma camada de entrada de 24 neurônios, 2 camadas ocultas de 10 neurônios e uma camada de saída de 4 neurônios. A rede pode ser personalizada com o número de camadas ocultas, bem como o número de neurônios nas camadas ocultas.

![rede](https://user-images.githubusercontent.com/32133062/105231313-6f1d6300-5b45-11eb-966c-dae4a954a9ea.png)

### Visão
A cobra pode ver em 8 direções. Em cada uma dessas direções a cobra procura 3 coisas:
+ Em qual direção esta a comida
+ Distância ate seu corpo
+ Distância ate a parede

3 x 8 direções = 24 entradas. As 4 saídas são simplesmente as direções que a cobra pode mover.

![snake-views](https://user-images.githubusercontent.com/32133062/105233974-52832a00-5b49-11eb-9965-63f1ba707c69.png)

## Evolução
### Selecão natural
A cada geração é criada uma população de 500 cobras. Para a primeira geração, todas os pesos da rede neural em cada uma das cobras são inicializadas aleatoriamente. Uma vez que toda a população está morta, uma pontuação de aptidão é calculada para cada uma das cobras. Usando essas pontuações de aptidão, algumas das melhores cobras são selecionadas para se reproduzir. Na reprodução, duas cobras são selecionadas e a rede neural de cada uma são cruzadas e, em seguida, a criança resultante sofre mutação. Isto é repetido para criar uma nova população de 500 novas cobras.

### Fitness
A aptidão das cobras depende de quanto tempo a cobra permanece viva, bem como a sua pontuação. No entanto, elas não são igualmente importantes, tendo uma pontuação mais elevada é recompensado mais do que uma cobra que simplesmente permanece viva sem ir atrais da comida. No entanto, existe a possibilidade de que uma cobra possa desenvolver uma estratégia em que ela circule em um determinado padrão e nunca morra. Mesmo que ter uma pontuação alta é priorizado a que vive mais, se uma cobra nuca more, então isso é um problema. Para evitar isso, cada cobra pode ser movimento no maixmo por 500 bloco. Cada vez que come um pedaço de comida os movimentos são resetados para 500. Isso significa que as cobras que evoluem e ficam em loops acabarão morrendo e as cobras que procuram comida não só terão uma pontuação mais alta, mas permanecerão vivas por mais tempo

### Cruzamento & Mutação
Quando duas cobras são selecionadas para reprodução, os pesos da rede neural das duas cobras são cruzada. O que isto significa é que parte do pesos de um dos pais é misturado com parte do segundo pai e os pesos resultante é atribuído à criança. Após o cruzamento, os pesos também são mutado de acordo com uma taxa de mutação. A taxa de mutação determina quanto dos pesos serão alterados aleatoriamente.

![snakeai-ai](https://user-images.githubusercontent.com/32133062/105237251-0f29bb00-5b4b-11eb-82dc-107d44be1316.gif)

## Dados por geração
### Gráfico
O gráfico representa a pontuação da melhor cobra de cada geração. Em algumas gerações, o gráfico pode cair abaixo do anterior, isso porque, mesmo que a pontuação possa ter sido pior, algum traço permitiu que a cobra vivesse mais tempo e ganhasse uma maior aptidão geral.

![snakeai-graph](https://user-images.githubusercontent.com/32133062/105240192-c58da000-5b4b-11eb-9424-2f029153d75e.png)

```sh
    # Para vizualizar este grafo execute
    $ pipenv run graph
```
