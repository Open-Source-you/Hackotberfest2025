import java.util.*;

public class file1<T extends Comparable<T>> 
{
	ArrayList<T> value = new ArrayList<>();
	HashMap<T, Integer> map = new HashMap<>();

	public void add(T item) 
	{
		value.add(item);   
		map.put(item, this.value.size() - 1);
		upheapidxfy(value.size() - 1);
	}

	private void upheapidxfy(int cidx) 
	{
		int pidx = (cidx - 1) / 2;
		if (Large(value.get(cidx), value.get(pidx)) > 0) 
		{
			swap(pidx, cidx);
			upheapidxfy(pidx);
		}
	}

	private void swap(int i, int j) 
	{
		T ith = value.get(i);
		T jth = value.get(j);
		
		value.set(i, jth);
		value.set(j, ith);
		map.put(ith, j);
		map.put(jth, i);
	}

	public void display() 
	{
		System.out.println(value);
	}

	public int size() 
	{
		return this.value.size();
	}

	public boolean isEmpty() 
	{
		return this.size() == 0;
	}

	public T remove() 
	{
		swap(0, this.value.size() - 1);
		T rv = this.value.remove(this.value.size() - 1);
		downheapidxfy(0);

		map.remove(rv);
		return rv;
	}

	private void downheapidxfy(int pidx) 
	{
		int lcidx = 2 * pidx + 1;
		int rcidx = 2 * pidx + 2;
		int mini = pidx;

		if (lcidx < this.value.size() && Large(value.get(lcidx), value.get(mini)) > 0)
		{
			mini = lcidx;
		}
		
		if (rcidx < this.value.size() && Large(value.get(rcidx), value.get(mini)) > 0) 
		{
			mini = rcidx;
		}
		
		if (mini != pidx)
		{
			swap(mini, pidx);
			downheapidxfy(mini);
		}
	}

	public T get() 
	{
		return this.value.get(0);
	}

	public int Large(T t, T o) 
	{
		return t.compareTo(o);
	}

	public void getPrior(T pair) 
	{
		int index = map.get(pair);
		upheapidxfy(index);
	}
}
