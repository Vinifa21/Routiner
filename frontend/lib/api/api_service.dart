// lib/api_service.dart

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'constants.dart'; // Arquivo onde você definiu a baseUrl

class ApiService {
  // Configuração inicial do Dio com a URL base da sua API
  final Dio _dio = Dio(BaseOptions(baseUrl: baseUrl));
  
  // Instância para acessar o armazenamento seguro do dispositivo
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  /// Tenta autenticar o usuário com o backend.
  /// Se o login for bem-sucedido (status 200), o access token é salvo
  /// de forma segura e a função retorna `true`. Caso contrário, retorna `false`.
  Future<bool> login(String username, String password) async {
    try {
      final response = await _dio.post('/api-auth/login/', data: {
        'username': username,
        'password': password,
      });

      if (response.statusCode == 200) {
        // Se o login for bem-sucedido, salva o token
        await _storage.write(key: 'accessToken', value: response.data['access']);
        return true;
      }
      return false;
    } catch (e) {
      // Imprime o erro no console para depuração
      print('Erro no login: $e');
      return false;
    }
  }

  /// Busca a lista de tópicos da API.
  /// Esta é uma rota protegida, então o token de acesso precisa ser
  /// enviado no cabeçalho (header) da requisição.
  Future<List<dynamic>?> getTopics() async {
    try {
      // Lê o token salvo no dispositivo
      final token = await _storage.read(key: 'accessToken');

      // Se não houver token, não há como buscar os dados
      if (token == null) {
        print('Token de acesso não encontrado.');
        return null;
      }

      // Adiciona o cabeçalho de autorização manualmente na requisição
      final response = await _dio.get(
        '/api/topics/',
        options: Options(
          headers: {'Authorization': 'Bearer $token'},
        ),
      );

      // Retorna a lista de tópicos
      return response.data;
    } catch (e) {
      print('Erro ao buscar tópicos: $e');
      return null;
    }
  }

  /// Realiza o logout do usuário, apagando o token de acesso do dispositivo.
  Future<void> logout() async {
    await _storage.delete(key: 'accessToken');
  }

  /// Verifica se existe um token salvo para determinar se o usuário
  /// já está logado no aplicativo.
  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'accessToken');
    return token != null;
  }
}