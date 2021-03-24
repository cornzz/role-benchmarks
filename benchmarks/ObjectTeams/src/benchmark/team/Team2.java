package benchmark.team;

// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;

public team class Team2 {

	// static Logger logger = LoggerFactory.getLogger(Team2.class);

	public class T2_Role1 playedBy Base {

		public void before() {
			// logger.info("before T2_Role1 operation1");
		}

		callin float replace(float n) {
			// logger.info("replace T2_Role1 operation1 BEGIN");
			float f = base.replace(n * 2);
			// logger.info("replace T2_Role1 operation1 END");
			return f;
		}

		public void after() {
			// logger.info("after T2_Role1 operation1");
		}

		void before() <- before float operation1(float n);

		float replace(float n) <- replace float operation1(float n);

		void after() <- after float operation1(float n);

	}

	public class T2_Role2 playedBy Base {

		public void before() {
			// logger.info("before T2_Role2 operation2");
		}

		callin float replace(float n) {
			// logger.info("replace T2_Role2 operation2 BEGIN");
			float f = base.replace(n / 2);
			// logger.info("replace T2_Role2 operation2 END");
			return f;
		}

		public void after() {
			// logger.info("after T2_Role2 operation2");
		}

		void before() <- before float operation2(float n);

		float replace(float n) <- replace float operation2(float n);

		void after() <- after float operation2(float n);

	}

	public void teamOperation(Base a, Base b, float n) {
		a.operation1(n);
		b.operation2(n);
	}

}