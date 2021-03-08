package benchmark;

import benchmark.team.Base;
import benchmark.team.Team1;
import benchmark.team.Team2;

import java.util.List;
import java.util.LinkedList;

// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;

public class TeamBenchmark2 extends Benchmark {

	// static Logger logger = LoggerFactory.getLogger(TeamBenchmark2.class);

	private Team1 team1;
	private Team2 team2;
	private Team1 team3;
	private List<Base> bases;

	@Override
	public boolean innerBenchmarkLoop(final int innerIterations) {
		// logger.info("-------- Context 1: Team1 --------");
		team1.activate();
		float n = 100.0f;
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 2: Team2, Team1 --------");
		team2.activate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 3: Team2 --------");
		team1.deactivate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 4: No active teams --------");
		team2.deactivate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 5: Team1, Team2, Team1 --------");
		// Callsite in TeamBenchmark2 unstable
		team1.activate();
		team2.activate();
		team3.activate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 6: Team1, Team2 --------");
		// Callsite in Team1 unstable <= Fixed, also no relink in Team2
		team1.deactivate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 7: Team1, Team1, Team2 --------");
		// Callsite in Team2 unstable <= Fixed, also no relink in second Team1
		team1.activate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		// logger.info("-------- Context 8: Team1, Team1 --------");
		// Callsite in Team1 unstable
		team2.deactivate();
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		team3.deactivate();
		team1.deactivate();

		return true;
	}

	public boolean setUp(final int innerIterations) {
        team1 = new Team1();
        team2 = new Team2();
        team3 = new Team1();
        bases = new LinkedList<>();

        for (int i = 0; i < innerIterations; ++i) {
            Base b = new Base(i);
            bases.add(b);
        }

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