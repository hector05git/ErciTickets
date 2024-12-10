package org.dam39.controllers;

import org.dam39.views.LoginDialog;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class LoginDialogController implements ActionListener {
    LoginDialog loginDialog;
    public LoginDialogController(LoginDialog loginDialog) {
        this.loginDialog = loginDialog;
    }
    @Override
    public void actionPerformed(ActionEvent e) {

    }
}
