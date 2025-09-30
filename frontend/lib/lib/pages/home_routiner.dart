import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: [
          SizedBox(height: 100,),
          Text(
            "Seja muito bem-vindo ao Routiner, seu mais ajudante de estudos!",
            style: TextStyle(
              fontSize: 40
            ),
          ),
          SizedBox(height: 100,),
          SizedBox(
            width: 900,
            child: 
              Text(
                "Aqui você terá um novo incentivo para executar seus exercícios e atividades diárias! Para acessar as questões, seu perfil e seu histórico, acesse os três tracinhos à esquerda da página e entre no que desejar!",
                style: TextStyle(
                  fontSize: 20,
                ),
                textAlign: TextAlign.center,
              )
            ,),
          SizedBox(height: 80,),
          Image.asset(
              'assets/images/routiner_logo_azul.png',
              height: 160,
            ),
        ],
      )
    );
  }
}