import 'package:flutter/material.dart';
import 'package:routiner/api/api_service.dart';


// Lista de matérias definida globalmente
const List<String> list = <String>['Cálculo','Geometria','Programação'];

// Nova lista de números (1 a 10)
const List<int> numberList = <int>[1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

class QuestionsPage extends StatefulWidget {
  const QuestionsPage({super.key});

  @override
  State<QuestionsPage> createState() => _QuestionsPageState();
}

class _QuestionsPageState extends State<QuestionsPage> {
  // Variáveis de estado para armazenar as seleções
  String? _materiaSelecionada;
  int? _numeroSelecionado; // NOVO ESTADO PARA O SEGUNDO DROPDOWN

  // Inicializa as seleções com o primeiro item de cada lista.
  @override
  void initState() {
    super.initState();
    _materiaSelecionada = list.first;
    _numeroSelecionado = numberList.first; // Inicialização da nova variável
  }

  @override
  Widget build(BuildContext context) {
    // Definimos a largura máxima do conteúdo para evitar overflow
    final screenWidth = MediaQuery.of(context).size.width;
    final contentWidth = screenWidth > 600 ? 600.0 : screenWidth * 0.9;

    return Center(
      child: Container(
        width: contentWidth, // Restringe a largura do Container
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start, // Alinha itens à esquerda
          children: [
            const SizedBox(height: 30),
            
            // --- 1. DROPDOWN DE MATÉRIAS ---
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Escolha a Matéria",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(width: 20,), 
                
                DropdownButton<String>(
                  value: _materiaSelecionada, 
                  onChanged: (String? novoValor) {
                    setState(() {
                      _materiaSelecionada = novoValor;
                    });
                  },
                  items: list.map<DropdownMenuItem<String>>((String valor) {
                    return DropdownMenuItem<String>(
                      value: valor,
                      child: Text(valor),
                    );
                  }).toList(),
                ),
              ],
            ),
            
            const SizedBox(height: 30), // Espaçamento entre os dropdowns
            
            // --- 2. NOVO DROPDOWN DE NÚMEROS (1 a 10) ---
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Escolha o Nível (1 a 10)", // Novo Label
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(width: 20,), 
                
                DropdownButton<int>( // Tipo mudou para <int>
                  value: _numeroSelecionado, 
                  
                  // Ação chamada quando um novo item é selecionado
                  onChanged: (int? novoValor) { // O tipo do valor é int
                    setState(() {
                      _numeroSelecionado = novoValor;
                    });
                  },
                  
                  // Constrói a lista de DropdownMenuItems a partir da nova lista 'numberList'
                  items: numberList.map<DropdownMenuItem<int>>((int valor) {
                    return DropdownMenuItem<int>(
                      value: valor,
                      child: Text(valor.toString()), // Converte o int para String
                    );
                  }).toList(),
                ),
              ],
            ),
            // --- Fim do Novo DropdownButton ---

            const SizedBox(height: 50),

            // Feedback visual das seleções
            Text(
              'Seleção: Matéria: $_materiaSelecionada | Nível: $_numeroSelecionado',
              style: const TextStyle(fontSize: 16, color: Colors.blue),
            ),

            const SizedBox(height: 60),
            
            Center(
              child: Text(
                "Questão: ",
                style: const TextStyle(
                  fontSize: 16,
                ),  
              ),
            ),

            const SizedBox(height: 60),

            // --- BOTÕES A, B, C, D ---
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                    // ação do botão A
                  },
                  child: const Text('A'),
                ),
                const SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    // ação do botão B
                  },
                  child: const Text('B'),
                ),
                const SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    // ação do botão C
                  },
                  child: const Text('C'),
                ),
                const SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    // ação do botão D
                  },
                  child: const Text('D'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
