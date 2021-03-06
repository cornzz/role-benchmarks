package benchmark;

import benchmark.team.Base;
import benchmark.team.Team1;
import benchmark.team.Team2;

// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;

public class TeamBenchmark4 extends Benchmark {

	// static Logger logger = LoggerFactory.getLogger(TeamBenchmark4.class);

	private Team1 team1;
	private Team2 team2;
	private Team1 team3;
	private Base a;
	private Base b;

	@Override
	public boolean innerBenchmarkLoop(final int innerIterations) {
		float n = 100.0f;
		int iterations = innerIterations * innerIterations;
		for (int i = 0; i < iterations; i++) {
			// logger.info("-------- Context 1: Team1 --------");
			team1.activate();
			a.operation1(n);
			// logger.info("100 -- {}", m);
			b.operation2(n);
			// logger.info("100 -- {}", m);

			// logger.info("-------- Context 2: Team2, Team1 --------");
			team2.activate();
			a.operation1(n);
			// logger.info("200 -- {}", m);
			b.operation2(n);
			// logger.info("50 -- {}", m);

			// logger.info("-------- Context 3: Team2 --------");
			team1.deactivate();
			a.operation1(n);
			// logger.info("400 -- {}", m);
			b.operation2(n);
			// logger.info("25 -- {}", m);

			// logger.info("-------- Context 4: Team1, Team2 --------");
			team1.activate();
			a.operation1(n);
			// logger.info("200 -- {}", m);
			b.operation2(n);
			// logger.info("50 -- {}", m);

			// logger.info("-------- Context 5: No active teams --------");
			team1.deactivate();
			team2.deactivate();
			a.operation1(n);
			// logger.info("200 -- {}", m);
			b.operation2(n);
			// logger.info("50 -- {}", m);

			// logger.info("-------- Context 6: Team1, Team1 --------");
			team1.activate();
			team3.activate();
			a.operation1(n);
			// logger.info("50 -- {}", m);
			b.operation2(n);
			// logger.info("200 -- {}", m);
			team3.deactivate();
			team1.deactivate();
		}

		return true;
	}

	public boolean setUp(final int innerIterations) {
        team1 = new Team1();
        team2 = new Team2();
        team3 = new Team1();
        a = new Base(1);
        b = new Base(2);

        return true;
    }

    @Override
    public Object benchmark() {
        throw new RuntimeException("Should never be reached");
    }

    @Override
    public boolean verifyResult(Object result) {
        throw new RuntimeException("Should never be reached");
    }
}