package org.dam39.controllers;

import org.dam39.database.TicketDAO;
import org.dam39.views.TicketCon;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.SQLException;
import java.util.ArrayList;

public class TicketController  implements ActionListener {


    public static final String BUY = "BUY";
    private TicketCon ticketCon;
    private TicketDAO ticketDAO;
    public  TicketController (TicketCon ticketCon, TicketDAO ticketDAO) {
        this.ticketCon = ticketCon;
        this.ticketDAO = ticketDAO;
        handleLoadComboBox();

    }
    public void handleLoadComboBox(){
        try {
            ArrayList <String> cons = ticketDAO.obtenerNombresDeConciertos();
            ticketCon.loadComboBox(cons);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public void handleBuy(){
        try {
            int id = ticketDAO.obtenerIdConciertoPorNombre(ticketCon.getNombreCon());
            //ticketDAO.comprarTicket();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }


    @Override
    public void actionPerformed(ActionEvent e) {
        switch (e.getActionCommand()) {
            case BUY:
                handleBuy();
                break;
        }

    }
}
