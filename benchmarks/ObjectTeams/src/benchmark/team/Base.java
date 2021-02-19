package benchmark.team;


public class Base {

	public int id;

	public Base(int id) {
		this.id = id;
	}

	public float operation1(float n) {
		return n * 2;
	}

	public float operation2(float n) {
		return n / 2;
	}

}