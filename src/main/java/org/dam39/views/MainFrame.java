package org.dam39.views;

import javax.swing.*;
import java.awt.event.ActionListener;

public class MainFrame extends JFrame implements InterfaceView{
    private JPanel MainPanel;
    public MainFrame() {
        initComponents();
        initWindow();
        setCommands();
    }

    @Override
    public void initWindow() {
        setContentPane(MainPanel);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
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

    }
}
