import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.math.BigDecimal;
import java.sql.*;
import java.util.*;
import java.util.List;

public class Splitwise extends JFrame {

    // --- Nested Classes ---
    static class Member {
        int id; String name;
        Member(int id, String name){ this.id=id; this.name=name;}
        public String toString(){ return name+" (ID:"+id+")";}
    }

    static class Expense {
        int id, payerId; String payerName, description;
        BigDecimal amount, sharePerPerson;
        List<String> participants;
        Expense(int id,int payerId,String payerName,BigDecimal amount,String description,List<String> participants,BigDecimal sharePerPerson){
            this.id=id; this.payerId=payerId; this.payerName=payerName; this.amount=amount;
            this.description=description; this.participants=participants; this.sharePerPerson=sharePerPerson;
        }
        String getParticipantsString(){ return String.join(", ", participants);}
    }

    // --- Database ---
    private static final String URL="jdbc:mysql://localhost:3306/splitwise_db";
    private static final String USER="root";
    private static final String PASS="password";

    public static Connection getConn() throws SQLException{ return DriverManager.getConnection(URL,USER,PASS); }

    public static void initDB(){
        try { Class.forName("com.mysql.cj.jdbc.Driver"); } catch(Exception e){ e.printStackTrace(); }
        try(Connection conn=getConn(); Statement stmt=conn.createStatement()){
            stmt.execute("CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL)");
            stmt.execute("CREATE TABLE IF NOT EXISTS expenses (id INT AUTO_INCREMENT PRIMARY KEY,payer_id INT NOT NULL,amount DECIMAL(10,2) NOT NULL,description VARCHAR(255),FOREIGN KEY (payer_id) REFERENCES members(id) ON DELETE CASCADE)");
            stmt.execute("CREATE TABLE IF NOT EXISTS expense_shares (id INT AUTO_INCREMENT PRIMARY KEY,expense_id INT NOT NULL,member_id INT NOT NULL,share DECIMAL(10,2) NOT NULL,FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE)");
            System.out.println("DB initialized");
        } catch(Exception e){ e.printStackTrace(); }
    }

    // --- GUI Components ---
    private DefaultListModel<Member> memberListModel=new DefaultListModel<>();
    private JList<Member> memberList=new JList<>(memberListModel);
    private DefaultTableModel expenseTableModel;
    private JTable expenseTable;
    private JTextArea balanceArea=new JTextArea();

    // --- Constructor ---
    public Splitwise(){
        setTitle("Splitwise"); setSize(900,600); setLocationRelativeTo(null); setDefaultCloseOperation(EXIT_ON_CLOSE);
        JTabbedPane tabbedPane=new JTabbedPane();
        tabbedPane.addTab("Members",membersPanel()); tabbedPane.addTab("Expenses",expensesPanel()); tabbedPane.addTab("Balances",balancesPanel());
        add(tabbedPane);
        refreshMembers(); refreshExpenses(); refreshBalances();
    }

    // --- Panels ---
    private JPanel membersPanel(){
        JPanel panel=new JPanel(new BorderLayout(10,10));
        panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
        memberList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        panel.add(new JScrollPane(memberList),BorderLayout.CENTER);
        JPanel btnPanel=new JPanel(new FlowLayout());
        JButton addBtn=new JButton("Add"); addBtn.addActionListener(e->addMember());
        JButton delBtn=new JButton("Delete"); delBtn.addActionListener(e->deleteMember());
        btnPanel.add(addBtn); btnPanel.add(delBtn); panel.add(btnPanel,BorderLayout.SOUTH);
        return panel;
    }

    private JPanel expensesPanel(){
        JPanel panel=new JPanel(new BorderLayout(10,10));
        panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
        String[] cols={"ID","Payer","Amount","Description","Participants","Share/Person"};
        expenseTableModel=new DefaultTableModel(cols,0){ public boolean isCellEditable(int r,int c){ return false;} };
        expenseTable=new JTable(expenseTableModel);
        panel.add(new JScrollPane(expenseTable),BorderLayout.CENTER);
        JPanel btnPanel=new JPanel(new FlowLayout());
        JButton addBtn=new JButton("Add"); addBtn.addActionListener(e->addExpense());
        JButton delBtn=new JButton("Delete"); delBtn.addActionListener(e->deleteExpense());
        JButton refBtn=new JButton("Refresh"); refBtn.addActionListener(e->{ refreshExpenses(); refreshBalances(); });
        btnPanel.add(addBtn); btnPanel.add(delBtn); btnPanel.add(refBtn); panel.add(btnPanel,BorderLayout.SOUTH);
        return panel;
    }

    private JPanel balancesPanel(){
        JPanel panel=new JPanel(new BorderLayout(10,10));
        panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
        balanceArea.setFont(new Font("Monospaced",Font.PLAIN,14)); balanceArea.setEditable(false);
        panel.add(new JScrollPane(balanceArea),BorderLayout.CENTER);
        JButton refBtn=new JButton("Refresh"); refBtn.addActionListener(e->refreshBalances()); panel.add(refBtn,BorderLayout.SOUTH);
        return panel;
    }

    // --- Member Functions ---
    private void addMember(){
        String name=JOptionPane.showInputDialog(this,"Enter name:"); if(name==null || name.trim().isEmpty()) return;
        try(Connection conn=getConn(); PreparedStatement ps=conn.prepareStatement("INSERT INTO members(name) VALUES(?)")){
            ps.setString(1,name.trim()); ps.executeUpdate(); refreshMembers();
        }catch(Exception e){ JOptionPane.showMessageDialog(this,"Error: "+e.getMessage()); }
    }

    private void deleteMember(){
        Member sel=memberList.getSelectedValue(); if(sel==null){ JOptionPane.showMessageDialog(this,"Select member"); return;}
        int c=JOptionPane.showConfirmDialog(this,"Delete "+sel.name+"?"); if(c!=JOptionPane.YES_OPTION) return;
        try(Connection conn=getConn(); PreparedStatement ps=conn.prepareStatement("DELETE FROM members WHERE id=?")){
            ps.setInt(1,sel.id); ps.executeUpdate(); refreshMembers(); refreshExpenses(); refreshBalances();
        }catch(Exception e){ JOptionPane.showMessageDialog(this,"Error: "+e.getMessage()); }
    }

    private void refreshMembers(){
        memberListModel.clear();
        try(Connection conn=getConn(); Statement stmt=conn.createStatement(); ResultSet rs=stmt.executeQuery("SELECT id,name FROM members ORDER BY name")){
            while(rs.next()) memberListModel.addElement(new Member(rs.getInt("id"),rs.getString("name")));
        }catch(Exception e){ e.printStackTrace(); }
    }

    // --- Expense Functions ---
    private void addExpense(){
        try{
            List<Member> members=new ArrayList<>();
            try(Connection conn=getConn(); Statement stmt=conn.createStatement(); ResultSet rs=stmt.executeQuery("SELECT id,name FROM members ORDER BY name")){
                while(rs.next()) members.add(new Member(rs.getInt("id"),rs.getString("name")));
            }
            if(members.isEmpty()){ JOptionPane.showMessageDialog(this,"Add members first"); return;}
            String amountStr=JOptionPane.showInputDialog(this,"Enter amount:"); if(amountStr==null) return;
            BigDecimal amount=new BigDecimal(amountStr); if(amount.compareTo(BigDecimal.ZERO)<=0){ JOptionPane.showMessageDialog(this,"Amount > 0"); return;}
            String desc=JOptionPane.showInputDialog(this,"Enter description:"); if(desc==null) return;
            Member payer=(Member)JOptionPane.showInputDialog(this,"Select payer","Payer",JOptionPane.QUESTION_MESSAGE,null,members.toArray(),members.get(0));
            if(payer==null) return;
            JPanel panel=new JPanel(new GridLayout(0,1));
            List<JCheckBox> cbs=new ArrayList<>();
            for(Member m: members){ JCheckBox cb=new JCheckBox(m.name); if(m.id==payer.id) cb.setSelected(true); cbs.add(cb); panel.add(cb);}
            int res=JOptionPane.showConfirmDialog(this,panel,"Select participants",JOptionPane.OK_CANCEL_OPTION);
            if(res==JOptionPane.OK_OPTION){
                List<Integer> participantIds=new ArrayList<>();
                for(int i=0;i<cbs.size();i++) if(cbs.get(i).isSelected()) participantIds.add(members.get(i).id);
                if(participantIds.isEmpty()){ JOptionPane.showMessageDialog(this,"Select at least one participant"); return;}
                try(Connection conn=getConn()){
                    conn.setAutoCommit(false);
                    int expenseId;
                    try(PreparedStatement ps=conn.prepareStatement("INSERT INTO expenses(payer_id,amount,description) VALUES(?,?,?)",Statement.RETURN_GENERATED_KEYS)){
                        ps.setInt(1,payer.id); ps.setBigDecimal(2,amount); ps.setString(3,desc); ps.executeUpdate();
                        ResultSet rs=ps.getGeneratedKeys(); if(rs.next()) expenseId=rs.getInt(1); else throw new SQLException("Expense ID fail");
                    }
                    BigDecimal share=amount.divide(BigDecimal.valueOf(participantIds.size()),2,BigDecimal.ROUND_HALF_UP);
                    try(PreparedStatement ps=conn.prepareStatement("INSERT INTO expense_shares(expense_id,member_id,share) VALUES(?,?,?)")){
                        for(int mid: participantIds){ ps.setInt(1,expenseId); ps.setInt(2,mid); ps.setBigDecimal(3,share); ps.addBatch();}
                        ps.executeBatch();
                    }
                    conn.commit();
                }
                refreshExpenses(); refreshBalances();
            }
        }catch(Exception e){ JOptionPane.showMessageDialog(this,"Error: "+e.getMessage()); }
    }

    private void deleteExpense(){
        int row=expenseTable.getSelectedRow(); if(row==-1){ JOptionPane.showMessageDialog(this,"Select expense"); return;}
        int id=(int)expenseTableModel.getValueAt(row,0);
        int c=JOptionPane.showConfirmDialog(this,"Delete expense ID "+id+"?"); if(c!=JOptionPane.YES_OPTION) return;
        try(Connection conn=getConn(); PreparedStatement ps=conn.prepareStatement("DELETE FROM expenses WHERE id=?")){ ps.setInt(1,id); ps.executeUpdate();}
        catch(Exception e){ JOptionPane.showMessageDialog(this,"Error: "+e.getMessage());}
        refreshExpenses(); refreshBalances();
    }

    private void refreshExpenses(){
        expenseTableModel.setRowCount(0);
        String sql="SELECT e.id,e.payer_id,m.name AS payer_name,e.amount,e.description,GROUP_CONCAT(m2.name) AS participants,AVG(es.share) AS share_per_person " +
                "FROM expenses e JOIN members m ON e.payer_id=m.id " +
                "JOIN expense_shares es ON es.expense_id=e.id " +
                "JOIN members m2 ON es.member_id=m2.id " +
                "GROUP BY e.id ORDER BY e.id DESC";
        try(Connection conn=getConn(); Statement stmt=conn.createStatement(); ResultSet rs=stmt.executeQuery(sql)){
            while(rs.next()){
                List<String> parts=Arrays.asList(rs.getString("participants").split(","));
                expenseTableModel.addRow(new Object[]{
                        rs.getInt("id"),
                        rs.getString("payer_name"),
                        rs.getBigDecimal("amount"),
                        rs.getString("description"),
                        String.join(", ",parts),
                        rs.getBigDecimal("share_per_person")
                });
            }
        }catch(Exception e){ e.printStackTrace();}
    }

    // --- Balances ---
    private void refreshBalances(){
        balanceArea.setText("");
        try(Connection conn=getConn()){
            Map<String,BigDecimal> balances=new HashMap<>();
            try(Statement stmt=conn.createStatement(); ResultSet rs=stmt.executeQuery("SELECT m.name,SUM(e.amount) AS paid FROM expenses e JOIN members m ON e.payer_id=m.id GROUP BY m.id")){
                while(rs.next()) balances.put(rs.getString("name"),rs.getBigDecimal("paid"));
            }
            try(Statement stmt=conn.createStatement(); ResultSet rs=stmt.executeQuery("SELECT m.name,SUM(es.share) AS owes FROM expense_shares es JOIN members m ON es.member_id=m.id GROUP BY m.id")){
                while(rs.next()){
                    String n=rs.getString("name"); BigDecimal owe=rs.getBigDecimal("owes");
                    balances.put(n, balances.getOrDefault(n,BigDecimal.ZERO).subtract(owe));
                }
            }
            for(Map.Entry<String,BigDecimal> e: balances.entrySet()) balanceArea.append(e.getKey()+" : "+e.getValue()+"\n");
        }catch(Exception e){ e.printStackTrace();}
    }

    // --- Main ---
    public static void main(String[] args){
        initDB();
        SwingUtilities.invokeLater(()->{
            new Splitwise().setVisible(true);
        });
    }
}
