class Fibonacci{
    public static void main(String[] args) {
        int num=0,num2=1,num3=1,count=1;
        while(count<=15)
        {
            System.out.print(num3+",");
            num3=num+num2;
            num=num2;
            num2=num3;
            count++;
        }
    }
}
