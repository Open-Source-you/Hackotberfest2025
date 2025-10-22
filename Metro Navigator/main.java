import java.util.*;
import java.io.*;

	
	public class main 
	{
		public class Stop 
		{
			HashMap<String, Integer> mapp = new HashMap<>();
		}

		static HashMap<String, Stop> stps;

		public main() 
		{
			stps = new HashMap<>();
		}

		public int numstps() 
		{
			return this.stps.size();
		}

		public boolean containsStop(String sname) 
		{
			return this.stps.containsKey(sname);
		}

		public void addStop(String sname) 
		{
			Stop stp = new Stop();
			stps.put(sname, stp);
		}

		public void removeStop(String sname) 
		{
			Stop stp = stps.get(sname);
			ArrayList<String> keys = new ArrayList<>(stp.mapp.keySet());

			for (String key : keys) 
			{
				Stop nbrstp = stps.get(key);
				nbrstp.mapp.remove(sname);
			}

			stps.remove(sname);
		}

		public int numStop() 
		{
			ArrayList<String> keys = new ArrayList<>(stps.keySet());
			int count = 0;

			for (String key : keys) 
			{
				Stop stp = stps.get(key);
				count = count + stp.mapp.size();
			}

			return count / 2;
		}

		public boolean containsStop(String sname1, String sname2) 
		{
			Stop stp1 = stps.get(sname1);
			Stop stp2 = stps.get(sname2);
			
			if (stp1 == null || stp2 == null || !stp1.mapp.containsKey(sname2)) {
				return false;
			}

			return true;
		}

		public void addStop(String sname1, String sname2, int value) 
		{
			Stop stp1 = stps.get(sname1); 
			Stop stp2 = stps.get(sname2); 

			if (stp1 == null || stp2 == null || stp1.mapp.containsKey(sname2)) {
				return;
			}

			stp1.mapp.put(sname2, value);
			stp2.mapp.put(sname1, value);
		}

		public void removeStop(String sname1, String sname2) 
		{
			Stop stp1 = stps.get(sname1);
			Stop stp2 = stps.get(sname2);
			
			//check if the vertices given or the edge between these vertices exist or not
			if (stp1 == null || stp2 == null || !stp1.mapp.containsKey(sname2)) {
				return;
			}

			stp1.mapp.remove(sname2);
			stp2.mapp.remove(sname1);
		}

		public void display_Map() 
		{
			System.out.println("\t Delhi Metro Map");
			System.out.println("\t------------------");
			System.out.println("----------------------------------------------------\n");
			ArrayList<String> keys = new ArrayList<>(stps.keySet());

			for (String key : keys) 
			{
				String str = key + " =>\n";
				Stop stp = stps.get(key);
				ArrayList<String> stpmapp = new ArrayList<>(stp.mapp.keySet());
				
				for (String nbr : stpmapp)
				{
					str = str + "\t" + nbr + "\t";
                    			if (nbr.length()<16)
                    			str = str + "\t";
                    			if (nbr.length()<8)
                    			str = str + "\t";
                    			str = str + stp.mapp.get(nbr) + "\n";
				}
				System.out.println(str);
			}
			System.out.println("\t------------------");
			System.out.println("---------------------------------------------------\n");

		}
		
		public void display_Stations() 
		{
			System.out.println("\n***********************************************************************\n");
			ArrayList<String> keys = new ArrayList<>(stps.keySet());
			int i=1;
			for(String key : keys) 
			{
				System.out.println(i + ". " + key);
				i++;
			}
			System.out.println("\n***********************************************************************\n");
		}
			
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		public boolean hasPath(String sname1, String sname2, HashMap<String, Boolean> process) 
		{
			// DIR EDGE
			if (containsStop(sname1, sname2)) {
				return true;
			}

			//MARK AS DONE
			process.put(sname1, true);

			Stop stp = stps.get(sname1);
			ArrayList<String> mapp = new ArrayList<>(stp.mapp.keySet());

			//TRAVERSE THE mapp OF THE Stop
			for (String nbr : mapp) 
			{

				if (!process.containsKey(nbr))
					if (hasPath(nbr, sname2, process))
						return true;
			}

			return false;
		}
		
		
		private class DijkstraPair implements Comparable<DijkstraPair> 
		{
			String sname;
			String psf;
			int cost;

			/*
			The compareTo method is defined in Java.lang.Comparable.
			Here, we override the method because the conventional compareTo method
			is used to compare strings,integers and other primitive data types. But
			here in this case, we intend to compare two objects of DijkstraPair class.
			*/ 

			/*
			Removing the overriden method gives us this errror:
			The type Graph_M.DijkstraPair must implement the inherited abstract method Comparable<Graph_M.DijkstraPair>.compareTo(Graph_M.DijkstraPair)

			This is because DijkstraPair is not an abstract class and implements Comparable interface which has an abstract 
			method compareTo. In order to make our class concrete(a class which provides implementation for all its methods)
			we have to override the method compareTo
			 */
			@Override
			public int compareTo(DijkstraPair o) 
			{
				return o.cost - this.cost;
			}
		}
		
		public int dijkstra(String src, String des, boolean nan) 
		{
			int val = 0;
			ArrayList<String> ans = new ArrayList<>();
			HashMap<String, DijkstraPair> map = new HashMap<>();

			file1<DijkstraPair> heap = new file1<>();

			for (String key : stps.keySet()) 
			{
				DijkstraPair np = new DijkstraPair();
				np.sname = key;
				//np.psf = "";
				np.cost = Integer.MAX_VALUE;

				if (key.equals(src)) 
				{
					np.cost = 0;
					np.psf = key;
				}

				heap.add(np);
				map.put(key, np);
			}

			//keep removing the pairs while heap is not empty
			while (!heap.isEmpty()) 
			{
				DijkstraPair rp = heap.remove();
				
				if(rp.sname.equals(des))
				{
					val = rp.cost;
					break;
				}
				
				map.remove(rp.sname);

				ans.add(rp.sname);
				
				Stop v = stps.get(rp.sname);
				for (String nbr : v.mapp.keySet()) 
				{
					if (map.containsKey(nbr)) 
					{
						int oc = map.get(nbr).cost;
						Stop k = stps.get(rp.sname);
						int nc;
						if(nan)
							nc = rp.cost + 120 + 40*k.mapp.get(nbr);
						else
							nc = rp.cost + k.mapp.get(nbr);

						if (nc < oc) 
						{
							DijkstraPair gp = map.get(nbr);
							gp.psf = rp.psf + nbr;
							gp.cost = nc;

							heap.updatePriority(gp);
						}
					}
				}
			}
			return val;
		}
		
		private class Pair 
		{
			String sname;
			String psf;
			int min_dis;
			int min_time;
		}
		
		public String MIN_DIST(String src, String dst) 
		{
			int min = Integer.MAX_VALUE;
			//int time = 0;
			String ans = "";
			HashMap<String, Boolean> process = new HashMap<>();
			LinkedList<Pair> stack = new LinkedList<>();

			// create a new pair
			Pair sp = new Pair();
			sp.sname = src;
			sp.psf = src + "  ";
			sp.min_dis = 0;
			sp.min_time = 0;
			
			// put the new pair in stack
			stack.addFirst(sp);

			// while stack is not empty keep on doing the work
			while (!stack.isEmpty()) 
			{
				// remove a pair from stack
				Pair rp = stack.removeFirst();

				if (process.containsKey(rp.sname)) 
				{
					continue;
				}

				// process put
				process.put(rp.sname, true);
				
				//if there exists a direct edge b/w removed pair and destination Stop
				if (rp.sname.equals(dst)) 
				{
					int temp = rp.min_dis;
					if(temp<min) {
						ans = rp.psf;
						min = temp;
					}
					continue;
				}

				Stop rpstp = stps.get(rp.sname);
				ArrayList<String> mapp = new ArrayList<>(rpstp.mapp.keySet());

				for(String nbr : mapp) 
				{
					// process only unprocess mapp
					if (!process.containsKey(nbr)) {

						// make a new pair of nbr and put in queue
						Pair np = new Pair();
						np.sname = nbr;
						np.psf = rp.psf + nbr + "  ";
						np.min_dis = rp.min_dis + rpstp.mapp.get(nbr); 
						//np.min_time = rp.min_time + 120 + 40*rpstp.mapp.get(nbr); 
						stack.addFirst(np);
					}
				}
			}
			ans = ans + Integer.toString(min);
			return ans;
		}
		
		
		public String MIN_TIME(String src, String dst) 
		{
			int min = Integer.MAX_VALUE;
			String ans = "";
			HashMap<String, Boolean> process = new HashMap<>();
			LinkedList<Pair> stack = new LinkedList<>();

			// create a new pair
			Pair sp = new Pair();
			sp.sname = src;
			sp.psf = src + "  ";
			sp.min_dis = 0;
			sp.min_time = 0;
			
			// put the new pair in queue
			stack.addFirst(sp);

			// while queue is not empty keep on doing the work
			while (!stack.isEmpty()) {

				// remove a pair from queue
				Pair rp = stack.removeFirst();

				if (process.containsKey(rp.sname)) 
				{
					continue;
				}

				// process put
				process.put(rp.sname, true);

				//if there exists a direct edge b/w removed pair and destination Stop
				if (rp.sname.equals(dst)) 
				{
					int temp = rp.min_time;
					if(temp<min) {
						ans = rp.psf;
						min = temp;
					}
					continue;
				}

				Stop rpstp = stps.get(rp.sname);
				ArrayList<String> mapp = new ArrayList<>(rpstp.mapp.keySet());

				for (String nbr : mapp) 
				{
					// process only unprocess mapp
					if (!process.containsKey(nbr)) {

						// make a new pair of nbr and put in queue
						Pair np = new Pair();
						np.sname = nbr;
						np.psf = rp.psf + nbr + "  ";
						//np.min_dis = rp.min_dis + rpstp.mapp.get(nbr);
						np.min_time = rp.min_time + 120 + 40*rpstp.mapp.get(nbr); 
						stack.addFirst(np);
					}
				}
			}
			Double minutes = Math.ceil((double)min / 60);
			ans = ans + Double.toString(minutes);
			return ans;
		}
		
		public ArrayList<String> get_Interchanges(String str)
		{
			ArrayList<String> arr = new ArrayList<>();
			String res[] = str.split("  ");
			arr.add(res[0]);
			int count = 0;
			for(int i=1;i<res.length-1;i++)
			{
				int index = res[i].indexOf('~');
				String s = res[i].substring(index+1);
				
				if(s.length()==2)
				{
					String prev = res[i-1].substring(res[i-1].indexOf('~')+1);
					String next = res[i+1].substring(res[i+1].indexOf('~')+1);
					
					if(prev.equals(next)) 
					{
						arr.add(res[i]);
					}
					else
					{
						arr.add(res[i]+" ==> "+res[i+1]);
						i++;
						count++;
					}
				}
				else
				{
					arr.add(res[i]);
				}
			}
			arr.add(Integer.toString(count));
			arr.add(res[res.length-1]);
			return arr;
		}
		
		public static void Create_Metro_Map(main g)
		{
			g.addStop("Noida Sector 62~B");
			g.addStop("Botanical Garden~B");
			g.addStop("Yamuna Bank~B");
			g.addStop("Rajiv Chowk~BY");
			g.addStop("Vaishali~B");
			g.addStop("Moti Nagar~B");
			g.addStop("Janak Puri West~BO");
			g.addStop("Dwarka Sector 21~B");
			g.addStop("Huda City Center~Y");
			g.addStop("Saket~Y");
			g.addStop("Vishwavidyalaya~Y");
			g.addStop("Chandni Chowk~Y");
			g.addStop("New Delhi~YO");
			g.addStop("AIIMS~Y");
			g.addStop("Shivaji Stadium~O");
			g.addStop("DDS Campus~O");
			g.addStop("IGI Airport~O");
			g.addStop("Rajouri Garden~BP");
			g.addStop("Netaji Subhash Place~PR");
			g.addStop("Punjabi Bagh West~P");
			
			g.addStop("Noida Sector 62~B", "Botanical Garden~B", 8);
			g.addStop("Botanical Garden~B", "Yamuna Bank~B", 10);
			g.addStop("Yamuna Bank~B", "Vaishali~B", 8);
			g.addStop("Yamuna Bank~B", "Rajiv Chowk~BY", 6);
			g.addStop("Rajiv Chowk~BY", "Moti Nagar~B", 9);
			g.addStop("Moti Nagar~B", "Janak Puri West~BO", 7);
			g.addStop("Janak Puri West~BO", "Dwarka Sector 21~B", 6);
			g.addStop("Huda City Center~Y", "Saket~Y", 15);
			g.addStop("Saket~Y", "AIIMS~Y", 6);
			g.addStop("AIIMS~Y", "Rajiv Chowk~BY", 7);
			g.addStop("Rajiv Chowk~BY", "New Delhi~YO", 1);
			g.addStop("New Delhi~YO", "Chandni Chowk~Y", 2);
			g.addStop("Chandni Chowk~Y", "Vishwavidyalaya~Y", 5);
			g.addStop("New Delhi~YO", "Shivaji Stadium~O", 2);
			g.addStop("Shivaji Stadium~O", "DDS Campus~O", 7);
			g.addStop("DDS Campus~O", "IGI Airport~O", 8);
			g.addStop("Moti Nagar~B", "Rajouri Garden~BP", 2);
			g.addStop("Punjabi Bagh West~P", "Rajouri Garden~BP", 2);
			g.addStop("Punjabi Bagh West~P", "Netaji Subhash Place~PR", 3);
		}
		
		public static String[] printCodelist()
		{
			System.out.println("List of station along with their codes:\n");
			ArrayList<String> keys = new ArrayList<>(stps.keySet());
			int i=1,j=0,m=1;
			StringTokenizer stname;
			String temp="";
			String codes[] = new String[keys.size()];
			char c;
			for(String key : keys) 
			{
				stname = new StringTokenizer(key);
				codes[i-1] = "";
				j=0;
				while (stname.hasMoreTokens())
				{
				        temp = stname.nextToken();
				        c = temp.charAt(0);
				        while (c>47 && c<58)
				        {
				                codes[i-1]+= c;
				                j++;
				                c = temp.charAt(j);
				        }
				        if ((c<48 || c>57) && c<123)
				                codes[i-1]+= c;
				}
				if (codes[i-1].length() < 2)
					codes[i-1]+= Character.toUpperCase(temp.charAt(1));
				            
				System.out.print(i + ". " + key + "\t");
				if (key.length()<(22-m))
                    			System.out.print("\t");
				if (key.length()<(14-m))
                    			System.out.print("\t");
                    		if (key.length()<(6-m))
                    			System.out.print("\t");
                    		System.out.println(codes[i-1]);
				i++;
				if (i == (int)Math.pow(10,m))
				        m++;
			}
			return codes;
		}
		
		public static void main(String[] args) throws IOException
		{
			main g = new main();
			Create_Metro_Map(g);
			
			System.out.println("\n\t\t\t****WELCOME TO THE METRO APP*****");
			
			BufferedReader inp = new BufferedReader(new InputStreamReader(System.in));
			// int choice = Integer.parseInt(inp.readLine());
			
			while(true)
			{
			System.out.println("               Please select an option:\n");
			
			System.out.println("1) [LIST] Know all the stations on the map");
			System.out.println("2) [MAP] Show the metro map");
			System.out.println("3) [DISTANCE] Get shortest distance from 'source' to 'destination' station");
			System.out.println("4) [TIME] Get shortest time to reach from 'source' to 'destination' station");
			System.out.println("5) [PATH - DISTANCE] Get shortest path (distance-wise) from 'source' to 'destination'");
			System.out.println("6) [PATH - TIME] Get shortest path (time-wise) from 'source' to 'destination'");
			System.out.println("7) [EXIT] Exit the application\n");
			
			System.out.print("Enter your choice (1-7): ");
			
				int choice = -1;
				try {
					choice = Integer.parseInt(inp.readLine());
				} catch(Exception e) {
					// default will handle
				}
				System.out.print("\n***********************************************************\n");
				if(choice == 7)
				{
					System.exit(0);
				}
				switch(choice)
				{
				case 1:
					g.display_Stations();
					break;
			
				case 2:
					g.display_Map();
					break;
				
				case 3:
					ArrayList<String> keys = new ArrayList<>(stps.keySet());
					String codes[] = printCodelist();
					System.out.println("\n1. TO ENTER SERIAL NO. OF STATIONS\n2. TO ENTER CODE OF STATIONS\n3. TO ENTER NAME OF STATIONS\n");
					System.out.println("ENTER YOUR CHOICE:");
				        int ch = Integer.parseInt(inp.readLine());
					int j;
						
					String st1 = "", st2 = "";
					System.out.println("ENTER THE SOURCE AND DESTINATION STATIONS");
					if (ch == 1)
					{
					    st1 = keys.get(Integer.parseInt(inp.readLine())-1);
					    st2 = keys.get(Integer.parseInt(inp.readLine())-1);
					}
					else if (ch == 2)
					{
					    String a,b;
					    a = (inp.readLine()).toUpperCase();
					    for (j=0;j<keys.size();j++)
					       if (a.equals(codes[j]))
					           break;
					    st1 = keys.get(j);
					    b = (inp.readLine()).toUpperCase();
					    for (j=0;j<keys.size();j++)
					       if (b.equals(codes[j]))
					           break;
					    st2 = keys.get(j);
					}
					else if (ch == 3)
					{
					    st1 = inp.readLine();
					    st2 = inp.readLine();
					}
					else
					{
					    System.out.println("Invalid choice");
					    System.exit(0);
					}
				
					HashMap<String, Boolean> process = new HashMap<>();
					if(!g.containsStop(st1) || !g.containsStop(st2) || !g.hasPath(st1, st2, process))
						System.out.println("THE INPUTS ARE INVALID");
					else
					System.out.println("SHORTEST DISTANCE FROM "+st1+" TO "+st2+" IS "+g.dijkstra(st1, st2, false)+"KM\n");
					break;
				
				case 4:
					System.out.print("ENTER THE SOURCE STATION: ");
					String sat1 = inp.readLine();
					System.out.print("ENTER THE DESTINATION STATION: ");
					String sat2 = inp.readLine();
				
					HashMap<String, Boolean> process1= new HashMap<>();				
					System.out.println("SHORTEST TIME FROM ("+sat1+") TO ("+sat2+") IS "+g.dijkstra(sat1, sat2, true)/60+" MINUTES\n\n");
					break;
				
				case 5:
					System.out.println("ENTER THE SOURCE AND DESTINATION STATIONS");
					String s1 = inp.readLine();
					String s2 = inp.readLine();
				
					HashMap<String, Boolean> process2 = new HashMap<>();
					if(!g.containsStop(s1) || !g.containsStop(s2) || !g.hasPath(s1, s2, process2))
						System.out.println("THE INPUTS ARE INVALID");
					else 
					{
						ArrayList<String> str = g.get_Interchanges(g.MIN_DIST(s1, s2));
						int len = str.size();
						System.out.println("SOURCE STATION : " + s1);
						System.out.println("SOURCE STATION : " + s2);
						System.out.println("DISTANCE : " + str.get(len-1));
						System.out.println("NUMBER OF INTERCHANGES : " + str.get(len-2));
						//System.out.println(str);
						System.out.println("~~~~~~~~~~~~~");
						System.out.println("START  ==>  " + str.get(0));
						for(int i=1; i<len-3; i++)
						{
							System.out.println(str.get(i));
						}
						System.out.print(str.get(len-3) + "   ==>    END");
						System.out.println("\n~~~~~~~~~~~~~");
					}
					break;
				
				case 6:
					System.out.print("ENTER THE SOURCE STATION: ");
					String ss1 = inp.readLine();
					System.out.print("ENTER THE DESTINATION STATION: ");
					String ss2 = inp.readLine();
				
					HashMap<String, Boolean> process3 = new HashMap<>();
					if(!g.containsStop(ss1) || !g.containsStop(ss2) || !g.hasPath(ss1, ss2, process3))
						System.out.println("THE INPUTS ARE INVALID");
					else
					{
						ArrayList<String> str = g.get_Interchanges(g.MIN_TIME(ss1, ss2));
						int len = str.size();
						System.out.println("SOURCE STATION : " + ss1);
						System.out.println("DESTINATION STATION : " + ss2);
						System.out.println("TIME : " + str.get(len-1)+" MINUTES");
						System.out.println("NUMBER OF INTERCHANGES : " + str.get(len-2));
						//System.out.println(str);
						System.out.println("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
						System.out.print("START  ==>  " + str.get(0) + " ==>  ");
						for(int i=1; i<len-3; i++)
						{
							System.out.println(str.get(i));
						}
						System.out.print(str.get(len-3) + "   ==>    END");
						System.out.println("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
					}
					break;	
               	         default:  //If switch expression does not match with any case, 
                	        	//default statements are executed by the program.
                            	//No break is needed in the default case
                    	        System.out.println("Please enter a valid option! ");
                        	    System.out.println("The options you can choose are from 1 to 6. ");
                            
				}
			}
			
		}	
	}
