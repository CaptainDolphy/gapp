
import 'package:flutter/material.dart';

import 'package:webview_cookie_manager/webview_cookie_manager.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _cookieManager = WebviewCookieManager();

  final String _url = 'https://gevo.edookit.net/';
  final String cookieValue = 'some-cookie-value';
  final String domain = 'youtube.com';
  final String cookieName = 'some_cookie_name';
  late  WebViewController _controller;


  @override
  void initState() {
    super.initState();
    _cookieManager.clearCookies();
    _controller = WebViewController()
      ..loadRequest(
        Uri.parse(_url),
      )
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setUserAgent(
          "Mozilla/5.0 (Linux; Android 4.4.4; One Build/KTU84L.H4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.135 Mobile Safari/537.36"
      );

      _controller.setNavigationDelegate(
        NavigationDelegate(
            onPageFinished: (url) {
            getCookies(_controller,_cookieManager);
            }
        )
      );
    }
  }

  void getCookies(_controller, _cookieManager) {
    if (_controller.currentUrl() != "https://gevo.edookit.net/") {
      var cookies = _cookieManager.getCookies(_controller.currentUrl());
      print(cookies);
    }
  }


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Plugin example app'),
          actions: [
            IconButton(
              icon: Icon(Icons.ac_unit),
              onPressed: () async {
                // TEST CODE
                var _cookieManager;
                await _cookieManager.getCookies(null);
              },
            )
          ],
        ),
        body: WebViewWidget(
          controller: _controller,
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