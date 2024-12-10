package org.dam39.utils;

public class Session {
    // Variables estáticas para almacenar el usuario y el token
    private static String username;
    private static String token;

    public static void setUsername(String username) {
        Session.username = username;
    }

    public static void setToken(String token) {
        Session.token = token;
    }

    public static String getUsername() {
        return username;
    }

    public static String getToken() {
        return token;
    }

    // Método para verificar si el usuario está autenticado
    public static boolean isAuthenticated() {
        return username != null && token != null;
    }
}