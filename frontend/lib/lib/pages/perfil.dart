import 'package:flutter/material.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        children: [
          SizedBox(height: 80,),
          Icon(
            Icons.account_circle_sharp,
            size: 200,
          ),
          SizedBox(height: 100),
          Text(
            "Nome do Usuário",
            style: TextStyle(
              fontFamily: "Helvetica",
              fontSize: 26
            ),
          ),
        ],
      ),
    );
  }
}