package org.dam39.database;



import java.sql.*;
import java.util.ArrayList;

public class TicketDAO extends Conexion {



        private Connection conexion;
        // Método para obtener todos los nombres de conciertos
        public ArrayList<String> obtenerNombresDeConciertos() throws SQLException {
            ArrayList<String> nombresConciertos = new ArrayList<>();
            if (!initDBConnection()) {
                throw new SQLException("ERROR AL CONECTAR CON LA DDBB");
            }
            try {
                    String query = "SELECT titulo FROM conciertos";
                 PreparedStatement preparedStatement = conexion.prepareStatement(query);
                 ResultSet rs = preparedStatement.executeQuery() ;

                // Recorrer los resultados de la consulta y agregar los títulos a la lista
                while (rs.next()) {
                    nombresConciertos.add(rs.getString("titulo"));
                }

            } catch (SQLException e) {
                e.printStackTrace();
                throw e;
            }

            return nombresConciertos;

    }

    public String comprarTicket(String token, int idUsuario, int idConcierto, int idButaca, String metodoPago) throws SQLException {
        String codigoTicket = null;

        if (conexion == null) {
            throw new SQLException("ERROR: No se pudo conectar con la base de datos.");
        }

        CallableStatement callableStatement = null;

        try {

            String query = "{ ? = call comprar_ticket(?, ?, ?, ?, ?) }";
            callableStatement = conexion.prepareCall(query);


            callableStatement.registerOutParameter(1, java.sql.Types.VARCHAR);
            callableStatement.setString(2, token);
            callableStatement.setInt(3, idUsuario);
            callableStatement.setInt(4, idConcierto);
            callableStatement.setInt(5, idButaca);
            callableStatement.setString(6, metodoPago);

            callableStatement.execute();

            codigoTicket = callableStatement.getString(1);

        } catch (SQLException e) {
            e.printStackTrace();
            throw new SQLException("Error al realizar la compra: " + e.getMessage());
        } finally {
            if (callableStatement != null) {
                callableStatement.close();
            }
        }

        return codigoTicket;  // Retornar el código del ticket generado
    }


    public int obtenerIdConciertoPorNombre(String nombreConcierto) throws SQLException {
        int conciertoId = 0;

        if (!initDBConnection()) {
            throw new SQLException("ERROR AL CONECTAR CON LA DDBB");
        }

        try {

            String query = "SELECT id FROM conciertos WHERE titulo = ?";
            PreparedStatement preparedStatement = conexion.prepareStatement(query);
            preparedStatement.setString(1, nombreConcierto);
            ResultSet rs = preparedStatement.executeQuery();

            if (rs.next()) {
                conciertoId = rs.getInt("id");
            } else {
                throw new SQLException("Concierto no encontrado con el nombre: " + nombreConcierto);
            }

        } catch (SQLException e) {
            e.printStackTrace();
            throw e;
        }

        return conciertoId;
    }



}
