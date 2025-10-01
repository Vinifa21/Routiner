Projeto para o Hackathon da MagaluCloud

# **ROUTINER**

## **Descrição**

Aplicativo web destinado a estudantes universitários, com o objetivo principal de estimular o estudo de forma intuitiva e divertida.

Sua funcionalidade principal é uma **trilha de exercícios** criada de acordo com a matéria que o aluno deseja estudar, seguindo um modelo similar ao **Duolingo**. Os exercícios serão organizados por nível de dificuldade e extraídos diretamente do livro de estudo selecionado pelo aluno (ex: *Cálculo I* do Stewart).

## **Público Alvo**

Estudantes universitários que buscam uma plataforma para auxiliar no incentivo e na organização de seus estudos.

## **Requisitos Funcionais**

### **Usuário Não-Logado**
* Interage somente com a página de **Login/Cadastro**.
* Pode criar uma nova conta ou acessar uma conta existente.

### **Usuário Logado**

* **Seleção de Conteúdo:**
    * Deve poder escolher uma **matéria**, um **livro didático** e um **tema** para estudar.

* **Trilha de Exercícios:**
    * Deve poder responder a mini-questionários com questões objetivas e receber feedback instantâneo (erros/acertos).
    * Deve receber pontuação baseada na performance nos exercícios.

* **Sistema de Progressão:**
    * Exercícios de maior dificuldade serão desbloqueados com base na pontuação acumulada.
    * Será exibida uma **barra de progresso** do tema sendo estudado (Ex: 75% do tema “Limites” estudado).
    * Será exibida a quantidade de temas concluídos na matéria (Ex: 1 de 3 temas de Cálculo I estudado).

* **Navegação e Flexibilidade:**
    * Deve poder trocar a matéria, o tema ou o livro que deseja estudar a qualquer momento.
        * **Ex 1 (Matéria):** Trocar de *Cálculo I* para *Ágebra Linear*.
        * **Ex 2 (Tema):** Dentro da trilha *Cálculo I*, poder trocar do tema “Limites
