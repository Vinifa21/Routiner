// lib/main.dart

import 'package:flutter/material.dart';

// Importa a estrutura de layout customizada
import 'package:routiner/widgets/scaffold_routiner.dart'; 
// Importa todas as páginas separadas
import 'package:routiner/lib/pages/home_routiner.dart';
import 'package:routiner/lib/pages/questoes.dart';
import 'package:routiner/lib/pages/historico.dart';
import 'package:routiner/lib/pages/perfil.dart';


void main() {
  runApp(const MyApp());
}

// ----------------------------------------------------
// 1. MyApp (Configuração de Tema e Cores)
// ----------------------------------------------------

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    const customBlue = Color(0xFF38B6FF);

    return MaterialApp(
      title: 'Routiner',
      debugShowCheckedModeBanner: false, 
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: customBlue,
          onPrimary: Colors.white, 
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: customBlue,
          foregroundColor: Colors.white, 
          toolbarHeight: 80.0, 
        ),
        useMaterial3: true,
      ),
      home: const RoutinerHomePage(),
    );
  }
}

// ----------------------------------------------------
// 2. RoutinerHomePage (Lógica de Estado e Navegação)
// ----------------------------------------------------

class RoutinerHomePage extends StatefulWidget {
  const RoutinerHomePage({super.key});

  @override
  State<RoutinerHomePage> createState() => _RoutinerHomePageState();
}

class _RoutinerHomePageState extends State<RoutinerHomePage> {
  // Índice para controlar qual página está sendo mostrada no 'body'
  int _selectedIndex = 0;

  // A lista de Widgets/Páginas agora referencia as classes separadas
  static const List<Widget> _widgetOptions = <Widget>[
    HomePage(),      // Índice 0
    const QuestionsPage(), // Índice 1
    const HistoryPage(),   // Índice 2
    const ProfilePage(),   // Índice 3
  ];

  // Função para mudar o estado e recarregar o body com o novo índice
  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    // Retorna o Scaffold customizado, passando o conteúdo da página ativa (body)
    // e a função que será chamada pelo Drawer para mudar o índice.
    return RoutinerScaffold(
      body: _widgetOptions.elementAt(_selectedIndex),
      selectedIndex: _selectedIndex,
      onItemTapped: _onItemTapped,
    );
  }
}