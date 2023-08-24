# Guia de utilização e manutenção

## Funcionamento geral da aplicação (para devs)

### ```Avaliation Strategy``` e suas limitações

Vamos começar do começo, esta aplicação está focada em realizar avaliações, sendo que, por norma e com a exceção de observações, existirá sempre alguém a avaliar e alguém a ser avaliado numa dada questão.

Como isto é algo bastante especifico e que podemos nem sempre querer fazer, foi deliniada toda a lógica relativa às avaliações numa class chamada de ```Avaliation Strategy```. Como o próprio nome indica, a estratégia de processamento que queremos utilizar será a de avaliação que tal como sugeri em cima, assume que:

   1. Existe sempre um avaliado, avaliador e uma pergunta (à exceção das observações)
   2. O Avaliado é avaliado por **TODOS** os avaliadores presentes no excel de input
   3. O Avaliado tem de estar presente em **TODAS** as perguntas

Secalhar tou a mostrar os pontos negativos demasiado cedo 🤲 mas estes erros ainda não são detetados pelo programa e queremos que, caso estes ocorram (que mais tarde ou mais cedo, ocorrerão...) alguém que leu isto seja capaz de perceber melhor o porquê de eles estarem a acontecer e que, esperançosamente, os corrija.

### ```Avaliation Strategy``` entender as limitações

Vamos ao que interessa, a ```Avaliation Strategy``` é a parte mais complexa do código e entendê-la fará com que entendam tudo o que está à sua volta. Com isto, quero começar por introduzir os seus métodos mais importantes.

#### Parse

Introduzo então o método ```parse```, ele é responsável por interpretar os dados do excel e coloca-los numa estrutura de dados que seja fácil para o programador de manipular/entender.

Vamos ver o método parse com as suas entranhas desprotegidas, tirem algum tempo para interpretar o que cada linha de código está a fazer:

(A equipa tentou o seu melhor para dar nomes de jeito às coisas, por isso, esperamos que seja de fácil leitura 🙏🙏)

```py
def parse(self) -> list[Question]:

        # 1º passo
        config_layout: Config = self.parser.get_config()
        file = self.parser.get_target_file()

        # 2º passo
        # Pega em todas as perguntas das configurações
        questions = config_layout.get_type(Type.QUESTIONS)[0]["questions"]
        question_list: list[Question] = self.__get_questions(questions)

        # 3º passo
        # Pega em todos os avaliadores
        measurer_label = config_layout.get_type(Type.MEASURER)[0]
        measurer_list: list[Measurer] = self.__get_measurers(measurer_label)
        
        # 4º passo
        # Pega em todos os avaliados
        measured_names = config_layout.get_type(Type.MEASURED)[0]["names"]
        measured_list: list[Measured] = self.__get_measured(measured_names, question_list)

        # 5º passo
        # Avalia cada avaliado com cada avaliador
        # e guarda o resultado no próprio avaliado
        for measurer in measurer_list:
            for measured in measured_list:    
                measurer.evaluate(measured, file)

        question_list = Question.mix_questions(question_list, self.name_divider)
        
        # Isto serve apenas para prevenir erros de configuração
        # Para quem estiver o README.md, podem ignorar isto
        num_questions = len(self.__get_questions_names(question_list))
        for measured in measured_list:
            if measured.get_number_of_question() != num_questions:
                print(f"\n{measured.get_name()} tem {measured.get_number_of_question()} perguntas, mas deveria ter {num_questions}.")
                exit(1)

        return question_list
```

##### 1º Passo

```py
config_layout: Config = self.parser.get_config()
file = self.parser.get_target_file()
```

Ora, indo direto ao assunto temos então o 1ºpasso que trata de ler um config_layout e ler um file... mas que chinesada que praqui vai podem estar-se a dizer para vocês mesmos mas não é complicado o que isto faz. O config_layout está apenas a buscar as configurações que o utilizador escolheu, num arquivo deste estilo:

(sim, isto está a ser lido como se fosse um dicionário ou como se fosse uma hashmap para as pessoas que não estejam habituadas a Python, facilitando a sua manipulação dentro do código)

```json
{
    "layout": [
      {
          "type": "DATE",
          "label": "Carimbo de data/hora"
      },
      {
          "type": "MEASURER",
          "label": "Nome do avaliador"
      },
      {
          "type": "MEASURED",
          "names": ["Beatriz Simões", "Beatriz Sousa", "Catarina Oliveira", "Cláudia Santos", "Inês Faria", "Inês Geraldes", "Letícia Santos", "Márcia Costa", "Margarida Ribeiro", "Mariana Coelho", "Raquel Baptista"]
      },
      {
          "type": "QUESTIONS",
          "questions": [
            
            {
              "label": "O membro coopera com os seus colegas para alcançar objetivos comuns que tenham sido estabelecidos",
              "type": "NUMBER"
          },
          {
            "label": "O membro assume, em regra, objetivos ambiciosos e exigentes, embora realistas, para si e para os seus colegas.",
            "type": "NUMBER"
          },
          {
              "label": "O membro compromete-se com os resultados a alcançar de acordo com os objetivos estratégicos do departamento e júnior empresa, e é persistente perante obstáculos e dificuldades",
              "type": "NUMBER"
          },
          {
            "label": "O membro aceita correr riscos para atingir os resultados desejados e assume as responsabilidades pelo sucesso ou fracasso dos mesmos. ",
            "type": "NUMBER"
          },
          {
            "label": "O membro tem noção do que é prioritário para uma tarefa, respondendo, em regra, prontamente nos momentos de pressão e urgência.",
            "type": "NUMBER"
          },
          {
            "label": "O membro procura desenvolver o seu conhecimento técnico nas áreas relevantes para o seu departamento ou projeto em que esteja envolvido, promovendo um autodesenvolvimento contínuo.",
            "type": "NUMBER"
          },
          {
            "label": "O membro é capaz de publicitar a EPIC Júnior de uma forma correta e precisa.",
            "type": "NUMBER"
          },
          {
            "label": "O membro consegue elaborar designs para diferentes tipos de divulgação, procurando manter os componentes que constroem a imagem pública da EPIC Júnior.",
            "type": "NUMBER"
          }, 
          {
            "label": "O membro sabe comportar-se de uma forma correta e adequada e de uma maneira profissional e respeitosa, em situações em que representa a EPIC Júnior",
            "type": "NUMBER"
          },
          
          {
            "label": "O membro cumpre os objetivos das tarefas pelos quais é responsável.",
            "type": "NUMBER"
          },
          {
            "label": "O membro respeita os valores, os membros, as instalações e todos os recursos da EPIC Júnior.",
            "type": "NUMBER"
          },

              
            {
              "label": "Observações",
              "type": "OBSERVATION"
            }
          ]
      }
    ],
    "output": [
      {
          "type": "HEADER",
          "label": "Avaliação de desempenho",
          "col-span": "full",
          "row-span": 2,
          "bg-color": "FFC000",
          "text-color": "FFFFFF",
          "x-alignment": "center",
          "y-alignment": "center"
      },
      {
          "type": "CONTENT",
          "rows": [
              {
                  "type": "MEASURER",
                  "label": "Avaliador",
                  "col-span": 2,
                  "row-span": 1,
                  "bg-color": "AAAAAA",
                  "text-color": "000000",
                  "x-alignment": "center",
                  "y-alignment": "center"
              },
              {
                  "type": "MEASURED",
                  "label": "Avaliado",
                  "col-span": 2,
                  "row-span": 1,
                  "bg-color": "AAAAAA",
                  "text-color": "000000",
                  "x-alignment": "center",
                  "y-alignment": "center"
              },
              {
                  "type": "MEASURE",
                  "col-span": 1,
                  "row-span": 1,
                  "bg-color": "FFFFFF",
                  "text-color": "000000",
                  "x-alignment": "left",
                  "y-alignment": "center",
                  "border": "thin",
                  "border-color": "000000"
              }
          ]
      }
  ],
```

E o file é simplesmente o excel de onde queremos receber os dados.

##### 2º Passo

```py
questions = config_layout.get_type(Type.QUESTIONS)[0]["questions"]
question_list: list[Question] = self.__get_questions(questions)
```

Simples, estamos a buscar as questões que o utilizador quer avaliar ao ficheiro de configuração que o utilizador especificou. Certamente que o programa conseguiria detetar as questões no excel automáticamente e sim, se programado para tal, o programa seria capaz de fazer isso. Mas por questões de tempo e por questões de configurabilidade acabamos por optar por não deixar o programa fazer isto automáticamente. (Pode ser algo a pensar futuramente)

De seguida, vamos buscar todas as questões ao excel, isto porque precisamos de saber qual é o X ou a Abcissa de cada pergunta para posteriormente irmos ao excel de input buscar mais dados.

##### 3º passo

```py
measurer_label = config_layout.get_type(Type.MEASURER)[0]
measurer_list: list[Measurer] = self.__get_measurers(measurer_label)
```

Funciona da mesma forma que o segundo passo, só há um senão, que é, agora estamos a ir ao excel de input para ver qual é o Y ou a Ordenada de cada avaliador ao invés da abcissa. Outra nota é que a variavel measurer_label especifica apenas o "*nome*" da coluna onde estão especificados os avaliadores, como no exemplo:

| Nome do Avaliador |
|-------------------|
| Rafaela Carvalho  |
| Paula Ferreira    |
| Mariana Oliveira  |
| Inês Cabral       |
| Mariana Arezes    |
| Paulo Vieira      |
| Gonçalo Figueiredo|
| Catarina Milheiro |
| Inês Bastos       |

Aqui, "**Nome do Avaliador**" é a measurer_label.

##### 4º passo

```py
measured_names = config_layout.get_type(Type.MEASURED)[0]["names"]
measured_list: list[Measured] = self.__get_measured(measured_names, question_list)
```

Tal como no segundo e no terceiro passo, vamos ao arquivo de configuração buscar os nomes das pessoas que queremos avaliar e de seguida vamos ao excel... mas vamos ao excel fazer o quê? Não existe nada a fazer no excel com os nomes dos avaliados, afinal de contas, já sabemos quem queremos avaliar, onde estão as perguntas e quem são e onde estão os avaliadores. Para esclarecer esta dúvida vamos então dar uma vista de olhos no método ```__get_measured```:

```py
def __get_measured(self, measured_names_in_layout, question_list: list[Question]) -> list[Measured]:
        measured_list: list[Measured] = []
        for measured_name in measured_names_in_layout:
            measured_list.append(Measured(measured_name, question_list))
        return measured_list
```

Vou descrever o que vejo. Estamos a pegar nos nomes especificados na configuração, a criar instâncias de "```Measured```" e por ultimo a colocar estas instâncias numa lista de avaliados.

Ou seja, temos de ir à classe ```Measured``` para ver o que realmente está a acontecer. Vamos então expôr as tripas de ```Measured```:

```py
class Measured:
    __questions = []

    def __init__(self, name: str, all_questions: list[Question]) -> None:
        self.name = name
        self.__questions = self.__my_questions(all_questions)
    
    def __my_questions(self, questions: list[Question]) -> list[Question]:
        result: list[Question] = []
        num_obs = 0
        for question in questions:

            if question.get_question_type() == Type.OBSERVATION:
                num_obs += 1
                result.append(question)
            
            cleaned_name = self.name.lower()
            if cleaned_name in question.get_question().lower():
                result.append(question)
        
        if len(result) <= num_obs:
            print(f"{self.name} não tem perguntas para ser avaliada.")
            exit(1)
        return result
```

Analisando então o construtor temos que o avaliado tem um nome e um grupo de questões onde ele é avaliado. Mas como podem ver nos argumentos de ```__init__```, nós passamos todas as questões e não apenas as questões que pertencem a este avaliado.

Devido a isto, necessitamos de fazer uma filtragem nas perguntas e ver quais são as perguntas que têm o nome do avaliado nelas contidas. É isso que faz o ```self.__my_questions```.

Voltando então ao ```parse```, entramos no passo 5.

##### passo 5

```py
for measurer in measurer_list:
    for measured in measured_list:    
        measurer.evaluate(measured, file)

question_list = Question.mix_questions(question_list, self.name_divider)
```

Este é sem dúvida o passo mais complexo sendo que estamos a percorrer a nossa lista de avaliadores, seguida da nossa lista de avaliados e depois invocámos o método ```measurer.evaluate``` onde precisamos de passar quem o avaliador está a avaliar e em que ficheiro.

Já se está a ver que vamos ter de explorar o que o evaluate faz em concreto então vamos a isso.

```py
def evaluate(self, measured: "Measured", file: DataFrame) -> list[Question]:
        questions_to_evaluate: list[Question] = measured.get_questions()

        # Apenas verifica erros
        # Podemos ignorar
        if len(question_to_evaluate) == 0:
            print(f"{measured.get_name()} não tem perguntas para ser avaliada/o.")
            exit(1)

        # cross each question col index with the row index of the measurer
        for question in questions_to_evaluate:    
            grade = file.iloc[self.row_index, question.get_pos_in_document()]

            if question.get_question_type() == Type.OBSERVATION:
                grade = grade if grade == grade and grade != "" else "Nada a apontar"

            question.add_grade(grade = grade, measurer = self, measured=measured)
        
        return question_to_evaluate.copy()
```

O mais importante a tirar deste método é o ```file.iloc[self.row_index, question.get_pos_in_document()]``` que vai ao excel com o número da linha do avaliador e com o número da coluna da pergunta para buscar a avaliação em si, dai que guardamos o resultado numa variável chamada "grade".

Em seguida, temos alguns cheques meio manhosos (não vou mentir), mas apenas se aplica a perguntas do tipo "Observação" e faz com que, caso o avaliador não tenha colocado nenhum texto, seja capaz de substituir isso com "Nada a apontar".

(Para quem estiver curioso com o ```grade == grade```, fizemos isto porque muitas vezes quando a celula do excel estava fazia a grade retornava como "nan" e a única maneira de sabermos se o valor da celula está a "nan" ou não, é se compararmos com ela mesma... super confuso, eu sei, mas leiam isto: <https://stackoverflow.com/questions/944700/how-to-check-for-nan-values>)

Depois disto feito, guardamos na própria pergunta uma tuple com a "nota", com o avaliador e com o avaliado.

```return question_to_evaluate.copy()``` neste caso não interessa.

```py
question_list = Question.mix_questions(question_list, self.name_divider)
```

O mix questions faz algo que pode parecer estranho caso não haja contexto mas que depois de explicado creio que vá fazer mais sentido.

Então, mencionando algo que nunca disse antes, é que as perguntas até este momento tinham todas este formato:

"1. O membro coopera com os seus colegas para alcançar objetivos comuns que tenham sido estabelecidos. **[Gonçalo Figueiredo]**"

O que significa que a este ponto do programa se houver 5 avaliados e 5 perguntas, a nossa ```question_list``` teria 25 perguntas dentro.

Então agora precisamos de juntar as supostas 25 perguntas em 5 do estilo:

"1. O membro coopera com os seus colegas para alcançar objetivos comuns que tenham sido estabelecidos."

Sem o "**[Gonçalo Figueiredo]**" especificado e é precisamente isso que esta função faz.

Isto é tudo que o parse faz, a partir daqui vamos explorar a fundo como funciona o método ```convert_to_layout```.
