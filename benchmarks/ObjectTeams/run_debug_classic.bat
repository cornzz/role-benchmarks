@echo OFF
set JAVA_HOME=C:\Program Files\Java\jdk-14.0.2
set WEAV="weavables.txt"
echo Benchmark2
"%JAVA_HOME%"\bin\java -server -Xmx4G -ea -Dot.weavable=%WEAV% -server -XX:-TieredCompilation -Xmx4G --add-reads jdk.dynalink=ALL-UNNAMED --add-reads java.base=ALL-UNNAMED --add-reads jdk.localedata=ALL-UNNAMED -Xbootclasspath/a:..\..\implementations\objectteams\classic-3.8.0\otre_min.jar -javaagent:..\..\implementations\objectteams\classic-3.8.0\otredyn_agent.jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,address="8000" -jar benchmarks-classic-3.8.0.jar benchmark.BankBenchmark2 1 2
echo Benchmark
"%JAVA_HOME%"\bin\java -server -Xmx4G -ea -Dot.weavable=%WEAV% -server -XX:-TieredCompilation -Xmx4G --add-reads jdk.dynalink=ALL-UNNAMED --add-reads java.base=ALL-UNNAMED --add-reads jdk.localedata=ALL-UNNAMED -Xbootclasspath/a:..\..\implementations\objectteams\classic-3.8.0\otre_min.jar -javaagent:..\..\implementations\objectteams\classic-3.8.0\otredyn_agent.jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,address="8000" -jar benchmarks-classic-3.8.0.jar benchmark.BankBenchmark 1 2
