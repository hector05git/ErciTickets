package org.dam39.views;

import javax.swing.*;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import static org.dam39.controllers.TicketController.BUY;

public class TicketCon extends JFrame implements InterfaceView {
    private JPanel mainPanel;
    private JSpinner sp_but;
    private JComboBox cb_con;
    private JButton btn_buy;

    public TicketCon() {
        setCommands();
    }


    public void loadComboBox(ArrayList<String> cons) {
        DefaultComboBoxModel<String>
                model = new DefaultComboBoxModel<>();
        for (String con : cons) {
            model.addElement(con);
        }
        cb_con.setModel(model);
    }

    @Override
    public void initWindow() {
        pack();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setCommands();
    }

    public String getNombreCon(){
        return (String) cb_con.getSelectedItem();
    }
    public int getSpinner(){
        return (int) sp_but.getValue();
    }


    @Override
    public void showWindow() {

    }

    @Override
    public void closeWindow() {

    }

    @Override
    public void setCommands() {
        btn_buy.setActionCommand(BUY);

    }

    @Override
    public void addListener(ActionListener listener) {
        btn_buy.addActionListener(listener);

    }

    @Override
    public void initComponents() {

    }
}
