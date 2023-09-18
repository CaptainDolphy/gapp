
import 'package:flutter/material.dart';

import 'package:webview_cookie_manager/webview_cookie_manager.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(MyApp());
}
enum _MenuOptions {
  listCookies,
}
class Menu extends StatefulWidget {
  const Menu({required this.controller, super.key});

  final WebViewController controller;

  @override
  State<Menu> createState() => _MenuState();
}

class _MenuState extends State<Menu> {
  final cookieManager = WebViewCookieManager();
  // Add this line

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<_MenuOptions>(
      onSelected: (value) async {
        switch (value) {
          case _MenuOptions.listCookies:
            await _onListCookies(widget.controller);
        }
      },
      itemBuilder: (context) => [
        const PopupMenuItem<_MenuOptions>(
          value: _MenuOptions.listCookies,
          child: Text('List cookies'),
        )
      ],
    );
  }

  Future<void> _onListCookies(WebViewController controller) async {
    final String cookies = await controller
        .runJavaScriptReturningResult('document.cookie') as String;
    print(cookies);
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(cookies.isNotEmpty ? cookies : 'There are no cookies.'),
      ),
    );
  }
}






class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final cookieManager = WebviewCookieManager();

  final String _url = 'https://gevo.edookit.net/';
  final String cookieValue = 'some-cookie-value';
  final String domain = 'youtube.com';
  final String cookieName = 'some_cookie_name';
  late final WebViewController controller;


  @override
  void initState() {
    super.initState();
    cookieManager.clearCookies();
    controller = WebViewController()
      ..loadRequest(
        Uri.parse(_url),
      )
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setUserAgent(
          "Mozilla/5.0 (Linux; Android 4.4.4; One Build/KTU84L.H4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.135 Mobile Safari/537.36"
      );


      controller.setNavigationDelegate(
        NavigationDelegate(
            onPageFinished: (url) {
            getCookies(controller,cookieManager);
            }
        )
      );
  }


  void getCookies(controller, cookieManager) async {
    Menu(controller: controller);
    final String cookies = await controller
        .runJavaScriptReturningResult('document.cookie') as String;
    print(cookies);

  }



  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Plugin example app'),
          actions: [
            Menu(controller: controller)
                //await cookieManager.getCookies(null);

          ],
        ),
        body: WebViewWidget(
          controller: controller,
          /*onWebViewCreated: (controller) async {
            await cookieManager.setCookies([
              Cookie(cookieName, cookieValue)
                ..domain = domain
                ..expires = DateTime.now().add(Duration(days: 10))
                ..httpOnly = false
            ]);
          },
          onPageFinished: (_) async {
            final gotCookies = await cookieManager.getCookies(_url);
            for (var item in gotCookies) {
              print(item);
            }
          },*/
        ),
      ),
    );
  }
}