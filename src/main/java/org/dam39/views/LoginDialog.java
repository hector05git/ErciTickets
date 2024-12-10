package org.dam39.views;

import javafx.application.Platform;
import javafx.embed.swing.JFXPanel;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import org.dam39.utils.Session;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;

public class LoginDialog extends JDialog implements InterfaceView{
    private JPanel MainPanel;
    public LoginDialog() {

        initWindow();
        setCommands();
        initComponents();
    }

    @Override
    public void initWindow() {
    setContentPane(MainPanel);
    pack();
    setLocationRelativeTo(null);

    }

    @Override
    public void showWindow() {
    setVisible(true);
    }

    @Override
    public void closeWindow() {
    dispose();
    }

    @Override
    public void setCommands() {

    }

    @Override
    public void addListener(ActionListener listener) {

    }

    @Override
    public void initComponents() {

        // Crea un panel JFXPanel, que permite integrar JavaFX en Swing
        JFXPanel fxPanel = new JFXPanel();
        // Añade el fxPanel al centro de la ventana (en el contenedor BorderLayout.CENTER)
        add(fxPanel, BorderLayout.CENTER);

        // Ejecuta el siguiente bloque de código en el hilo de la interfaz de usuario de JavaFX
        Platform.runLater(() -> {
            // Crea un componente WebView, que permite mostrar contenido web
            WebView webView = new WebView();
            // Obtiene el motor que maneja el contenido de la WebView
            WebEngine webEngine = webView.getEngine();

            // Configura un listener que detecta cuando se carga la página en el WebEngine
            webEngine.getLoadWorker().stateProperty().addListener((observable, oldState, newState) -> {
                // Verifica si la carga de la página fue exitosa
                if (newState == javafx.concurrent.Worker.State.SUCCEEDED) {
                    // Obtiene la URL actual de la página cargada
                    String currentUrl = webEngine.getLocation();

                    // Verifica si la URL contiene "login_ok", indicando que el login fue exitoso
                    if (currentUrl.contains("login_ok")) {
                        // Obtiene las cookies del navegador mediante JavaScript
                        String cookies = (String) webEngine.executeScript("document.cookie");

                        // Llama a un método para procesar las cookies obtenidas
                        getCookies(cookies);

                        // Muestra un mensaje de éxito del login
//                        showLoginSuccessMessage();
                    }
                }
            });

            // Carga la página de login en el WebView
            webEngine.load("http://127.0.0.1:5000/login");

            // Establece la escena del fxPanel con el WebView para mostrar la página cargada
            fxPanel.setScene(new Scene(webView));
        });

        // Ajusta el tamaño de la ventana según el contenido (si es necesario)
        pack();

    }
    private void getCookies(String cookies) {
        // Imprime las cookies obtenidas para depuración
        System.out.println("Cookies: " + cookies);

        // Separa las cookies por el delimitador "; " (espacio y punto y coma) para obtener cada cookie individualmente
        String[] cookieArray = cookies.split("; ");

        // Inicializa la variable que almacenará el token
        String token = null;
        // Itera sobre el array de cookies para buscar la cookie que empieza con "token="
        for (String cookie : cookieArray) {
            if (cookie.startsWith("token=")) {
                // Si encuentra el "token", extrae el valor después del "="
                token = cookie.split("=")[1];
                break;  // Sale del bucle después de encontrar el token
            }
        }

        // Inicializa la variable que almacenará el login del usuario
        String userlogin = null;
        // Itera sobre el array de cookies para buscar la cookie que empieza con "userlogin="
        for (String cookie : cookieArray) {
            if (cookie.startsWith("userlogin=")) {
                // Si encuentra el "userlogin", extrae el valor después del "="
                userlogin = cookie.split("=")[1];
                break;  // Sale del bucle después de encontrar el userlogin
            }
        }

        // Establece el nombre de usuario en la sesión usando la clase Session
        Session.setUsername(userlogin);
        // Establece el token en la sesión usando la clase Session
        Session.setToken(token);
    }

}
