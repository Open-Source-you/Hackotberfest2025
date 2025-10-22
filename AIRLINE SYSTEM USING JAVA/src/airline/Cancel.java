package airline;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class Cancel extends JFrame {

    // Text fields for input
    private JTextField passengerNoField, cancellationNoField, cancellationDateField, flightCodeField;

    public static void main(String[] args) {
        new Cancel();
    }

    // Constructor to initialize the frame
    public Cancel() {
        initialize();
    }

    // Method to set up the frame components
    private void initialize() {
        setTitle("CANCELLATION");
        getContentPane().setBackground(Color.WHITE);
        setBounds(100, 100, 860, 500);
        setLayout(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Title label
        JLabel cancellationLabel = new JLabel("CANCELLATION");
        cancellationLabel.setFont(new Font("Tahoma", Font.PLAIN, 31));
        cancellationLabel.setBounds(185, 24, 259, 38);
        add(cancellationLabel);

        // Image for cancellation
        ImageIcon cancelIcon = new ImageIcon(ClassLoader.getSystemResource("icon/cancel.png"));
        Image scaledImage = cancelIcon.getImage().getScaledInstance(250, 250, Image.SCALE_DEFAULT);
        JLabel cancelImageLabel = new JLabel(new ImageIcon(scaledImage));
        cancelImageLabel.setBounds(470, 100, 250, 250);
        add(cancelImageLabel);

        // Labels and text fields for cancellation information
        setupLabel("PASSENGER NO", 60, 100, 132, 26);
        passengerNoField = createTextField(250, 100);

        setupLabel("CANCELLATION NO", 60, 150, 150, 27);
        cancellationNoField = createTextField(250, 150);

        setupLabel("CANCELLATION DATE", 60, 200, 180, 27);
        cancellationDateField = createTextField(250, 200);

        setupLabel("FLIGHT CODE", 60, 300, 150, 27);
        flightCodeField = createTextField(250, 300);

        // Cancel button
        JButton cancelButton = new JButton("CANCEL");
        cancelButton.setFont(new Font("Tahoma", Font.PLAIN, 14));
        cancelButton.setBackground(Color.BLACK);
        cancelButton.setForeground(Color.BLACK);
        cancelButton.setBounds(250, 350, 150, 30);
        add(cancelButton);

        // Action listener for the cancel button
        cancelButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ae) {
                handleCancellation();
            }
        });

        // Frame settings
        setVisible(true);
        setLocation(400, 200);
    }

    // Helper method to set up labels
    private void setupLabel(String text, int x, int y, int width, int height) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("Tahoma", Font.PLAIN, 17));
        label.setBounds(x, y, width, height);
        add(label);
    }

    // Helper method to create text fields
    private JTextField createTextField(int x, int y) {
        JTextField textField = new JTextField();
        textField.setBounds(x, y, 150, 27);
        add(textField);
        return textField;
    }

    // Method to handle ticket cancellation logic
    private void handleCancellation() {
        String passengerNo = passengerNoField.getText();
        String cancellationNo = cancellationNoField.getText();
        String cancellationDate = cancellationDateField.getText();
        String flightCode = flightCodeField.getText();

        try {
            // Assuming 'conn' is a class handling database connection
            conn connection = new conn();
            String query = "INSERT INTO cancellation (passenger_no, cancellation_no, cancellation_date, flight_code) " +
                           "VALUES (?, ?, ?, ?)";
            PreparedStatement pstmt = ((Object) connection).prepareStatement(query);
            pstmt.setString(1, passengerNo);
            pstmt.setString(2, cancellationNo);
            pstmt.setString(3, cancellationDate);
            pstmt.setString(4, flightCode);

            pstmt.executeUpdate();
            JOptionPane.showMessageDialog(null, "Ticket Canceled");
            setVisible(false);

        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error: Failed to cancel the ticket");
        }
    }
}
