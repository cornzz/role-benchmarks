@echo OFF
set JAVA_HOME=C:\Program Files\Java\jdk-14.0.2
set WEAV="weavables.txt"
IF "%1" == "1" (
	set BENCHMARK="benchmark.BankBenchmark"
) ELSE IF "%1" == "2" (
	set BENCHMARK="benchmark.BankBenchmark2"
) ELSE IF "%1" == "3" (
	set BENCHMARK="benchmark.TeamBenchmark"
) ELSE IF "%1" == "4" (
	set BENCHMARK="benchmark.TeamBenchmark2"
)


IF "%4" == "" (
	"%JAVA_HOME%"\bin\java -server -Xmx4G -ea -Dot.weavable=%WEAV% -server -XX:-TieredCompilation -Xmx4G --add-reads jdk.dynalink=ALL-UNNAMED --add-reads java.base=ALL-UNNAMED --add-reads jdk.localedata=ALL-UNNAMED -Xbootclasspath/a:..\..\implementations\objectteams\classic-3.8.0\otre_min.jar -javaagent:..\..\implementations\objectteams\classic-3.8.0\otredyn_agent.jar -jar benchmarks-classic-3.8.0.jar %BENCHMARK% %2 %3
) ELSE (
	"%JAVA_HOME%"\bin\java -server -Xmx4G -ea -Dot.weavable=%WEAV% -server -XX:-TieredCompilation -Xmx4G --add-reads jdk.dynalink=ALL-UNNAMED --add-reads java.base=ALL-UNNAMED --add-reads jdk.localedata=ALL-UNNAMED -Xbootclasspath/a:..\..\implementations\objectteams\classic-3.8.0\otre_min.jar -javaagent:..\..\implementations\objectteams\classic-3.8.0\otredyn_agent.jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,address="8000" -jar benchmarks-classic-3.8.0.jar %BENCHMARK% %2 %3
)