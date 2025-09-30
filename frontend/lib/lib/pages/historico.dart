import 'package:flutter/material.dart';

class HistoryPage extends StatelessWidget {
  const HistoryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        children: [
          SizedBox(height: 160,),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                "Você está a X dias fazendo seus exercicios",
                style: TextStyle(
                  fontSize: 24,
                  fontFamily: "Helvetica",
                ),
              ),
              Icon(
                Icons.local_fire_department,
                size: 80,
                color: Color(0XFFFF914D),
              )
            ],
          ),
          SizedBox(height: 100,),
          Text(
            "Faltam Y exercicios para você terminar sua meta diária!",
            style: TextStyle(
              fontFamily: "Helvetica",
              fontSize: 20
            ),
          )
        ],
      ),
    );
  }
}