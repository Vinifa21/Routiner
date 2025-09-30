import 'package:flutter/material.dart';

// O widget de estrutura de página que será reutilizado
class RoutinerScaffold extends StatelessWidget {
  // O corpo é o conteúdo variável (Home, Questões, Histórico)
  final Widget body;
  
  // O índice atual para destacar o item ativo no Drawer
  final int selectedIndex;
  
  // A função que o Drawer chamará para mudar o estado do body
  final Function(int) onItemTapped;

  const RoutinerScaffold({
    super.key,
    required this.body,
    required this.selectedIndex,
    required this.onItemTapped,
  });

  @override
  Widget build(BuildContext context) {
    // Definimos a cor customizada aqui para usar no DrawerHeader.
    // O ideal é usar Theme.of(context).colorScheme.primary, mas mantemos o valor
    // fixo do seu código original por preferência.
    const customBlue = Color(0xFF38B6FF); 

    return Scaffold(
      // AppBar no topo (estrutura fixa)
      appBar: AppBar(
        title: Image.asset(
          'assets/images/routiner_logo_texto.png',
          height: 30,
        ),
      ),
      
      // Conteúdo principal (variável)
      body: body,

      // Drawer (estrutura fixa)
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            // Cabeçalho do Drawer
            DrawerHeader(
              decoration: const BoxDecoration(
                color: customBlue, 
              ),
              child: Center(
                child: Image.asset(
                  'assets/images/routiner_logo.png', 
                  height: 100,
                  fit: BoxFit.contain,
                ),
              ),
            ),

            // Espaço entre o Header e o primeiro item (Home)
            const SizedBox(height: 20.0),
            
            // Item: Home
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Home'),
              // Usamos a função de callback para notificar a RoutinerHomePage
              onTap: () {
                Navigator.pop(context); 
                onItemTapped(0);      
              },
            ),
            
            // Espaço entre itens
            const SizedBox(height: 20.0),
            
            // Item: Perfil 
            ListTile(
              leading: const Icon(Icons.person),
              title: const Text('Perfil'),
              onTap: () {
                Navigator.pop(context); 
                onItemTapped(3);
              },
            ),
            
            // Espaço entre itens
            const SizedBox(height: 20.0),
            
            // Item: Questões
            ListTile(
              leading: const Icon(Icons.quiz),
              title: const Text('Questões'),
              onTap: () {
                Navigator.pop(context);
                onItemTapped(1); // Navega para Questões
              },
            ),
            
            // Espaço entre itens
            const SizedBox(height: 20.0),
            
            // Item: Meu Histórico
            ListTile(
              leading: const Icon(Icons.history),
              title: const Text('Meu Histórico'),
              onTap: () {
                Navigator.pop(context);
                onItemTapped(2); // Navega para Histórico
              },
            ),
          ],
        ),
      ),
    );
  }
}