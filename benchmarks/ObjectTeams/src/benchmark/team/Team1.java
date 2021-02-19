package benchmark.team;


public team class Team1 {

	public class T1_Role1 playedBy Base {

		public void before() {
		}

		callin float replace(float n) {
			return base.replace(n / 2);
		}

		void before() <- before float operation1(float n);

		float replace(float n) <- replace float operation1(float n);
	}

	public class T1_Role2 playedBy Base {

		public void before() {
		}

		callin float replace(float n) {
			return base.replace(n * 2);
		}

		void before() <- before float operation2(float n);

		float replace(float n) <- replace float operation2(float n);
	}

}