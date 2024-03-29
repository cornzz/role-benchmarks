#!/bin/bash
# make script fail on first error
set -e
# make SCRIPT_PATH absolute
cd ../../implementations
pushd `dirname $0` > /dev/null
SCRIPT_PATH=`pwd`
popd > /dev/null

if [ "$1" = "1" ]
then
	BENCHMARK="benchmark.TeamBenchmark"
elif [ "$1" = "2" ]
then
	BENCHMARK="benchmark.TeamBenchmark2"
elif [ "$1" = "3" ]
then
	BENCHMARK="benchmark.TeamBenchmark3"
elif [ "$1" = "4" ]
then
	BENCHMARK="benchmark.TeamBenchmark4"
elif [ "$1" = "5" ]
then
	BENCHMARK="benchmark.BankBenchmark"
elif [ "$1" = "6" ]
then
	BENCHMARK="benchmark.BankBenchmark2"
fi

if [ "$4" = "1" ]
then
	NO_DEG=-Dotdyn.nodeg
	REL_THR=-Dotdyn.urt=0
else
	NO_DEG=
	REL_THR=
fi

# /bin/bash $SCRIPT_PATH/build-otj.sh 14 indy 3.8.0

JFR="-XX:StartFlightRecording=filename=bench-indy3.jfr,settings=${SCRIPT_PATH}/extensive"
#--add-exports=jdk.management.agent/jdk.internal.agent=ALL-UNNAMED"
# -XX:FlightRecorderOptions=stackdepth=128 -XX:StartFlightRecording=name=JMC_Default,maxsize=100m -Djava.net.preferIPv4Stack=true -XX:+UnlockDiagnosticVMOptions -Djdk.attach.allowAttachSelf=true --add-exports=java.management/sun.management=ALL-UNNAMED


#/bin/bash $SCRIPT_PATH/java14.sh

#~/Downloads/openjdk-15-ea+33_osx-x64_bin/jdk-15.jdk/Contents/Home/bin/java

WEAV="/net/home/kummer/BA/role-benchmarks/benchmarks/ObjectTeams/weavables.txt"

/bin/bash $SCRIPT_PATH/java14.sh -ea -Dot.weavable=$WEAV $NO_DEG $REL_THR -server -XX:-TieredCompilation -Xmx4G --add-reads jdk.dynalink=ALL-UNNAMED --add-reads java.base=ALL-UNNAMED --add-reads jdk.localedata=ALL-UNNAMED -Xbootclasspath/a:./objectteams/indy-3.8.0/otre_min.jar -javaagent:./objectteams/indy-3.8.0/otredyn_agent.jar -jar ../benchmarks/ObjectTeams/benchmarks-indy-3.8.0.jar $BENCHMARK ${2} ${3}
