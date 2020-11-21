# Simulação de Capacitores

## Introdução
 O presente código soluciona numéricamente a [equação de poisson](https://en.wikipedia.org/wiki/Poisson%27s_equation), conhecida no âmbito da eletróstática. A solução da equação diferencial parcial é dada pelo [método da diferença finita](https://en.wikipedia.org/wiki/Finite_difference_method).
Para a simulação de capacitores com diferentes geometrias, temos que resolver a [equação de laplace](https://en.wikipedia.org/wiki/Laplace%27s_equation), um caso particular da equação de poisson. Geralmente em um capacitor é definido o potencial que a placa estará, sendo assim é necessário que entremos com o valor que o contorno terá. Da mesma forma que resolução analítica por meio do método de separação de variáveis temos que estábelecer as constantes.
É possível também resolver e observar o comportamento do potencial na presença de cargas.

## Guia rápido
### Equação de poisson -- Potencial na presença de Cargas

`from poisson_cartesian_v1 import *`

```
dim=10
rounds=10
potencial=poisson_equation(dim,dim,realism=True)
potencial.charge_space(2,[0,9],[0,9],[1,-1])
potencial.run(rounds=100)
potencial.plot2d()
potencial.plot3d()
```

### Equação de Laplace -- Capacitores
`from poisson_cartesian_v1 import *`

```
dim=10
rounds=10
capacitor=poisson_equation(dim,dim,realism=False)
cem=np.ones(dim)*100
zero=np.zeros(dim)
capacitor.contour_rectangle_capacitor(cem,-cem,zero,zero)
resultado=capacitor.run(precision=10**-4)
capacitor.plot2d(save_image=True)
capacitor.plot3d()

```


## Como funciona

### Esssencial

'poisson_equation(X,Y,realism=True)'

É preciso iniciar a utilização do código entrando com o tamnanho do grid de interesse. Passa-se o número de sítios ao longo eixo x e do eixo y. Caso escolha por uma simulação mais realísta o número de sítios no GRID aumenta 100 vezes, o número de sítios no eixo x e y são aumentados em 10 vezes

Em Seguida é necesssário passar as condições de contorno do problema. Há duas possibilidades:
1) utilizar o método `contour_rectangle_capacitor(x_chao,x_topo,y_chao,y_topo) ` que gera um contorno retangula de potencial ao grid. É necessário entrar com os valores na forma de um vetor (preferencialmente numpy) para cada sítio do contorno. Por exemplo, num o contorno no eixo x superior e inferior num grid 4X4 seria [1,1,1,1] e [0,0,0,0].

2) utilizar o método `charge_space(numero_de_cargas,posições_eixo_x,posiçoes_eixo_y,valor_das_cargas)` para entrar com a densidade de carga presente no grid.

### Visualização

Há dois métodos para a visualização dos resultados das simulações. Um reporta o resultada em uma gráfico 3d utilizando o método `plot3d(save_image=False,dpi=300,name='iamge.jpg')` , e outro expõe uma mapa de calor `plot2d(save_image=False,dpi=300,name='image.jpg')`, ou seja uma projeção 2d dos resultados

Abaixo há exemplos de visualizações geradas pela simulação de uma capacitor, uma das placas com voltagem de -100 e outro com voltagem de +100.

![iamge3d](https://github.com/estevanmendes/eletrostatica/blob/master/img/3d_laplace_equation_capacitor.jpg)

![iamge2d](https://github.com/estevanmendes/eletrostatica/blob/master/img/2d_laplace_equation_capacitor.jpg)
### Salvar os dados 




## Referências

* Landau, Rubin H., Manuel J. Pï, and Cristian C. Bordeianu. Computational physics: Problem solving with Python. John Wiley & Sons, 2015.
