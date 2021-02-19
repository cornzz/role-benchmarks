package benchmark.team;


public team class Team2 {

	public class T2_Role1 playedBy Base {

		public void before() {
		}

		callin float replace(float n) {
			return base.replace(n / 2);
		}

		void before() <- before float operation1(float n);

		float replace(float n) <- replace float operation1(float n);
	}

	public class T2_Role2 playedBy Base {

		public void before() {
		}

		callin float replace(float n) {
			return base.replace(n / 2);
		}

		void before() <- before float operation2(float n);

		float replace(float n) <- replace float operation2(float n);
	}

	public void teamOperation(Base a, Base b, float n) {

		a.operation1(n);
		b.operation2(n);
	}

}