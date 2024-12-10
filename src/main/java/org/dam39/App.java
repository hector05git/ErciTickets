package org.dam39;

import com.formdev.flatlaf.FlatDarkLaf;
import org.dam39.controllers.LoginDialogController;
import org.dam39.controllers.MainFrameController;
import org.dam39.controllers.TicketController;
import org.dam39.database.TicketDAO;
import org.dam39.views.LoginDialog;
import org.dam39.views.MainFrame;
import org.dam39.views.TicketCon;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        FlatDarkLaf.setup();
        MainFrame frame = new MainFrame();
        MainFrameController controller = new MainFrameController(frame);
        frame.addListener(controller);
        LoginDialog loginDialog = new LoginDialog();
        LoginDialogController controller1 = new LoginDialogController(loginDialog);
        loginDialog.addListener(controller1);
        TicketCon ticketCon = new TicketCon();
        TicketDAO ticketDAO = new TicketDAO();
        TicketController ticketController = new TicketController(ticketCon, ticketDAO);
        ticketCon.addListener(ticketController);
        new LoginDialog().showWindow();
    }
}
