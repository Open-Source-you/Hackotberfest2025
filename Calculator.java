import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
public class Calculator implements ActionListener 
{
	JFrame calc;
		
	ImageIcon icon;

	JButton numButtons[] = new JButton[10];
	JButton funcButtons[] = new JButton[10];

	JButton zero;
	JButton dot;
	JButton plus;
	JButton one;
	JButton two;
	JButton three;
	JButton minus;
	JButton four;
	JButton five;
	JButton six;
	JButton multi;
	JButton seven;
	JButton eight;
	JButton nine;
	JButton div;
	JButton equal;
	JButton c;
	JButton del;
	JButton percent;
		
	JTextField calc1;
		
	JLabel jLabel;

	double num1=0,num2=0,result=0;
	char operator;

		Calculator() {
		Font btn=new Font("Arial",Font.PLAIN,30);
		Font btn1=new Font("Arial",Font.BOLD,20);

		calc=new JFrame("Calculator");
		calc.setSize(300,350);
		calc.setLocation(500,200);
		calc.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		calc.setLayout(null);		

		icon=new ImageIcon("calc-icon.png");
		calc.setIconImage(icon.getImage());
		
		Container cont=calc.getContentPane();
		cont.setBackground(Color.BLACK);

		Color color=new Color(255,132,0);
		Color color1=new Color(64,64,64);

		Cursor cur=new Cursor(Cursor.HAND_CURSOR);

		zero=new JButton("0");
		zero.setSize(150,50);
		zero.setLocation(0,270);
		zero.setFont(btn1);
		zero.setBackground(Color.GRAY);
		zero.setForeground(Color.WHITE);
		zero.setCursor(cur);
		zero.setFocusable(false);
		numButtons[0]=zero;
		
		dot=new JButton(".");
		dot.setSize(75,50);
		dot.setLocation(150,270);
		dot.setFont(btn1);
		dot.setBackground(Color.GRAY);
		dot.setForeground(Color.WHITE);
		dot.setCursor(cur);
		dot.setFocusable(false);
		funcButtons[0]=dot;
		
		plus=new JButton("+");
		plus.setSize(75,50);
		plus.setLocation(225,220);
		plus.setFont(btn1);
		plus.setBackground(color);
		plus.setForeground(Color.WHITE);
		plus.setCursor(cur);
		plus.setFocusable(false);
		funcButtons[1]=plus;
		
		one=new JButton("1");
		one.setSize(75,50);
		one.setLocation(0,220);
		one.setFont(btn1);
		one.setBackground(Color.GRAY);
		one.setForeground(Color.WHITE);
		one.setCursor(cur);
		one.setFocusable(false);
		numButtons[1]=one;
		
		two=new JButton("2");
		two.setSize(75,50);
		two.setLocation(75,220);
		two.setFont(btn1);
		two.setBackground(Color.GRAY);
		two.setForeground(Color.WHITE);
		two.setCursor(cur);
		two.setFocusable(false);
		numButtons[2]=two;
		
		three=new JButton("3");
		three.setSize(75,50);
		three.setLocation(150,220);
		three.setFont(btn1);
		three.setBackground(Color.GRAY);
		three.setForeground(Color.WHITE);
		three.setCursor(cur);
		three.setFocusable(false);
		numButtons[3]=three; 
		
		minus=new JButton("-");
		minus.setSize(75,50);
		minus.setLocation(225,170);
		minus.setFont(btn1);
		minus.setBackground(color);
		minus.setForeground(Color.WHITE);
		minus.setCursor(cur);
		minus.setFocusable(false);
		funcButtons[2]=minus;
		
		four=new JButton("4");
		four.setSize(75,50);
		four.setLocation(0,170);
		four.setFont(btn1);
		four.setBackground(Color.GRAY);
		four.setForeground(Color.WHITE);
		four.setCursor(cur);
		four.setFocusable(false);
		numButtons[4]=four;
		
		five=new JButton("5");
		five.setSize(75,50);
		five.setLocation(75,170);
		five.setFont(btn1);
		five.setBackground(Color.GRAY);
		five.setForeground(Color.WHITE);
		five.setCursor(cur);
		five.setFocusable(false);
		numButtons[5]=five;
		
		six=new JButton("6");
		six.setSize(75,50);
		six.setLocation(150,170);
		six.setFont(btn1);
		six.setBackground(Color.GRAY);
		six.setForeground(Color.WHITE);
		six.setCursor(cur);
		six.setFocusable(false);
		numButtons[6]=six;
		
		multi=new JButton("x");
		multi.setSize(75,50);
		multi.setLocation(225,120);
		multi.setFont(btn1);
		multi.setBackground(color);
		multi.setForeground(Color.WHITE);
		multi.setCursor(cur);
		multi.setFocusable(false);
		funcButtons[3]=multi;
		
		seven=new JButton("7");
		seven.setSize(75,50);
		seven.setLocation(0,120);
		seven.setFont(btn1);
		seven.setBackground(Color.GRAY);
		seven.setForeground(Color.WHITE);
		seven.setCursor(cur);
		seven.setFocusable(false);
		numButtons[7]=seven;
		
		eight=new JButton("8");
		eight.setSize(75,50);
		eight.setLocation(75,120);
		eight.setFont(btn1);
		eight.setBackground(Color.GRAY);
		eight.setForeground(Color.WHITE);
		eight.setCursor(cur);
		eight.setFocusable(false);
		numButtons[8]=eight;
		
		nine=new JButton("9");
		nine.setSize(75,50);
		nine.setLocation(150,120);
		nine.setFont(btn1);
		nine.setBackground(Color.GRAY);
		nine.setForeground(Color.WHITE);
		nine.setCursor(cur);
		nine.setFocusable(false);
		numButtons[9]=nine;
		
		div=new JButton("/");
		div.setSize(75,50);
		div.setLocation(225,70);
		div.setFont(btn1);
		div.setBackground(color);
		div.setForeground(Color.WHITE);
		div.setCursor(cur);
		div.setFocusable(false);
		funcButtons[4]=div;
		
		equal=new JButton("=");
		equal.setSize(75,50);
		equal.setLocation(225,270);
		equal.setFont(btn1);
		equal.setBackground(color);
		equal.setForeground(Color.WHITE);
		equal.setCursor(cur);
		equal.setFocusable(false);
		funcButtons[5]=equal;

		c=new JButton("C");
		c.setSize(75,50);
		c.setLocation(0,70);
		c.setFont(btn1);
		c.setBackground(color1);
		c.setForeground(Color.WHITE);
		c.setCursor(cur);
		c.setFocusable(false);
		funcButtons[6]=c;

		del=new JButton("Del");
		del.setSize(75,50);
		del.setLocation(75,70);
		del.setFont(btn1);
		del.setBackground(color1);
		del.setForeground(Color.WHITE);
		del.setCursor(cur);
		del.setFocusable(false);
		funcButtons[8]=del;

		percent=new JButton("%");
		percent.setSize(75,50);
		percent.setLocation(150,70);
		percent.setFont(btn1);
		percent.setBackground(color1);
		percent.setForeground(Color.WHITE);
		percent.setCursor(cur);
		percent.setFocusable(false);
		funcButtons[7]=percent;	
		
		calc1=new JTextField();
		calc1.setSize(300,70);
		calc1.setLocation(0,0);
		calc1.setFont(btn1);
		calc1.setBackground(Color.BLACK);
		calc1.setForeground(Color.WHITE);
		calc1.setEditable(false);	
		
		calc.add(zero);
		calc.add(dot);
		calc.add(plus);
		calc.add(one);
		calc.add(two);
		calc.add(three);
		calc.add(minus);
		calc.add(four);
		calc.add(five);
		calc.add(six);
		calc.add(multi);
		calc.add(seven);
		calc.add(eight);
		calc.add(nine);
		calc.add(c);
		calc.add(del);
		calc.add(percent);
		calc.add(div);
		calc.add(equal);
		calc.add(calc1);

		for(int i=0;i<9;i++)
		{
			funcButtons[i].addActionListener(this);
		}
		for(int i=0;i<10;i++)
		{

			numButtons[i].addActionListener(this);
		}

		calc.setResizable(false);

		calc.setVisible(true);
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		for (int i=0;i<10;i++) {
			if (e.getSource().equals(numButtons[i])){
				calc1.setText(calc1.getText().concat(String.valueOf(i)));
			}
		}
		if (e.getSource().equals(dot)){
			calc1.setText(calc1.getText().concat("."));
		}
		if (e.getSource().equals(plus)){
			num1=Double.parseDouble(calc1.getText());
			operator='+';
			calc1.setText("");
		}
		if (e.getSource().equals(minus)){
			num1=Double.parseDouble(calc1.getText());
			operator='-';
			calc1.setText("");
		}
		if (e.getSource().equals(multi)){
			num1=Double.parseDouble(calc1.getText());
			operator='*';
			calc1.setText("");
		}
		if (e.getSource().equals(div)){
			num1=Double.parseDouble(calc1.getText());
			operator='/';
			calc1.setText("");
		}
		if (e.getSource().equals(percent)){
			num1=Double.parseDouble(calc1.getText());
			operator='%';
			calc1.setText("");
		}
		if(e.getSource().equals(equal)){
			num2=Double.parseDouble(calc1.getText());
			switch(operator){
			case'+':
				result=num1+num2;
				break;
			case'-':
				result=num1-num2;
				break;
			case'*':
				result=num1*num2;
				break;
			case'/':
				result=num1/num2;
				break;
			case'%':
				result=num1%num2;
				break;		 
			}
			calc1.setText(String.valueOf(result));
			num1=result;
		}
		if(e.getSource().equals(c)){
			calc1.setText("");
		}
		if(e.getSource().equals(del)){
			String string=calc1.getText();
			calc1.setText("");
			for(int i=0;i<string.length()-1;i++){
				calc1.setText(calc1.getText()+string.charAt(i));
			}
		}
	}
}
