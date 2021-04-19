@ECHO OFF
set dir=..\..\implementations
set JAVA_HOME=C:\Program Files\Java\jdk-14.0.2
set ANT_HOME=C:\Users\corny\OneDrive\Uni\BA\7. Semester\BA\role-benchmarks\implementations\apache-ant-1.9.15

"%ANT_HOME%"\bin\ant jar -lib %dir%\objectteams\classic-3.8.0\ecotj-head.jar -Dlib=%dir%\objectteams\classic-3.8.0 -Dsource=14 -Dtarget=14 -Dver=3.8.0 -Dapr=classic
