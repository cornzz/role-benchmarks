package benchmark;

import benchmark.team.Base;
import benchmark.team.Team1;

import java.util.List;
import java.util.LinkedList;

public class TeamBenchmark extends Benchmark {

	private Team1 team1;
	private List<Base> bases;

	@Override
	public boolean innerBenchmarkLoop(final int innerIterations) {
		team1.activate();
		float n = 100.0f;
		for (Base a : bases) {
			for (Base b : bases) {
				a.operation1(n);
				b.operation2(n);
			}
		}
		team1.deactivate();

		return true;
	}

	public boolean setUp(final int innerIterations) {
        team1 = new Team1();
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